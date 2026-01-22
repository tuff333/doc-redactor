@echo off
echo Installing Doc‑Redactor dependencies...

cd /d C:\projects\doc-redactor

echo Installing Python packages from requirements.txt...
python -m pip install -r backend\requirements.txt

echo Installing spaCy English model...
python -m spacy download en_core_web_sm

echo Installation complete.
pause