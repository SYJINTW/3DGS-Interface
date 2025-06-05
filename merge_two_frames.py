import io_3dgs
import numpy as np

# Load main frame
main_gs = io_3dgs.GaussianModelV2("/mnt/data1/syjintw/MMSys25_extension/dataset/1000/point_cloud/iteration_30000/point_cloud.ply")
main_gs.export_gs_to_ply("/mnt/data1/syjintw/MMSys25_extension/dataset/1000_point_cloud_ascii.ply", ascii=True) 

# Load second frame
tmp_gs = io_3dgs.GaussianModelV2("/mnt/data1/syjintw/MMSys25_extension/dataset/1001/point_cloud/iteration_30000/point_cloud.ply")
tmp_gs.export_gs_to_ply("/mnt/data1/syjintw/MMSys25_extension/dataset/1001_point_cloud_ascii.ply", ascii=True) 

main_gs.add_attribute("x_1", "f4", tmp_gs.data["x"]["data"])
main_gs.add_attribute("y_1", "f4", tmp_gs.data["y"]["data"])
main_gs.add_attribute("z_1", "f4", tmp_gs.data["z"]["data"])

# main_gs.export_gs_to_ply("/mnt/data1/syjintw/MMSys25_extension/dataset/longdress_multiframe/point_cloud/iteration_30000/point_cloud.ply")
main_gs.export_gs_to_ply("/mnt/data1/syjintw/MMSys25_extension/dataset/longdress_multiframe/point_cloud/iteration_30000/point_cloud.ply", ascii=True) 

gs = io_3dgs.GaussianModelV2("/mnt/data1/syjintw/MMSys25_extension/dataset/longdress_multiframe/point_cloud/iteration_30000/point_cloud.ply")
print(gs.data.keys())

