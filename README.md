# image-editor-for-ebook

電子書籍の自作のための簡単な画像処理（ガンマ補正・リサイズ）を行うWindows用 GUIアプリ

![image-20230107154633566](README.assets/image-20230107154633566.png)



## 使用方法

![image-editor](README.assets/image-editor.gif)

1. [Releases](https://github.com/nigimitama/image-editor-for-ebook/releases)から.exeファイルをダウンロードして実行してください
2. 処理したい画像やフォルダをドラッグ&ドロップしてください
3. 出力先を指定したい場合は設定してください
   - デフォルトでは入力元のディレクトリに`_edited`の接尾辞を付け足したディレクトリを新規作成してそこに出力します。
4. 必要に応じてガンマ補正や横幅の値を設定してください
5. （もし予期せぬエラーが起きた場合は.exeファイルと同じディレクトリに`error.log`というログファイルが生成されます。エラー報告時にお使いください）
