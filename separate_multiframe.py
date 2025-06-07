import os
import io_3dgs
import numpy as np
from pathlib import Path

scene_name = "longdress"
total_frames = 5
# Load multiframe
load_dir = Path(f"/mnt/data1/syjintw/MMSys25_extension/dataset/longdress_multiframe_5_compressed")
multiframe_gs = io_3dgs.GaussianModelV2(load_dir/"point_cloud/iteration_30000/point_cloud.ply")

save_root_dir = Path(f"/mnt/data1/syjintw/MMSys25_extension/dataset/separate_frames")
save_root_dir.mkdir(parents=True, exist_ok=True)

for frame in range(total_frames):
    save_dir = Path(save_root_dir/f"{scene_name}_{frame}")
    save_dir.mkdir(parents=True, exist_ok=True)
    tmp_gs = multiframe_gs.copy()
    if frame == 0:
        pass
    else:
        tmp_gs.data["x"]["data"] = tmp_gs.data[f"x_{frame}"]["data"]
        tmp_gs.data["y"]["data"] = tmp_gs.data[f"y_{frame}"]["data"]
        tmp_gs.data["z"]["data"] = tmp_gs.data[f"z_{frame}"]["data"]
    
    # Delete redundant attributes
    for i in range(1, total_frames):
        tmp_gs.delete_attribute(f"x_{i}")
        tmp_gs.delete_attribute(f"y_{i}")
        tmp_gs.delete_attribute(f"z_{i}")

    # Copy cfg
    os.system(f"cp {load_dir}/cfg_args {save_dir}/cfg_args")
    tmp_gs.export_gs_to_ply(save_dir/"point_cloud"/"iteration_30000"/"point_cloud.ply")
