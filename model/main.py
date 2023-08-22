import torch
from transformers import LlamaTokenizer, LlamaForCausalLM, pipeline
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

model_path = 'openlm-research/open_llama_3b'
# model_path = 'openlm-research/open_llama_7b'

tokenizer = LlamaTokenizer.from_pretrained(model_path)
model = LlamaForCausalLM.from_pretrained(
    model_path, torch_dtype=torch.float16, device_map='auto',
)

pipe = pipeline(
    "text-generation", 
    model=model, # pyright: ignore
    tokenizer=tokenizer, 
    max_new_tokens=2**8,
    device=device,
)
hf = HuggingFacePipeline(pipeline=pipe)

callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

template = """Question: {question}

Answer: 
"""

question = "Explain recursion to me. With a code example in Python."

prompt = PromptTemplate(template=template, input_variables=['question'])

# hf(prompt)

llm_chain = LLMChain(
    prompt=prompt, 
    llm=hf,
    callback_manager=callback_manager,
    verbose=True,
    return_final_only=True,
)

answer = llm_chain.run(question)
# answer = llm_chain(question)
# answer = llm_chain.predict(question=question)

print(answer)

