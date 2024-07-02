import gradio as gr
from utils import predict

with gr.Blocks() as demo:
    """ Gradio app """
    gr.ChatInterface(predict)
