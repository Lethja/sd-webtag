import gradio as gr


with gr.Blocks() as SDWebTag:
    with gr.Row():
        with gr.Column():
            tag_set = gr.Dropdown(label="Tag Set", allow_custom_value=True, elem_id="tag_set")
            gallery = gr.Gallery(label="Gallery", show_label=False, elem_id="gallery", object_fit="contain",
                                 type="filepath")
        with gr.Column():
            add = gr.Textbox(label="Add Tags")
            tags = gr.CheckboxGroup(label="Tags", elem_id="tags")

SDWebTag.launch()