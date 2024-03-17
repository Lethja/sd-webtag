import gradio as gr

from utility import *


def callback_update_gallery(tag_set):
    return populate_gallery(tag_set)


def callback_update_tag_dropdown(choice):
    tag_set_directory(choice)
    return gr.Dropdown(show_label=False,
                       allow_custom_value=True,
                       elem_id="tag_set",
                       choices=generate_tag_set_list(),
                       value=choice)
