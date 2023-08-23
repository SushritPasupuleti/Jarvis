import torch
from torch import bfloat16
from transformers import LlamaTokenizer, LlamaForCausalLM, pipeline, StoppingCriteria, StoppingCriteriaList
import transformers
from langchain import PromptTemplate, LLMChain
from langchain.llms import HuggingFacePipeline
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

if torch.cuda.is_available():
    device = torch.device("cuda")
    n_gpu = torch.cuda.device_count()
    torch.cuda.get_device_name(0)
else:
    device = torch.device("cpu")

model_path = 'openlm-research/open_llama_7b'
# model_path = 'openlm-research/open_llama_3b'

bnb_config = transformers.BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type='nf4',
    bnb_4bit_use_double_quant=True,
    bnb_4bit_compute_dtype=bfloat16
)

model = LlamaForCausalLM.from_pretrained(
    model_path, 
    torch_dtype=torch.float16, 
    device_map='auto',
    quantization_config=bnb_config,
)

tokenizer = LlamaTokenizer.from_pretrained(model_path)

stop_list = ['\nHuman:', '\n```\n']

stop_token_ids = [tokenizer(x)['input_ids'] for x in stop_list]
stop_token_ids = [torch.LongTensor(x).to(device) for x in stop_token_ids]

# define custom stopping criteria object
class StopOnTokens(StoppingCriteria):
    def __call__(self, input_ids: torch.LongTensor, scores: torch.FloatTensor, **kwargs) -> bool:
        for stop_ids in stop_token_ids:
            if torch.eq(input_ids[0][-len(stop_ids):], stop_ids).all():
                return True
        return False

stopping_criteria = StoppingCriteriaList([StopOnTokens()])

pipe = pipeline(
    task="text-generation", 
    model=model, # pyright: ignore
    tokenizer=tokenizer, 
    max_new_tokens=2**9,
    stopping_criteria=stopping_criteria,  # without this model rambles during chat
    # device=device,
    repetition_penalty=1.2,
    return_full_text=True,
)
hf = HuggingFacePipeline(pipeline=pipe)

callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

# template = """{question}
#
# Provide a code example in Python.
# """

template = """{question}"""

question = "Explain recursion to me."

prompt = PromptTemplate(template=template, input_variables=['question'])

llm_chain = LLMChain(
    prompt=prompt, 
    llm=hf,
    callback_manager=callback_manager,
    verbose=True,
    # return_final_only=True,
)

# answer = llm_chain.run(question)

# print(answer)

