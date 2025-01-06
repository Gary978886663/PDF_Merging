import os
from PyPDF2 import PdfMerger
from PIL import Image

def convert_to_pdf(file_path, output_dir):
    """
    将非PDF文件（如图片）转换为PDF，并调整为A4大小，同时自动调整方向（短边为宽，长边为长）。

    :param file_path: 原始文件路径
    :param output_dir: 转换后的PDF文件保存目录
    :return: 转换后的PDF文件路径
    """
    try:
        img = Image.open(file_path)
        img = img.convert("RGB")

        # 检测图片方向，确保短边为宽，长边为长
        width, height = img.size
        if width > height:  # 如果宽大于高，则旋转90度
            img = img.rotate(90, expand=True)

        # A4尺寸 (宽: 595点, 高: 842点)
        a4_width, a4_height = (595, 842)
        img_width, img_height = img.size

        # 按比例调整图片大小以适应A4
        aspect_ratio = min(a4_width / img_width, a4_height / img_height)
        new_width = int(img_width * aspect_ratio)
        new_height = int(img_height * aspect_ratio)
        
        # 使用 Image.Resampling.LANCZOS 调整大小
        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

        # 创建A4白色背景
        a4_image = Image.new("RGB", (a4_width, a4_height), (255, 255, 255))
        paste_x = (a4_width - new_width) // 2
        paste_y = (a4_height - new_height) // 2
        a4_image.paste(img, (paste_x, paste_y))

        # 保存为PDF
        output_pdf = os.path.join(output_dir, os.path.basename(file_path) + ".pdf")
        a4_image.save(output_pdf, "PDF")
        return output_pdf
    except Exception as e:
        print(f"文件 {file_path} 转换为PDF时出错: {e}")
        return None

def merge_pdfs(pdf_list, output_filename):
    """
    合并多个PDF文件。

    :param pdf_list: 包含PDF文件路径的列表
    :param output_filename: 合并后PDF的输出文件名
    """
    merger = PdfMerger()
    try:
        for pdf in pdf_list:
            if os.path.exists(pdf) and pdf.lower().endswith('.pdf'):
                print(f"正在添加: {pdf}")
                merger.append(pdf)
            else:
                print(f"文件不存在或不是PDF: {pdf}")
        merger.write(output_filename)
        print(f"PDF合并完成，输出文件: {output_filename}")
    except Exception as e:
        print(f"合并过程中发生错误: {e}")
    finally:
        merger.close()

if __name__ == "__main__":
    prefix = r"C:\Users\xxx\xxx\xxxx\xxxx/"
    output_dir = prefix  # 转换后的PDF文件保存路径

    # 指定要合并的PDF文件路径列表
    original_files = [
        prefix + "file1.jpg",
        prefix + "file2.pdf",
        prefix + "file3.pdf"
    ]

    # 转换非PDF文件为PDF，并过滤出所有PDF文件
    pdf_files = []
    for file_path in original_files:
        if file_path.lower().endswith(".pdf"):
            pdf_files.append(file_path)
        else:
            print(f"正在转换文件为PDF: {file_path}")
            converted_pdf = convert_to_pdf(file_path, output_dir)
            if converted_pdf:
                pdf_files.append(converted_pdf)

    # 输出文件名
    output_pdf = prefix + "merged_output.pdf"

    # 合并PDF文件
    merge_pdfs(pdf_files, output_pdf)
