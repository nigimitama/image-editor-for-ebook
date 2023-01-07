import traceback
from pathlib import Path
import tkinter as tk
from tkinter import ttk
from modules.editing import edit_image
from modules.size_calculaiton import calc_total_size, to_megabyte


class ExecuteButton(ttk.Frame):

    def __init__(self, master, input_path, output_path, message, settings):
        super().__init__(master, relief=tk.FLAT)
        ttk.Button(self, text="実行する", width=10,
                   command=lambda: self._process_image(input_path, output_path, message, settings)).grid(pady=10)

    def _process_image(self, input_path, output_path, message, settings):
        try:
            text: str = input_path.get()
            paths = [Path(path) for path in text.split('\n')]
            save_dir = Path(output_path.get())
            save_dir.mkdir(exist_ok=True)

            for path in paths:
                edit_image(input_path=path, save_dir=save_dir, gamma=settings["gamma"].get(), new_width=settings["width"].get())

            # リサイズ前後のファイルサイズを計測する
            output_paths = [save_dir / path.name for path in paths]
            size_before = to_megabyte(calc_total_size(paths))
            size_after = to_megabyte(calc_total_size(output_paths))

            message.set(f"""
処理が完了しました。
ファイルサイズ： {size_before:.1f}MB -> {size_after:.1f}MB ({size_after/size_before - 1:.1%})
""".strip())
        except Exception as e:
            message.set(f"エラーが発生しました - {e}\n\n{traceback.format_exc()}")
