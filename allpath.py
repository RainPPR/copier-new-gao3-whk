import os

allpathlist = {
    "语文": "语文",
    "数学": "数学",
    "英语": "英语",
    "物理": "物理",
    "化学": "化学",
    "生物": "生物",
    "其他": "其他",
    "0 其他": "其他",
    "1 语文": "语文",
    "2 数学": "数学",
    "3 英语": "英语",
    "4 物理": "物理",
    "5 化学": "化学",
    "6 生物": "生物",
    "0其他": "其他",
    "1语文": "语文",
    "2数学": "数学",
    "3英语": "英语",
    "4物理": "物理",
    "5化学": "化学",
    "6生物": "生物",
}


def getallpath(parent_path):
    """
    在 parent_path 下查找 allpathlist 中指定的文件夹。
    返回实际存在的源文件夹到目标文件夹的映射: {source_name: target_name}
    """
    result = {}
    if not parent_path or not os.path.isdir(parent_path):
        return result

    for source_name, target_name in allpathlist.items():
        full_path = os.path.join(parent_path, source_name)
        if os.path.isdir(full_path):
            result[source_name] = target_name

    return result
