@echo off

cl.exe /O2 /D_USRDLL /D_WINDLL dllmain.c /MT /link /DLL /OUT:implantDLL.dll
