import os
import sys
from pdf2image import convert_from_path
from PIL import Image

def pdf_to_long_image(pdf_path):
    try:
        # 直接调用 convert_from_path，依赖系统环境变量中的 poppler
        pages = convert_from_path(pdf_path)
    except Exception as e:
        print(f"转换 PDF 时出错: {e}")
        sys.exit(1)

    if not pages:
        print("未能从 PDF 中提取到任何页面。")
        sys.exit(1)

    # 计算拼接后图像的宽度和总高度（此处将页面从上到下依次拼接）
    max_width = max(page.width for page in pages)
    total_height = sum(page.height for page in pages)

    # 创建一张空白图用于拼接
    long_img = Image.new("RGB", (max_width, total_height), color="white")

    # 逐页粘贴到空白图上
    y_offset = 0
    for page in pages:
        long_img.paste(page, (0, y_offset))
        y_offset += page.height

    # 构造输出路径（与原 PDF 同目录，文件名相同但扩展名为 .jpg）
    base_name = os.path.splitext(os.path.basename(pdf_path))[0]
    output_path = os.path.join(os.path.dirname(pdf_path), f"{base_name}.jpg")

    # 保存最终拼接图
    try:
        long_img.save(output_path)
        print(f"已将所有页面拼接为长图：{output_path}")
    except Exception as e:
        print(f"保存图片时出错: {e}")
        sys.exit(1)

def main():
    # 获取当前脚本所在目录
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # 列出当前目录下所有 PDF 文件
    pdf_files = [f for f in os.listdir(current_dir) if f.lower().endswith('.pdf')]

    if len(pdf_files) == 0:
        print("当前目录下没有找到 PDF 文件。")
        sys.exit(1)
    elif len(pdf_files) > 1:
        print("当前目录下有多个 PDF 文件，请确保只有一个 PDF 文件。")
        sys.exit(1)
    else:
        # 只有一个 PDF 文件，进行转换
        pdf_path = os.path.join(current_dir, pdf_files[0])
        print(f"正在处理 PDF 文件：{pdf_path}")
        pdf_to_long_image(pdf_path)

if __name__ == "__main__":
    main()
