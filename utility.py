import glob
import os

tag_set_dir = os.path.abspath("Sets")


def generate_tag_set_list():
    r = []
    ld = os.listdir(tag_set_dir)

    for e in ld:
        if os.path.isdir(os.path.join(tag_set_dir, e)):
            r.append(e)

    return r


def populate_gallery():  # TODO: Call when tag set changes and get all images in the new location
    r = []
    ex = ("*.jpeg", "*.jpg", "*.png", "*.svg")

    for e in ex:
        r.extend(glob.glob(os.path.join(tag_set_dir, e)))

    return r.sort()
