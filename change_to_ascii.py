import io_3dgs
import numpy as np

# Load main frame
main_gs = io_3dgs.GaussianModelV2("/mnt/data1/syjintw/MMSys25_extension/dataset/longdress_multiframe_5_compressed/point_cloud/iteration_30000/point_cloud.ply")
main_gs.export_gs_to_ply("/mnt/data1/syjintw/MMSys25_extension/dataset/longdress_multiframe_5_point_cloud_ascii.ply", ascii=True) 
