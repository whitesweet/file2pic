from PIL import Image
import numpy as np
import os


def read_png_file(file_path):

    # 读取图片
    image = Image.open(file_path)

    data = np.array(image)

    # 转换为二维数组
    two_d_array = data.tolist()
    
    decimal_array = []
    for sublist in two_d_array:
        for rgb in sublist:
            for element in rgb:
                decimal_array.append(element)

    # 末尾有255值得填充值，全部去掉
    while decimal_array[-1] == 255:
        decimal_array.pop()

    # 末尾有0值得填充值，全部去掉
    while decimal_array[-1] == 0:
        decimal_array.pop()

    return decimal_array


def generate_file(file_name, decimal_array):
    # 将十进制数转换为二进制数据
    binary_data = bytes(decimal_array)

    # 保存生成的file文件
    with open("restore\\" + file_name + ".txt", "wb") as file:
        file.write(binary_data)


# 文件夹路径
directory_path = "output"

# 获取文件夹下所有的png文件路径
png_files = [
    os.path.join(directory_path, file)
    for file in os.listdir(directory_path)
    if file.endswith(".png")
]

for file_path in png_files:
    file_name = os.path.basename(file_path).split(".")[0]
    decimal_array = read_png_file(file_path)
    generate_file(file_name, decimal_array)
