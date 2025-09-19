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

[Code]
var
  PasswordCorrect: Boolean;
  PasswordPage: TInputQueryWizardPage;

procedure InitializeWizard();
begin
  PasswordCorrect := False;

  // Tạo page password riêng
  PasswordPage := CreateInputQueryPage(
    wpWelcome, // đặt ngay đầu, nhưng không dùng wpLicense
    'Password Required',
    'Enter the setup password to continue',
    ''
  );

  PasswordPage.Add('Password:', True); // True = ẩn ký tự
end;

function NextButtonClick(CurPageID: Integer): Boolean;
var
  Password: String;
begin
  Result := True;

  if CurPageID = PasswordPage.ID then
  begin
    Password := PasswordPage.Values[0];

    if Password = 'superprettygirluniverse' then
      PasswordCorrect := True
    else
    begin
      MsgBox('Incorrect password! Setup will exit.', mbError, MB_OK);
      WizardForm.Close;
      Result := False;
    end;
  end;
end;



