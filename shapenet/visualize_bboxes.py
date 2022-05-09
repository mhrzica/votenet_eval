# from ast import arg
# from curses import raw
# from functools import partial

# from scipy.fft import fftfreq
# from attr import ib

from attr import ib
import numpy as np
import open3d as o3d
import open3d.visualization.gui as gui

# import matplotlib.pyplot as plt
import argparse
import glob
import os
from pathlib import Path

# import copy


def get_bboxes_from_ply(bboxes):
    vertices_size = np.asarray(bboxes.vertices).shape[0]
    bboxes_list = []
    for iBox in range(0, vertices_size, 8):
        vertices = np.asarray(bboxes.vertices)[iBox : (iBox + 8)][:]
        bbox_point_cloud = o3d.geometry.PointCloud()
        bbox_point_cloud.points = o3d.utility.Vector3dVector(vertices)
        bbox = o3d.geometry.OrientedBoundingBox.create_from_points(bbox_point_cloud.points)
        bboxes_list.append(bbox)

    return bboxes_list


def get_bboxes_from_npy(bboxes_load):
    bboxes_list = []

    if bboxes_load.ndim > 1:
        bboxes_load = bboxes_load.flatten()

    for iBox in range(0, bboxes_load.size, 8):
        bbox = bboxes_load[iBox : iBox + 8]

        if bbox.sum() == 0:
            continue

        box3d_pts_3d = compute_box_3d(bbox[0:3], bbox[3:6])

        bbox_pcd = o3d.geometry.PointCloud()
        bbox_pcd.points = o3d.utility.Vector3dVector(box3d_pts_3d)

        R_scene_to_bbox = heading2rotmat(bbox[6])
        R_bbox_to_scene = np.linalg.inv(R_scene_to_bbox)
        bbox_pcd.rotate(R_bbox_to_scene)

        bbox_o3d = o3d.geometry.OrientedBoundingBox.create_from_points(bbox_pcd.points)

        bboxes_list.append(bbox_o3d)

    return bboxes_list


def get_bbox_line_set_from_npy(bboxes_load):
    line_set_list = []

    if bboxes_load.ndim > 1:
        bboxes_load = bboxes_load.flatten()

    for iBox in range(0, bboxes_load.size, 8):
        bbox = bboxes_load[iBox : iBox + 8]

        if bbox.sum() == 0:
            continue

        R_scene_to_bbox = heading2rotmat(bbox[6])
        R_bbox_to_scene = np.linalg.inv(R_scene_to_bbox)

        bbox_vertices_scene = box_center_to_corner(bbox[0:3], bbox[3:6], R_bbox_to_scene)

        lines = [[0, 1], [1, 2], [2, 3], [0, 3], [4, 5], [5, 6], [6, 7], [4, 7], [0, 4], [1, 5], [2, 6], [3, 7]]

        # Use the same color for all lines
        colors = [[1, 0, 0] for _ in range(len(lines))]

        line_set = o3d.geometry.LineSet()
        line_set.points = o3d.utility.Vector3dVector(bbox_vertices_scene)
        line_set.lines = o3d.utility.Vector2iVector(lines)
        line_set.colors = o3d.utility.Vector3dVector(colors)

        line_set_list.append(line_set)
    return line_set_list


def compute_box_3d(center, size):
    l, w, h = size

    x_corners = [-l, l, l, -l, -l, l, l, -l]
    y_corners = [w, w, -w, -w, w, w, -w, -w]
    z_corners = [h, h, h, h, -h, -h, -h, -h]

    corners_3d = np.vstack([x_corners, y_corners, z_corners])

    corners_3d[0, :] += center[0]
    corners_3d[1, :] += center[1]
    corners_3d[2, :] += center[2]
    return np.transpose(corners_3d)


def box_center_to_corner(center, size, rotation_matrix):
    l, w, h = size

    # Create a bounding box outline
    bounding_box = np.array([[-l, -l, l, l, -l, -l, l, l], [w, -w, -w, w, w, -w, -w, w], [-h, -h, -h, -h, h, h, h, h],])

    # Repeat the [x, y, z] eight times
    eight_points = np.tile(center, (8, 1))

    # Translate the rotated bounding box by the
    # original center position to obtain the final box
    corner_box = np.dot(rotation_matrix, bounding_box) + eight_points.transpose()

    return corner_box.transpose()


def save_image(vis):
    vis.capture_screen_image("/media/mateja/ubuntu_storage/Git_repos/votenet/output/proba/img.png")
    print("Saved")
    return False


def visualize_pc_scene_with_ply_bboxes(
    scene_name, pc_path, bbox_path, objectness_prob, bbox_line_width_px, bbox_color, show_axes
):
    pc = o3d.io.read_point_cloud(str(pc_path))
    pc.paint_uniform_color([0.4, 0.4, 0.4])

    # Sort by conf
    sorted_id = np.argsort(objectness_prob)
    objectness_prob = objectness_prob[sorted_id]

    bboxes = o3d.io.read_triangle_mesh(str(bbox_path))
    bboxes_list = get_bboxes_from_ply(bboxes)

    bboxes_list = np.array(bboxes_list)[sorted_id]

    scene_bbox_visualization(scene_name, pc, bboxes_list, objectness_prob, bbox_line_width_px, bbox_color, show_axes)

    # OLD, default line width size
    # bboxes_list.append(pc)
    # vis = o3d.visualization.draw(bboxes_list, title=str(scene_name), show_ui=True, point_size=2)

    stop = 1


