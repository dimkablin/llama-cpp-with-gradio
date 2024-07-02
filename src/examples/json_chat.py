import gradio as gr
import json

from env import DEFAULT_JSON
from utils import predict

# Initialize values
CURR_JSON = DEFAULT_JSON

def json_update(json_schema: str) -> str:
    """
    Updates the global JSON schema based on a provided JSON string.

    Args:
        json_schema (str): A JSON string to be parsed and set as the new global schema.

    Returns:
        dict: The newly parsed JSON schema, or an error message if parsing fails.
    """
    global CURR_JSON
    try:
        json_schema = json.loads(json_schema)
    except json.JSONDecodeError as e:
        return {"error": f"Invalid JSON format: {str(e)}"}
    
    CURR_JSON = json_schema
    return json_schema

def wrapped_predict(message: str, history: list) -> iter:
    """
    A generator function that yields responses from a predictive model based on the current JSON schema.

    Args:
        message (str): The message input by the user.
        history (list): A list of previous messages in the chat history.

    Yields:
        str: Predicted responses from the model.
    """
    response_format = {
        "type": "json_object",
        "schema": CURR_JSON
    }
    response = ""
    for response in predict(message, history, response_format):
        yield response

with gr.Blocks() as demo:
    gr.Markdown("# Chat Interface with JSON Schema output")

    # Here we get JSON output
    with gr.Tab("Chat"):
        chatbot = gr.ChatInterface(
            fn=wrapped_predict,
            description="Enter your message and get a response based on the validated JSON schema.",
            examples=[
                "Первая книга, которую я прочитал, была написана Джорджем Оруэллом и называлась 1984.",
                "Второй по счету книгой в моей коллекции является Мастер и Маргарита Михаила Булгакова."
            ]
        )

    # Here we can change the response JSON
    with gr.Tab("Settings"):
        json_input = gr.Textbox(value=json.dumps(CURR_JSON, ensure_ascii=False, indent=4), lines=15, label="Edit JSON Schema")
        json_output = gr.JSON(value=CURR_JSON, label="JSON Schema")

        update_button = gr.Button("Update JSON Schema")
        update_button.click(fn=json_update, inputs=json_input, outputs=json_output)
