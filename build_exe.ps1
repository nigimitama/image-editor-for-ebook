# --------------------------
# Windows用のexeファイルの生成
# --------------------------

# NOTE: --collect-data tkinterDnD をつけないとexe起動時にtkdndファイルがなくてエラーになる
pyinstaller --onefile --collect-data tkinterDnD --noconsole src/app.py
