from tika import parser


class Parser:
    def __init__(self, file):
        self._file = file
        self._allowed_formats = {"pdf", "txt"}
        self._table = {
            fmt: getattr(self, f"parse_{fmt}")
            for fmt in self._allowed_formats
        }

    def parse_pdf(self):
        return parser.from_buffer(self._file.read())

    def parse_txt(self):
        return self._file.read()

    @property
    def parsed(self):
        file_format = self._file.filename.split('.')[-1]
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
        pass

    @property
    def mp3(self):
        pass


