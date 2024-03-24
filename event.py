import gradio as gr

from utility import *

global_tag_set_state = None


def event_download_tag_set():
    # Placeholder
    print("Download Pressed")


def event_load_page():
    global global_tag_set_state
    d = event_update_tag_dropdown(global_tag_set_state)
    g = populate_gallery(global_tag_set_state)
    return d, g


def event_upload_files(files, tag_set):
    move_files_to_tag_set(files, tag_set)
    return event_update_gallery(tag_set)


def event_update_gallery(tag_set):
    return populate_gallery(tag_set)


def event_update_tag_dropdown(choice):
    tag_set_directory(choice)
    global global_tag_set_state
    global_tag_set_state = choice
    return gr.Dropdown(show_label=False,
                       allow_custom_value=True,
                       elem_id="tag_set",
                       container=False,
                       choices=generate_tag_set_list(),
                       value=choice)


def event_update_tag_checkbox_group(evt: gr.SelectData, tag_set, name):
    all_tags = get_all_tags(tag_set)
    file = get_image_tag_file(tag_set, name[evt.index][0])
    tags = read_tag_file(file)
    return gr.CheckboxGroup(label="Tags",
                            elem_id="tags",
                            interactive=True,
                            choices=all_tags,
                            value=tags)


def event_update_tag_state(choice):
    return choice
