import allpath
import ignore
import os
import shutil
import sys
import tkinter as tk
from tkinter import filedialog, scrolledtext


def get_parent_of_selected_folder():
    """弹出文件夹选择框，并返回所选文件夹的父级文件夹路径。"""
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    selected_dir = filedialog.askdirectory(title="请选择文件夹")
    root.destroy()
    if selected_dir:
        return os.path.dirname(os.path.abspath(selected_dir))
    return None


def collect_files(source_dir, source_name, target_name, script_dir):
    """收集 source_dir 下所有需要复制的文件，返回 (full_rel_path, short_name, target_sub_path) 列表。"""
    files_to_copy = []
    if not os.path.isdir(source_dir):
        return files_to_copy

    target_base = os.path.join(script_dir, target_name)

    for root, dirs, files in os.walk(source_dir):
        for file in files:
            source_file = os.path.join(root, file)
            rel_path = os.path.relpath(source_file, source_dir)
            # 统一使用正斜杠
            rel_path_fwd = rel_path.replace('\\', '/')
            full_rel_path = f"{source_name}/{rel_path_fwd}"

            # 检查是否需要复制（扩展名在允许列表中，且不在忽略列表中）
            if not ignore.is_need(full_rel_path):
                continue

            # 检查目标文件是否已存在
            target_sub_path = rel_path_fwd.replace(f"{source_name}/", "", 1) if rel_path_fwd.startswith(f"{source_name}/") else rel_path_fwd
            target_file = os.path.join(target_base, target_sub_path)
            if os.path.exists(target_file):
                continue

            files_to_copy.append((full_rel_path, file, target_sub_path))

    return files_to_copy


def show_confirmation_dialog(file_list, all_need, parent_path, script_dir):
    """弹出确认窗口，显示文件列表，用户确认后执行复制。"""
    dialog = tk.Tk()
    dialog.title("确认复制文件")
    dialog.geometry("600x500")

    total_files = len(file_list)
    tk.Label(dialog, text=f"共找到 {total_files} 个文件待复制：").pack(pady=5)

    text_area = scrolledtext.ScrolledText(dialog, width=70, height=25)
    text_area.pack(padx=10, pady=5)

    for _, short_name, _ in file_list:
        text_area.insert(tk.END, short_name + "\n")

    text_area.config(state="disabled")

    btn_frame = tk.Frame(dialog)
    btn_frame.pack(pady=10)

    def do_execute():
        dialog.destroy()
        execute_copy(file_list, all_need, parent_path, script_dir)

    def do_cancel():
        dialog.destroy()
        print("已取消复制。")

    tk.Button(btn_frame, text="执行复制", command=do_execute, width=15).pack(side=tk.LEFT, padx=10)
    tk.Button(btn_frame, text="不执行", command=do_cancel, width=15).pack(side=tk.LEFT, padx=10)

    dialog.mainloop()


def execute_copy(file_list, all_need, parent_path, script_dir):
    """执行实际的复制操作。"""
    copied = 0

    for source_name, target_name in all_need.items():
        source_dir = os.path.join(parent_path, source_name)

        if not os.path.isdir(source_dir):
            continue

        # 筛选出属于该 source_name 的文件
        relevant_files = [(fp, sn, sp) for fp, sn, sp in file_list if fp.startswith(f"{source_name}/")]

        for full_rel_path, _, target_sub_path in relevant_files:
            source_file = os.path.join(source_dir, target_sub_path.replace('/', '\\'))
            target_dir = os.path.join(script_dir, target_name)
            target_file = os.path.join(target_dir, target_sub_path)
            target_file_dir = os.path.dirname(target_file)

            if not os.path.exists(target_file_dir):
                os.makedirs(target_file_dir)

            if os.path.exists(source_file):
                shutil.copy2(source_file, target_file)
                copied += 1
                print(f"复制: {target_sub_path}")

    print(f"复制完成！共复制 {copied} 个文件。")


if __name__ == "__main__":
    parent_path = get_parent_of_selected_folder()
    if not parent_path:
        print("未选择任何文件夹。")
        sys.exit(1)

    print(f"选择的文件夹父级路径为: {parent_path}")

    all_need = allpath.getallpath(parent_path)
    print(f"找到的文件夹映射: {all_need}")

    if not all_need:
        print("未找到任何匹配的文件夹。")
        sys.exit(0)

    script_dir = os.path.dirname(os.path.abspath(__file__))

    # 收集所有需要复制的文件
    all_files = []
    for source_name, target_name in all_need.items():
        source_dir = os.path.join(parent_path, source_name)
        print(f"正在扫描: {source_dir}")
        files = collect_files(source_dir, source_name, target_name, script_dir)
        all_files.extend(files)
        print(f"  -> 找到 {len(files)} 个待复制文件")

    if not all_files:
        print("没有需要复制的文件。")
        sys.exit(0)

    print(f"总计 {len(all_files)} 个文件待复制")
    show_confirmation_dialog(all_files, all_need, parent_path, script_dir)