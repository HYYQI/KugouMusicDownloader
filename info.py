# !注! 该代码段来自ai，仅修改，可能有bug
# return: str

import sys
from prettytable import PrettyTable

def parse_audio_qualities(data):
    qualities = []
    quality_types = [
        ('128', '128kbps'),
        ('320', '320kbps'),
        ('sq', '无损'),
        ('high', '高解析度')
    ]

    for prefix, name in quality_types:
        hash_key = f"{prefix}hash"
        size_key = f"{prefix}filesize"
        privilege_key = f"{prefix}privilege"

        # 获取音质参数
        quality_hash = data['extra'].get(hash_key, "")
        file_size = data['extra'].get(size_key, 0)
        can_download = (
            quality_hash.strip() != "" and
            file_size > 0 and
            data.get(privilege_key, 1) == 0
        )

        # 转换文件大小为MB
        size_mb = round(file_size / (1024 * 1024), 2) if file_size > 0 else 0

        qualities.append({
            "name": name,
            "hash": quality_hash,
            "size": f"{size_mb} MB" if can_download else "N/A",
            "downloadable": "是" if can_download else "否"
        })

    return qualities

def main(data):
    qualities = parse_audio_qualities(data)
    
    # 过滤可下载项
    downloadable = [q for q in qualities if q['downloadable'] == '是']
    
    if not downloadable:
        print("错误：没有可下载的音质版本")
        sys.exit(1)

    # 创建表格
    table = PrettyTable()
    table.field_names = ["序号", "音质", "能否下载", "大小", "Hash"]
    table.align["Hash"] = "c"

    for idx, q in enumerate(qualities):
        table.add_row([
            idx,
            q['name'],
            q['downloadable'],
            q['size'],
            q['hash'] if q['hash'] else "N/A"
        ])

    print(table)
    user_choice = int(input("序号："))
    try:
        index = int(user_choice)
        if index < 0 or index >= len(qualities):
            raise ValueError("序号超出范围")
        
        target = qualities[index]
        # 疑似不可用(未证实)
        if not target["downloadable"]:
            print(f"错误：序号 {index} 的音质不可下载")
            sys.exit(1)
            
        return target["hash"]
    
    except ValueError:
        print("错误：请输入有效的数字序号")
        sys.exit(1)
