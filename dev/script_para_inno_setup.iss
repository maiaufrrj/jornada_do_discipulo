; Script gerado pelo Inno Setup
[Setup]
AppName=A Jornada do Discípulo
AppVersion=1.0
DefaultDirName={pf}\A Jornada do Discípulo
DefaultGroupName=A Jornada do Discípulo
OutputDir=.
OutputBaseFilename=InstaladorAJornadaDoDiscipulo
Compression=lzma
SolidCompression=yes

[Languages]
Name: "portuguese"; MessagesFile: "compiler:Languages\Portuguese.isl"

[Files]
Source: "C:\Users\JM\Documents\python_scripts\game\dist\main.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\JM\Documents\python_scripts\game\*"; DestDir: "{app}\data"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\A Jornada do Discípulo"; Filename: "{app}\main.exe"
Name: "{group}\{cm:UninstallProgram,A Jornada do Discípulo}"; Filename: "{uninstallexe}"

[Run]
Filename: "{app}\main.exe"; Description: "{cm:LaunchProgram,A Jornada do Discípulo}"; Flags: nowait postinstall skipifsilent