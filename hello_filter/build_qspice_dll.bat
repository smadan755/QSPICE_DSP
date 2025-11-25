@echo off
call "C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars32.bat"
cl /LD /O2 "%~1" /Fe:"%~dpn1.dll"
