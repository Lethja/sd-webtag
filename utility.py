import argparse
import glob
import io
import os
import pathlib
import shutil

global_tag_sets_dir = os.path.abspath("Sets")
global_zip_sets_dir = os.path.abspath("Zips")


def args_parse():
    global global_tag_sets_dir, global_zip_sets_dir

    parser = argparse.ArgumentParser()

    parser.add_argument("--path",
                        default=os.path.abspath("Sets"),
                        help="Where to store images and their tags")

    parser.add_argument("--listen",
                        action="store_true",
                        help="Accept connections from everywhere with direct access to the server. " +
                             "In a home/office environment this usually means other devices in the same IPv4 subnet")

    parser.add_argument("--share",
                        action="store_true",
                        default=False,
                        help="Create a Gradio SSH tunnel to make this server accessible from the Internet " +
                             "to friends and strangers alike through gratio.live")

    parser.add_argument("--zip",
                        default=os.path.abspath("Zips"),
                        help="Where to write Zips for exporting")

    args = parser.parse_args()
    global_tag_sets_dir = os.path.abspath(os.path.expandvars(os.path.expanduser(args.path)))
    global_zip_sets_dir = os.path.abspath(os.path.expandvars(os.path.expanduser(args.zip)))

    return args


def generate_tag_set_list():
    r = []
    ld = os.listdir(tag_dir())

    for e in ld:
        if os.path.isdir(os.path.join(tag_dir(), e)):
            r.append(e)

    r.sort()
    return r


def get_all_tags(tag_set):
    t = []
    d = os.path.join(tag_dir(), tag_set)
    r = glob.glob(os.path.join(d, "*.[Tt][Xx][Tt]"))

    for txt in r:
        s = read_tag_file(txt)

        for i, part in enumerate(s):
            part = part.strip()
            if part and part not in t:
                t.append(part)

    t.sort()
    return t


def get_image_tag_file(tag_set, name):
    global global_tag_sets_dir
    g = pathlib.PurePath(name)
    p = pathlib.PurePath(tag_dir() + "/" + tag_set + "/" + g.stem)
    files = glob.glob(os.path.join(p, ".[Tt][Xx][Tt]"))
    file = str(p) + ".txt"

    if len(files) > 1:
        merge_tag_files(files, file)

    return file


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
    if not os.path.exists(file) or os.path.getsize(file) > 2048:
        return []

    f = io.open(file)
    c = f.read()
    f.close()

    s = c.split(",")

    for i, part in enumerate(s):
        part = part.strip()
        if not part:
            s.remove(part)

    return s


def move_files_to_tag_set(files, tag_set):
    for file in files:
        p = pathlib.Path(file)
        d = pathlib.PurePath(tag_dir() + "/" + tag_set + "/" + p.name)
        shutil.move(p, d)


def populate_gallery(tag_set) -> list[str]:
    r = []
    ex = ("*.[Jj][Pp][Ee][Gg]", "*.[Jj][Pp][Gg]", "*.[Pp][Nn][Gg]", "*.[Ss][Vv][Gg]")
    d = os.path.join(tag_dir(), tag_set)

    for e in ex:
        r.extend(glob.glob(os.path.join(d, e)))

    return r


def startup_check():
    if not os.path.isdir(zip_dir()):
        pathlib.Path(zip_dir()).mkdir(parents=True, exist_ok=True)

    if not os.path.isdir(tag_dir()):
        pathlib.Path(tag_dir()).mkdir(parents=True, exist_ok=True)

    existing_tag_sets = generate_tag_set_list()
    set_tag = next(iter(existing_tag_sets), "Default")
    tag_set_directory(set_tag)

    return set_tag


def tag_dir():
    return global_tag_sets_dir


def tag_set_directory(tag_set):
    fullpath = os.path.join(tag_dir(), tag_set)
    if not os.path.isdir(fullpath):
        os.mkdir(fullpath)


def write_tags_to_file(tags, file):
    tags.sort()
    s = ", ".join(tags)
    f = io.open(file, "w")
    f.write(s)
    f.close()


def zip_create_from_directory(directory):
    from datetime import datetime, timezone

    d = pathlib.PurePath(directory)
    n = d.name + " " + datetime.now(timezone.utc).isoformat(timespec="seconds")
    return shutil.make_archive(zip_dir() + "/" + n, "zip", d)


def zip_dir():
    return global_zip_sets_dir
