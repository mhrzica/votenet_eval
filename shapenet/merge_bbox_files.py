import argparse
import numpy as np
import pathlib
from pathlib import Path


def merge_bbox_files(output_path, bboxes_path, fixed_height_bboxes_path=[], partially_visible_bboxes_path=[]):
    bboxes_file_list = [x for x in Path(bboxes_path).rglob("*.npy")]

    for iFile in sorted(bboxes_file_list, reverse=False):

        bbox_list = []

        bbox_original = np.load(iFile)
        if bbox_original.ndim == 1:
            for iBox in range(0, bbox_original.size, 8):
                box = bbox_original[iBox : iBox + 8]
                bbox_list.append(box)
        else:
            bbox_list = bbox_original

        if fixed_height_bboxes_path:
            add_bbox_path = fixed_height_bboxes_path + "/" + iFile.name
            path = Path(add_bbox_path)

            if path.is_file():
                bboxes_fixed_height = np.load(add_bbox_path)

                for iBox in range(0, bboxes_fixed_height.size, 8):
                    box = bboxes_fixed_height[iBox : iBox + 8]
                    bbox_list.append(box)

        if partially_visible_bboxes_path:
            add_bbox_path = partially_visible_bboxes_path + "/" + iFile.name
            path = Path(add_bbox_path)
            if path.is_file():
                partially_visible_bboxes = np.load(add_bbox_path)

                for iBox in range(0, partially_visible_bboxes.size, 8):
                    box = partially_visible_bboxes[iBox : iBox + 8]
                    bbox_list.append(box)

        bbox_merged_path = output_path + "/" + iFile.name
        np.save(bbox_merged_path, bbox_list)

        stop = 1


def merge_bbox_files_v2(scenes_path, gt_path, output_path):
    scenes_list = [x.stem for x in Path(scenes_path).rglob("*.ply")]

    for scene in sorted(scenes_list, reverse=False):

        bbox_file = scene + "_bbox.npy"
        gt_path_list = [
            pathlib.PurePath(gt_path, "bbox_npy", bbox_file),
            pathlib.PurePath(gt_path, "fixed_height_bbox_npy", bbox_file),
            pathlib.PurePath(gt_path, "Max_height_bbox_slice_of_shelf_npy", bbox_file),
        ]
        merged_bboxes_path = pathlib.PurePath(output_path, bbox_file)

        bbox_list = []
        for gt_file in gt_path_list:

            if Path(gt_file).is_file():
                bboxes_load = np.load(gt_file)

                if bboxes_load.ndim > 1:
                    bboxes_load = bboxes_load.flatten()

                for iBox in range(0, bboxes_load.size, 8):
                    box = bboxes_load[iBox : iBox + 8]
                    bbox_list.append(box)

        np.save(merged_bboxes_path, bbox_list)

        stop = 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--scenes_path", help="Path to scenes folder. Scenes should be in ply format.")
    parser.add_argument(
        "--gt_path",
        help="Path to GT folder. This folder should have three folders: bbox_npy, fixed_height... and max_height...",
    )
    parser.add_argument("--output_path", help="Path to folder where merged bbox files will be saved.")
    parser.add_argument("--bboxes_path", help="")
    parser.add_argument(
        "--fixed_height_bboxes_path",
        help="Add this path if you want to merge original bbox files with top bboxes with fixed height",
    )
    parser.add_argument(
        "--partially_visible_bboxes_path",
        help="Add this path if you want to merge original bbox files with partially visible top bboxes",
    )
    args = parser.parse_args()

    # If both fixed_height_bboxes_path and partially_visible_bboxes_path are given, all bboxes will be merged with original bboxes
    # If only one of the paths is given, program will merge original bboxes and bboxes

    # merge_bbox_files(
    #     args.output_path, args.bboxes_path, args.fixed_height_bboxes_path, args.partially_visible_bboxes_path
    # )

    merge_bbox_files_v2(args.scenes_path, args.gt_path, args.output_path)
    print("DONE!")
