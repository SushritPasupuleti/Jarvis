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

model_path = "codellama/CodeLlama-7b-hf"

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

# tokenizer = CodeLlamaTokenizer.from_pretrained(model_path)
tokenizer = LlamaTokenizer.from_pretrained(model_path)

PROMPT = '''def fibonacci(n: int) -> int:
    """ <FILL_ME>
    return result
'''

stop_list = ['\n\n\n']

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

input_ids = tokenizer(PROMPT, return_tensors="pt")["input_ids"]
input_ids = input_ids.to(device)
generated_ids = model.generate(input_ids, max_new_tokens=128, #pyright: ignore
    do_sample=True,
    # temperature=0,
    top_p=0,
    # n=1,
    # stop=["\n"],
    # extra={
    #     "language": "python",
    # }
    stopping_criteria=stopping_criteria,
)

filling = tokenizer.batch_decode(generated_ids[:, input_ids.shape[1]:], skip_special_tokens = True)[0]

print(PROMPT.replace("<FILL_ME>", filling))
