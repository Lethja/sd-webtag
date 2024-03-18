import gradio as gr

from utility import *


def event_download_tag_set():
    # Placeholder
    print("Download Pressed")


def event_upload_files(files, tag_set):
    move_files_to_tag_set(files, tag_set)
    return event_update_gallery(tag_set)


def event_update_gallery(tag_set):
    return populate_gallery(tag_set)


def event_update_tag_dropdown(choice):
    tag_set_directory(choice)
    return gr.Dropdown(show_label=False,
                       allow_custom_value=True,
                       elem_id="tag_set",
                       choices=generate_tag_set_list(),
                       value=choice)
