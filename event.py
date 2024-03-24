import gradio as gr

from utility import *

global_tag_set_state = None
global_tag_set_image = None


def event_add_tag(add_tag, tag_set, tag_list):
    split = add_tag.split(",")
    k = 0

    for i in range(len(split)):
        split[i] = split[i].strip()
        if len(split[i]) and split[i] not in tag_list:
            tag_list.append(split[i])
            k += 1

    if not k:
        return tag_list

    file = get_image_tag_file(tag_set, global_tag_set_image)

    write_tags_to_file(tag_list, file)

    all_tags = get_all_tags(tag_set)
    tags = read_tag_file(file)
    return gr.CheckboxGroup(label="Tags",
                            elem_id="tags",
                            interactive=True,
                            choices=all_tags,
                            value=tags)


def event_check_tag(tag_set, tag_list):
    file = get_image_tag_file(tag_set, global_tag_set_image)
    write_tags_to_file(tag_list, file)
    return tag_list


def event_export_tag_set(tag_set):
    p = os.path.join(global_tag_sets_dir, tag_set)
    z = zip_create_from_directory(p)
    return gr.DownloadButton("Download", value=z)


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
    global global_tag_set_image

    all_tags = get_all_tags(tag_set)
    global_tag_set_image = name[evt.index][0]
    file = get_image_tag_file(tag_set, global_tag_set_image)
    tags = read_tag_file(file)
    return gr.CheckboxGroup(label="Tags",
                            elem_id="tags",
                            interactive=True,
                            choices=all_tags,
                            value=tags)


def event_update_tag_state(choice):
    return choice
