@echo off
:: Устанавливаем кодировку UTF-8 для текущего окна монитора
chcp 65001 >nul
title Airbnb Clone Absolute Secure Stack
cls

:: Execute the secure python launcher
call .venv\Scripts\activate
python secure_launcher.py

if errorlevel 1 pause
