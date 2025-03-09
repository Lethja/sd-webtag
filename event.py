import gradio as gr

from utility import *

# TODO: Remove these globals if possible, use gr.State() object(s) instead
global_tag_set_state = None
global_tag_set_image = None


def event_add_tag(add_tag, tag_set, tag_list, add_tag_all_checkbox, session_tag_set):
    # TODO: Add logic for when add_tag_all_checkbox is True
    if global_tag_set_image is None and add_tag_all_checkbox is False:
        return tag_list

    split = add_tag.split(",")

    if not split:
        return tag_list

    for i, part in enumerate(split):
        part = part.strip().title()
        if len(part) and part not in tag_list:
            tag_list.append(part)

    file = get_image_tag_file(tag_set, session_tag_set.value)

    write_tags_to_file(tag_list, file)

    all_tags = get_all_tags(tag_set)
    tags = read_tag_file(file)
    return gr.CheckboxGroup(label="Tags", elem_id="tags", interactive=True, choices=all_tags, value=tags)


def event_check_tag(tag_set, tag_list):
    file = get_image_tag_file(tag_set, global_tag_set_image)
    write_tags_to_file(tag_list, file)
    return tag_list


def event_explore_check(z):
    return gr.DownloadButton("Download Export", value=z, interactive=True if z else False)


def event_export_reset(tag_set):
    # TODO: Workaround: https://github.com/gradio-app/gradio/issues/7788
    p = os.path.join(tag_dir(), tag_set)
    return gr.FileExplorer(label="Exporting", height=200, root_dir=str(p))


def event_export_tag_set(tag_set):
    p = os.path.join(tag_dir(), tag_set)
    zip_create_from_directory(p)
    return gr.FileExplorer(label="Exports", glob="*.zip", height=200, root_dir=zip_dir())


def event_load_page(session_tag_set):
    global global_tag_set_state

    if session_tag_set is None or session_tag_set.value is None:
        tag_set = global_tag_set_state
    else:
        tag_set = session_tag_set.value

    d, s = event_update_tag_dropdown(tag_set)
    g = populate_gallery(tag_set)
    return d, g, s


def event_upload_files(files, tag_set):
    move_files_to_tag_set(files, tag_set)
    return event_update_gallery(tag_set)


def event_update_gallery(tag_set):
    return populate_gallery(tag_set)


def event_update_tag_dropdown(choice):
    tag_set_directory(choice)
    global global_tag_set_state
    global_tag_set_state = choice
    return [gr.Dropdown(show_label=False, allow_custom_value=True, elem_id="tag_set", container=False,
                       choices=generate_tag_set_list(), value=choice), gr.State(value=choice)]


def event_update_tag_checkbox_group(evt: gr.SelectData, tag_set, name):
    all_tags = get_all_tags(tag_set)
    session_img = gr.State(name[evt.index][0])
    file = get_image_tag_file(tag_set, session_img.value)
    tags = read_tag_file(file)

    return [gr.CheckboxGroup(label="Tags", elem_id="tags", interactive=True, choices=all_tags, value=tags), session_img]


def event_update_tag_state(choice):
    return choice


def set_tag_get_state():
    global global_tag_set_state
    return global_tag_set_state


def set_tag_set_state(state):
    global global_tag_set_state
    global_tag_set_state = state
