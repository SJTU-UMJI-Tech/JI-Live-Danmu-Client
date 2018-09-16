# JI-Live-Danmu-Client

## Usage:

1. Set secret key in Danmu/config.py
```bash
vim Danmu/config.py
```
2. Run Live Danmu(Optional:Set server url)
```bash
LiteDanmu.py [-h] [-serverurl SERVERURL] [-sk SecretKey]
```

## Build:

1. Install pyinstaller
```bash
pip install pyinstaller
```
2. Build
```bash
pyinstaller .\LiteDanmu.py
mv dist/LiteDanmu/PyQt5/Qt/plugins/platforms/ dist/LiteDanmu
```
3. Run
```bash
dist/LiteDanmu/LiteDanmu.exe [-h] [-serverurl SERVERURL] [-sk SecretKey]
```
