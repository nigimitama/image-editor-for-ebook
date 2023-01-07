import tkinter as tk
from tkinter import ttk
from tkinter import filedialog


class OutputDirForm(ttk.LabelFrame):

    def __init__(self, master, output_path):
        super().__init__(master, text="出力先の設定")

        frame_1 = ttk.Frame(self)
        ttk.Label(frame_1, text="出力先:").grid(column=0, row=0)
        ttk.Label(frame_1, textvariable=output_path).grid(column=1, row=0)
        frame_1.grid(padx=10, pady=5, sticky=(tk.W, tk.E))

        frame_2 = ttk.Frame(self)
        ttk.Button(frame_2, text="別のフォルダを選択する", command=lambda: self._ask_dir(output_path)).grid(padx=5)
        frame_2.grid(padx=10, pady=5, sticky=(tk.W, tk.E))

    def _ask_dir(self, output_path):
        output_dir: str = filedialog.askdirectory()
        if output_dir:
            output_path.set(output_dir)
