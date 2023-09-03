import os
import sys
import re
import tkinter as tk
from tkinter import ttk, filedialog, messagebox


def convert_lrc_to_srt():
    lrc_file = lrc_file_entry.get()
    srt_dir = srt_dir_entry.get()

    if not lrc_file:
        messagebox.showerror("Error", "Please select an LRC file.")
        return

    if not os.path.exists(lrc_file):
        messagebox.showerror("Error", "The specified LRC file does not exist.")
        return

    if not srt_dir:
        srt_dir = os.path.dirname(lrc_file)

    lrc_name = os.path.basename(lrc_file)
    srt_name = os.path.splitext(lrc_name)[0] + '.srt'
    srt_file = os.path.join(srt_dir, srt_name)

    lyrics = {}
    start_time = 0
    with open(lrc_file, 'r', encoding='utf-8') as f:
        for line in f:
            match = re.match(r'\[(\d+):(\d+).(\d+)\](.*)', line)
            if match:
                min, sec, ms = match.group(1, 2, 3)
                text = match.group(4)
                srt_timestamp = f'00:{min}:{sec},{ms}'
                if srt_timestamp in lyrics:
                    lyrics[srt_timestamp].append(text)
                else:
                    lyrics[srt_timestamp] = [text]

    with open(srt_file, 'w', encoding='utf-8') as f:
        index = 1
        last_time_stamp = None
        last_text = None
        for timestamp in sorted(lyrics.keys()):
            if(last_time_stamp == None):
                last_time_stamp = timestamp
                last_text = '\n'.join(lyrics[timestamp])
                continue
            text = '\n'.join(lyrics[timestamp])
            f.write('{}\n{} --> {}\n{}\n\n'.format(index,
                    last_time_stamp, timestamp, last_text))
            index += 1
            last_time_stamp = timestamp
            last_text = text

    messagebox.showinfo(
        "Success", f"Conversion complete. SRT file saved as {srt_file}")


root = tk.Tk()
root.title("LRC to SRT Converter")

# 使用ttk主题创建按钮和标签
style = ttk.Style()
style.configure("TButton", padding=10)
style.configure("TLabel", padding=5, font=("Helvetica", 12))

# 创建标签和输入框用于选择LRC文件
lrc_label = ttk.Label(root, text="选择LRC文件:")
lrc_label.grid(row=0, column=0, padx=10, pady=5)
lrc_file_entry = ttk.Entry(root)
lrc_file_entry.grid(row=0, column=1, padx=10, pady=5)

lrc_file_button = ttk.Button(root, text="浏览", command=lambda: lrc_file_entry.insert(
    0, filedialog.askopenfilename()))
lrc_file_button.grid(row=0, column=2, padx=10, pady=5)

# 创建标签和输入框用于选择SRT文件的输出目录
srt_label = ttk.Label(root, text="保存目录（可选）:")
srt_label.grid(row=1, column=0, padx=10, pady=5)
srt_dir_entry = ttk.Entry(root)
srt_dir_entry.grid(row=1, column=1, padx=10, pady=5)

srt_dir_button = ttk.Button(
    root, text="浏览", command=lambda: srt_dir_entry.insert(0, filedialog.askdirectory()))
srt_dir_button.grid(row=1, column=2, padx=10, pady=5)

# 创建转换按钮
convert_button = ttk.Button(root, text="Convert", command=convert_lrc_to_srt)
convert_button.grid(row=2, column=0, columnspan=3, pady=10)

root.mainloop()
