import fire
from examples import text_chat, json_chat, function_chat


def launch_chat(arg):
    demos = {
        "text": text_chat.demo,
        "json": json_chat.demo,
        "function": None
    }

    if arg not in demos or demos[arg] is None:
        raise AttributeError(f"There is no chat for: {arg}")
    
    demo = demos[arg]
    
    demo.launch(server_name="127.0.0.1", 
                server_port=8000, 
                share=False,
                show_api=False)


if __name__ == "__main__":
    fire.Fire(launch_chat)