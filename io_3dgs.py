import numpy as np
from plyfile import PlyData, PlyElement

"""
Load different SH of 3DGS
Export 3DGS
    - Different SH degree
    - Binary / ASCII-version of 3DGS
    - Only export specific attributes
Reduce SH degree
Delete Gaussian points
Get boundary
Shift 3DGS
"""

class GaussianModel():
    num_of_point = 0
    sh_deg = -1
    xyz = -1
    features_dc = -1
    features_rest = -1
    opacities = -1
    scales = -1
    rots = -1

    def __init__(self, gs_path: str):
        self.load_gaussian_ply(gs_path)
        pass
    
    def __str__(self):
        return f"This Gaussians contains {self.num_of_point} of Gaussian point and SH degree is {self.sh_deg}"
        
    def load_gaussian_ply(self, path: str) -> list:
        
        with open(path, 'rb') as f:
            plydata = PlyData.read(f)
        
        # --------------------------------- Position --------------------------------- #
        self.xyz = np.stack((np.asarray(plydata.elements[0]["x"]),
                            np.asarray(plydata.elements[0]["y"]),
                            np.asarray(plydata.elements[0]["z"])),  axis=1)
        
        # ------------------------- Number of Gaussian points ------------------------ #
        self.num_of_point = self.xyz.shape[0]
                
        # ------------------------------------ SH0 ----------------------------------- #
        self.features_dc = np.zeros((self.num_of_point, 3, 1))
        self.features_dc[:, 0, 0] = np.asarray(plydata.elements[0]["f_dc_0"])
        self.features_dc[:, 1, 0] = np.asarray(plydata.elements[0]["f_dc_1"])
        self.features_dc[:, 2, 0] = np.asarray(plydata.elements[0]["f_dc_2"])

        # -------------------------- Additional degree of SH ------------------------- #
        #! [YC] Modify it to support lower SH
        extra_f_names = [p.name for p in plydata.elements[0].properties if p.name.startswith("f_rest_")]
        extra_f_names = sorted(extra_f_names, key = lambda x: int(x.split('_')[-1]))
        # assert len(extra_f_names)==3*(3 + 1) ** 2 - 3
        self.sh_deg = int(((len(extra_f_names) + 3) / 3) ** (1/2) - 1) # Calculate SH degree
        if self.sh_deg != 0:
            self.features_rest = np.zeros((self.num_of_point, len(extra_f_names)))
            for idx, attr_name in enumerate(extra_f_names):
                self.features_rest[:, idx] = np.asarray(plydata.elements[0][attr_name])
            # Reshape (P, F*SH_coeffs) to (P, F, SH_coeffs except DC)
            self.features_rest = self.features_rest.reshape((self.features_rest.shape[0], 3, (self.sh_deg + 1) ** 2 - 1))

        # ---------------------------------- Opacity --------------------------------- #
        self.opacities = np.asarray(plydata.elements[0]["opacity"])[..., np.newaxis]

        # ----------------------------------- Scale ---------------------------------- #
        scale_names = [p.name for p in plydata.elements[0].properties if p.name.startswith("scale_")]
        scale_names = sorted(scale_names, key = lambda x: int(x.split('_')[-1]))
        self.scales = np.zeros((self.num_of_point, len(scale_names)))
        for idx, attr_name in enumerate(scale_names):
            self.scales[:, idx] = np.asarray(plydata.elements[0][attr_name])

        # --------------------------------- Rotation --------------------------------- #
        rot_names = [p.name for p in plydata.elements[0].properties if p.name.startswith("rot")]
        rot_names = sorted(rot_names, key = lambda x: int(x.split('_')[-1]))
        self.rots = np.zeros((self.num_of_point, len(rot_names)))
        for idx, attr_name in enumerate(rot_names):
            self.rots[:, idx] = np.asarray(plydata.elements[0][attr_name])

    def export_gs_to_ply(self, save_path: str, 
                         xyz=True, normals=True, colors=True, opacities=True, scales=True, rots=True,
                         ascii=False):
        
        # -------------------------- Create attribute names -------------------------- #
        l = []
        data = tuple()
        if xyz:
            l.extend(['x', 'y', 'z'])
            data += (self.xyz,)

        if normals:
            l.extend(["nx", "ny", "nz"])
            _normals = np.zeros_like(self.xyz) # Create fake normal data
            data += (_normals,)
            
        # All channels except the 3 DC
        if colors:
            for i in range(self.features_dc.shape[1]*self.features_dc.shape[2]):
                l.append('f_dc_{}'.format(i))
            _f_dc = self.features_dc.reshape(self.features_dc.shape[0], self.features_dc.shape[1]*self.features_dc.shape[2])
            data += (_f_dc,)

            if self.features_rest.shape[0] > 0: # Handle SH0
                for i in range(self.features_rest.shape[1]*self.features_rest.shape[2]):
                    l.append('f_rest_{}'.format(i))
                _f_rest = self.features_rest.reshape(self.features_rest.shape[0], self.features_rest.shape[1]*self.features_rest.shape[2])
                data += (_f_rest,)

        if opacities:
            l.append('opacity')
            data += (self.opacities,)

        if scales:
            for i in range(self.scales.shape[1]):
                l.append('scale_{}'.format(i))
            data += (self.scales,)

        if rots:
            for i in range(self.rots.shape[1]):
                l.append('rot_{}'.format(i))
            data += (self.rots,)
        
        # ---------------- Using PlyElement library to store Gaussian ---------------- #
        dtype_full = [(attribute, 'f4') for attribute in l]
        elements = np.empty(self.num_of_point, dtype=dtype_full)
        attributes = np.concatenate(data, axis=1)
        elements[:] = list(map(tuple, attributes))
        el = PlyElement.describe(elements, 'vertex')
        
        if ascii:
            PlyData([el], text=True).write(save_path)
        else:
            PlyData([el]).write(save_path)
    
    def shift(self, center=[0,0,0]):
        self.xyz = self.xyz + center
    
    def get_bound(self):
        max_indices = []
        max_values = []
        for i in range(3):
            _col = self.xyz[:, i]
            _max_index = np.argmax(_col)
            _max_value = _col[_max_index]
            max_indices.append(_max_index)
            max_values.append(_max_value)

        min_indices = []
        min_values = []
        for i in range(3):
            _col = self.xyz[:, i]
            _min_index = np.argmin(_col)
            _min_value = _col[_min_index]
            min_indices.append(_min_index)
            min_values.append(_min_value)

        return min_values, max_values, min_indices, max_indices

    def delete_Gaussian(self, indices_to_delete: list):
        if self.xyz is not -1:
            self.xyz = np.delete(self.xyz, indices_to_delete, axis=0)
        if self.opacities is not -1:
            self.opacities = np.delete(self.opacities, indices_to_delete, axis=0)
        if self.features_dc is not -1:
            self.features_dc = np.delete(self.features_dc, indices_to_delete, axis=0)
        if self.features_rest is not -1:
            self.features_rest = np.delete(self.features_rest, indices_to_delete, axis=0)
        if self.scales is not -1:
            self.scales = np.delete(self.scales, indices_to_delete, axis=0)
        if self.rots is not -1:
            self.rots = np.delete(self.rots, indices_to_delete, axis=0)
        
        # ---------------------------- Update num_of_point --------------------------- #
        self.num_of_point = self.xyz.shape[0]

    def reduce_SH(self, target_sh_deg):
        if target_sh_deg < self.sh_deg:
            num_of_coefficient = 3 * (target_sh_deg + 1) ** 2 - 3
            self.features_rest = self.features_rest[:,:,:int(num_of_coefficient/3)]
            self.sh_deg = target_sh_deg
        else:
            print(f"The target degree ({target_sh_deg}) is larger than Gaussians' degree ({self.sh_deg})")

    def limit_x(self, _min, _max):
        _bound = self.get_bound()
        _min = max(_min, _bound[0][0])
        _max = min(_max, _bound[1][0])
        print(np.where((self.xyz[:, 0] < _min) | (self.xyz[:, 0] > _max)))
        indices = np.where((self.xyz[:, 0] < _min) | (self.xyz[:, 0] > _max))[0]
        print(f"Delete {indices.shape[0]} points")
        self.delete_Gaussian(indices)
    
    def limit_y(self, _min, _max):
        _bound = self.get_bound()
        _min = max(_min, _bound[0][1])
        _max = min(_max, _bound[1][1])
        print(_min, _max)
        indices = np.where((self.xyz[:, 1] < _min) | (self.xyz[:, 1] > _max))[0]
        print(f"Delete {indices.shape[0]} points")
        self.delete_Gaussian(indices)

    def limit_z(self, _min, _max):
        _bound = self.get_bound()
        _min = max(_min, _bound[0][2])
        _max = min(_max, _bound[1][2])
        print(_min, _max)
        indices = np.where((self.xyz[:, 2] < _min) | (self.xyz[:, 2] > _max))[0]
        print(f"Delete {indices.shape[0]} points")
        self.delete_Gaussian(indices)

    def recenter(self):
        bound = self.get_bound()
        center_x = (bound[0][0] + bound[1][0]) / 2
        center_y = (bound[0][1] + bound[1][1]) / 2
        center_z = (bound[0][2] + bound[1][2]) / 2
        self.shift([0-center_x, 0-center_y, 0-center_z])
    
    def sort(self):
        # sort_idx = np.argsort(self.xyz[:, 0])
        sort_idx = np.argsort(self.opacities[:, 0])
        print(sort_idx)
        self.xyz = self.xyz[sort_idx]
        self.features_dc = self.features_dc[sort_idx]
        self.features_rest = self.features_rest[sort_idx]
        self.opacities = self.opacities[sort_idx]
        self.scales = self.scales[sort_idx]
        self.rots = self.rots[sort_idx]


