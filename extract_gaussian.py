import io_3dgs

main_gs = io_3dgs.GaussianModelV2("/mnt/data1/syjintw/MMSys25_extension/dataset.old/longdress_1/point_cloud/iteration_30000/point_cloud.ply")
main_gs.export_gs_to_ply("/mnt/data1/syjintw/MMSys25_extension/point_cloud_ascii.ply", ascii=True)
main_gs = io_3dgs.GaussianModelV2("/mnt/data1/syjintw/MMSys25_extension/point_cloud_ascii.ply")
tmp_gs = main_gs.extract_gaussians([i for i in range(2, 5)])
tmp_gs.export_gs_to_ply("/mnt/data1/syjintw/MMSys25_extension/point_cloud_ascii_2_5.ply", ascii=True)
