import logging as logger
from langchain_community.llms import HuggingFacePipeline
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
from langchain_core.prompts import PromptTemplate
import torch
from omegaconf import OmegaConf
from scipy.io.wavfile import write

template = """В мире, где информация растет быстрее, чем мы успеваем ее переработать, вопросы подростков остаются одними из самых важных. Они хотят понять окружающий мир, но часто не могут пробиться сквозь плотные, скучные или сложные тексты статей и новостей. Как рассказать им о сложных вещах простым языком, без потери смысла? 
Представьте, что где-то сидит отец с дочерью-подростком. Она видит в ленте новость или статью и хочет понять, о чем же на самом деле идет речь. Он, глядя на нее, рассказывает: понятным, доступным и интересным языком. Она задает вопросы — острые, смелые, иногда неожиданные. Он отвечает — развернуто и честно, с терпением и заботой. Так создается диалог, который становится не просто обменом информации, а мостом между поколениями, между текстом и теми, кто хочет его понять.
Твоя задача создавать такие "беседы" на русском языке, превращая статьи или новости в диалог отца и дочери. Такой подкаст поможет подросткам понять смысл самых разных тем: от науки до социальных событий. Один задает вопросы, а другой — отвечает, направляя и разворачивая сложное содержание простым языком. Диалог должен быть логичным, информативным и интерактивным, передавая даже непростые темы доступно и с интересом. Я тебе буду скидывать текст статьи в интернете, тебе нужно их изучить и написать вдумчивый диалог между отцом и дочерью, согласно тем данным, которые я написал.
Пускай дочка начнет первой.

## Текст статьи:
{text}

## Диалог:"""


class Mistral:
    def __init__(self):
        model_name = "unsloth/mistral-7b-instruct-v0.2-bnb-4bit"
        model = AutoModelForCausalLM.from_pretrained(model_name, ignore_mismatched_sizes=True)
        tokenizer = AutoTokenizer.from_pretrained(model_name, ignore_mismatched_sizes=True)
        pipe = pipeline('text-generation', model=model, tokenizer=tokenizer, max_new_tokens=1000)
        llm = HuggingFacePipeline(pipeline=pipe)
        prompt = PromptTemplate(template=template, input_variables=["text"])
        self.llm_chain = prompt | llm

    def get_answer(self, question: str) -> str:
        logger.info(f'{question=}')
        result = self.llm_chain.invoke({"text": question})
        logger.info(f'r{result=}')
        return result


text = '''
Дочь: А как искусственный интеллект это делает лучше, чем мы?
А что если искусственный интеллект интерпретирует данные неправильно?
Отец: Дочь, искусственный интеллект может за считаные минуты проанализировать тысячи снимков и выявить закономерности, которые не всегда заметны человеческому глазу. Это помогает врачам снизить процент ошибок и увеличить шансы на успешное лечение пациентов.
'''


class Audio:
    def __init__(self):
        self.sample_rate = 48000
        # speaker = 'eugene'
        # speaker = speaker
        self.put_accent = True
        self.put_yo = True
        torch.hub.download_url_to_file('https://raw.githubusercontent.com/snakers4/silero-models/master/models.yml',
                                       'latest_silero_models.yml',
                                       progress=False)
        models = OmegaConf.load('latest_silero_models.yml')

        language = 'ru'
        model_id = 'v4_ru'
        # device = torch.device('cuda')
        device = torch.device('cpu')

        self.model, example_text = torch.hub.load(
            repo_or_dir='snakers4/silero-models',
            model='silero_tts',
            language=language,
            speaker=model_id
        )
        self.model.to(device)

    def splitter(self, text):
            a = text.split('Дочь:')
            for i in range(len(a)):
                a[i] = a[i].split('Отец:')
            return a

    def generate(self, save_dir, text):
        logger.info(f'Generate from {text=}')
        lst = self.splitter(text)
        # gpu or cpu
        result = torch.empty(0)
        logger.info(f'{lst=}')
        for i in lst[1:]:
            # audio(model, 'baya', i[0])
            result = torch.cat((result, self.audio(self.model, 'baya', i[0])), dim=0)
            # audio(model, 'aidar', i[1])
            if len(i) >= 2:
                result = torch.cat((result, self.audio(self.model, 'eugene', i[1])), dim=0)

        return write(save_dir, self.sample_rate, result.cpu().numpy())

    def audio(self, model, speaker, example_text):
        logger.info(f'Generate audio from {speaker=} starts')
        audio = model.apply_tts(text=example_text,
                                speaker=speaker,
                                sample_rate=self.sample_rate,
                                put_accent=self.put_accent,
                                put_yo=self.put_yo)
        logger.info(f'Generate audio from {speaker=} ended')
        # display(Audio(audio, rate=sample_rate))
        return audio


model = Mistral()
audio = Audio()
