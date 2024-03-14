import glob
import os

tag_set_dir = os.path.abspath("Sets")


def generate_tag_set_list():
    r = []
    ld = os.listdir(tag_set_dir)

    for e in ld:
        if os.path.isdir(os.path.join(tag_set_dir, e)):
            r.append(e)

    r.sort()
    return r


def populate_gallery(tag_set) -> list[str]:  # TODO: Call when tag set changes and get all images in the new location
    r = []
    ex = ("*.jpeg", "*.jpg", "*.png", "*.svg")
    d = os.path.join(tag_set_dir, tag_set)

    for e in ex:
        r.extend(glob.glob(os.path.join(d, e)))

    return r


def startup_check():
    if not os.path.isdir(tag_set_dir):
        os.mkdir(tag_set_dir)

    existing_tag_sets = generate_tag_set_list()

    if len(existing_tag_sets) == 0:
        set_tag = "Default"
        os.mkdir(os.path.join(tag_set_dir, set_tag))
    else:
        set_tag = existing_tag_sets[0]

    return set_tag


def switch_tag_set(tag_set):
    if tag_set is not list:
        fullpath = os.path.join(tag_set_dir, tag_set)
        if not os.path.isdir(fullpath):
            os.mkdir(fullpath)

    return populate_gallery(tag_set)

