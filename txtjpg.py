from PIL import Image
import numpy as np
import math
import os
import glob


def read_all_txt_files_in_directory(directory_path):
    # 获取文件夹下所有的 .txt 文件路径
    txt_files = glob.glob(os.path.join(directory_path, "*.txt"))

    # 读取每个 .txt 文件的文件名和内容
    file_contents = []
    for file_path in txt_files:
        file_name = os.path.basename(file_path)
        with open(file_path, "rb") as file:
            content = file.read()
            file_contents.append((file_name, content))

    return file_contents


def pad_array_to_multiple_of_three(arr):
    # 计算数组的当前长度
    length = len(arr)

    # 计算需要补足的 0 的数量
    padding_needed = (3 - (length % 3)) % 3

    # 使用 0 填充数组
    padded_array = arr + [0] * padding_needed

    return padded_array


def find_dimensions(c):
    for b in range(1, int(math.sqrt(c)) + 1):
        a = c // b
        if a * b == c and 0.8 * b <= a <= 1.2 * b:
            return a, b
    return None, None


def pad_and_convert_to_2d(arr):
    c = len(arr) // 3  # 计算有多少个 RGB 元素（每个元素包含3个值）

    # 找到合适的维度 a 和 b
    a, b = find_dimensions(c)

    # 如果找不到合适的 a 和 b，则填充数组
    while a is None or b is None:
        arr.extend([255, 255, 255])
        c = len(arr) // 3
        a, b = find_dimensions(c)

    print("维度 a 和 b 为：", a, b)

    # 将一维数组转换为二维数组
    rgb_elements = [(arr[i], arr[i + 1], arr[i + 2]) for i in range(0, len(arr), 3)]
    two_d_array = [rgb_elements[i * b : (i + 1) * b] for i in range(a)]

    return two_d_array


def generateJpg(file_name, binary_data):
    # 将二进制数据分割成每 8 个比特为一组，并转换为十进制数
    decimal_array = [byte for byte in binary_data]

    # 打印结果
    # print(decimal_array)

    # 补足数组长度为 3 的倍数
    padded_array = pad_array_to_multiple_of_three(decimal_array)

    # 将一维数组转换为二维数组
    two_d_array = pad_and_convert_to_2d(padded_array)

    # 示例二维数组，每个元素是一个 (R, G, B) 元组
    # two_d_array = [
    #     [(255, 0, 0), (0, 255, 0), (0, 0, 255)],  # 红色, 绿色, 蓝色
    #     [(255, 255, 0), (0, 255, 255), (255, 0, 255)],  # 黄色, 青色, 紫色
    #     [(255, 255, 255), (0, 0, 0), (128, 128, 128)],  # 白色, 黑色, 灰色
    # ]

    # 将二维数组转换为 NumPy 数组
    data = np.array(two_d_array, dtype=np.uint8)

    # 获取数组的尺寸
    height, width, _ = data.shape

    # 创建一个新的图片对象
    image = Image.fromarray(data, "RGB")

    # 保存生成的图片
    image.save("output\\" + file_name + ".jpg")


# 文件夹路径
directory_path = "input"

# 调用函数读取所有 .txt 文件内容
all_txt_contents = read_all_txt_files_in_directory(directory_path)

for file_name, content in all_txt_contents:
    generateJpg(file_name, content)
