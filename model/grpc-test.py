import grpc
import chat_pb2 as chat__pb2
import chat_pb2_grpc as chat__pb2_grpc

# print("Hello World")

# print("Question: ", chat__pb2.Question)
# print("Answer: ", chat_pb2.Answer)

channel = grpc.insecure_channel('localhost:50051')
client = chat__pb2_grpc.QuestionAnswerStub(channel)

request = chat__pb2.Question(question="What is the weather like today?")

client.AskQuestion(request)

print("Answer: ", client.AskQuestion(request))
