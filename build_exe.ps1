# --------------------------
# Windows用のexeファイルの生成
# --------------------------

# NOTE: --collect-data tkinterDnD をつけないとexe起動時にtkdndファイルがなくてエラーになる
pyinstaller --name image_editor --onefile --collect-data tkinterDnD --noconsole src/app.py
