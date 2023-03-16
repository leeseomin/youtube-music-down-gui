import os
import sys
import subprocess
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

def check_ytdlp_installation():
    try:
        subprocess.run(["yt-dlp", "--version"], check=True, text=True, capture_output=True)
    except FileNotFoundError:
        messagebox.showinfo("설치 필요", "yt-dlp를 설치해야 합니다. 설치를 시작합니다.")
        if sys.platform.startswith("win"):
            subprocess.run(["pip", "install", "yt-dlp"], capture_output=True)
        elif sys.platform.startswith("linux") or sys.platform.startswith("darwin"):
            subprocess.run(["pip3", "install", "yt-dlp"], capture_output=True)
        else:
            messagebox.showerror("오류", "지원하지 않는 운영 체제입니다.")
            sys.exit(1)

def update_progress(progress):
    progress_var.set(progress)
    root.update_idletasks()

def download_audio():
    url = url_entry.get()
    output_path = path_entry.get()

    if not url or not output_path:
        messagebox.showerror("오류", "모든 필드를 작성해 주세요.")
        return

    command = ["yt-dlp", "-f", "bestaudio[ext=m4a]", "--extract-audio", "--audio-format", "mp3", "--add-metadata", "--embed-thumbnail", "-o", f"{output_path}/%(title)s.%(ext)s", url, "--newline"]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)

    for line in process.stdout:
        if "download" in line and "%" in line:
            progress = line.strip().split()[1].strip("%")
            update_progress(progress)

    process.wait()
    update_progress(100)
    messagebox.showinfo("완료", "다운로드가 완료되었습니다.")

def browse_directory():
    output_path = filedialog.askdirectory()
    path_entry.delete(0, tk.END)
    path_entry.insert(0, output_path)

check_ytdlp_installation()

root = tk.Tk()
root.title("YouTube Audio Downloader")

frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

url_label = ttk.Label(frame, text="YouTube URL:")
url_label.grid(row=0, column=0, sticky=tk.W, pady=5)

url_entry = ttk.Entry(frame, width=50)
url_entry.grid(row=0, column=1, sticky=tk.W, pady=5)

path_label = ttk.Label(frame, text="저장 위치:")
path_label.grid(row=1, column=0, sticky=tk.W, pady=5)

path_entry = ttk.Entry(frame, width=50)
path_entry.grid(row=1, column=1, sticky=tk.W, pady=5)

browse_button = ttk.Button(frame, text="찾아보기", command=browse_directory)
browse_button.grid(row=1, column=2, sticky=tk.W, padx=5, pady=5)

download_button = ttk.Button(frame, text="다운로드", command=download_audio)
download_button.grid(row=2, column=1, columnspan=2, pady=10)

progress_var = tk.StringVar()
progress_label = ttk.Label(frame, textvariable=progress_var)
progress_label.grid(row=3, column=1, sticky=tk.W, pady=5)

root.mainloop()
