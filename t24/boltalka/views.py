from rest_framework import viewsets, generics, status
from rest_framework.request import Request
from rest_framework.response import Response

from .serlializers import VoiceSerializer
from .models import Voice


class BoltalkaMain(generics.CreateAPIView):
    serializer_class = VoiceSerializer

    # def get_text(self, request):
    #     if request.content_type == "multipart/form-data":
    #         text = Parser(request.FILES[0]).parsed
    #         if text is None:
    #             return Response({"errors": "Доступны только .txt и только .pdf файлы для ввода"}, status=status.HTTP_400_BAD_REQUEST)
    #     if request.content_type == "application/json":
    #         if request.data.get("link"):
    #             text = Parser.parse_site(request.data["link"])
    #         if request.data.get("text"):
    #             text = request.data["text"]
    #     if text is None:
    #         return Response({"errors": "Не найден текст в запросе"}, status=status.HTTP_400_BAD_REQUEST)

    # def get_serializer2(self, request):
    #     text = None
    #     print(request.content_type)
    #     short_text = Generator(text).short
    #     mp3 = Generator(short_text).mp3
    #     if not request.session.session_key:
    #         request.session.save()
    #     session_id = request.session.session_key
    #
    #     serializer = AnswerSerializer(data={
    #         "text": short_text,
    #         "voice": mp3,
    #     })
