import os

from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat import ChatCompletion

from core.models import Templater

load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))


def gpt_query(templater: Templater, answer: str = None) -> ChatCompletion:
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": templater.system},
            {"role": "user", "content": templater.prompt(answer)}
        ]
    )
    return completion
