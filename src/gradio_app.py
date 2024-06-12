import gradio as gr
from llama_cpp import Llama

from env import MODEL_PATH, N_CTX, N_THREADS, REPEAT_PENALTY, SYSTEM_PROMPT, TEMPERATURE, TOP_K, TOP_P


model = Llama(
    model_path=MODEL_PATH,
    n_ctx=N_CTX,
    n_parts=1,
    verbose=False,
    n_threads=N_THREADS
)


def predict(message, history):
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    for human, assistant in history:
        messages.append({"role": "user", "content": human })
        messages.append({"role": "assistant", "content":assistant})
    
    messages.append({"role": "user", "content": message})
    
    response = ""
    for part in model.create_chat_completion(
            messages,
            temperature=TEMPERATURE,
            top_k=TOP_K,
            top_p=TOP_P,
            repeat_penalty=REPEAT_PENALTY,
            stream=True,
        ):
            delta = part["choices"][0]["delta"]
            if "content" in delta:
                response += delta["content"]
                yield response
    history.append({"role": "assistant", "content": response})


if __name__ == "__main__":
    gr.ChatInterface(predict).launch(server_name="127.0.0.1", 
                                     server_port=8000, 
                                     share=False)
