@echo off
REM --- Installa i pacchetti richiesti (solo se non sono già installati) ---
pip install -r requirements.txt

REM --- Avvia il programma Python ---
python main.py

REM --- Mantieni la finestra aperta dopo l'esecuzione ---
pause