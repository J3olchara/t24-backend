from rest_framework import serializers


class AnswerSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=8192)
    file = serializers.FileField()


class ErrorsSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=512)
