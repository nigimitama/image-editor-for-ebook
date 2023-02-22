import tkinter as tk
from tkinter import ttk


class SettingForm(ttk.LabelFrame):

    def __init__(self, master, settings: dict[str, tk.Variable]):
        super().__init__(master, text="処理の設定")

        # gamma correction
        frame_gamma = ttk.Frame(self)
        ttk.Label(frame_gamma, text="ガンマ補正：").grid(column=0, row=0, padx=5)
        tk.Entry(frame_gamma, textvariable=settings["gamma"], width=5).grid(column=1, row=0)
        frame_gamma.grid(column=0, row=0, padx=10, pady=5, sticky=tk.W)

        frame_gamma_target = ttk.Frame(self)
        ttk.Label(frame_gamma_target, text="ガンマ補正の対象：").grid(column=0, row=0, rowspan=2)
        enum = settings["gamma_target_enum"]
        tk.Radiobutton(frame_gamma_target, text="全ページ", value=enum["all"], variable=settings["gamma_target"]).grid(column=1, row=0, sticky=tk.W)
        tk.Radiobutton(frame_gamma_target, text="モノクロのページだけ", value=enum["gray"], variable=settings["gamma_target"]).grid(column=1, row=1, sticky=tk.W)
        frame_gamma_target.grid(column=1, row=0, padx=10, pady=5)

        # resizing
        frame_width = ttk.Frame(self)
        ttk.Label(frame_width, text="横幅 (px)：").grid(column=0, row=0, padx=5)
        tk.Entry(frame_width, textvariable=settings["width"], width=5).grid(column=1, row=0)
        frame_width.grid(padx=10, pady=5, sticky=tk.W)

        # jpg quality
        frame_quality = ttk.Frame(self)
        ttk.Label(frame_quality, text="保存するjpgの品質：").grid(column=0, row=0, padx=5)
        tk.Entry(frame_quality, textvariable=settings["quality"], width=5).grid(column=1, row=0)
        frame_quality.grid(padx=10, pady=5, sticky=tk.W)


