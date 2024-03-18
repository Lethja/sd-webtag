import glob
import os
import pathlib
import shutil

global_tag_sets_dir = os.path.abspath("Sets")


def generate_tag_set_list():
    r = []
    ld = os.listdir(global_tag_sets_dir)

    for e in ld:
        if os.path.isdir(os.path.join(global_tag_sets_dir, e)):
            r.append(e)

    r.sort()
    return r


def move_files_to_tag_set(files, tag_set):
    for file in files:
        p = pathlib.Path(file)
        shutil.move(p, pathlib.PurePath(global_tag_sets_dir + "/" + tag_set + "/" + p.name))


def populate_gallery(tag_set) -> list[str]:
    r = []
    ex = ("*.[Jj][Pp][Ee][Gg]", "*.[Jj][Pp][Gg]", "*.[Pp][Nn][Gg]", "*.[Ss][Vv][Gg]")
    d = os.path.join(global_tag_sets_dir, tag_set)

    for e in ex:
        r.extend(glob.glob(os.path.join(d, e)))

    return r


def startup_check():
    if not os.path.isdir(global_tag_sets_dir):
        os.mkdir(global_tag_sets_dir)

    existing_tag_sets = generate_tag_set_list()

    if len(existing_tag_sets) == 0:
        set_tag = "Default"
        tag_set_directory(set_tag)
    else:
        set_tag = existing_tag_sets[0]

    return set_tag


def tag_set_directory(tag_set):
    fullpath = os.path.join(global_tag_sets_dir, tag_set)
    if not os.path.isdir(fullpath):
        os.mkdir(fullpath)
