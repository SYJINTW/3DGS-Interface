import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import io_3dgs
import argparse
import numpy as np
from pathlib import Path

if __name__ == "__main__":
    # Argument parser for command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--start_frame", help="Start frame", type=int)
    parser.add_argument("--num_frames", help="Number of frames", type=int)
    parser.add_argument("--level", help="Level of detail", type=int)
    parser.add_argument("--input", help="Input file directory", type=str)
    parser.add_argument("--output", help="Output file directory", type=str)
    args = parser.parse_args()

    start_frame = args.start_frame
    total_frames = args.num_frames

    # Load main frame
    main_gs = io_3dgs.GaussianModelV2(Path(args.input)/f"{start_frame}"/"point_cloud"/"iteration_30000"/"point_cloud.ply")
    
    for frame in range(1, total_frames):
        # Load second frame
        tmp_gs = io_3dgs.GaussianModelV2(Path(args.input)/f"{start_frame + frame}"/"point_cloud"/"iteration_30000"/"point_cloud.ply")
        
        main_gs.add_attribute(f"x_{frame}", "f4", tmp_gs.data["x"]["data"])
        main_gs.add_attribute(f"y_{frame}", "f4", tmp_gs.data["y"]["data"])
        main_gs.add_attribute(f"z_{frame}", "f4", tmp_gs.data["z"]["data"])

    save_dir = Path(args.output)/"point_cloud"/"iteration_30000"
    save_dir.mkdir(parents=True, exist_ok=True)
    main_gs.export_gs_to_ply(save_dir/"point_cloud.ply")

    # gs = io_3dgs.GaussianModelV2(save_dir/"point_cloud.ply")
    # print(gs.data.keys())
