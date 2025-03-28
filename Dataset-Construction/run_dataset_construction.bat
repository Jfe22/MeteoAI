@echo off

call %0\..\venv\Scripts\activate

rem Run python script
python dataset_construction.py

pause