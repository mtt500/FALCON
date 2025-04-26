import os
import csv

# ⚠️ 替换为你的实际文件夹路径
input_folder = "C:\\Users\\lzy\\OneDrive\\Desktop\\新建文件夹\\wooyun_archive数据"
output_csv = "deleted_invalid_files.csv"

# 判定为“无效”的关键词和最小长度
keywords = ['漏洞', '报告', 'Summary', '影响', '详情', '复现', 'POC']
min_length = 100

deleted_files = []

for root, dirs, files in os.walk(input_folder):
    for filename in files:
        if filename.endswith('.txt'):
            file_path = os.path.join(root, filename)
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    if len(content.strip()) < min_length or not any(k in content for k in keywords):
                        deleted_files.append([file_path])
                        os.remove(file_path)
                        print(f"🗑️ 已删除：{file_path}")
            except Exception as e:
                deleted_files.append([file_path])
                print(f"⚠️ 读取失败也删除：{file_path}")
                os.remove(file_path)

# 写入删除记录
with open(output_csv, 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['已删除文件路径'])
    writer.writerows(deleted_files)

print(f"\n✅ 共删除无效文本文档 {len(deleted_files)} 个，路径已保存至：{output_csv}")
