import traceback
from pathlib import Path
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import tkinterDnD  # python-tkdnd package
from edit_image import edit_image


class FileInputForm(ttk.LabelFrame):

    def __init__(self, master):
        super().__init__(master, text="処理対象の設定")

        self.message_ = tk.StringVar()
        self.message_.set('処理したいファイルやフォルダをここにドラッグ&ドロップしてください')

        self.paths_ = tk.StringVar()

        ttk.Label(self, ondrop=self._receive_filepaths, textvar=self.message_, padding=5).grid(padx=10, pady=5)

    def _receive_filepaths(self, event):
        """ドロップされたときに実行されるcallback"""
        input_text: str = event.data
        texts = [text.replace('{', '').strip() for text in input_text.split('}') if text.strip() != '']

        if len(texts) == 1 and Path(texts[0]).is_dir():
            paths = Path(texts[0]).glob('*')
            texts = list(map(str, paths))

        # 受け取ったファイルパスを共有の変数に格納する
        self.paths_.set('\n'.join(texts))

        # 表示の更新
        file_names = '\n'.join(texts) if len(texts) < 15 else ('\n'.join(texts[:5]) + '\n...\n' + '\n'.join(texts[-5:-1]))
        self.message_.set(f"{len(texts)} 個のファイルが見つかりました\n" + file_names)


class OutputDirForm(ttk.LabelFrame):

    def __init__(self, master, input_form: FileInputForm):
        super().__init__(master, text="出力先の設定")

        self.value = tk.StringVar()
        root_path = Path(Path().absolute().root).absolute()
        self.value.set(str(root_path))

        frame_1 = ttk.Frame(self)
        ttk.Label(frame_1, text="出力先:").grid(column=0, row=0)
        ttk.Label(frame_1, textvariable=self.value).grid(column=1, row=0)
        frame_1.grid(padx=10, pady=5)

        frame_2 = ttk.Frame(self)
        self.input_form = input_form
        ttk.Button(frame_2, text="自動設定", command=self._create_dir).grid(column=0, row=1, padx=5)
        ttk.Button(frame_2, text="フォルダを選択する", command=self._ask_dir).grid(column=1, row=1, padx=5)
        frame_2.grid(padx=10, pady=5)

    def _create_dir(self):
        paths: list[str] = self.input_form.paths_.get().split('\n')
        path = Path(paths[0])
        input_dir: Path = path if path.is_dir() else path.parent
        output_dir = input_dir.parent / f"{input_dir.name}_edited"
        self.value.set(output_dir)

    def _ask_dir(self):
        output_dir: str = filedialog.askdirectory()
        if output_dir:
            self.value.set(output_dir)


class MessageArea(ttk.Frame):

    def __init__(self, master):
        super().__init__(master, relief=tk.FLAT)

        self.value = tk.StringVar()
        self.value.set('')

        message_area = ttk.Label(self, textvar=self.value)
        message_area.grid()


class ExecuteButton(ttk.Frame):

    def __init__(self, master, input_form, output_dir_form, message_area):
        super().__init__(master, relief=tk.FLAT)

        self.input_form = input_form
        self.output_dir_form = output_dir_form
        self.message_area = message_area

        ttk.Button(self, text="実行する", width=10, command=self._process_image).grid(column=0, row=0, pady=10)

    def _process_image(self):
        try:
            texts: str = self.input_form.paths_.get()
            paths = [Path(path) for path in texts.split('\n')]
            save_dir = Path(self.output_dir_form.value.get())
            save_dir.mkdir(exist_ok=True)

            for path in paths:
                edit_image(input_path=path, save_dir=save_dir)

            self.message_area.value.set("完了しました。")
        except Exception as e:
            self.message_area.value.set(f"ERROR ({e})\n\n{traceback.format_exc()}")


class Application:

    def __init__(self):
        self.master = tkinterDnD.Tk()
        self.master.title("Image Processor")

        self.input_form = FileInputForm(self.master)
        self.input_form.grid(column=0, row=0, padx=10, pady=10)

        self.output_dir_form = OutputDirForm(self.master, self.input_form)
        self.output_dir_form.grid(column=0, row=1, padx=10, pady=10)

        self.message_area = MessageArea(self.master)
        self.message_area.grid(column=0, row=2)

        self.button_frame = ExecuteButton(self.master, self.input_form, self.output_dir_form, self.message_area)
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
    app = Application()
    app.run()
