import gradio as gr
import os
from contract.ccs import CSS
from contract.utils import (
    latex_delimiters_set,
    get_file_content,
    read_conf_file,
    parse_text,
)
from contract.chat import predict


def create_ui(
    conf_path: str = "./config/para.conf", demo_mode: bool = False
) -> gr.Blocks:
    config_dict = read_conf_file(conf_path)
    with gr.Blocks(title="合同Demo 🚀", css=CSS) as demo:
        if demo_mode:
            gr.HTML(
                "<h1><center>Literature GPT: A One-stop Web UI for Getting Started with Literature GPT</center></h1>"
            )
            gr.DuplicateButton(
                value="Duplicate Space for private use", elem_classes="duplicate-button"
            )
        chatbot = gr.Chatbot(
            latex_delimiters=latex_delimiters_set,
            sanitize_html=False,
            height=600,
            show_label=False,
            avatar_images=[
                "./resources/img/user.png",
                "./resources/img/openai-black.png",
            ],
            show_share_button=False,
            placeholder=get_file_content("./resources/md/chatbot_placeholder.md"),
        )
        chat_input = gr.MultimodalTextbox(
            file_count="multiple",
            file_types=[".pdf"],
            interactive=True,
            autoscroll=False,
            placeholder="在这里输入..",
            show_label=False,
        )
        file_list = gr.Textbox(visible=False)

        def user(history, query):
            return (
                history + [[parse_text(query["text"]), ""]],
                gr.MultimodalTextbox(value=None, interactive=False),
                query["files"],
            )

        chat_input.submit(
            user, [chatbot, chat_input], [chatbot, chat_input, file_list]
        ).then(predict, [chatbot, file_list], chatbot, api_name="bot_response").then(
            lambda: gr.MultimodalTextbox(interactive=True), None, [chat_input]
        )
    return demo


def main(conf_path: str = "./config/para.conf", demo_mode: bool = False):
    os.environ["GRADIO_SHARE"] = "true"
    gradio_share = os.environ.get("GRADIO_SHARE", "0").lower() in ["true", "1"]
    server_name = os.environ.get("GRADIO_SERVER_NAME", "0.0.0.0")
    create_ui(conf_path, demo_mode).queue().launch(
        share=gradio_share, server_name=server_name, inbrowser=True
    )


if __name__ == "__main__":
    conf_path: str = "./config/para.conf"
    demo_mode: bool = False
    main(conf_path, demo_mode)