class GaussianModelV2():
    """
    A class to load and manipulate the more flexible Gaussian models from PLY files.
    """
    data = {}
    num_of_point = 0
    sh_deg = -1

    def __init__(self, gs_path: str):
        self.load_gaussian_ply(gs_path)

    def copy(self):
        new_gs = GaussianModelV2.__new__(GaussianModelV2)
        new_gs.data = self.data.copy()
        new_gs.num_of_point = self.num_of_point
        new_gs.sh_deg = self.sh_deg
        return new_gs    

    def load_gaussian_ply(self, path: str) -> None:
        self.data = {}
        plydata = PlyData.read(path)
        self.num_of_point = plydata.elements[0][plydata.elements[0].properties[0].name].shape[0]
        for property in plydata.elements[0].properties:
            _property_data = {"val_dtype": property.val_dtype, "data": np.asarray(plydata.elements[0][property.name])}
            self.data.update({property.name: _property_data})
        data_keys = self.data.keys()
        if all(item in data_keys for item in ['f_dc_0', 'f_dc_1', 'f_dc_2']):
            self.sh_deg = 0
            if all(item in data_keys for item in [f'f_rest_{i}' for i in range(0*3, 3*3)]):
                self.sh_deg = 1
                if all(item in data_keys for item in [f'f_rest_{i}' for i in range(3*3, 3*3+5*3)]):
                    self.sh_deg = 2
                    if all(item in data_keys for item in [f'f_rest_{i}' for i in range(3*3+5*3, (3*3+5*3)+7*3)]):
                        self.sh_deg = 3
    
    def add_attribute(self, key: str, type: str, data: np.ndarray):
        if self.num_of_point == data.shape[0]:
            _property_data = {"val_dtype": type, "data": data}
            self.data.update({key: _property_data})
        else:
            print("Can't add attribute. Wrong number of points.")

    def delete_attribute(self, key: str):
        if key in self.data:
            del self.data[key]
        else:
            print(f"Attribute {key} not found in the model.")

    def export_gs_to_ply(self, save_path: str, ascii=False):
        
        assert hasattr(self, 'data'), "self.data must be loaded via load_gaussian_ply()"
        assert hasattr(self, 'num_of_point'), "self.num_of_point not found"
        
        data_full = []
        dtype_full = []
        
        for key, value in self.data.items():
            dtype_full.append((key, value["val_dtype"]))
            array = value["data"]
            if array.ndim == 1:
                array = array.reshape(-1, 1)  # 轉成 (N,1)
            data_full.append(array)
        
        attributes = np.concatenate(data_full, axis=1)
        elements = np.empty(self.num_of_point, dtype=dtype_full)
        elements[:] = list(map(tuple, attributes))
        el = PlyElement.describe(elements, 'vertex')

        if ascii:
            PlyData([el], text=True).write(save_path)
        else:
            PlyData([el]).write(save_path)