def visualize_mesh_scene_with_GT_bboxes(
    scene_name, mesh_scenes_path, data_idx, GT_bboxes_path, bbox_line_width_px, bbox_color, show_axes
):
    mesh_file = os.path.join(mesh_scenes_path, "%06d.ply" % (data_idx))
    mesh = o3d.io.read_triangle_mesh(str(mesh_file))

    bboxes_load = np.load(os.path.join(GT_bboxes_path, "%06d_bbox.npy" % (data_idx)))
    bboxes_list = get_bboxes_from_npy(bboxes_load)

    objectness_prob = []
    scene_bbox_visualization(scene_name, mesh, bboxes_list, objectness_prob, bbox_line_width_px, bbox_color, show_axes)


def visualize_pc_scene_with_GT_bboxes(
    scene_name, npz_scenes_path, data_idx, GT_bboxes_path, bbox_line_width_px, bbox_color, show_axes
):
    pc_npz = np.load(npz_scenes_path)
    pc = o3d.geometry.PointCloud()

    # pc.points = o3d.utility.Vector3dVector(pc_npz["pc"][:, 0:3])
    pc.points = o3d.utility.Vector3dVector(pc_npz["pc"])

    pc.paint_uniform_color([0.5, 0.5, 0.5])

    bboxes_load = np.load(GT_bboxes_path)
    bboxes_list = get_bboxes_from_npy(bboxes_load)

    line_set_list = get_bbox_line_set_from_npy(bboxes_load)

    objectness_prob = []
    # scene_bbox_visualization(scene_name, pc, bboxes_list, objectness_prob, bbox_line_width_px, bbox_color, show_axes)

    scene_bbox_visualization_v2(
        scene_name, pc, line_set_list, objectness_prob, bbox_line_width_px, bbox_color, show_axes
    )


def scene_bbox_visualization(
    scene_name, scene, bboxes_list, objectness_prob=[], bbox_line_width_px=5, bbox_color=[0, 0, 0], show_axes=False
):
    gui.Application.instance.initialize()

    vis = o3d.visualization.O3DVisualizer()
    vis.show_axes = show_axes
    vis.line_width = bbox_line_width_px

    for i, iBox in enumerate(bboxes_list):
        bbox_lineset = o3d.geometry.LineSet.create_from_oriented_bounding_box(iBox)

        colors = [bbox_color for i in range(len(bbox_lineset.lines))]
        bbox_lineset.colors = o3d.utility.Vector3dVector(colors)

        if len(objectness_prob) != 0:
            vis.add_geometry(str(i) + " " + str(objectness_prob[i]), bbox_lineset)
        else:
            vis.add_geometry("bbox" + str(i), bbox_lineset)

    vis.add_geometry("scene", scene)

    vis.reset_camera_to_default()
    vis.show_settings = True

    print(scene_name)

    gui.Application.instance.add_window(vis)
    gui.Application.instance.run()

    stop = 1


def scene_bbox_visualization_v2(
    scene_name, scene, bboxes_list, objectness_prob=[], bbox_line_width_px=5, bbox_color=[0, 0, 0], show_axes=False
):
    gui.Application.instance.initialize()

    vis = o3d.visualization.O3DVisualizer()
    vis.line_width = bbox_line_width_px
    vis.show_axes = show_axes

    for i, iBox in enumerate(bboxes_list):
        colors = [bbox_color for i in range(len(iBox.lines))]
        iBox.colors = o3d.utility.Vector3dVector(colors)

        if len(objectness_prob) != 0:
            vis.add_geometry(str(i) + " " + str(objectness_prob[i]), iBox)
        else:
            vis.add_geometry("bbox" + str(i), iBox)

    vis.add_geometry("scene", scene)

    vis.reset_camera_to_default()
    vis.show_settings = True

    print(scene_name)

    gui.Application.instance.add_window(vis)
    gui.Application.instance.run()

    stop = 1


def heading2rotmat(heading_angle):
    rotmat = np.zeros((3, 3))
    rotmat[2, 2] = 1
    cosval = np.cos(heading_angle)
    sinval = np.sin(heading_angle)
    rotmat[0:2, 0:2] = np.array([[cosval, -sinval], [sinval, cosval]])
    return rotmat


def transform_bboxes_to_scene(bboxes_list):
    bboxes_transformed_list = []

    return bboxes_transformed_list


