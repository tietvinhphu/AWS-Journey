@echo off
chcp 65001 > nul
title AWS Journey - Auto Sync & Commit

echo ========================================================
echo       ☁️  AWS JOURNEY - AUTOMATION TOOL ☁️
echo ========================================================
echo.

:: 1. Chạy script đồng bộ
echo [Process 1/4] Dang dong bo README... (Running sync script)
python "scripts/sync_readme.py"
if %errorlevel% neq 0 (
    echo [EROR] Script gap loi! Hay kiem tra lai code python.
    pause
    exit /b
)
echo [OK] Da cap nhat README.md va them Back-to-top.
echo.

:: 2. Thêm file vào Git
echo [Process 2/4] Dang thuc hien 'git add .' ...
git add .
echo [OK] Da add file.
echo.

:: 3. Hiển thị trạng thái
echo [Process 3/4] Trang thai thay doi (Git Status):
echo --------------------------------------------------------
git status --short
echo --------------------------------------------------------
echo.

:: 4. Commit và Push
set /p msg="Nhap noi dung Commit (De trong de huy): "
if "%msg%"=="" (
    echo Da huy Commit.
    pause
    exit /b
)

git commit -m "%msg%"
echo.
echo [Process 4/4] Dang day code len Github (Git Push)...
git push

echo.
echo ========================================================
echo       ✅  HOAN TAT QUY TRINH (DONE)
echo ========================================================
pause
