import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import io_3dgs
import argparse
import numpy as np
from pathlib import Path

level_to_res = [4, 2, 1] # level 0, 1, 2 correspond to resolution 4, 2, 1 respectively

if __name__ == "__main__":
    # Argument parser for command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--start_frame", help="Start frame", type=int)
    parser.add_argument("--num_frames", help="Number of frames", type=int)
    # parser.add_argument("--total_level", help="Total level of detail", type=int)
    parser.add_argument("--scene_name", help="Scene name", type=str)
    parser.add_argument("--input", help="Input file directory", type=str) # /mnt/data1/syjintw/MMSys25_extension/dataset/raw
    parser.add_argument("--output", help="Output file directory", type=str) # /mnt/data1/syjintw/MMSys25_extension/dataset/layered
    args = parser.parse_args()

    start_frame = args.start_frame
    total_frames = args.num_frames
    scene_name = args.scene_name

    # Only handle levels 0, 1, and 2 without scalable
    for offset in range(total_frames):
        frame = start_frame + offset
        res4_gs = io_3dgs.GaussianModelV2(Path(args.input)/f"{scene_name}"/"opacity"/f"{scene_name}_res4"/f"{frame}"/"point_cloud"/"iteration_30000"/"point_cloud.ply") 
        res2_gs = io_3dgs.GaussianModelV2(Path(args.input)/f"{scene_name}"/"opacity"/f"{scene_name}_res2"/f"{frame}"/"point_cloud"/"iteration_30000"/"point_cloud.ply") 
        res1_gs = io_3dgs.GaussianModelV2(Path(args.input)/f"{scene_name}"/"opacity"/f"{scene_name}_res1"/f"{frame}"/"point_cloud"/"iteration_30000"/"point_cloud.ply") 

        lod0_num_gaussians = res4_gs.num_of_point
        lod1_num_gaussians = res2_gs.num_of_point - res4_gs.num_of_point
        lod2_num_gaussians = res1_gs.num_of_point - res2_gs.num_of_point
        
        # print(res4_gs.num_of_point, res2_gs.num_of_point, res1_gs.num_of_point)
        # print(lod0_num_gaussians, lod1_num_gaussians, lod2_num_gaussians)

        # Create a new Gaussian model for the current frame
        lod0_gs = res4_gs.copy()
        opacity_0 = res4_gs.data["opacity"]["data"][:lod0_num_gaussians]
        opacity_1 = res2_gs.data["opacity"]["data"][:lod0_num_gaussians]
        opacity_2 = res1_gs.data["opacity"]["data"][:lod0_num_gaussians]
        lod0_gs.add_attribute(f"opacity", "f4", opacity_0)
        lod0_gs.add_attribute(f"opacity_1", "f4", opacity_1)
        lod0_gs.add_attribute(f"opacity_2", "f4", opacity_2)
        
        lod1_gs = res2_gs.copy().extract_gaussians([i for i in range(lod0_num_gaussians, lod0_num_gaussians + lod1_num_gaussians)])
        opacity_0 = np.array([0] * lod1_num_gaussians, dtype=np.float32)
        opacity_1 = res2_gs.data["opacity"]["data"][lod0_num_gaussians : lod0_num_gaussians + lod1_num_gaussians]
        opacity_2 = res1_gs.data["opacity"]["data"][lod0_num_gaussians : lod0_num_gaussians + lod1_num_gaussians]
        lod1_gs.add_attribute(f"opacity", "f4", opacity_0)
        lod1_gs.add_attribute(f"opacity_1", "f4", opacity_1)
        lod1_gs.add_attribute(f"opacity_2", "f4", opacity_2)
        
        lod2_gs = res1_gs.copy().extract_gaussians([i for i in range(lod0_num_gaussians + lod1_num_gaussians, lod0_num_gaussians + lod1_num_gaussians + lod2_num_gaussians)])
        opacity_0 = np.array([0] * lod2_num_gaussians, dtype=np.float32)
        opacity_1 = np.array([0] * lod2_num_gaussians, dtype=np.float32)
        opacity_2 = res1_gs.data["opacity"]["data"][lod1_num_gaussians : lod1_num_gaussians + lod2_num_gaussians]
        lod2_gs.add_attribute(f"opacity", "f4", opacity_0)
        lod2_gs.add_attribute(f"opacity_1", "f4", opacity_1)
        lod2_gs.add_attribute(f"opacity_2", "f4", opacity_2)
        
        # Save the extracted gaussians to a new file
        lod0_save_dir = Path(args.output)/f"{scene_name}"/"0"/f"{offset}"/"point_cloud"/"iteration_30000"
        lod0_save_dir.mkdir(parents=True, exist_ok=True)
        lod0_gs.export_gs_to_ply(lod0_save_dir/"point_cloud.ply")

        lod1_save_dir = Path(args.output)/f"{scene_name}"/"1"/f"{offset}"/"point_cloud"/"iteration_30000"
        lod1_save_dir.mkdir(parents=True, exist_ok=True)
        lod1_gs.export_gs_to_ply(lod1_save_dir/"point_cloud.ply")

        lod2_save_dir = Path(args.output)/f"{scene_name}"/"2"/f"{offset}"/"point_cloud"/"iteration_30000"
        lod2_save_dir.mkdir(parents=True, exist_ok=True)
        lod2_gs.export_gs_to_ply(lod2_save_dir/"point_cloud.ply")

    