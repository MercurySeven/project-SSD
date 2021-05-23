#!/bin/sh
briefcase create
cp linux/appimage/ssd/ssd.AppDir/usr/app_packages/shiboken6/Shiboken.abi3.so linux/appimage/ssd/ssd.AppDir/usr/app_packages/PySide6
cp linux/appimage/ssd/ssd.AppDir/usr/app_packages/shiboken6/shiboken6.abi3.so linux/appimage/ssd/ssd.AppDir/usr/app_packages/PySide6
cp linux/appimage/ssd/ssd.AppDir/usr/app_packages/shiboken6/libshiboken6.abi3.so.6.1 linux/appimage/ssd/ssd.AppDir/usr/app_packages/PySide6
rm -r linux/appimage/ssd/ssd.AppDir/usr/app_packages/PySide6/Qt/plugins/sqldrivers
rm -r linux/appimage/ssd/ssd.AppDir/usr/app_packages/PySide6/Qt/plugins/designer
briefcase build
rm linux/appimage/ssd/ssd.AppDir/usr/lib/libcairo.so.2
chmod +x appimagetool-x86_64.AppImage
./appimagetool-x86_64.AppImage linux/appimage/ssd/ssd.AppDir/
mkdir dist
mv ssd-x86_64.AppImage dist/SSD.AppImage
echo "build completata, appimage inserita nella cartella dist"

