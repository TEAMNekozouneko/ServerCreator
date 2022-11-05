# Server Creator
サーバーを簡単に生成するツールです。

## ビルド

### 推奨環境:
**Windows**: 10+  
**Python:** 3.7+

1. レポジトリをクローンする
```powershell
> git clone https://github.com/TeamNekozouneko/ServerCreator.git

> cd ServerCreator
```
2. 必要なライブラリをインストール
```powershell
> python -m pip install -r requirements.txt
```
3. ビルド
> dist/ ディレクトリ直下に `servercreator.exe` が生成されます。
```powershell
> pyinstaller servercreator.py --onefile
```