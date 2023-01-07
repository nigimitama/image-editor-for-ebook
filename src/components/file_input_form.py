from pathlib import Path
import tkinter as tk
from tkinter import ttk


class FileInputForm(ttk.LabelFrame):

    def __init__(self, master, input_path, output_path):
        super().__init__(master, text="処理対象の設定")
        message = tk.StringVar()
        message.set('処理したいファイルやフォルダをここにドラッグ&ドロップしてください')
        ttk.Label(self, ondrop=lambda event: self._callback(event, input_path, output_path, message),
                  textvar=message, padding=5).grid(padx=10, pady=5)

    def _callback(self, event, input_path, output_path, message):
        """ドロップされたときに実行されるcallback"""
        self._set_input_path(event, input_path)
        self._set_default_output_path(input_path, output_path)
        self._set_message(input_path, message)

    def _set_input_path(self, event, input_path):
        input_text: str = event.data
        texts = [text.replace('{', '').strip() for text in input_text.split('}') if text.strip() != '']

        if len(texts) == 1 and Path(texts[0]).is_dir():
            paths = Path(texts[0]).glob('*')
            paths = list(map(str, paths))

        # 受け取ったファイルパスを共有の変数に格納する
        input_path.set('\n'.join(paths))

    def _set_default_output_path(self, input_path, output_path):
        """入力されたファイルのパスをデフォルトの出力先にする"""
        paths: list[str] = input_path.get().split('\n')
        path = Path(paths[0])
        input_dir: Path = path if path.is_dir() else path.parent
        output_dir = input_dir.parent / f"{input_dir.name}_edited"
        output_path.set(output_dir)

    def _set_message(self, input_path, message):
        paths: list[str] = input_path.get().split('\n')
        file_names = '\n'.join(paths) if len(paths) < 15 else ('\n'.join(paths[:5]) + '\n...\n' + '\n'.join(paths[-5:-1]))
        message.set(f"{len(paths)} 個のファイルが見つかりました\n" + file_names)
