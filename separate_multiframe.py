import io_3dgs
import numpy as np
from pathlib import Path

scene_name = "longdress"
total_frames = 2
# Load multiframe
multiframe_gs = io_3dgs.GaussianModelV2("/mnt/data1/syjintw/MMSys25_extension/dataset/longdress_multiframe_compressed/point_cloud/iteration_30000/point_cloud.ply")

frame = 1
save_dir = Path(f"/mnt/data1/syjintw/MMSys25_extension/dataset/{scene_name}_{frame}/point_cloud/iteration_30000/")
save_dir.mkdir(parents=True, exist_ok=True)
tmp_gs = multiframe_gs.copy()
tmp_gs.delete_attribute("x_1")
tmp_gs.delete_attribute("y_1")
tmp_gs.delete_attribute("z_1")
tmp_gs.export_gs_to_ply(save_dir/"point_cloud.ply")

frame = 2
save_dir = Path(f"/mnt/data1/syjintw/MMSys25_extension/dataset/{scene_name}_{frame}/point_cloud/iteration_30000/")
save_dir.mkdir(parents=True, exist_ok=True)
tmp_gs = multiframe_gs.copy()
tmp_gs.data["x"]["data"] = tmp_gs.data["x_1"]["data"]
tmp_gs.delete_attribute("x_1")
tmp_gs.data["y"]["data"] = tmp_gs.data["y_1"]["data"]
tmp_gs.delete_attribute("y_1")
tmp_gs.data["z"]["data"] = tmp_gs.data["z_1"]["data"]
tmp_gs.delete_attribute("z_1")
tmp_gs.export_gs_to_ply(save_dir/"point_cloud.ply") 
