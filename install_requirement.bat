@echo off
cd InhaChat\InhaChatServer
python -m venv homepage1
call homepage1\Scripts\activate
cd homepage1
pip install -r ..\..\requirements.txt
pause