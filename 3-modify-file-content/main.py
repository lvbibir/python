import os
import re

# 定义要查找的文件后缀和要替换的字符串
fileExtension = '.ass'
strOld = '艾连'
strNew = '艾伦'

# 遍历目录中的所有文件，包含子目录
for root, dirs, files in os.walk('.'):
    # 遍历所有文件
    for file in files:
        # 如果文件以指定的后缀结尾，则打开文件进行替换
        if file.endswith(fileExtension):
            filePath = os.path.join(root, file)
            with open(filePath, 'r+', encoding='utf-8') as f:
                content = f.read()
                # 使用正则表达式进行替换
                new_content = re.sub(strOld, strNew, content)
                f.seek(0)
                f.write(new_content)
                f.truncate()