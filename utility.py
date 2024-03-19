import glob
import io
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


def get_all_tags(tag_set):
    t = []
    d = os.path.join(global_tag_sets_dir, tag_set)
    r = glob.glob(os.path.join(d, "*.[Tt][Xx][Tt]"))

    for txt in r:
        s = read_tag_file(txt)

        for i in range(len(s)):
            s[i] = s[i].strip()
            if len(s[i]) and s[i] not in t:
                t.append(s[i])

    t.sort()
    return t


def get_image_tag(tag_set, name):
    global global_tag_sets_dir
    g = pathlib.PurePath(name)
    p = pathlib.PurePath(global_tag_sets_dir + "/" + tag_set + "/" + g.name)
    files = glob.glob(os.path.join(p, "*.[Tt][Xx][Tt]"))
    file = str(p) + ".txt"

    if len(files) > 1:
        merge_tag_files(files, file)

    return read_tag_file(file)


def merge_tag_files(files, merge_file):
    r = []
    for file in files:
        tags = read_tag_file(file)
        for tag in tags:
            if tag not in r:
                r.append(tag)
        os.remove(file)

    write_tags_to_file(r, merge_file)


def read_tag_file(file):
    if not os.path.exists(file) or os.path.getsize(file) > 1024:
        return []

    f = io.open(file)
    c = f.read()
    f.close()

    s = c.split(",")

    for i in range(len(s)):
        s[i] = s[i].strip()
        if not len(s[i]):
            s.remove(s[i])

    return s


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


def write_tags_to_file(tags, file):
    tags.sort()
    s = ", ".join(tags)
    f = io.open(file, "w")
    f.write(s)
    f.close()
