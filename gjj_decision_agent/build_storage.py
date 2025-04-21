import zipfile
import os
import shutil


# 复制文件到目标目录
def copy_files(zip_file, src_files, dest_dir):
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        for file in src_files:
            # 打开文件并读取其内容
            with zip_ref.open(file) as src_file:
                # 获取目标文件路径
                dest_file_path = os.path.join(dest_dir, os.path.basename(file))
                # 将文件内容写入目标路径
                with open(dest_file_path, 'wb') as dest_file:
                    shutil.copyfileobj(src_file, dest_file)


# 获取指定目录下的C/C++文件（.c和.cpp）
def get_c_cpp_files(zip_file, directory):
    c_files = []
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        # 获取所有以指定目录开头的文件（即目录下的文件）
        for file in zip_ref.namelist():
            # 过滤出以指定目录开头，且文件后缀为 .c 或 .cpp 的文件
            if file.startswith(directory):
                if file.endswith('.c') or file.endswith('.cpp'):
                    c_files.append(file)
                    if len(c_files) >= 5:
                        break
    return c_files


# 处理每个CWE文件夹
def process_cwe_folder(zip_file, cwe_folder, storage_dir):
    # 获取CWE文件夹下的所有C/C++文件
    print(f"loading c files in {cwe_folder}..")
    c_files = get_c_cpp_files(zip_file, cwe_folder)

    print(f"copying c files in {cwe_folder}")
    copy_files(zip_file, c_files, storage_dir)


# 主函数
def main():
    zip_file = 'D:/百度下载/2017-10-01-juliet-test-suite-for-c-cplusplus-v1-3.zip'  # 压缩包路径
    storage_dir = './storage/testcases'  # 存储目录

    # 遍历zip文件中的testcases目录下的CWE文件夹
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        testcases_dir = 'C/testcases/'

        # 创建一个空的列表用于存放CWE文件夹路径
        cwe_folders = []

        # 获取ZIP文件中的所有文件和目录路径
        print("loading CWE folder..")
        for f in zip_ref.namelist():
            # 判断路径是否以 'C/testcases/' 开头并且是一个目录
            if f.startswith(testcases_dir) and f.endswith('/') and f != testcases_dir:
                # 检查该路径下是否有子文件夹
                subfolders = [subf for subf in zip_ref.namelist() if
                              subf.startswith(f) and subf != f and subf.endswith('/')]
                if not subfolders:
                    # 将该路径添加到 cwe_folders 列表中
                    cwe_folders.append(f)

    print("processing CWE folder..")
    for cwe_folder in cwe_folders:
        process_cwe_folder(zip_file, cwe_folder, storage_dir)


if __name__ == "__main__":
    main()
