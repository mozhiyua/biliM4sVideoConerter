import os
import shutil
import tkinter as tk
from tkinter import ttk, messagebox,filedialog
from tkinterdnd2 import DND_FILES, TkinterDnD


class M4SProcessorApp(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()
        self.title("M4S文件处理器")
        self.geometry("600x300")  

        self.target_folder = tk.StringVar()  # 存储用户选择的文件夹路径

        self.create_widgets()

    def create_widgets(self):
        # 拖放区域标签
        ttk.Label(self, text="拖放文件夹到此处 或 点击选择文件夹", font=("微软雅黑", 12)).pack(pady=10)

        # 拖放框
        self.drop_frame = ttk.Frame(self, relief="solid", borderwidth=2)
        self.drop_frame.pack(padx=20, pady=10, fill="both", expand=True)
        self.drop_frame.drop_target_register(DND_FILES)  # 注册拖放目标
        self.drop_frame.dnd_bind('<<Drop>>', self.on_drop)  # 绑定拖放事件
        ttk.Button(
            self.drop_frame,
            text="选择视频文件夹",
            command=self.choose_folder,
            width=15
        ).place(relx=0.5, rely=0.5, anchor="center")  # 居中放置选择按钮

        # 显示选中的路径
        ttk.Label(self, text="视频文件夹路径：").pack(pady=(10, 0), padx=20, anchor="w")
        self.path_entry = ttk.Entry(self, textvariable=self.target_folder, width=70)
        self.path_entry.pack(padx=20, fill="x")

        # 按钮
        ttk.Button(
            self,
            text="开始处理",
            command=self.start_processing,
            style="Accent.TButton"
        ).pack(pady=20)

        # 状态提示
        self.status_label = ttk.Label(self, text="", foreground="blue")
        self.status_label.pack(pady=5)

        # 样式
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Accent.TButton", foreground="white", background="#4CAF50", font=("微软雅黑", 10))

    def on_drop(self, event):
        """处理拖放文件夹事件（标准化路径格式）"""
        files = event.data.strip().split()
        folders = [os.path.normpath(f.strip('"')) for f in files]  # 关键修改
        if folders:
            self.target_folder.set(folders[0])
            self.status_label.config(text=f"已检测到文件夹：{folders[0]}")
        else:
            messagebox.showwarning("提示", "拖放的内容不是有效文件夹！")

    def choose_folder(self):
        folder = tk.filedialog.askdirectory(title="选择包含.m4s文件的文件夹")
        if folder:
            self.target_folder.set(folder)
            self.status_label.config(text=f"已选择文件夹：{folder}")

    def start_processing(self):
        """开始处理文件"""
        target_dir = self.target_folder.get()
        if not target_dir or not os.path.isdir(target_dir):
            messagebox.showerror("错误", "请选择有效的文件夹路径！")
            return

        try:
            self.status_label.config(text="处理中...")
            self.update()

            current_dir = os.path.normpath(target_dir)  # 标准化目标文件夹路径
            # 获取.m4s文件并拼接完整路径
            m4s_files = [
                os.path.join(current_dir, f)  # 直接拼接完整路径
                for f in os.listdir(current_dir)
                if f.lower().endswith('.m4s')
            ]

            if len(m4s_files) != 2:
                messagebox.showerror("错误", f"当前文件夹下需要恰好两个.m4s文件！当前找到 {len(m4s_files)} 个")
                return

            # 文件大小排序
            m4s_files.sort(key=lambda x: os.path.getsize(x))  # 直接用完整路径计算大小
            small_file = m4s_files[0]
            large_file = m4s_files[1]

            ending_dir = os.path.join(current_dir, "ending")
            ending_dir = os.path.normpath(ending_dir)  # 确保格式正确
            os.makedirs(ending_dir, exist_ok=True)
            self.status_label.config(text=f"已创建/检查ending文件夹：{ending_dir}")

            # 处理小文件
            small_dest = os.path.join(ending_dir, "audio.mp3")
            shutil.copy2(small_file, small_dest)  # small_file已是完整路径
            if not self.delete_first_n_bytes(small_dest, n=9):
                raise RuntimeError("小文件处理失败")
            self.status_label.config(text="文件处理完成！")

            # 处理大文件
            large_dest = os.path.join(ending_dir, "video.mp4")
            shutil.copy2(large_file, large_dest)  # large_file已是完整路径
            if not self.delete_first_n_bytes(large_dest, n=9):
                raise RuntimeError("大文件处理失败")
            self.status_label.config(text="文件处理完成！")

            messagebox.showinfo("成功", f"所有文件处理完成！\n处理后的文件保存在：{ending_dir}")
            self.status_label.config(text="")

        except Exception as e:
            import traceback
            error_msg = traceback.format_exc()
            messagebox.showerror("处理失败", f"错误详情：\n{error_msg}")
            self.status_label.config(text=f"错误：{error_msg}")

    @staticmethod
    def delete_first_n_bytes(filename, n=9):
        try:
            if not os.path.isfile(filename):
                raise FileNotFoundError(f"文件 '{filename}' 不存在")

            original_size = os.path.getsize(filename)
            if original_size < n:
                raise ValueError(f"文件大小（{original_size}字节）小于所需的字节数（{n}）")

            with open(filename, "rb") as f:
                content = f.read()

            new_content = content[n:]

            with open(filename, "wb") as f:
                f.write(new_content)

            new_size = os.path.getsize(filename)
            expected_size = original_size - n
            if new_size != expected_size:
                raise RuntimeError(f"文件大小异常（原：{original_size} → 新：{new_size}）")

            return True

        except Exception as e:
            raise e  # 向上抛出异常由start_processing处理


if __name__ == "__main__":
    app = M4SProcessorApp()
    app.mainloop()
