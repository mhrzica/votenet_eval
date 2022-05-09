import argparse
import numpy as np
import pathlib
from pathlib import Path
import re
import shutil


# def merge_dataset_files(scenes_path, gt_path, output_path):


# if __name__ == "__main__":
#     parser = argparse.ArgumentParser()
#     parser.add_argument("--scenes_path", help="Path to scenes folder. Scenes should be in ply format.")
#     parser.add_argument(
#         "--gt_path",
#         help="Path to GT folder. This folder should have three folders: bbox_npy, fixed_height... and max_height...",
#     )
#     parser.add_argument("--output_path", help="Path to folder where merged bbox files will be saved.")

#     args = parser.parse_args()

#     # If both fixed_height_bboxes_path and partially_visible_bboxes_path are given, all bboxes will be merged with original bboxes
#     # If only one of the paths is given, program will merge original bboxes and bboxes

#     # merge_bbox_files(
#     #     args.output_path, args.bboxes_path, args.fixed_height_bboxes_path, args.partially_visible_bboxes_path
#     # )

#     merge_dataset_files(args.scenes_path, args.gt_path, args.output_path)
#     print("DONE!")

SRC_DIRS = [
    {
        "dir_path": "/media/mateja/ubuntu_storage/Datasets/KINECT/K1-13_supporting_plane/gt/bookshelf/merged_bboxes",
        "pattern": "*.npy",
    },
    {"dir_path": "/media/mateja/ubuntu_storage/Datasets/KINECT/K1-13_supporting_plane/bookshelf", "pattern": "*.npz",},
    {
        "dir_path": "/media/mateja/ubuntu_storage/Datasets/KINECT/K1-13_supporting_plane/gt/bookshelf_clutter/merged_bboxes",
        "pattern": "*.npy",
    },
    {
        "dir_path": "/media/mateja/ubuntu_storage/Datasets/KINECT/K1-13_supporting_plane/bookshelf_clutter",
        "pattern": "*.npz",
    },
    {
        "dir_path": "/media/mateja/ubuntu_storage/Datasets/KINECT/K1-13_supporting_plane/gt/desk/merged_bboxes",
        "pattern": "*.npy",
    },
    {"dir_path": "/media/mateja/ubuntu_storage/Datasets/KINECT/K1-13_supporting_plane/desk", "pattern": "*.npz",},
    {
        "dir_path": "/media/mateja/ubuntu_storage/Datasets/KINECT/K1-13_supporting_plane/gt/desk2a/merged_bboxes",
        "pattern": "*.npy",
    },
    {"dir_path": "/media/mateja/ubuntu_storage/Datasets/KINECT/K1-13_supporting_plane/desk2a", "pattern": "*.npz",},
    {
        "dir_path": "/media/mateja/ubuntu_storage/Datasets/KINECT/K1-13_supporting_plane/gt/desk2b/merged_bboxes",
        "pattern": "*.npy",
    },
    {"dir_path": "/media/mateja/ubuntu_storage/Datasets/KINECT/K1-13_supporting_plane/desk2b", "pattern": "*.npz",},
]
OUTPUT_DIR = "/media/mateja/ubuntu_storage/Datasets/KINECT/test_dataset"


def collect_all_files(dir_path, glob_pattern):
    files = {}
    src_dir = Path(dir_path)
    files[src_dir.name] = {}
    files[src_dir.name]["files"] = [file for file in src_dir.rglob(glob_pattern)]
    if files[src_dir.name]["files"]:
        match = re.match(r"(?P<number>\d+)_(?P<type>\w+)", str(files[src_dir.name]["files"][0].name))
        if match:
            files[src_dir.name]["type"] = match.group("type")
        files[src_dir.name]["size"] = len(files[src_dir.name]["files"])
    else:
        files[src_dir.name]["size"] = 0
        files[src_dir.name]["type"] = "none"

    return files


def get_output_index_status():
    npy_files = collect_all_files(OUTPUT_DIR, "*.npy")
    npz_files = collect_all_files(OUTPUT_DIR, "*.npz")
    return {
        list(npz_files.values())[0]["type"]: {"current_index": list(npz_files.values())[0]["size"]},
        list(npy_files.values())[0]["type"]: {"current_index": list(npy_files.values())[0]["size"]},
    }


def save_to_output_dir(input_files):
    index_dict = get_output_index_status()

    for current_dict in input_files:
        for dir_name, dict_data in current_dict.items():
            current_type = dict_data["type"]
            if current_type in index_dict:
                current_index = index_dict[current_type]["current_index"]
            else:
                index_dict[current_type] = {"current_index": 0}
                current_index = 0
            print(f"Saving files from {dir_name}")
            for file in sorted(dict_data["files"]):
                print(file)
                output_file_name = f"{current_index:06d}_{dict_data['type']}{file.suffix}"
                output_file = Path(OUTPUT_DIR) / output_file_name
                print(output_file)
                shutil.copy(file, output_file)
                current_index += 1
            index_dict[current_type]["current_index"] = current_index


def main():
    input_files = []
    for src in SRC_DIRS:
        input_files.append(collect_all_files(src.get("dir_path"), src.get("pattern")))
    save_to_output_dir(input_files)


if __name__ == "__main__":
    main()
