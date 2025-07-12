@echo off

call %0\..\.venv\Scripts\activate

:loop

rem Run python script
python data_fetch.py

rem Wait for 10800 seconds (3 hours)
timeout /t 10800

rem Loop back to start
goto loop