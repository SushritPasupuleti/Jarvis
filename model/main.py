import torch
from transformers import LlamaTokenizer, LlamaForCausalLM, pipeline
from langchain import PromptTemplate, LLMChain
from langchain.llms import HuggingFacePipeline

if torch.cuda.is_available():
    device = torch.device("cuda")
    n_gpu = torch.cuda.device_count()
    torch.cuda.get_device_name(0)
else:
    device = torch.device("cpu")

# model_path = 'openlm-research/open_llama_3b'
model_path = 'openlm-research/open_llama_7b'

tokenizer = LlamaTokenizer.from_pretrained(model_path)
model = LlamaForCausalLM.from_pretrained(
    model_path, torch_dtype=torch.float16, device_map='auto',
)

pipe = pipeline(
    "text-generation", model=model, tokenizer=tokenizer, max_new_tokens=10
)
hf = HuggingFacePipeline(pipeline=pipe)

# prompt = """
# Question: What is the largest animal?
# """

# hf(prompt)

# llm_chain = LLMChain(prompt=prompt, llm=hf)

# question = "What is the smallest animal?"

# llm_chain.run(question)

# print("Asking HF", hf('Q: What is the largest animal?\nA:'))

prompt = 'Q: What is the largest animal?\nA:'
input_ids = tokenizer(prompt, return_tensors="pt").input_ids

if device.type == 'cuda':
    # model.half()
    input_ids = input_ids.to('cuda')

generation_output = model.generate(# pyright: ignore
    input_ids=input_ids, 
    # max_new_tokens=32
    max_new_tokens=32*2
)
print(tokenizer.decode(generation_output[0]))
