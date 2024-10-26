from langchain_community.llms import HuggingFacePipeline
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
from langchain_core.prompts import PromptTemplate

template = """В мире, где информация растет быстрее, чем мы успеваем ее переработать, вопросы подростков остаются одними из самых важных. Они хотят понять окружающий мир, но часто не могут пробиться сквозь плотные, скучные или сложные тексты статей и новостей. Как рассказать им о сложных вещах простым языком, без потери смысла? 
Представьте, что где-то сидит отец с дочерью-подростком. Она видит в ленте новость или статью и хочет понять, о чем же на самом деле идет речь. Он, глядя на нее, рассказывает: понятным, доступным и интересным языком. Она задает вопросы — острые, смелые, иногда неожиданные. Он отвечает — развернуто и честно, с терпением и заботой. Так создается диалог, который становится не просто обменом информации, а мостом между поколениями, между текстом и теми, кто хочет его понять.
Твоя задача создавать такие "беседы" на русском языке, превращая статьи или новости в диалог отца и дочери. Такой подкаст поможет подросткам понять смысл самых разных тем: от науки до социальных событий. Один задает вопросы, а другой — отвечает, направляя и разворачивая сложное содержание простым языком. Диалог должен быть логичным, информативным и интерактивным, передавая даже непростые темы доступно и с интересом. Я тебе буду скидывать текст статьи в интернете, тебе нужно их изучить и написать вдумчивый диалог между отцом и дочерью, согласно тем данным, которые я написал.

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
        return self.llm_chain.invoke({"text": question})


model = Mistral()
