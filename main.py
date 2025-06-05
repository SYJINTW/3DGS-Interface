import io_3dgs
import numpy as np

# gs = io_3dgs.GaussianModel("/mnt/data1/syjintw/MMSys25_extension/dataset/truck/point_cloud/iteration_30000/point_cloud.ply")
# gs.export_gs_to_ply("/mnt/data1/syjintw/MMSys25_extension/Draco-for-3DGS-multiframe/myData/point_cloud.ply", ascii=False)

gs = io_3dgs.GaussianModelV2("/mnt/data1/syjintw/MMSys25_extension/dataset/truck/point_cloud/iteration_30000/point_cloud.ply")
# print(gs.data["x"])
gs.add_attribute("x1", "f4", gs.data["x"]["data"])
# print(gs.data.keys())
gs.export_gs_to_ply("/mnt/data1/syjintw/MMSys25_extension/dataset/truck/point_cloud/iteration_30000/output.ply")

gs = io_3dgs.GaussianModelV2("/mnt/data1/syjintw/MMSys25_extension/dataset/truck/point_cloud/iteration_30000/output.ply")
print(gs.data.keys())

