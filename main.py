import io_3dgs

gs = io_3dgs.GaussianModel("./point_cloud.ply")
print(gs)
print(gs.get_bound())
gs.limit_x(-2, 0)
gs.limit_y(-2, 0)
gs.limit_z(-2, 0)
print(gs)
print(gs.get_bound())
gs.export_gs_to_ply(f"./test_partial.ply")