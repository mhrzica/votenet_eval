#!/bin/bash

echo "#######################################################"
echo "Show GPU info"
echo "#######################################################"
nvidia-smi

echo "#######################################################"
echo "Run demo evaluation"
echo "#######################################################"
python3 eval_mateja.py --dataset sunrgbd --use_shapenet --checkpoint_path /votenet/output/Dataset_220322_all_classes_v3_changed_predictions_IoU/checkpoint.tar --dump_dir /tmp --use_cls_nms --use_3d_nms --num_point 50000 --batch_size 20 --nms_iou 0.1 --conf_thresh 0.75 --cluster_sampling seed_fps
