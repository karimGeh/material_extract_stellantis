echo "activating virtualenv : Start"
python .\.venv\Scripts\activate_this.py
echo "activating virtualenv : End"
echo "running main.py : Start"
.venv\Scripts\python.exe .\main.py
echo "Extract file generated"