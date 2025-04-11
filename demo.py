import os
import shutil


def copy_and_rename_files(root_dir):
    """
    遍历目录结构，复制并重命名所有文件到根目录。

    :param root_dir: 根目录路径
    """
    # 获取根目录的绝对路径，用于后续路径解析
    # root_abs_path = os.path.abspath(root_dir)

    for dirpath, dirnames, filenames in os.walk(root_dir):
        # 获取当前路径的各级目录名
        parts = dirpath.split(os.sep)

        # 找到年份目录的位置
        year_index = None
        for i, part in enumerate(parts):
            if part.isdigit() and len(part) == 4:  # 检查是否为年份目录
                year_index = i
                break

        # 如果没有找到年份目录，跳过该路径
        if year_index is None or year_index < len(parts) - 2:
            continue

        # 提取年份、一级、二级、三级目录名
        level1 = parts[year_index]  # 年份目录
        level2 = parts[year_index + 1] if year_index + 1 < len(parts) else ""
        level3 = parts[year_index + 2] if year_index + 2 < len(parts) else ""

        # 遍历当前目录下的所有文件
        for filename in filenames:
            # 构造新文件名
            new_filename_parts = [level1, level2]
            if level3 != "":  # 如果存在三级目录
                new_filename_parts.append(level3)
            new_filename_parts.append(filename)
            new_filename = "-".join(new_filename_parts).strip('-')

            # 确保文件名不超长
            max_length = 255  # 根据操作系统调整
            base, ext = os.path.splitext(new_filename)
            if len(new_filename) > max_length:
                truncated_base = base[: max_length - len(ext)]
                new_filename = truncated_base + ext

            new_filepath = os.path.join(root_dir, new_filename)

            # 复制文件到根目录并重命名
            old_filepath = os.path.join(dirpath, filename)
            try:
                shutil.copy2(old_filepath, new_filepath)  # 使用 copy2 保留元数据
                print(f"Copied: {old_filepath} -> {new_filepath}")
            except Exception as e:
                print(f"Error copying {old_filepath}: {e}")


if __name__ == "__main__":
    # 设置根目录路径
    root_directory = "/mnt/c/Users/lvbibir/Desktop/2025-02-27 AI相关工作/管理办法、制度"

    # 确保根目录存在
    if not os.path.exists(root_directory):
        print(f"Error: Directory {root_directory} does not exist.")
    else:
        copy_and_rename_files(root_directory)
