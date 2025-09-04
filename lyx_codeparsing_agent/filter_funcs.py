import re

# 你关注的字符串操作函数 + system 函数
string_funcs = [
    'strcpy', 'strncpy', 'strcat', 'strncat',
    'sprintf', 'snprintf', 'strlen', 'strcmp',
    'strncmp', 'strstr', 'strchr', 'strrchr', 'strtok'
]
target_funcs = ['system'] + string_funcs

# 读取反编译后的代码文件
input_file = 'decompiled_output.txt'
output_file = 'filtered_output.txt'

with open(input_file, 'r', encoding='utf-8') as f:
    content = f.read()

# 以分隔线划分函数块
func_blocks = re.split(r'-{10,}', content)

filtered_blocks = []

# 逐个检查函数块是否包含目标函数
for block in func_blocks:
    if not block.strip():
        continue

    # 提取函数名
    match = re.search(r'Function:\s+(\w+)', block)
    if match:
        func_name = match.group(1)
        # 判断函数名或函数体是否包含目标关键词
        if any(target in func_name for target in target_funcs) or \
           any(f"{target}(" in block for target in target_funcs):
            filtered_blocks.append(block.strip())

# 保存到文件
with open(output_file, 'w', encoding='utf-8') as f:
    for block in filtered_blocks:
        f.write(block + '\n' + '-' * 40 + '\n\n')

# 同时输出到终端
print("===== Filtered Functions =====\n")
for block in filtered_blocks:
    print(block)
    print("\n" + "-" * 40 + "\n")

print(f"✅ 已保存到文件: {output_file}")