def visualize_votenet_results(data_path):
    box_files = [x for x in Path(data_path).rglob("*_pred_confident_nms_bbox.ply")]
    for box_file in sorted(box_files, reverse=False):
        scene_name = box_file.name[0:6]
        pc = scene_name + "_pc.ply"
        pc_path = os.path.join(data_path, pc)

        objectness_prob_file = scene_name + "_objectness_prob.npy"
        objectness_prob_path = os.path.join(data_path, objectness_prob_file)
        objectness_prob = np.load(objectness_prob_path)

        print(pc_path)
        print(box_file)

        bbox_line_width_px = 5
        bbox_color = [0, 0, 0]
        show_axes = False
        visualize_pc_scene_with_ply_bboxes(
            scene_name, pc_path, box_file, objectness_prob, bbox_line_width_px, bbox_color, show_axes
        )

        stop = 1


def visualize_GT_with_npz_scene(data_path):
    box_files = [x for x in Path(data_path).rglob("*_bbox.npy")]
    for box_file in sorted(box_files, reverse=False):
        scene_name = box_file.name[0:6]
        pc = scene_name + "_pc.npz"
        pc_path = os.path.join(data_path, pc)

        print(pc_path)
        print(box_file)

        bbox_line_width_px = 3
        # bbox_color = [1, 0, 0]
        bbox_color = [1, 0, 1]
        show_axes = True
        visualize_pc_scene_with_GT_bboxes(
            scene_name, pc_path, box_file.stem, box_file, bbox_line_width_px, bbox_color, show_axes
        )

        stop = 1


def visualize_GT_with_mesh_scene(GT_bboxes_path, mesh_scenes_path, scene_list=[]):
    if scene_list:
        data_idx_list = [int(line.rstrip()) for line in open(scene_list)]
    else:
        data_idx_list = [int(x.stem[0:6]) for x in Path(GT_bboxes_path).rglob("*.npy")]

    for data_idx in sorted(data_idx_list, reverse=False):
        print("------------- ", data_idx)
        bbox_line_width_px = 5
        # bbox_color = [1, 0, 1]
        bbox_color = [1, 0.5, 0]
        show_axes = False
        visualize_mesh_scene_with_GT_bboxes(
            data_idx, mesh_scenes_path, data_idx, GT_bboxes_path, bbox_line_width_px, bbox_color, show_axes
        )
        stop = 1


def visualize_GT_with_off_scene(data_path, GT_bboxes_path):
    off_files = [x for x in Path(data_path).rglob("*.off")]
    for model in sorted(off_files, reverse=False):

        scene_name = model.stem

        if scene_name != "24c62fe437ecf586d42b9650f19dd425":
            continue

        scene = o3d.io.read_triangle_mesh(str(model))
        scene.compute_triangle_normals()
        scene.compute_vertex_normals()

        bboxes_path = os.path.join(GT_bboxes_path, scene_name)
        bboxes_list = get_bboxes_from_npz(bboxes_path)

        line_set_list = get_bbox_line_set_from_npy(bboxes_list)

        bbox_line_width_px = 5
        # bbox_color = [0.9, 0.35, 0]
        bbox_color = [1, 0, 1]
        show_axes = False

        objectness_prob = []
        scene_bbox_visualization_v2(
            scene_name, scene, line_set_list, objectness_prob, bbox_line_width_px, bbox_color, show_axes
        )

        stop = 1


def get_bboxes_from_npz(bboxes_path):
    bboxes_files = [x for x in Path(bboxes_path).rglob("*.npz")]
    bboxes_list = []
    for iBbox in bboxes_files:
        bbox_npz = np.load(iBbox)
        bbox = np.zeros([8,])
        bbox[0:3] = bbox_npz["center"]
        bbox[3:6] = bbox_npz["wlh_half"]
        bboxes_list.append(bbox)

    bboxes_list = np.asarray(bboxes_list)
    return bboxes_list


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--data_path", help="Path to folder containing dataset scene files (scenes and annoted bboxes in PLY format)."
    )
    parser.add_argument(
        "--visualize_votenet_results", action="store_true", help="Visualize votenet eval results. Can show box by box."
    )
    parser.add_argument(
        "--visualize_GT_with_mesh_scene", action="store_true", help="Visualize Ivana's annoted GT bboxes."
    )
    parser.add_argument("--visualize_GT_with_npz_scene", action="store_true", help="Visualize Petra's scenes.")
    parser.add_argument(
        "--visualize_GT_with_off_scene", action="store_true", help="Visualize Mateja's GT with mesh in off file."
    )
    parser.add_argument(
        "--scene_list",
        help="If you want to visualize selected scenes, add this path to TXT file where each line is an int number (index).",
    )
    parser.add_argument("--GT_bboxes_path", help="Path to NPY files with annoted GT bboxes by Ivana.")
    parser.add_argument("--mesh_scenes_path", help="Path to PLY scenes on which GT was annoted.")
    args = parser.parse_args()

    print("Visualize scenes with bboxes.")
    if args.visualize_votenet_results:
        visualize_votenet_results(args.data_path)

    if args.visualize_GT_with_npz_scene:
        visualize_GT_with_npz_scene(args.data_path)

    if args.visualize_GT_with_mesh_scene:
        visualize_GT_with_mesh_scene(args.GT_bboxes_path, args.mesh_scenes_path, args.scene_list)

    if args.visualize_GT_with_off_scene:
        visualize_GT_with_off_scene(args.data_path, args.GT_bboxes_path)

    print("DONE!")
