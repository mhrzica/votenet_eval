import argparse
import os
import shutil 
from random import sample
from pathlib import Path
import math
import numpy as np

def copy_dataset_files(scene, input_folder_path, output_folder_path):
    pc = '%s_%s'%(scene, 'pc.npz')
    bb = '%s_%s'%(scene, 'bbox.npy')
    votes = '%s_%s'%(scene, 'votes.npz')

    point_cloud = os.path.join(input_folder_path, pc)
    bboxes = os.path.join(input_folder_path, bb)
    point_votes = os.path.join(input_folder_path, votes)

    " COPY FILES"
    shutil.copy(point_cloud, output_folder_path)
    shutil.copy(bboxes, output_folder_path)
    shutil.copy(point_votes, output_folder_path)

    "REWRITE FILES"
    # bboxes_load = np.load(os.path.join(input_folder_path, bb))
    # np.save(os.path.join(output_folder_path, bb), bboxes_load)

    # pc_load = np.load(os.path.join(input_folder_path, pc))
    # np.savez_compressed(os.path.join(output_folder_path, pc), pc = pc_load['pc'])

    # votes_load = np.load(os.path.join(input_folder_path, votes))
    # np.savez_compressed(os.path.join(output_folder_path, votes), point_votes = votes_load['point_votes'])


def move_dataset_files(scene, input_folder_path, output_folder_path):
    pc = '%s_%s'%(scene, 'pc.npz')
    bb = '%s_%s'%(scene, 'bbox.npy')
    votes = '%s_%s'%(scene, 'votes.npz')

    point_cloud = os.path.join(input_folder_path, pc)
    bboxes = os.path.join(input_folder_path, bb)
    point_votes = os.path.join(input_folder_path, votes)

    " COPY FILES"
    # shutil.copy(point_cloud, output_folder_path)
    # shutil.copy(bboxes, output_folder_path)
    # shutil.copy(point_votes, output_folder_path)
    
    "MOVE FILES"
    shutil.move(point_cloud, output_folder_path)
    shutil.move(bboxes, output_folder_path)
    shutil.move(point_votes, output_folder_path)


def split_dataset(dataset_path, test_data_path, val_data_path, train_data_path, test_percentage, val_percentage):
    for root, dirs, files in os.walk(dataset_path):
        for dir in dirs:
            if dir == 'pc_bbox_votes_50k_val' or dir == 'pc_bbox_votes_50k_train':
                stop = 1
                continue
            
            dir_path = os.path.join(root, dir)

            print('--- SOURCE: ---')
            print(dir)
            scene_names_path = sorted([x for x in Path(dir_path).rglob("*.npy")])
            scene_names = [x.stem[:-5] for x in scene_names_path]

            test_size = int(math.ceil(test_percentage*len(scene_names)))
            test_list = sample(scene_names, test_size)

            training_val_list = set(scene_names) - set(test_list)

            val_size = int(math.ceil(val_percentage*len(training_val_list)))
            val_list = sample(training_val_list, val_size)

            train_list = list(training_val_list - set(val_list))
            stop = 1


            print('Move %d scenes to _eval folder:'%(test_size))
            print(test_data_path)

            for scene in test_list:
                move_dataset_files(scene, dir_path, test_data_path)

            print('Move %d scenes to _val folder:'%(val_size))
            print(val_data_path)

            for scene in val_list:
                move_dataset_files(scene, dir_path, val_data_path)

            print('Move %d scenes to _train folder:'%(len(train_list)))
            print(train_data_path)

            for scene in train_list:
                move_dataset_files(scene, dir_path, train_data_path)


if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset_path', help='Path to folder containing dataset scene folders. Each folder is a different class.')
    parser.add_argument('--output_folder', help='Path to folder which contains two subfolder /pc_bbox_votes_50k_val and /pc_bbox_votes_50k_train.')
    parser.add_argument('--test_percentage', type=float, help='Percentage of files to be used as test dataset.')
    parser.add_argument('--val_percentage', type=float, help='Percentage of files (after removoing files for test dataset) to be used as validation dataset.')
    args = parser.parse_args()

    print("\n\n\nTRAIN-VALIDATION-TEST DATASET SPLIT INITIATED!")
    print("\nData from \n%s  \n\nwill be MOVED to \n%s"%(args.dataset_path, args.output_folder))

    print('\n\nDo you want to proceed? (Y/N)')
    c = input()
    if c == 'n' or c == 'N':
        print('Exiting...')
        exit()
    elif c == 'y' or c == 'Y':
        test_data_path = os.path.join(args.output_folder, 'pc_bbox_votes_50k_eval')
        val_data_path = os.path.join(args.output_folder, 'pc_bbox_votes_50k_val')
        train_data_path = os.path.join(args.output_folder, 'pc_bbox_votes_50k_train')      
        if not os.path.exists(test_data_path):
            os.mkdir(test_data_path)
        if not os.path.exists(val_data_path):
            os.mkdir(val_data_path)
        if not os.path.exists(train_data_path):
            os.mkdir(train_data_path)
            
        split_dataset(args.dataset_path, test_data_path, val_data_path, train_data_path, args.test_percentage, args.val_percentage)
    
    print("DONE!")