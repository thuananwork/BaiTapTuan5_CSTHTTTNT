@echo off
setlocal EnableDelayedExpansion
cd /d "%~dp0"
title Du doan sinh vien bo hoc - Nhom 6
echo ==================================================
echo  Du an: Du doan nguy co sinh vien bo hoc (TabICLv2)
echo  Thu muc: %cd%
echo ==================================================

REM ---------- 1. Tim Python (neu chua co thi cai bang winget) ----------
set "PY="
where py >nul 2>nul && (py -3 --version >nul 2>nul && set "PY=py -3")
if not defined PY (
    python --version >nul 2>nul && set "PY=python"
)
if not defined PY (
    echo [!] Chua co Python. Dang cai Python 3.12 bang winget ^(can internet, co the hien hop thoai xin quyen^)...
    winget install -e --id Python.Python.3.12 --accept-package-agreements --accept-source-agreements
    for %%P in ("%LocalAppData%\Programs\Python\Python312\python.exe" "%ProgramFiles%\Python312\python.exe") do (
        if exist %%P set "PY="%%~P""
    )
)
if not defined PY (
    echo [LOI] Khong cai duoc Python tu dong. Hay cai tay tai https://www.python.org/downloads/ ^(nho tick "Add python.exe to PATH"^) roi chay lai run.bat.
    pause
    exit /b 1
)
echo Dung Python: %PY%
%PY% --version

REM ---------- 2. Tao moi truong ao .venv ----------
if not exist ".venv\Scripts\python.exe" (
    echo Tao moi truong ao .venv ...
    %PY% -m venv .venv
    if errorlevel 1 (
        echo [LOI] Khong tao duoc .venv.
        pause
        exit /b 1
    )
)
set "VPY=%cd%\.venv\Scripts\python.exe"

REM ---------- 3. Cai thu vien (chi lam lan dau) ----------
if not exist ".venv\.da_cai_co_ban" (
    echo Cai thu vien co ban: numpy pandas matplotlib scikit-learn python-docx ...
    "%VPY%" -m pip install --upgrade pip
    "%VPY%" -m pip install numpy pandas matplotlib scikit-learn python-docx
    if errorlevel 1 (
        echo [LOI] Cai thu vien co ban that bai. Kiem tra internet roi chay lai.
        pause
        exit /b 1
    )
    echo ok> ".venv\.da_cai_co_ban"
)

:MENU
echo.
echo ================= MENU =================
echo  1. Chay phan tich va mo trang web ket qua   ^(khuyen dung, khoang 15 giay^)
echo  2. Chi mo trang web ^(khong chay lai phan tich^)
echo  3. Chay TabICLv2 khao sat ^(cai tabicl+PyTorch, can internet, lau^)
echo  4. Dung lai bao cao Word ^(CHU Y: GHI DE file Word, mat cho da sua tay^)
echo  Q. Thoat
echo ========================================
choice /c 1234Q /n /m "Chon: "
if errorlevel 5 goto END
if errorlevel 4 goto WORD
if errorlevel 3 goto TABICL
if errorlevel 2 goto WEB
if errorlevel 1 goto ANALYZE

:ANALYZE
echo.
echo --- Chay phan tich ---
"%VPY%" src\phan_tich.py
if errorlevel 1 (
    echo [LOI] phan_tich.py bao loi. Xem thong bao o tren.
    pause
    goto MENU
)
goto WEB

:WEB
echo.
echo --- Mo trang web ket qua ---
"%VPY%" src\web.py
goto MENU

:TABICL
echo.
if not exist "results\tables\split_seed42.json" (
    echo Chua co results\tables\split_seed42.json. Hay chon muc 1 truoc.
    goto MENU
)
if not exist ".venv\.da_cai_tabicl" (
    echo Cai tabicl ^(keo theo PyTorch, vai GB^) ...
    "%VPY%" -m pip install tabicl
    if errorlevel 1 (
        echo [LOI] Cai tabicl that bai.
        pause
        goto MENU
    )
    echo ok> ".venv\.da_cai_tabicl"
)
echo Chay TabICLv2 ^(lan dau se tai trong so tu HuggingFace^) ...
"%VPY%" src\chay_tabicl.py
if errorlevel 1 echo [LOI] chay_tabicl.py bao loi. Gui dong loi cho nguoi ho tro.
pause
goto MENU

:WORD
echo.
echo CANH BAO: lenh nay GHI DE report\BaoCao_TabICLv2_BoHoc.docx.
choice /c YN /n /m "Tiep tuc? (Y/N): "
if errorlevel 2 goto MENU
"%VPY%" src\viet_bao_cao.py
pause
goto MENU

:END
endlocal
