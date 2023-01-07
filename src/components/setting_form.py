import tkinter as tk
from tkinter import ttk


class SettingForm(ttk.LabelFrame):

    def __init__(self, master, settings):
        super().__init__(master, text="処理の設定")

        frame_1 = ttk.Frame(self)
        ttk.Label(frame_1, text="ガンマ補正").grid(column=0, row=0)
        tk.Entry(frame_1, textvariable=settings["gamma"], width=5).grid(column=1, row=0)
        frame_1.grid(padx=10, pady=5)

        frame_2 = ttk.Frame(self)
        ttk.Label(frame_2, text="横幅 (px)").grid(column=0, row=0)
        tk.Entry(frame_2, textvariable=settings["width"], width=5).grid(column=1, row=0)
        frame_2.grid(padx=10, pady=5)
