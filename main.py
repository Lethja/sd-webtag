import gradio as gr

from utility import *

startup_tag = startup_check()

with gr.Blocks() as SDWebTag:
    with gr.Row():
        with gr.Column():
            tag_set = gr.Dropdown(label="Tag Set", allow_custom_value=True, elem_id="tag_set",
                                  choices=generate_tag_set_list(), value=startup_tag)
            gallery = gr.Gallery(label="Gallery", show_label=False, elem_id="gallery", object_fit="contain",
                                 type="filepath", value=populate_gallery(startup_tag))
        with gr.Column():
            add = gr.Textbox(label="Add Tags")
            tags = gr.CheckboxGroup(label="Tags", elem_id="tags")

    tag_set.input(switch_tag_set, inputs=tag_set, outputs=gallery)

SDWebTag.launch()
