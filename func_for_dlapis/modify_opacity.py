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
    # parser.add_argument("--num_frames", help="Number of frames", type=int)
    parser.add_argument("--level", help="Level of detail", type=int)
    parser.add_argument("--input", help="Input file path", type=str)
    parser.add_argument("--output", help="Output file directory", type=str)
    args = parser.parse_args()
    
    main_gs = io_3dgs.GaussianModelV2(args.input)
    if args.level == 1:
        main_gs.data["opacity"]["data"] = main_gs.data["opacity_1"]["data"]
    elif args.level == 2:
        main_gs.data["opacity"]["data"] = main_gs.data["opacity_2"]["data"]
    
    # Delete redundant attributes
    main_gs.delete_attribute(f"opacity_1")
    main_gs.delete_attribute(f"opacity_2")

    save_dir = Path(args.output)/"point_cloud"/"iteration_30000"
    save_dir.mkdir(parents=True, exist_ok=True)
    main_gs.export_gs_to_ply(save_dir/"point_cloud.ply")

