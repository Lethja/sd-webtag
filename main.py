import argparse
from event import *
from utility import *


def args_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("--listen",
                        action="store_true",
                        help="Listen to all network traffic on the local network")

    parser.add_argument("--share",
                        action="store_true",
                        default=False,
                        help="Use the Gradio tunnel make the server over the internet to friends (and strangers)")
    return parser.parse_args()


def init():
    global global_tag_set_state
    global_tag_set_state = startup_check()

    with gr.Blocks(css=".gradio-container {min-width: 100% !important;}") as SDWebTag:
        with gr.Row():
            with gr.Column(scale=1):
                with gr.Accordion("Tag Set"):
                    tag_set_dropdown = event_update_tag_dropdown(global_tag_set_state)
                    with gr.Blocks():
                        upload = gr.UploadButton(label="Upload/Import",
                                                 file_types=["image", "text"],
                                                 file_count="multiple")

                    with gr.Accordion("Exports", open=False):
                        export = gr.Button("Export Tag Set")
                        explore = gr.FileExplorer(label="Exports",
                                                  file_count="single",
                                                  glob="*.zip",
                                                  root_dir=global_zip_sets_dir,
                                                  interactive=True)
                        download = gr.DownloadButton("Download Export", interactive=False)

                gallery = gr.Gallery(label="Gallery",
                                     show_label=False,
                                     show_share_button=False,
                                     show_download_button=False,
                                     interactive=False,
                                     elem_id="gallery",
                                     object_fit="contain",
                                     type="filepath")
            with gr.Column(scale=2):
                with gr.Accordion("Add Tags", open=False):
                    add_tag_textbox = gr.Textbox(label="Add Tags", show_label=False, container=False)

                tag_list = gr.CheckboxGroup(label="Tags",
                                            elem_id="tags",
                                            interactive=True)

        SDWebTag.load(event_load_page,
                      outputs=[tag_set_dropdown, gallery])

        add_tag_textbox.submit(event_add_tag,
                               inputs=[add_tag_textbox, tag_set_dropdown, tag_list],
                               outputs=tag_list)

        explore.change(event_explore_check,
                       inputs=explore,
                       outputs=download)

        export.click(event_export_tag_set,
                     inputs=tag_set_dropdown,
                     outputs=explore,
                     show_progress="full")

        tag_list.input(event_check_tag,
                       inputs=[tag_set_dropdown, tag_list],
                       outputs=tag_list)

        tag_set_dropdown.input(event_update_tag_dropdown,
                               inputs=tag_set_dropdown,
                               outputs=tag_set_dropdown)

        tag_set_dropdown.input(event_update_gallery,
                               inputs=tag_set_dropdown,
                               outputs=gallery)

        gallery.select(event_update_tag_checkbox_group,
                       inputs=[tag_set_dropdown, gallery],
                       outputs=tag_list)

        upload.upload(event_upload_files,
                      inputs=[upload, tag_set_dropdown],
                      outputs=gallery)

    return SDWebTag


args = args_parse()
init().launch(share=args.share,
              server_name="0.0.0.0" if args.listen else "127.0.0.1")
