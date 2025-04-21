# ---------------------------------------------------------------------------- #
#                         USAGE OF GaussianModel CLASS                         #
# ---------------------------------------------------------------------------- #
import io_3dgs

gs_path = "./point_cloud.ply" # Original 3DGS with SH3
gs = io_3dgs.GaussianModel(gs_path)
print(gs)

print("[info] Get boundary [max], [min], [max_idx], [min_idx]")
print(gs.get_bound())

# ---------------------------------------------------------------------------- #
#                                    Delete                                    #
# ---------------------------------------------------------------------------- #
print("[info] Delete")
gs.delete_Gaussian([i for i in range(gs.num_of_point - 2)])
print(gs)

# ---------------------------------------------------------------------------- #
#                               Reduce SH degree                               #
# ---------------------------------------------------------------------------- #
print("[info] Reduce 3 --> 2")
gs.reduce_SH(gs.sh_deg - 1)
print(gs)
gs.export_gs_to_ply(f"./test_SH{gs.sh_deg}.ply")

print("[info] Reduce 2 --> 1")
gs.reduce_SH(gs.sh_deg - 1)
print(gs)
gs.export_gs_to_ply(f"./test_SH{gs.sh_deg}.ply")

print("[info] Reduce 1 --> 0")
gs.reduce_SH(gs.sh_deg - 1)
print(gs)
gs.export_gs_to_ply(f"./test_SH{gs.sh_deg}.ply")

# ---------------------------------------------------------------------------- #
#                                     Load                                     #
# ---------------------------------------------------------------------------- #
print("[info] Load SH2")
gs_SH2 = io_3dgs.GaussianModel("./test_SH2.ply")
print(gs_SH2)

print("[info] Load SH1")
gs_SH1 = io_3dgs.GaussianModel("./test_SH1.ply")
print(gs_SH1)

print("[info] Load SH0")
gs_SH0 = io_3dgs.GaussianModel("./test_SH0.ply")
print(gs_SH0)

# ---------------------------------------------------------------------------- #
#                                Export as ASCII                               #
# ---------------------------------------------------------------------------- #
print("[info] Export as ASCII")
gs.export_gs_to_ply(f"./test_ASCII.ply", ascii=True)
