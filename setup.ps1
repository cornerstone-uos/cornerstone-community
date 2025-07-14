# Script to install starter pack for WP PDK
# Author: Matthew Anderson

$klayout_version = "0.30.1"
$klive_version = "0.3.3"

# --------------------------------------------------------------------------------------------------
# install klayout & siepic tools & klive
# --------------------------------------------------------------------------------------------------


$klayout_install_url = "https://www.klayout.org/downloads/Windows/klayout-$klayout_version-win64-install.exe"
$installed = (Test-Path "$Env:AppData\KLayout\klayout_app.exe")

if (-Not $installed) {
    Write-Output "Installing KLayout"
    Write-Output "Downloading KLayout installer from $klayout_install_url..."
    $installerPath = ((Get-Location).Path + "\klayout-$klayout_version-win64-install.exe")
    curl.exe -L -o $installerPath $klayout_install_url
    Start-Process -FilePath $installerPath -Args "/S" -Wait
    Remove-Item $installerPath
}

# # Install Klive from powershell
# $url = "https://github.com/gdsfactory/klive/archive/refs/tags/v$klive_version.zip"
# $installed = (Test-Path "$klayout_salt\klive")

# if (-Not $installed) {

#     curl.exe -L -o "klive.zip" $url
#     mkdir klive
#     tar xfz "klive.zip" --exclude 'docs/*' -C klive --strip-components 1

#     Move-Item "klive\klayout" "$klayout_salt\klive"

#     Remove-Item klive.zip
#     Remove-Item klive -Recurse
# }

# --------------------------------------------------------------------------------------------------
# Create USerProfile
# --------------------------------------------------------------------------------------------------

# create powershell profile in user scope is not already there
$profilePath = $profile.CurrentUserAllHosts
if (-not (Test-Path $profilePath)) {
    New-Item -ItemType File -Path $profilePath -Force
}

# --------------------------------------------------------------------------------------------------
# Install VS Code
# --------------------------------------------------------------------------------------------------

$installed = (Get-Command code -ErrorAction Ignore)
if (-Not $installed) {
    Write-Output "Installing VS Code..."
    $vscodeInstallerUrl = "https://code.visualstudio.com/sha/download?build=stable&os=win32-x64-user"
    $vscodeInstallerPath = "$env:USERPROFILE\Downloads\vscode_installer.exe"

    # Download the VS Code installer
    curl.exe -L -o $vscodeInstallerPath $vscodeInstallerUrl

    # Install VS Code for the current user
    Start-Process -FilePath $vscodeInstallerPath -ArgumentList "/VERYSILENT /MERGETASKS=!runcode" -Wait

    # Modify $profile.CurrentUserAllHosts to add VS Code to PATH
    Add-Content $profilePath '$env:vscodepath = (Join-Path $env:LocalAppData -ChildPath "Programs\Microsoft VS Code\bin")'
    Add-Content $profilePath '$env:Path += ";$env:vscodepath"'

    # execute to update
    . $profilePath

    # Clean up the installer
    Remove-Item -Path $vscodeInstallerPath
}

#Install python extension
$extensions = (code --list-extensions)
if (-Not ("ms-python.python" -in $extensions)) {
    code --install-extension ms-python.python
}
if (-Not ("ms-toolsai.jupyter" -in $extensions)) {
    code --install-extension ms-toolsai.jupyter
}
if (-Not ("tomoki1207.pdf" -in $extensions)) {
    code --install-extension tomoki1207.pdf
}
if (-Not ("mhutchie.git-graph" -in $extensions)) {
    code --install-extension mhutchie.git-graph
}
if (-Not ("github.vscode-pull-request-github" -in $extensions)) {
    code --install-extension github.vscode-pull-request-github
}
if (-Not ("eamodio.gitlens" -in $extensions)) {
    code --install-extension eamodio.gitlens
}


# modify settings of jupyter to change network port to localhost
$settingsFile = "$env:APPDATA\Code\User\settings.json"
if (-Not (Test-Path $settingsFile)) {
    New-Item -ItemType File -Path $settingsFile -Force
}
$jsonContent = Get-Content $settingsFile | ConvertFrom-Json
if ($jsonContent."jupyter.serverHost") {
    $jsonContent."jupyter.serverHost" = "localhost"
}
else {
    $jsonContent | Add-Member -MemberType NoteProperty -Name "jupyter.serverHost" -Value "localhost"
}
$jsonContent | ConvertTo-Json | Set-Content $settingsFile

# --------------------------------------------------------------------------------------------------
# Install uv + test env
# --------------------------------------------------------------------------------------------------

# Install uv from Astral (if not already installed)
if (-not (Test-Path "$HOME\.local\bin\uv.exe")) {
    Write-Host "Installing uv..."
    irm https://astral.sh/uv/install.ps1 | iex
} else {
    Write-Host "uv already installed, skipping installation."
}

# Add uv to PATH for this session
$uvDir = "$HOME\.local\bin"
$env:PATH += ";$uvDir"
$uvPath = Join-Path $uvDir "uv.exe"

if (-not (Test-Path $uvPath)) {
    Write-Error "uv did not install correctly. Aborting."
    exit 1
}

Write-Host "Creating venv in dummy project folder..."

# Create a dummy project folder
$projectDir = "dummy-project"
New-Item -ItemType Directory -Path $projectDir | Out-Null

# Navigate into the project folder
Set-Location $projectDir

# Create a pyproject.toml to make it a valid Python project
@"
[project]
name = "dummy"
version = "0.1.0"
description = "Temporary test project"
requires-python = ">=3.12"
"@ | Set-Content -Encoding UTF8 -Path "pyproject.toml"

# Create the venv inside the project folder
uv venv

# Install a test package
uv pip install requests

# Run a test command
Write-Host "Running test Python script..."
uv run python -c "import requests; print('requests version:', requests.__version__)"

# Return to original directory
Set-Location ..

Write-Host "Done."


# ------------------------------
# Install Git
# ------------------------------


# Define URL and destination
$gitUrl = "https://github.com/git-for-windows/git/releases/download/v2.49.0.windows.1/PortableGit-2.49.0-64-bit.7z.exe"
$destination = "$env:USERPROFILE\Downloads\PortableGit.7z.exe"

# Download the file
Invoke-WebRequest -Uri $gitUrl -OutFile $destination

# Define target extract folder
$extractPath = "$env:USERPROFILE\Downloads\PortableGit"

# Create the folder
New-Item -ItemType Directory -Force -Path $extractPath

# Run the self-extracting archive
Start-Process -FilePath $destination -ArgumentList "/SILENT", "/DIR=$extractPath" -Wait

$gitBin = "$extractPath\cmd"
$env:PATH = "$gitBin;$env:PATH"

# Get current path
$currentPath = [Environment]::GetEnvironmentVariable("Path", "User")

# Add Git path if not already present
if ($currentPath -notlike "*$gitBin*") {
    [Environment]::SetEnvironmentVariable("Path", "$gitBin;$currentPath", "User")
}

git --version
