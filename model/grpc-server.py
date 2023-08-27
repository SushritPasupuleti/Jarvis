import grpc
from concurrent import futures
import random
import chat_pb2 as chat__pb2
import chat_pb2_grpc as chat__pb2_grpc

from main import llm_chain

max_workers = 10

class QuestionAnswerServicer(chat__pb2_grpc.QuestionAnswerServicer):
    # the caller is responsible for checking cache before calling this
    def AskQuestion(self, request, context):
        print("Request: ", request)
        print("Context: ", context)

        answer = llm_chain.run(request.question)

        return chat__pb2.Answer(answer=answer)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=max_workers))
    chat__pb2_grpc.add_QuestionAnswerServicer_to_server(
        QuestionAnswerServicer(), server
    )
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    print("gRPC Server is running on port 50051")
    serve()
