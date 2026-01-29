# ReconMaster Desktop (EXE) Build

This project runs a local FastAPI UI and wraps it into a native desktop window using **pywebview**.
No browser tab is required for end users.

## 1) Install (Dev)
- Create a virtual environment
- Install `requirements.txt`

## 2) Run (Dev)
- Linux/Kali:
  - `python3 Desktop/desktop_app.py`

## 3) Build EXE (Windows)
Use PyInstaller on Windows:
- Install requirements
- `pip install pyinstaller`
- `pyinstaller --noconsole --onefile Desktop/desktop_app.py --name ReconMaster`

The resulting executable will appear in `dist/ReconMaster.exe`.

## 4) Build Linux Binary (optional)
- `pyinstaller --onefile Desktop/desktop_app.py --name reconmaster`

Note: pywebview on Linux needs a GUI backend (GTK/Qt). For Kali, installing the Qt backend is typically the smoothest option.
