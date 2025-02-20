import json
import json5
import os

# ********** 需修改 dir_(默认路径好像是 C:\Users\用户名\.vscode\userdata\User 下)
print('开始settings.json排序')
dir_ = r'/mnt/c/Users/lvbibir/AppData/Roaming/Code/User/'
src_name = "settings.json"  # 源文件名
new_name = "settings_.json"  # 新文件
old_name = "settings_old.json"  # 源文件重命名

src_file = os.path.join(dir_, src_name)
new_file = os.path.join(dir_, new_name)
old_file = os.path.join(dir_, old_name)

# 读取源文件内容
with open(src_file, 'r', encoding='utf-8') as f:
    text = json5.load(f)

# print(type(text))


def to_lower(req_list: list):
    # 统一大小写
    lower_upper = {}  # key: 处理后的字符串，value: 处理前的字符串
    res_list = []
    for t in req_list:
        new_t = t.lower()
        res_list.append(new_t)  # 全部转为小写字母
        lower_upper[new_t] = t
    return res_list, lower_upper


def my_sorted(dic: dict):
    # 递归对每一层排序
    # 循环判断某个key对应的value是否为dict，是的话先进行里层排序
    for k, v in dic.items():
        if type(v) == dict:
            dic[k] = my_sorted(v)
    # 排序：
    # 1. 对key排序
    key_list, lower_upper = to_lower(list(dic.keys()))
    key_list.sort()
    # 2. 按key_list顺序重新构建dict
    new_dic = {lower_upper[k]: dic[lower_upper[k]] for k in key_list}

    return new_dic


# 排序
text = my_sorted(text)

# 将排序后的json内容写入新文件
json_text = json.dumps(text)
with open(new_file, 'w', encoding='utf-8') as f:
    f.write(json_text)

# 重命名源文件为 settings_old.json，新文件为 settings.json
# 如果已存在 settings_old.json，先删除
if os.path.exists(old_file):
    os.remove(old_file)
os.rename(src_file, old_file)
os.rename(new_file, src_file)
print('settings.json排序完毕')
