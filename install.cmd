echo "installing virtualenv : Start"
pip install virtualenv
echo "installing virtualenv : End"
echo "creating virtualenv : Start"
python -m virtualenv .venv
echo "creating virtualenv : End"
echo "activating virtualenv : Start"
python .\.venv\Scripts\activate_this.py
echo "activating virtualenv : End"
echo "installing requirements : Start"
.venv\Scripts\pip.exe install -r requirements.txt
echo "installing requirements : End"
echo ""