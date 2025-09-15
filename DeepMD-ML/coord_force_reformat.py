import numpy as np

def parse_xyz(xyz_file):
    """
    解析.xyz文件并输出每个时间步的坐标、力和原子数
    """
    coords_all = []  # 所有时间步的坐标
    forces_all = []  # 所有时间步的力
    energies_all = []  # 所有时间步的能量
    box_all = []  # 所有时间步的盒子信息

    with open(xyz_file, 'r') as file:
        lines = file.readlines()

    current_coords = []
    current_forces = []
    current_box = None
    atom_count = None  # 每个时间步的原子数

    # 读取每一行
    for line in lines:
        parts = line.split()

        # 跳过包含 "Lattice" 的行
        if 'Lattice' in line:
            # 只处理晶格信息，不进行后续的处理
            continue

        # 判断原子数
        if line.strip().isdigit():
            if atom_count is not None:
                # 输出每个时间步的数据数量
                print(f"Processed timestep: {len(current_coords)} atoms, {len(current_forces)} forces")

                coords_all.append(np.array(current_coords))  # 保持二维结构
                forces_all.append(np.array(current_forces))  # 保持二维结构

            # 重置数据
            atom_count = int(line.strip())  # 获取每个时间步的原子数
            current_coords = []
            current_forces = []

        elif len(parts) > 3:  # 读取坐标和力
            element = parts[0]  # 元素符号
            coords = list(map(float, parts[1:4]))  # 坐标
            forces = list(map(float, parts[4:7]))  # 力

            current_coords.append(coords)
            current_forces.append(forces)

    # 输出最后一个时间步的数据数量
    if atom_count is not None:
        print(f"Processed timestep: {len(current_coords)} atoms, {len(current_forces)} forces")
        coords_all.append(np.array(current_coords))
        forces_all.append(np.array(current_forces))

    return np.array(coords_all), np.array(forces_all)

def check_data_integrity(coords_all, forces_all):
    """
    检查每个时间步的数据是否符合要求
    """
    for i, (coord, force) in enumerate(zip(coords_all, forces_all)):
        print(f"Timestep {i+1}:")
        print(f"Coord shape: {coord.shape}, Force shape: {force.shape}")
        if coord.shape != (496, 3):
            print(f"Warning: Coord at timestep {i+1} has incorrect shape: {coord.shape}")
        if force.shape != (496, 3):
            print(f"Warning: Force at timestep {i+1} has incorrect shape: {force.shape}")

# 调用解析函数
xyz_file = "glass.xyz"  # 替换为你的文件路径


coords_all, forces_all = parse_xyz(xyz_file)
forces_all_flattened = forces_all.reshape(3, -1)
coords_all_flattened = coords_all.reshape(3, -1)
# 调用检查函数
check_data_integrity(coords_all_flattened, forces_all_flattened)

# 检查变换后的形状
print(f"Flattened coords_all shape: {coords_all.shape}")

# 保存为新的 npy 文件
np.save('coords.npy', coords_all_flattened)
np.save('forces.npy', forces_all_flattened)
