import os
from dotenv import load_dotenv

load_dotenv()


SYSTEM_PROMPT = os.getenv('SYSTEM_PROMPT', "Ты Сайга - дружелюбный и болтливый ассистент.")
MODEL_PATH = os.getenv('MODEL_PATH', 'weights/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf')
N_CTX = int(os.getenv('N_CTX', 8192))
TOP_K = int(os.getenv('TOP_K', 30))
TOP_P = float(os.getenv('TOP_P', 0.9))
TEMPERATURE = float(os.getenv('TEMPERATURE', 0.6))
REPEAT_PENALTY = float(os.getenv('REPEAT_PENALTY', 1.1))
N_THREADS = int(os.getenv('N_THREADS', 7))

DEFAULT_JSON = {
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "Стеллаж": {
        "type": "integer",
        "description": "Стеллаж, на котором находится книга."
      },
      "Полка": {
        "type": "integer",
        "description": "Полка, на которой находится книга."
      },
      "Автор": {
        "type": "string",
        "description": "Автор книги."
      },
      "Название": {
        "type": "string",
        "description": "Название книги"
      }
    },
    "required": [
      "Стеллаж",
      "Полка",
      "Автор",
      "Название"
    ]
  },
  "required": ["items"]
}

EXAMPLES = [
    "Первая книга, которую я прочитал, была написана Джорджем Оруэллом и называлась 1984.",
    "Второй по счету книгой в моей коллекции является Мастер и Маргарита Михаила Булгакова.",
    "первый стелаж первая полка книга автора иванов иван иванович название мое путешествие по архиву следующая книга автора петрова петра петровича название новое путешествие по архиву вторая полка книга автора сидоров сидор сидорович название мое путешествие по стелажам следующая книга автора владимир владимирович владимиров название как же достали эти стелажи второй стелаж первая полка книга автора усталов устал усталович название как я здесь оказался следующая книга автора убегаев убегай убегаевич название нахуй это вон туда"
]