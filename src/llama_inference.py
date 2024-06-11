from llama_cpp import Llama
from env import MODEL_PATH, N_CTX, N_THREADS, REPEAT_PENALTY, SYSTEM_PROMPT, TEMPERATURE, TOP_K, TOP_P


model = Llama(
    model_path=MODEL_PATH,
    n_ctx=N_CTX,
    n_parts=1,
    verbose=False,
    n_threads=N_THREADS
)
