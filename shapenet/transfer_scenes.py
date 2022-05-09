import argparse
import os
import shutil 
import numpy as np

def transfer_scenes(data_path):
    scene_folders = sorted(list(set([os.path.basename(x) \
                for x in os.listdir(data_path)])))
    
    for iFolder, folder_name in enumerate(scene_folders):
        point_cloud = os.path.join(data_path, folder_name)+'/pc_uc.npz'
        bboxes = os.path.join(data_path, folder_name)+'/bbox.npy'
        point_votes = os.path.join(data_path, folder_name)+'/votes_uc.npz'

        scene_name = '{:06d}'.format(int(folder_name[-5:]))
        point_cloud_copy = os.path.join(data_path, scene_name)+'_pc.npz'
        bboxes_copy = os.path.join(data_path, scene_name)+'_bbox.npy'
        point_votes_copy = os.path.join(data_path, scene_name)+'_votes.npz'

        shutil.copyfile(point_cloud, point_cloud_copy)
        shutil.copyfile(bboxes, bboxes_copy)
        shutil.copyfile(point_votes, point_votes_copy)
        stop = 1

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_path', help='Path to folder containing dataset scene folders.')
    args = parser.parse_args()

    print("Starting copying files.")
    transfer_scenes(args.data_path)
    print("DONE!")