@echo off
REM make a folder for PokeScraper assets
mkdir PokeScraper_Data

REM install the packages
echo Installing required Python packages...
python -m pip install requests
python -m pip install colorama

REM run the scraper
echo Running PokeScraper...
python pokescraper.py

REM Finished
echo Script ended
pause
