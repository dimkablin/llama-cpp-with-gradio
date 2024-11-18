import gradio as gr
import json
from llama_cpp import Llama
from env import EXAMPLES, MODEL_PATH, N_CTX, N_THREADS

# Initialize LLama model
model = Llama(
    model_path=MODEL_PATH,
    n_ctx=N_CTX,
    n_parts=1,
    verbose=False,
    n_threads=N_THREADS
)

# Example functions that can be triggered
def get_current_time():
    from datetime import datetime
    return {"message": f"Current time is: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"}

def get_greeting(name):
    return {"message": f"Hello, {name}! How can I assist you today?"}

# Dictionary to map function names to actual function calls
FUNCTIONS = {
    "get_current_time": get_current_time,
    "get_greeting": get_greeting
}

def wrapped_predict(message: str, history: list) -> iter:
    """
    A generator function that yields responses from a predictive model 
    and calls specific functions when requested.

    Args:
        message (str): The message input by the user.
        history (list): A list of previous messages in the chat history.

    Yields:
        str: Predicted responses from the model.
    """
    # Construct the prompt
    prompt = """
    Ты ассистент, который может отвечать на вопросы пользователей и вызывать определенные функции. Если пользователь спрашивает что-то, что требует вызова функции, ответьте 'call <имя_функции>:<аргумент>'.
    Доступные функции:
    - get_current_time: Возвращает текущую дату и время.
    - get_greeting(name): Приветствует пользователя с указанным именем.
    
    Пользователь: {}
    """.format(message)

    # Generate response using LLama model
    response = model(prompt, max_tokens=100)
    response_text = response["choices"][0]["text"].strip()

    # Check if response calls a function
    if response_text.startswith("call "):
        try:
            # Parse function call
            function_call = response_text[len("call "):]
            if ":" in function_call:
                func_name, arg = function_call.split(":", 1)
                if func_name in FUNCTIONS:
                    # Call function with an argument
                    result = FUNCTIONS[func_name](arg)
                    yield json.dumps(result, ensure_ascii=False)
                else:
                    yield json.dumps({"error": f"Function '{func_name}' not found."})
            elif function_call in FUNCTIONS:
                # Call function without arguments
                result = FUNCTIONS[function_call]()
                yield json.dumps(result, ensure_ascii=False)
            else:
                yield json.dumps({"error": f"Function '{function_call}' not found."})
        except Exception as e:
            yield json.dumps({"error": str(e)})
    else:
        # If no function call, yield the model's response as usual
        yield response_text

# Create the Gradio interface
with gr.Blocks(css=".gap { min-height: 75vh; }") as demo:
    gr.Markdown("# Chat Interface with Function Calling Example")

    # Here we get function-calling output
    with gr.Tab("Chat"):
        chatbot = gr.ChatInterface(
            fn=wrapped_predict,
            description="Enter your message and let the model call specific functions when appropriate."
        )

# Export demo for usage in __main__.py
demo = demo
