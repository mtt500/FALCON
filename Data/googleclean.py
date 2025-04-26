import os

def remove_comments_only(text):
    lines = text.splitlines()
    cleaned_lines = []
    for line in lines:
        if "评论" in line or "登录后才能发表评论" in line:
            break
        cleaned_lines.append(line)
    return "\n".join(cleaned_lines)

def batch_clean_wooyun(folder_path, output_path):
    os.makedirs(output_path, exist_ok=True)

    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.txt'):
                input_file = os.path.join(root, file)
                relative_path = os.path.relpath(input_file, folder_path)
                output_file = os.path.join(output_path, relative_path)

                os.makedirs(os.path.dirname(output_file), exist_ok=True)

                with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
                    raw_text = f.read()

                cleaned_text = remove_comments_only(raw_text)

                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(cleaned_text)

                print(f"✅ 处理完成：{relative_path}")

# 示例使用
input_folder = "C:\\Users\\lzy\\OneDrive\\Desktop\\新建文件夹\\wooyun_archive数据" # ⚠️ 替换为你的原始文档路径
output_folder = "C:\\Users\\lzy\\OneDrive\\Desktop\\新建文件夹\\wooyun-clean" # ⚠️ 替换为你要保存清洗结果的路径
batch_clean_wooyun(input_folder, output_folder)
