from rest_framework import generics

from .serlializers import VoiceSerializer


class BoltalkaMain(generics.CreateAPIView):
    serializer_class = VoiceSerializer
