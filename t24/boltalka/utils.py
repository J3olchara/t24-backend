from pdfminer.high_level import extract_text
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
import io


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
            return ord(char) < 255 or ord("а") <= ord(char) <= ord("я") or ord("А") <= ord(char) <= ord("Я")

        return ''.join(filter(filter_func, text))

    def parse_pdf(self):
        pdf_text = extract_text(io.BytesIO(self._file.read()))
        return self.filter_symbols(pdf_text)

    def parse_txt(self):
        return self._file.read()

    @property
    def parsed(self):
        file_format = self._file.name.split('.')[-1]
        if file_format in self._allowed_formats:
            return self._table[file_format]()

    @staticmethod
    def parse_site(link):
        pass


class Generator:
    def __init__(self, text):
        self._text = text

    @property
    def short(self) -> str:
        return self._text

    @property
    def voice(self):
        file_path = settings.STATIC_ROOT
        return str((file_path / "eng.mp3").relative_to(settings.BASE_DIR))


