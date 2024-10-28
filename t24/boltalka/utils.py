from pdfminer.high_level import extract_text
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.base import ContentFile
from .tensors import audio
# from .tensors import model

from uuid import uuid4
import io
import os


class Parser:
    def __init__(self, file: InMemoryUploadedFile):
        self._file = file
        self._allowed_formats = {"pdf", "txt"}
        self._table = {
            fmt: getattr(self, f"parse_{fmt}")
            for fmt in self._allowed_formats
        }

    @staticmethod
    def filter_symbols(text: str):
        def filter_func(char):
            c = ord(char)
            ok = True
            ok = ok or c <= 255
            ok = ok or ord("а") <= c <= ord("я")
            ok = ok or ord("А") <= c <= ord("Я")
            if not ok:
                return ''
            if char == '\n':
                return ' '
            return char

        return ''.join(map(filter_func, text))

    def parse_pdf(self):
        return extract_text(io.BytesIO(self._file.read()))

    def parse_txt(self):
        return self._file.read().decode()

    @property
    def parsed(self):
        file_format = self._file.name.split('.')[-1]
        if file_format in self._allowed_formats:
            return self.filter_symbols(self._table[file_format]())

    @staticmethod
    def parse_site(link):
        pass


class Generator:
    def __init__(self, text):
        self._text = text

    @property
    def short(self) -> str:
        # return model.get_answer(self._text)
        return self._text

    @property
    def voice(self):
        filename = f"{uuid4()}.wav"
        file_path = settings.MEDIA_ROOT / filename
        audio.generate(file_path, self._text)
        with open(file_path, 'rb') as wav:
            file = ContentFile(content=wav.read(), name=filename)
        os.remove(file_path)
        return file
