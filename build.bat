@echo off

PyInstaller launcher.py --noconsole -i favicon.ico -n Stalker -y

if exist "Stalker App" (
    rmdir /s /q "Stalker App"
)

del "Stalker.spec"
rmdir /s /q "build"
copy "favicon.ico" "dist\Stalker\"
copy "LICENSE.txt" "dist\Stalker\"
move "dist/Stalker" "Stalker"
rename "Stalker" "Stalker App"
rmdir "dist"
mkdir "Stalker App/saves"
