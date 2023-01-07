import tkinter as tk
from tkinter import ttk


class MessageArea(ttk.Frame):

    def __init__(self, master, message):
        super().__init__(master, relief=tk.FLAT)

        message_area = ttk.Label(self, textvar=message)
        message_area.grid(padx=10)
