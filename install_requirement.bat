@echo off
py -m venv Server
call Server\Scripts\activate
cd Server
pip install -r ..\requirements.txt
pause