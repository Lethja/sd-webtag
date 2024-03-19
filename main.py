from event import *
from utility import *


def init():
    global global_tag_set_state
    global_tag_set_state = startup_check()

    with gr.Blocks() as SDWebTag:
        with gr.Row():
            with gr.Column():
                with gr.Accordion("Tag Set"):
                    tag_set_dropdown = event_update_tag_dropdown(global_tag_set_state)
                    with gr.Blocks():
                        with gr.Row():
                            upload = gr.UploadButton(label="Import",
                                                     file_types=["image", "text"],
                                                     file_count="multiple")
                            download = gr.DownloadButton("Export")

                gallery = gr.Gallery(label="Gallery",
                                     show_label=False,
                                     show_share_button=False,
                                     show_download_button=False,
                                     interactive=False,
                                     elem_id="gallery",
                                     object_fit="contain",
                                     type="filepath")
            with gr.Column():
                with gr.Accordion("Add Tags", open=False):
                    add = gr.Textbox(label="Add Tags", show_label=False)

                tags = gr.CheckboxGroup(label="Tags",
                                        elem_id="tags",
                                        interactive=True)

        SDWebTag.load(event_load_page, outputs=[tag_set_dropdown, gallery])

        tag_set_dropdown.input(event_update_tag_dropdown,
                               inputs=tag_set_dropdown,
                               outputs=tag_set_dropdown)

        tag_set_dropdown.input(event_update_gallery,
                               inputs=tag_set_dropdown,
                               outputs=gallery)

        gallery.select(event_update_tag_checkbox_group, inputs=[tag_set_dropdown, gallery], outputs=tags)

        upload.upload(event_upload_files,
                      inputs=[upload, tag_set_dropdown],
                      outputs=gallery)

        download.click(event_download_tag_set)

    return SDWebTag


init().launch()
