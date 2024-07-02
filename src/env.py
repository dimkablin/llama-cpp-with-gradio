import os
from dotenv import load_dotenv

load_dotenv()


SYSTEM_PROMPT = os.getenv('SYSTEM_PROMPT', "Ты — Лина, виртуальный ассистент и просто очень хороший собеседник.")
MODEL_PATH = os.getenv('MODEL_PATH', 'src/models/saiga-q4_K.gguf')
N_CTX = int(os.getenv('N_CTX', 8192))
TOP_K = int(os.getenv('TOP_K', 30))
TOP_P = float(os.getenv('TOP_P', 0.9))
TEMPERATURE = float(os.getenv('TEMPERATURE', 0.6))
REPEAT_PENALTY = float(os.getenv('REPEAT_PENALTY', 1.1))
N_THREADS = int(os.getenv('N_THREADS', 7))

DEFAULT_JSON = {
    "type": "object",
    "properties": {
        "order": {
            "type": "integer",
            "description": "Порядковый номер книги."
        },
        "author": {
            "type": "string",
            "description": "Автор книги."
        },
        "book_name": {
            "type": "string",
            "description": "Название книги"
        }
    },
    "required": [
        "order",
        "author",
        "book_name"
    ]
}