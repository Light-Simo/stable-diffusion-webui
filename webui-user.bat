@echo off

set PYTHON="C:\Users\Simo Benkirane\Documents\Projects\stable-diffusion-webui\venv\Scripts\python.exe"
set GIT=
set VENV_DIR=
set COMMANDLINE_ARGS="--share" "--enable-insecure-extension-access"

echo Current Directory: %CD%

call webui.bat


