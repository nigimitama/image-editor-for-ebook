import traceback
from pathlib import Path
import tkinter as tk
from tkinter import ttk
from modules.editing import edit_image
from modules.size_calculaiton import calc_total_size, to_megabyte


class ExecuteButton(ttk.Frame):

    def __init__(self, master, input_path: tk.StringVar, output_path: tk.StringVar, message: tk.StringVar, settings: dict):
        super().__init__(master, relief=tk.FLAT)
        self.button = tk.Button(self, text="実行する", width=10, command=lambda: self._execute(input_path, output_path, message, settings))
        self.button.grid(pady=10)

    def _execute(self, input_path: tk.StringVar, output_path: tk.StringVar, message: tk.StringVar, settings: dict):
        try:
            self.button["state"] = tk.DISABLED
            message.set("処理中...")

            if self._is_valid_input(input_path, output_path, message, settings):
                # buttonのstateやmessageの変更を反映させるためafterで非同期にする
                wait_time_ms = 100
                self.master.after(wait_time_ms, lambda: self._process_image(input_path, output_path, message, settings))
            else:
                self.button["state"] = tk.NORMAL

        except Exception as e:
            message.set(f"エラーが発生しました - {e}\n\n{traceback.format_exc()}")

    def _process_image(self, input_path: tk.StringVar, output_path: tk.StringVar, message: tk.StringVar, settings: dict):
        text: str = input_path.get()
        paths = [Path(path) for path in text.split('\n')]
        save_dir = Path(output_path.get())
        save_dir.mkdir(exist_ok=True)

        for path in paths:
            reversed_enum = {value: key for (key, value) in settings["gamma_target_enum"].items()}
            edit_image(
                input_path=path,
                save_dir=save_dir,
                gamma=settings["gamma"].get(),
                gamma_target=reversed_enum[settings["gamma_target"].get()],
                new_width=settings["width"].get()
            )

        # リサイズ前後のファイルサイズを計測する
        output_paths = [save_dir / path.name for path in paths]
        size_before = to_megabyte(calc_total_size(paths))
        size_after = to_megabyte(calc_total_size(output_paths))

        message.set(f"""
処理が完了しました。
ファイルサイズ： {size_before:.1f}MB -> {size_after:.1f}MB ({size_after/size_before - 1:.1%})
""".strip())

        self.button["state"] = tk.NORMAL

    def _is_valid_input(self, input_path: tk.StringVar, output_path: tk.StringVar, message: tk.StringVar, settings: dict) -> bool:
        """ユーザーの入力値を検証する"""
        # NOTE: tk.IntVarとtk.DoubleVarはget()した時点でTclErrorになるのでassertできず
        try:
            assert input_path.get() != "", "処理対象の画像ファイルを選択してください"
            assert output_path.get() != "", "出力先のフォルダを選択してください"
            return True
        except AssertionError as e:
            message.set(f"{e}")
            return False
