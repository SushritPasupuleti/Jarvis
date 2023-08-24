import sys
from main import llm_chain

if sys.argv[1] != None:
    question = sys.argv[1]
else:
    question = "Explain recursion to me."

# print("Question: ", question)

answer = llm_chain.run(question)

print(answer)
