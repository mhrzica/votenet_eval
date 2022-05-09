import argparse
import logging
import numpy as np
import os
from pathlib import Path

def change_heading_angle(bboxes_folder_path, save_path=None):
    bboxes_file_list = [x for x in Path(bboxes_folder_path).rglob("*.npy")]

    if not bboxes_file_list:
        logging.error("No (bbox).npy files found")
        raise Exception("No (bbox).npy files found")
    
    for iFile in bboxes_file_list:
        bboxes = np.load(iFile)
        for iBox in bboxes:
            iBox[6] *= -1
        np.save(iFile, bboxes)

def change_class_label(bboxes_folder_path, save_path=None):
    bboxes_file_list = [x for x in Path(bboxes_folder_path).rglob("*.npy")]

    if not bboxes_file_list:
        logging.error("No (bbox).npy files found")
        raise Exception("No (bbox).npy files found")
    
    for iFile in bboxes_file_list:
        bboxes = np.load(iFile)
        for iBox in bboxes:
            iBox[7] = 8.
        np.save(iFile, bboxes)

def change_bbox_files_to_zeros(bboxes_folder_path, save_path=None):
    bboxes_file_list = [x for x in Path(bboxes_folder_path).rglob("*.npy")]

    if not bboxes_file_list:
        logging.error("No (bbox).npy files found")
        raise Exception("No (bbox).npy files found")
    
    for iFile in bboxes_file_list:
        bboxes = [np.zeros([8,])]
        np.save(iFile, bboxes)

def create_missing_empty_votes_files(bboxes_folder_path, save_path=None):
    bboxes_file_list = [x for x in Path(bboxes_folder_path).rglob("*.npy")]

    if not bboxes_file_list:
        logging.error("No (bbox).npy files found")
        raise Exception("No (bbox).npy files found")
    
    for iFile in bboxes_file_list:
        point_votes = np.zeros([50000,10])
        
        votes_file = '%s_%s'%(iFile.stem[:-5], 'votes.npz')
        votes_path = os.path.join(bboxes_folder_path, votes_file)
        np.savez_compressed(votes_path, point_votes = point_votes)
        stop = 1

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_path', help='Path to folder containing .npy files with bboxes.')
    parser.add_argument("--change_heading_angle", action="store_true", help="Switch heading angle.")
    parser.add_argument("--change_class_label", action="store_true", help="Change bbox class index.")
    parser.add_argument("--empty_bboxes", action="store_true", help="Save /empty/ bbox files.")
    parser.add_argument("--empty_votes", action="store_true", help="Save /empty/ bbox files.")
    args = parser.parse_args()

    if args.change_heading_angle:
        print('Changing heading angles in:\n%s'%args.data_path)
        change_heading_angle(args.data_path)
        print("DONE!")
    
    if args.change_class_label:
        print('Changing class labels in:\n%s'%args.data_path)
        change_class_label(args.data_path)
        print("DONE!")

    if args.empty_bboxes:
        print('Save "empty" _bboxes.npy in:\n%s'%args.data_path)
        change_bbox_files_to_zeros(args.data_path)
        print("DONE!")
    
    if args.empty_votes:
        print('Save "empty" _votes.npz in:\n%s'%args.data_path)
        create_missing_empty_votes_files(args.data_path)
        print("DONE!")