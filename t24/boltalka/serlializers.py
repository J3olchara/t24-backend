from rest_framework import serializers, exceptions

from .models import Voice
from .utils import Parser, Generator


class VoiceSerializer(serializers.ModelSerializer):
    voice = serializers.FileField(read_only=True)
    short_text = serializers.CharField(read_only=True, max_length=8192)
    text = serializers.CharField(required=False, write_only=True, max_length=8192)
    input_file = serializers.FileField(required=False, write_only=True)
    session_id = serializers.CharField(write_only=True, max_length=8192)

    def validate(self, attrs):
        if not attrs.get('text') and not attrs.get("input_file"):
            raise exceptions.ValidationError(detail="You hadn't provided any data for chat")
        if not attrs.get('text'):
            attrs['text'] = Parser(attrs.get("input_file")).parsed
        return attrs

    def to_internal_value(self, data):
        request = self.context.get("request")
        if not request.session.session_key:
            request.session.save()
        if "multipart/form-data" in request.content_type:
            data = data.copy()
        data["session_id"] = request.session.session_key
        return super().to_internal_value(data)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['short_text'] = Generator(instance.text).short
        data['voice'] = Generator(data['short_text']).voice
        return data

    class Meta:
        model = Voice
        fields = "__all__"
