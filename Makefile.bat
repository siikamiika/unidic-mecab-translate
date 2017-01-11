@echo off
REM  
REM  Makefile.bat for UniDic-mecab-2.1.1
REM
@echo Makefile.bat for UniDic-mecab-2.1.1

mkdir ..\dic\unidic
if errorlevel 1 goto ERROREXIT

@echo mecab-dict-index...
..\bin\mecab-dict-index -d . -o ..\dic\unidic -f utf8 -t utf8
if errorlevel 1 goto ERROREXIT

@echo installing...
copy dicrc ..\dic\unidic

@echo mecab dictionary compiled successfully.
goto LAST

:ERROREXIT
@echo cannot make mecab dictionary.
@echo installation halted.
pause

:LAST
@echo on
