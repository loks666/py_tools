from PIL import Image
import os

def convert_to_ico(input_image_path, output_sizes=None):
    """
    将 PNG 或 JPG 图片转换为 ICO 图标格式，支持自定义尺寸。
    :param input_image_path: 输入图片路径
    :param output_sizes: 要生成的图标尺寸（整数或列表）。默认生成所有尺寸 [16, 32, 48, 64, 128, 256]。
    """
    if not os.path.exists(input_image_path):
        print(f"输入图片文件 '{input_image_path}' 不存在。")
        return

    # 根据输入图片路径生成输出图标路径
    base_name, _ = os.path.splitext(input_image_path)  # 去掉扩展名
    output_icon_path = f"{base_name}.ico"  # 替换为 .ico 扩展名

    # 设置默认尺寸或处理单个整数输入
    if output_sizes is None:
        output_sizes = [16, 32, 48, 64, 128, 256]  # 默认生成所有尺寸
    elif isinstance(output_sizes, int):
        output_sizes = [output_sizes]  # 单个整数转为列表

    try:
        # 打开输入图片
        with Image.open(input_image_path) as img:
            # 将图片转换为 RGBA 模式（确保兼容性）
            img = img.convert("RGBA")

            # 保存为 ICO 格式
            img.save(output_icon_path, format="ICO", sizes=[(size, size) for size in output_sizes])
            print(f"成功将 '{input_image_path}' 转换为图标 '{output_icon_path}'，尺寸：{output_sizes}")
    except Exception as e:
        print(f"图片转换为 ICO 时出错：{e}")

if __name__ == "__main__":
    input_image = r'D:\Program\Project\Python\py_tools\tool\ai.png'
    icon_sizes = 256  # 传入单个整数
    # 调用转换函数
    convert_to_ico(input_image, output_sizes=icon_sizes)
