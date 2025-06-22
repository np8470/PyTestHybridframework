pytest -s -v -m "regression" --html=Reports\report.html testCases/ --browser chrome
REM pytest -s -v -m "system" --html=Reports\report.html testCases/ --browser firefox
REM pytest -s -v -m "regression or system" --html=Reports\report.html testCases/ --browser chrome
REM pytest -s -v -m "system and regression" --html=Reports\report.html testCases/ --browser firefox