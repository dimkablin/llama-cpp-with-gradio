import gradio as gr
from utils import predict

with gr.Blocks(css=".gap { min-height: 85vh; }") as demo:
    """ Gradio app """
    gr.ChatInterface(predict)
