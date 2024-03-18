from event import *
from utility import *


def init():
    startup_tag = startup_check()

    with gr.Blocks() as SDWebTag:
        with gr.Row():
            with gr.Column():
                with gr.Accordion("Tag Set"):
                    tag_set_dropdown = event_update_tag_dropdown(startup_tag)
                    with gr.Blocks():
                        with gr.Row():
                            upload = gr.UploadButton(label="Import",
                                                     file_types=["image", "text"],
                                                     file_count="multiple")
                            download = gr.DownloadButton("Export")

                gallery = gr.Gallery(label="Gallery",
                                     show_label=False,
                                     elem_id="gallery",
                                     object_fit="contain",
                                     type="filepath",
                                     value=populate_gallery(startup_tag))
            with gr.Column():
                with gr.Accordion("Add Tags", open=False):
                    add = gr.Textbox(label="Add Tags", show_label=False)

                tags = gr.CheckboxGroup(label="Tags", elem_id="tags")

        SDWebTag.load(event_update_gallery, inputs=tag_set_dropdown, outputs=gallery)
        tag_set_dropdown.input(event_update_tag_dropdown, inputs=tag_set_dropdown, outputs=tag_set_dropdown)
        tag_set_dropdown.input(event_update_gallery, inputs=tag_set_dropdown, outputs=gallery)
        upload.upload(event_upload_files, inputs=[upload, tag_set_dropdown], outputs=gallery)
        download.click(event_download_tag_set)

    return SDWebTag


init().launch()
