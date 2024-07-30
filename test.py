from PIL import Image
import numpy as np
import math
import os
import glob


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


with open(os.path.join("1.txt"), "rb") as file:
    content = file.read()

print(content)

# 将二进制数据分割成每 8 个比特为一组，并转换为十进制数
decimal_array = [byte for byte in content]

# 打印结果
print(decimal_array)

# 补足数组长度为 3 的倍数
padded_array = pad_array_to_multiple_of_three(decimal_array)

# 将一维数组转换为二维数组
two_d_array = pad_and_convert_to_2d(padded_array)
print("two_d_array:", two_d_array)

# 将二维数组转换为 NumPy 数组
data = np.array(two_d_array, dtype=np.uint8)

# 创建一个新的图片对象
image = Image.fromarray(data, "RGB")

# 保存图片到文件
image.save("example_image.png")

# 从文件读取图片
read_image = Image.open("example_image.png")

new_data = np.array(read_image)

# 转换为二维数组
new_two_d_array = new_data.tolist()

# 打印结果
print("new_two_d_array:", new_two_d_array)

new_decimal_array = []
for sublist in new_two_d_array:
    for rgb in sublist:
        for element in rgb:
            new_decimal_array.append(element)
print(new_decimal_array)

# 将十进制数转换为二进制数据
binary_data = bytes(new_decimal_array)
print(binary_data)

# 保存生成的txt文件
with open("2.txt", "wb") as file:
    file.write(binary_data)
