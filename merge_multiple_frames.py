import io_3dgs
import numpy as np
from pathlib import Path

start_frame = 1000
total_frames = 5

# Load main frame
main_gs = io_3dgs.GaussianModelV2(f"/mnt/data1/syjintw/MMSys25_extension/dataset/raw_dynamic_frames/{start_frame}/point_cloud/iteration_30000/point_cloud.ply")

for frame in range(1, total_frames):
    # Load second frame
    tmp_gs = io_3dgs.GaussianModelV2(f"/mnt/data1/syjintw/MMSys25_extension/dataset/raw_dynamic_frames/{start_frame + frame}/point_cloud/iteration_30000/point_cloud.ply")
    
    main_gs.add_attribute(f"x_{frame}", "f4", tmp_gs.data["x"]["data"])
    main_gs.add_attribute(f"y_{frame}", "f4", tmp_gs.data["y"]["data"])
    main_gs.add_attribute(f"z_{frame}", "f4", tmp_gs.data["z"]["data"])

save_dir = Path(f"/mnt/data1/syjintw/MMSys25_extension/dataset/longdress_multiframe_{total_frames}/point_cloud/iteration_30000")
save_dir.mkdir(parents=True, exist_ok=True)
main_gs.export_gs_to_ply(save_dir/"point_cloud.ply")

gs = io_3dgs.GaussianModelV2(save_dir/"point_cloud.ply")
print(gs.data.keys())

