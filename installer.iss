[Setup]
AppName=Windrose App
AppVersion=1.0
AppPublisher=Le Quang Thanh
AppPublisherURL=https://github.com/thanhst
AppSupportURL=https://github.com/thanhst
AppUpdatesURL=https://github.com/thanhst
AppCopyright=© 2025 Le Quang Thanh _ Nguyen Thanh Huyen _ nguoi dep nhat vu tru
DefaultDirName={pf}\WindroseApp
DefaultGroupName=WindroseApp
OutputBaseFilename=WindroseAppInstaller
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Files]
Source: "dist\app\*"; DestDir: "{app}"; Flags: recursesubdirs

[Icons]
Name: "{group}\WindroseApp"; Filename: "{app}\app.exe"
Name: "{commondesktop}\WindroseApp"; Filename: "{app}\app.exe"
