from rest_framework import views
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from .serlializers import AnswerSerializer
from utils import Parser, Generator


class BoltalkaMain(views.APIView):
    def post(self, request: Request):
        text = None
        if request.content_type == "multipart/form-data":
            text = Parser(request.FILES[0]).parsed
            if text is None:
                return Response({"errors": "Доступны только .txt и только .pdf файлы для ввода"}, status=status.HTTP_400_BAD_REQUEST)
        if request.content_type == "application/json":
            if request.data.get("link"):
                text = Parser.parse_site(request.data["link"])
            if request.data.get("text"):
                text = request.data["text"]
        if text is None:
            return Response({"errors": "Не найден текст в запросе"}, status=status.HTTP_400_BAD_REQUEST)
        short_text = Generator(text).short
        mp3 = Generator(short_text).mp3
        return Response(AnswerSerializer(text=text, mp3=mp3).data, status=status.HTTP_200_OK)





