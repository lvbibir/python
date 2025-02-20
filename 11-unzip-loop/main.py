import os
import zipfile
import py7zr
import rarfile
import subprocess

def extract_zip(file_path, password, extract_dir):
    # with zipfile.ZipFile(file_path) as zfile:
        # zfile.extractall(path=extract_dir, pwd=password.encode())
    subprocess.run(['unzip', f'-P{password}', file_path, '-d', extract_dir], check=True, stdout=subprocess.DEVNULL)

def extract_7z(file_path, password, extract_dir):
    with py7zr.SevenZipFile(file_path, mode='r', password=password) as z:
        z.extractall(path=extract_dir)

def extract_rar(file_path, password, extract_dir):
#    with rarfile.RarFile(file_path) as rfile:
#        rfile.extractall(path=extract_dir, pwd=password)
    subprocess.run(['unrar', f'-p{password}', 'x', file_path, extract_dir], check=True, stdout=subprocess.DEVNULL)

def unzip_nested_files(file_path):
    current_file = file_path
    count = 1

    while True:
        directory = os.path.dirname(current_file)
        file_name = os.path.basename(current_file)
        password = file_name.replace('.zip', '').replace('.7z', '').replace('.rar', '')

        try:
            if zipfile.is_zipfile(current_file):
                extract_zip(current_file, password, directory)
            elif py7zr.is_7zfile(current_file):
                extract_7z(current_file, password, directory)
            elif rarfile.is_rarfile(current_file):
                extract_rar(current_file, password, directory)
            else:
                print(f"未知的压缩格式或文件不是压缩文件：{current_file}")
                break

        except Exception as e:
            print(f"解压失败，文件：{current_file}，可能是密码错误或文件已损坏。错误信息：{e}")
            break

        print(f"计数{count}\t成功解压{current_file}\t", end='')
        os.remove(current_file)

        extracted_files = os.listdir(directory)
        extracted_files = [os.path.join(directory, f) for f in extracted_files if os.path.isfile(os.path.join(directory, f))]

        # 寻找新的压缩文件
        new_file = None
        for file in extracted_files:
            if zipfile.is_zipfile(file) or py7zr.is_7zfile(file) or rarfile.is_rarfile(file):
                new_file = file
                break
        print(f"解压后的文件:{new_file}\t")

        if not new_file:
            print(f"解压后未找到新的压缩文件或解压后文件不是有效的压缩文件：{extracted_files}")
            break

        current_file = new_file
        count += 1

    print("循环解压完成")

# 示例用法
file_path = "/home/lvbibir/python/tmp/34471.zip"  # 初始压缩文件路径
unzip_nested_files(file_path)