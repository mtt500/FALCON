import os
import subprocess
from typing import List

def decompile_binary(binary_file: str, output_dir: str, ghidra_path: str) -> bool:
    """
    反编译单个二进制文件
    """
    try:
        # 规范化路径
        binary_file = os.path.abspath(binary_file)
        output_dir = os.path.abspath(output_dir)
        ghidra_path = os.path.abspath(ghidra_path)
        
        # 创建项目目录
        project_dir = os.path.join(output_dir, "ghidra_project")
        os.makedirs(project_dir, exist_ok=True)
        
        # 构建 Ghidra 命令
        analyze_headless = os.path.join(ghidra_path, "support", "analyzeHeadless.bat")
        script_dir = os.path.join(os.getcwd(), "ghidra_scripts")
        
        cmd = [
            f'"{analyze_headless}"',
            f'"{project_dir}"',
            "temp_project",
            "-import", f'"{binary_file}"',
            "-processor", "MIPS:LE:32:default",  # 默认处理器，Ghidra 会自动检测
            "-scriptPath", f'"{script_dir}"',
            "-postScript", "DecompileScript.java",
            "-deleteProject"
        ]
        
        # 执行 Ghidra
        process = subprocess.Popen(
            ' '.join(cmd),
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8',
            errors='replace'
        )
        
        stdout, stderr = process.communicate(timeout=600)  # 10分钟超时
        
        # 检查反编译结果
        temp_output = "decompiled_output.txt"
        if os.path.exists(temp_output):
            # 使用原始文件名作为输出文件名
            output_file = os.path.join(output_dir, f"{os.path.basename(binary_file)}_decompiled.txt")
            os.replace(temp_output, output_file)
            return True
            
        return False
        
    except Exception as e:
        print(f"处理文件出错: {str(e)}")
        return False

def batch_decompile(input_dir: str, output_dir: str, ghidra_path: str):
    """
    批量反编译目录下的所有文件（无后缀）
    """
    # 获取所有文件（不考虑后缀）
    files_to_process = []
    for root, _, files in os.walk(input_dir):
        for file in files:
            # 跳过隐藏文件和临时文件
            if not file.startswith('.') and not file.endswith('~'):
                full_path = os.path.join(root, file)
                # 检查是否为二进制文件
                try:
                    with open(full_path, 'rb') as f:
                        # 读取文件头部几个字节
                        header = f.read(4)
                        # 简单的二进制文件检查（ELF, PE, MZ 等魔数）
                        if header.startswith(b'\x7fELF') or header.startswith(b'MZ'):
                            files_to_process.append(full_path)
                except:
                    continue
    
    print(f"找到 {len(files_to_process)} 个二进制文件需要处理")
    
    # 处理每个文件
    for i, file_path in enumerate(files_to_process, 1):
        print(f"处理第 {i}/{len(files_to_process)} 个文件: {file_path}")
        if decompile_binary(file_path, output_dir, ghidra_path):
            print(f"成功: {file_path}")
        else:
            print(f"失败: {file_path}")

if __name__ == "__main__":
    GHIDRA_PATH = r"D:\ghidra\ghidra_10.4_PUBLIC_20230928\ghidra_10.4_PUBLIC"
    INPUT_DIR = r"D:\Security_Competition\code_parsing_agent\dataset\cve-binfiles"  # 替换为你的数据集目录
    OUTPUT_DIR = r"decompiled_results_v1"
    
    batch_decompile(INPUT_DIR, OUTPUT_DIR, GHIDRA_PATH) 