import argparse
import logging
import numpy as np
import os
from pathlib import Path

def get_box3d_dim_statistics(bboxes_folder_path, save_path=None):
    bboxes_file_list = [x for x in Path(bboxes_folder_path).rglob("*.npy")]

    if not bboxes_file_list:
        logging.error("No (bbox).npy files found")
        raise Exception("No (bbox).npy files found")
    
    dimension_list = []
    for iFile in bboxes_file_list:
        bboxes = np.load(iFile)

        if bboxes.sum() == 0:
            stop = 1
            continue

        for iBox in bboxes:
            dimension_list.append(np.array([iBox[3], iBox[4], iBox[5]])) 
    
    median_box3d = np.median(dimension_list,0)
    print("\n\nMedian bbox size: np.array([%f,%f,%f])" % \
        (median_box3d[0]*2, median_box3d[1]*2, median_box3d[2]*2))

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_path', help='Path to folder containing .npy files with bboxes.')
    args = parser.parse_args()

    # bboxes_folder_path = '/media/mateja/ubuntu_storage/Git_repos/votenet/shapenet/pc_bbox_votes_50k_train/'
    get_box3d_dim_statistics(args.data_path)
    print("DONE!")