""""
Multiply existing set of dataset (pc, bbox and votes) and rename it iteratively
to create larger dataset of the same data.

Input: 
- absolute path to the dataset folder
- total number of files (scenes) wanted in the end

"""
import argparse
import os
import shutil 
import numpy as np

def multiply_dataset(data_path, total_nuber_of_files):
    scan_names = sorted(list(set([os.path.basename(x)[0:6] \
                for x in os.listdir(data_path)])))
    no_copies = total_nuber_of_files//len(scan_names)

    for iCopy in range(no_copies):
        print(iCopy)
        for iScan, scan_name in enumerate(scan_names):
            scan_name_copy = '{:06d}'.format(iScan + len(scan_names) * (1 + iCopy))
            # scan_name = scan_names[iCopy]
            
            point_cloud = os.path.join(data_path, scan_name)+'_pc.npz'
            bboxes = os.path.join(data_path, scan_name)+'_bbox.npy'
            point_votes = os.path.join(data_path, scan_name)+'_votes.npz'

            point_cloud_copy = os.path.join(data_path, scan_name_copy)+'_pc.npz'
            bboxes_copy = os.path.join(data_path, scan_name_copy)+'_bbox.npy'
            point_votes_copy = os.path.join(data_path, scan_name_copy)+'_votes.npz'

            shutil.copyfile(point_cloud, point_cloud_copy)
            shutil.copyfile(bboxes, bboxes_copy)
            shutil.copyfile(point_votes, point_votes_copy)

            # test
            # original = np.load(bboxes)
            # copy = np.load(bboxes_copy)
            # comparison = original == copy
            # equal_arrays = comparison.all()
            # print(equal_arrays)
            #
            stop = 1

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_path', help='Path to folder containing dataset to multiply.')
    parser.add_argument('--total_number_of_scenes')
    args = parser.parse_args()

    multiply_dataset(args.data_path, int(args.total_number_of_scenes))