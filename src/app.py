import traceback
from pathlib import Path
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import tkinterDnD  # python-tkdnd package
from edit_image import edit_image


class Variables:

    def __init__(self) -> None:
        self.input_path = tk.StringVar()
        self.output_path = tk.StringVar(value=str(Path(Path().absolute().root).absolute()))
        self.message = tk.StringVar()


class FileInputForm(ttk.LabelFrame):

    def __init__(self, master, variables: Variables):
        super().__init__(master, text="処理対象の設定")
        self.variables = variables

        self.message_ = tk.StringVar()
        self.message_.set('処理したいファイルやフォルダをここにドラッグ&ドロップしてください')

        ttk.Label(self, ondrop=self._receive_filepaths, textvar=self.message_, padding=5).grid(padx=10, pady=5)

    def _set_default_output_path(self):
        """入力されたファイルのパスをデフォルトの出力先にする"""
        paths: list[str] = self.variables.input_path.get().split('\n')
        path = Path(paths[0])
        input_dir: Path = path if path.is_dir() else path.parent
        output_dir = input_dir.parent / f"{input_dir.name}_edited"
        self.variables.output_path.set(output_dir)

    def _receive_filepaths(self, event):
        """ドロップされたときに実行されるcallback"""
        input_text: str = event.data
        texts = [text.replace('{', '').strip() for text in input_text.split('}') if text.strip() != '']

        if len(texts) == 1 and Path(texts[0]).is_dir():
            paths = Path(texts[0]).glob('*')
            texts = list(map(str, paths))

        # 受け取ったファイルパスを共有の変数に格納する
        self.variables.input_path.set('\n'.join(texts))
        self._set_default_output_path()

        # 表示の更新
        file_names = '\n'.join(texts) if len(texts) < 15 else ('\n'.join(texts[:5]) + '\n...\n' + '\n'.join(texts[-5:-1]))
        self.message_.set(f"{len(texts)} 個のファイルが見つかりました\n" + file_names)


class OutputDirForm(ttk.LabelFrame):

    def __init__(self, master, variables: Variables):
        super().__init__(master, text="出力先の設定")
        self.variables = variables

        frame_1 = ttk.Frame(self)
        ttk.Label(frame_1, text="出力先:").grid(column=0, row=0)
        ttk.Label(frame_1, textvariable=self.variables.output_path).grid(column=1, row=0)
        frame_1.grid(padx=10, pady=5)

        frame_2 = ttk.Frame(self)
        ttk.Button(frame_2, text="フォルダを選択する", command=self._ask_dir).grid(column=1, row=1, padx=5)
        frame_2.grid(padx=10, pady=5)


    def _ask_dir(self):
        output_dir: str = filedialog.askdirectory()
        if output_dir:
            self.variables.output_path.set(output_dir)


class MessageArea(ttk.Frame):

    def __init__(self, master, variables: Variables):
        super().__init__(master, relief=tk.FLAT)

        message_area = ttk.Label(self, textvar=variables.message)
        message_area.grid()


class ExecuteButton(ttk.Frame):

    def __init__(self, master, variables: Variables):
        super().__init__(master, relief=tk.FLAT)
        self.variables = variables

        ttk.Button(self, text="実行する", width=10, command=self._process_image).grid(column=0, row=0, pady=10)

    def _process_image(self):
        try:
            texts: str = self.variables.input_path.get()
            paths = [Path(path) for path in texts.split('\n')]
            save_dir = Path(self.variables.output_path.get())
            save_dir.mkdir(exist_ok=True)

            for path in paths:
                edit_image(input_path=path, save_dir=save_dir)

            self.variables.message.set("完了しました。")
        except Exception as e:
            self.variables.message.set(f"ERROR ({e})\n\n{traceback.format_exc()}")


class Application:

    def __init__(self):
        self.master = tkinterDnD.Tk()
        self.master.title("Image Processor")

        self.variables = Variables()

        self.input_form = FileInputForm(self.master, self.variables)
        self.input_form.grid(column=0, row=0, padx=10, pady=10)

        self.output_dir_form = OutputDirForm(self.master, self.variables)
        self.output_dir_form.grid(column=0, row=1, padx=10, pady=10)

        self.message_area = MessageArea(self.master, self.variables)
        self.message_area.grid(column=0, row=2)

        self.button_frame = ExecuteButton(self.master, self.variables)
        self.button_frame.grid(column=0, row=3)

        self.master.columnconfigure(0)
        self.master.columnconfigure(1)
        self.master.rowconfigure(0)
        self.master.rowconfigure(1)
        self.master.rowconfigure(2)
        self.master.rowconfigure(3)

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
