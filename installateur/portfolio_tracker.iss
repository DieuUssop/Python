; portfolio_tracker.iss — Recette de l'installateur Windows (Inno Setup 6).
; Ne pas lancer directement : double-cliquer sur fabriquer_installateur.bat
; (à la racine du projet), qui prépare le programme puis compile cette recette.

#ifndef Version
  #define Version "1.0"
#endif

[Setup]
AppId={{8F3B2A61-5C4D-4E7A-9B1F-2D6C8E4A7B90}
AppName=Portfolio Tracker
AppVersion={#Version}
AppVerName=Portfolio Tracker {#Version}
AppPublisher=Kévin Brulé · Master G2C
VersionInfoVersion=1.0.0.0
; Installation pour l'utilisateur, sans droits administrateur, dans un dossier où
; l'application peut écrire (comptes, base de titres) : %LOCALAPPDATA%\Programs
PrivilegesRequired=lowest
DefaultDirName={autopf}\Portfolio Tracker
DefaultGroupName=Portfolio Tracker
DisableProgramGroupPage=yes
OutputDir=..\installateur_windows
OutputBaseFilename=Installer_Portfolio_Tracker
SetupIconFile=..\assets\icone.ico
UninstallDisplayIcon={app}\assets\icone.ico
UninstallDisplayName=Portfolio Tracker
Compression=lzma2/max
SolidCompression=yes
WizardStyle=modern
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
CloseApplications=yes

[Languages]
Name: "fr"; MessagesFile: "compiler:Languages\French.isl"
Name: "en"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "bureau"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"

[InstallDelete]
; Lors d'une mise à jour : Python et le code sont remplacés en entier.
; Les comptes (data\comptes) ne sont jamais touchés.
Type: filesandordirs; Name: "{app}\python"
Type: filesandordirs; Name: "{app}\src"

[Files]
Source: "..\build_installateur\programme\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\Portfolio Tracker"; Filename: "{app}\python\python.exe"; Parameters: """{app}\lanceur.py"""; WorkingDir: "{app}"; IconFilename: "{app}\assets\icone.ico"; Comment: "Suivi et analyse de portefeuille"
Name: "{group}\{cm:UninstallProgram,Portfolio Tracker}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\Portfolio Tracker"; Filename: "{app}\python\python.exe"; Parameters: """{app}\lanceur.py"""; WorkingDir: "{app}"; IconFilename: "{app}\assets\icone.ico"; Tasks: bureau

[Run]
Filename: "{app}\python\python.exe"; Parameters: """{app}\lanceur.py"""; WorkingDir: "{app}"; Description: "{cm:LaunchProgram,Portfolio Tracker}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: filesandordirs; Name: "{app}\python"
Type: filesandordirs; Name: "{app}\src"

[Code]
// À la désinstallation : proposer d'effacer aussi les comptes et les portefeuilles
// enregistrés (sinon ils sont conservés pour une réinstallation).
procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
begin
  if (CurUninstallStep = usPostUninstall) and DirExists(ExpandConstant('{app}\data\comptes')) then
    if MsgBox('Supprimer aussi les comptes et les portefeuilles enregistrés ?' + #13#10 +
              'Cette suppression est définitive.' + #13#10#13#10 +
              'Non = ils sont conservés et retrouvés si vous réinstallez Portfolio Tracker.',
              mbConfirmation, MB_YESNO or MB_DEFBUTTON2) = IDYES then
      DelTree(ExpandConstant('{app}'), True, True, True);
end;
