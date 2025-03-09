#!/usr/bin/env python3

from event import *
from utility import *

def init(tag_set_state):
    set_tag_set_state(tag_set_state)

    with gr.Blocks(css=".gradio-container {min-width: 100% !important;}", title="SD WebTag") as SDWebTag:
        session_set = gr.State(value=None)
        session_img = gr.State(value=None)

        with gr.Row():
            with gr.Column(scale=1):
                with gr.Accordion("Tag Set"):
                    tag_set_dropdown = gr.Dropdown(show_label=False, allow_custom_value=True, elem_id="tag_set",
                                                   container=False, choices=generate_tag_set_list())
                    with gr.Blocks():
                        upload = gr.UploadButton(label="Upload/Import", file_types=["image", "text"],
                                                 file_count="multiple")

                    with gr.Accordion("Exports", open=False):
                        export = gr.Button("Export Tag Set")
                        explore = gr.FileExplorer(label="Exports", file_count="single", glob="*.zip", height=200,
                                                  root_dir=zip_dir(), interactive=True)
                        download = gr.DownloadButton("Download Export", interactive=False)

                gallery = gr.Gallery(label="Gallery", show_label=False, show_share_button=False,
                                     show_download_button=False, interactive=False, elem_id="gallery",
                                     object_fit="contain", type="filepath")
            with gr.Column(scale=2):
                with gr.Accordion("Add Tags", open=False):
                    with gr.Row():
                        add_tag_textbox = gr.Textbox(label="Add Tags", show_label=False, container=False,
                                                     placeholder="Enter tags here (seperated by ,) press return to add",
                                                     scale=1)
                        add_tag_all_checkbox = gr.Checkbox(label="Add to All", value=False, interactive=False, scale=0)

                tag_list = gr.CheckboxGroup(label="Tags", elem_id="tags", interactive=True)

        SDWebTag.load(event_load_page, inputs=[session_set], outputs=[tag_set_dropdown, gallery, session_set])

        add_tag_textbox.submit(event_add_tag,
                               inputs=[add_tag_textbox, tag_set_dropdown, tag_list, add_tag_all_checkbox, session_img],
                               outputs=tag_list)

        explore.change(event_explore_check, inputs=explore, outputs=download)

        # TODO: Workaround: https://github.com/gradio-app/gradio/issues/7788
        export.click(event_export_reset, inputs=tag_set_dropdown, outputs=explore).then(event_export_tag_set,
                                                                                        inputs=tag_set_dropdown,
                                                                                        outputs=explore)

        tag_list.input(event_check_tag, inputs=[tag_set_dropdown, tag_list, session_img], outputs=tag_list)

        tag_set_dropdown.input(event_update_tag_dropdown, inputs=tag_set_dropdown, outputs=[tag_set_dropdown, session_set])

        tag_set_dropdown.input(event_update_gallery, inputs=tag_set_dropdown, outputs=gallery)

        gallery.select(event_update_tag_checkbox_group, inputs=[tag_set_dropdown, gallery], outputs=[tag_list, session_img])

        upload.upload(event_upload_files, inputs=[upload, tag_set_dropdown], outputs=gallery)

    return SDWebTag


args = args_parse()
init(startup_check()).launch(share=args.share, allowed_paths=[tag_dir(), zip_dir()] + args.path_allow,
              server_name="0.0.0.0" if args.listen else "127.0.0.1")
