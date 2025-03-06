from PIL import Image

def rgb888_to_rgb565(r, g, b):
    """将RGB888格式转换为RGB565格式"""
    r5 = (r >> 3) & 0x1F  # 8位红色 -> 5位红色
    g6 = (g >> 2) & 0x3F  # 8位绿色 -> 6位绿色
    b5 = (b >> 3) & 0x1F  # 8位蓝色 -> 5位蓝色
    return (r5 << 11) | (g6 << 5) | b5


def convert_image_to_c_array(image_path, array_name):
    """将图片转换为RGB565格式的C语言数组，按矩阵排布"""
    # 打开图片并转换为RGB模式
    image = Image.open(image_path).convert("RGB")
    width, height = image.size

    # 生成C语言数组的头部
    output = f"const uint16_t {array_name}[{width * height}] = {{\n"

    # 遍历像素并转换为RGB565格式
    for y in range(height):  # 遍历每一行
        output += "    "  # 每行的缩进
        for x in range(width):  # 遍历每一列
            r, g, b = image.getpixel((x, y))
            rgb565 = rgb888_to_rgb565(r, g, b)
            output += f"0x{rgb565:04X}"  # 格式化为16位十六进制
            if x < width - 1:  # 如果不是行的最后一个像素，加逗号
                output += ", "
        output += ",\n" if y < height - 1 else "\n"  # 每行末尾的逗号

    output += "};\n"
    return output


# 示例用法
if __name__ == "__main__":
    image_path = "E:/resources/desk/red-eye.jpg"  # 替换为你的图片路径
    array_name = "image_data"   # C语言数组的名称
    c_array = convert_image_to_c_array(image_path, array_name)

    # 打印或保存C语言数组
    print(c_array)
    with open("image_data.h", "w") as f:
        f.write(c_array)
    print("C语言数组已保存到 image_data.h")