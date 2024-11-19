import gradio as gr
import json
from utils import predict

robot_position = [5, 5]  

def robot_move(direction: str):
    global robot_position
    x, y = robot_position
    if direction == "UP":
        x -= 1
    elif direction == "DOWN":
        x += 1
    elif direction == "LEFT":
        y -= 1
    elif direction == "RIGHT":
        y += 1
    else:
        return {"message": f"The robot cannot move {direction}."}
    
    # Update robot position
    robot_position = [x, y]
    return {"message": f"The robot has moved {direction} to position ({x}, {y})."}

# Dictionary to map function names to actual function calls
FUNCTIONS = {
    "robot_move": robot_move
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
    response_format = {
        "type": "json_object",
        "schema": CURR_JSON
    }
    message = "Create JSON with this text: " + message

    for response in predict(message, history, response_format=response_format):
        yield response
        # try:
        #     function_call = json.loads(response)
        # except json.JSONDecodeError:
        #     yield response
        #     return

        # if function_call:
        #     function_name = function_call.get("function_name")
        #     args = function_call.get("args", {})
        #     # Call the appropriate function
        #     if function_name in FUNCTIONS:
        #         function_result = FUNCTIONS[function_name](**args)
        #         yield json.dumps(function_result)
        #     else:
        #         yield json.dumps({"error": "Function not found."})
        # else:
        #     yield response

with gr.Blocks(css=".gap { min-height: 75vh; }") as demo:
    gr.Markdown("# Chat Interface with Robot Movement Example")

    with gr.Tab("Chat"):
        chatbot = gr.ChatInterface(
            fn=wrapped_predict,
            description="Enter your message and control the robot by issuing commands such as 'move up', 'move down', etc."
        )

demo = demo

CURR_JSON = {
    "type": "function",
    "function": {
        "name": "robot_move",
        "description": "Move the robot in one of the four cardinal directions.",
        "parameters": {
            "type": "object",
            "properties": {
                "direction": {
                    "type": "object",
                    "enum": ["UP", "DOWN", "RIGHT", "LEFT"],
                    "description": "The next move of the robot."
                }
            },
            "required": ["direction"]
        },
        "required": ["name", "parameters"]
    },
    "required": ["function"]
}