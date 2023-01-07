import traceback
from pathlib import Path
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import tkinterDnD  # python-tkdnd package
from edit_image import edit_image


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



class OutputDirForm(ttk.LabelFrame):

    def __init__(self, master, output_path):
        super().__init__(master, text="出力先の設定")

        frame_1 = ttk.Frame(self)
        ttk.Label(frame_1, text="出力先:").grid(column=0, row=0)
        ttk.Label(frame_1, textvariable=output_path).grid(column=1, row=0)
        frame_1.grid(padx=10, pady=5)

        frame_2 = ttk.Frame(self)
        ttk.Button(frame_2, text="別のフォルダを選択する", command=lambda: self._ask_dir(output_path)).grid(padx=5)
        frame_2.grid(padx=10, pady=5)

    def _ask_dir(self, output_path):
        output_dir: str = filedialog.askdirectory()
        if output_dir:
            output_path.set(output_dir)


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


class MessageArea(ttk.Frame):

    def __init__(self, master, message):
        super().__init__(master, relief=tk.FLAT)

        message_area = ttk.Label(self, textvar=message)
        message_area.grid(padx=10)


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

            message.set("完了しました。")
        except Exception as e:
            message.set(f"エラーが発生しました - {e}\n\n{traceback.format_exc()}")


class Application:

    def __init__(self):
        self.master = tkinterDnD.Tk()
        self.master.title("Image Processor")

        # コンポーネント間で共有する変数たち
        input_path = tk.StringVar()
        output_path = tk.StringVar(value=str(Path(Path().absolute().root).absolute()))
        message = tk.StringVar()
        settings = {
            "gamma": tk.DoubleVar(value=1.6),
            "width": tk.IntVar(value=1080),
        }

        # コンポーネントたち
        # MEMO: sticky=(tk.W, tk.E) で左右めいっぱいに伸ばす
        FileInputForm(self.master, input_path, output_path).grid(column=0, row=0, padx=10, pady=5, sticky=(tk.W, tk.E))
        OutputDirForm(self.master, output_path).grid(column=0, row=1, padx=10, pady=5, sticky=(tk.W, tk.E))
        SettingForm(self.master, settings).grid(column=0, row=2, padx=10, pady=5, ipadx=20, sticky=(tk.W, tk.E))
        MessageArea(self.master, message).grid(column=0, row=3, sticky=tk.W)
        ExecuteButton(self.master, input_path, output_path, message, settings).grid(column=0, row=4)

        # ウィンドウを引き伸ばしたときに各コンポーネントも引き伸ばされるよう設定する
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.master.rowconfigure(1, weight=1)
        self.master.rowconfigure(2, weight=1)
        self.master.rowconfigure(3, weight=1)
        self.master.rowconfigure(4, weight=1)

    def run(self):
        self.master.mainloop()


if __name__ == "__main__":
    try:
        app = Application()
        app.run()
    except Exception as e:
        import logging
        logger = logging.getLogger('app')
        logger.addHandler(logging.FileHandler('error.log'))
        logger.error(f"ERROR - {e}", exc_info=True)
