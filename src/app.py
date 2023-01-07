from pathlib import Path
import tkinter as tk
import tkinterDnD  # python-tkdnd package
from components.file_input_form import FileInputForm
from components.output_dir_form import OutputDirForm
from components.setting_form import SettingForm
from components.message_area import MessageArea
from components.execute_button import ExecuteButton


class Application:

    def __init__(self):
        self.master = tkinterDnD.Tk()
        self.master.title("Image Editor for eBook")

        # コンポーネント（tkの用語でいうとウィジェット）間で共有する変数たち
        input_path = tk.StringVar()
        output_path = tk.StringVar(value=str(Path(Path().absolute().root).absolute()))
        message = tk.StringVar()
        settings = {
            "gamma": tk.DoubleVar(value=1.6),
            "width": tk.IntVar(value=1080),
            "gamma_target": tk.IntVar(value=1),
            "gamma_target_enum": { "all": 0, "gray": 1 }
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
