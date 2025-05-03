import io_3dgs
import numpy as np

# gs = io_3dgs.GaussianModel("/mnt/data1/syjintw/MMSys25_extension/Draco-for-3DGS/myData/3dgs.ply")
# x = np.arange(136641)
# gs.xyz[:,0] = x
# gs.export_gs_to_ply("/mnt/data1/syjintw/MMSys25_extension/Draco-for-3DGS/myData/3dgs_idx.ply", ascii=True)

gs = io_3dgs.GaussianModel("/mnt/data1/syjintw/MMSys25_extension/Draco-for-3DGS/output/3dgs_idx_default.ply")
gs.sort()
gs.export_gs_to_ply("/mnt/data1/syjintw/MMSys25_extension/Draco-for-3DGS/output/3dgs_idx_default_ascii.ply", ascii=True)
