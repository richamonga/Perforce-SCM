@echo off 

if EXIST "BuildAction" (
echo Error: Folder exist
) else (
MKDIR "BuildAction"
echo Folder created
)