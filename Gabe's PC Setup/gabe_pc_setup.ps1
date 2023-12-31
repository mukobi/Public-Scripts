# PowerShell Setup Script for Windows 11
# Installs Chocolatey, many packages using Chocolatey, Oh My Posh, and Anaconda

# NOTE - To first allow executing this script, run the following:
# Set-ExecutionPolicy RemoteSigned -Scope CurrentUser

# Ensuring the script is running with Administrator privileges
if (-NOT ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator))
{
    Write-Warning "[!] Please run this script as an Administrator!"
    break
}

# Function to check and install a Chocolatey package
function Install-ChocoPackage {
    param(
        [string]$packageName
    )

    if (choco list --local-only | Select-String "$packageName") {
        Write-Host "[+] $packageName is already installed." -ForegroundColor Green
    } else {
        Write-Host "[ ] Installing $packageName..." -ForegroundColor Yellow
        choco install $packageName -y
        Write-Host "[+] $packageName installation complete." -ForegroundColor Green
    }
}

# Installing Chocolatey if not already installed
if (!(Get-Command choco -ErrorAction SilentlyContinue)) {
    Write-Host "[ ] Installing Chocolatey..." -ForegroundColor Yellow
    Set-ExecutionPolicy Bypass -Scope Process -Force
    [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
    Invoke-Expression ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
    Write-Host "[+] Chocolatey installation complete." -ForegroundColor Green
} else {
    Write-Host "[+] Chocolatey is already installed." -ForegroundColor Green
}

# Updating Chocolatey
Write-Host "[ ] Updating Chocolatey..." -ForegroundColor Yellow
choco upgrade chocolatey -y
Write-Host "[+] Chocolatey update complete." -ForegroundColor Green

# Install packages using Chocolatey
Install-ChocoPackage "googledrive"
Install-ChocoPackage "7zip"
Install-ChocoPackage "slack"
Install-ChocoPackage "dotnet-all"
Install-ChocoPackage "git"
Install-ChocoPackage "github-desktop"
Install-ChocoPackage "vscode-insiders"
Install-ChocoPackage "anaconda3"
Install-ChocoPackage "cascadiacodepl"
Install-ChocoPackage "nodejs"
Install-ChocoPackage "obsidian"
Install-ChocoPackage "visualstudio2019community"
Install-ChocoPackage "nvidia-display-driver"
Install-ChocoPackage "geforce-experience"
Install-ChocoPackage "nvidia-broadcast"
Install-ChocoPackage "razer-synapse-3"
Install-ChocoPackage "vcredist140"
Install-ChocoPackage "vcredist2015"
Install-ChocoPackage "pomodoro-schedule-notifier"
Install-ChocoPackage "steam"
Install-ChocoPackage "zoom"
Install-ChocoPackage "discord"
Install-ChocoPackage "vlc"
Install-ChocoPackage "qbittorrent"
Install-ChocoPackage "microsoft-windows-terminal"
Install-ChocoPackage "gimp"
Install-ChocoPackage "foobar2000"
Install-ChocoPackage "office365business"
Install-ChocoPackage "adobereader"
Install-ChocoPackage "wiztree"
Install-ChocoPackage "malwarebytes"
Install-ChocoPackage "ccleaner"
Install-ChocoPackage "powertoys"
Install-ChocoPackage "everything"
Install-ChocoPackage "calibre"
Install-ChocoPackage "signal"
Install-ChocoPackage "whatsapp"
Install-ChocoPackage "toggl"
Install-ChocoPackage "drawio"
Install-ChocoPackage "screentogif"
Install-ChocoPackage "logitech-camera-settings"
Install-ChocoPackage "hwinfo"


# Setting PowerShell Execution Policy for scripts
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
Write-Host "[+] PowerShell script execution policy set." -ForegroundColor Green

# Install NuGet Provider for PowerShellGet
Write-Host "Installing NuGet provider..." -ForegroundColor Yellow
Install-PackageProvider -Name NuGet -MinimumVersion 2.8.5.201 -Force
Write-Host "NuGet provider installed." -ForegroundColor Green

# Install Oh My Posh
winget install JanDeDobbeleer.OhMyPosh -s winget
Write-Host "Oh My Posh installed." -ForegroundColor Green

# Copy Om My Posh theme
$ohMyPoshConfigSource = "G:\My Drive\Personal\Backup\Terminal Prompt\gabe.omp.json"
$ohMyPoshThemesDir = "C:\Users\Gabe\AppData\Local\Programs\oh-my-posh\themes"
if (-not (Test-Path $ohMyPoshThemesDir)) {
    New-Item -ItemType Directory -Path $ohMyPoshThemesDir
}
Copy-Item -Path $ohMyPoshConfigSource -Destination $ohMyPoshThemesDir -Force
Write-Host "[+] Oh My Posh configuration file copied to themes directory." -ForegroundColor Green

# Copy PowerShell profile script
$psProfileSource = "G:\My Drive\Personal\Backup\Terminal Prompt\Microsoft.PowerShell_profile.ps1"
$psProfileDest = "C:\Users\Gabe\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1"
Copy-Item $psProfileSource $psProfileDest -Force
Write-Host "[+] PowerShell profile script copied." -ForegroundColor Green

# Setting up Anaconda environment
Write-Host "[ ] Setting up Anaconda environment 'ais'..." -ForegroundColor Yellow
& conda create --name ais python=3.11 -y
& conda activate ais
& conda install numpy pandas scikit-learn scikit-learn-intelex matplotlib seaborn requests tqdm beautifulsoup4 -y
# & pip3 install torch --index-url https://download.pytorch.org/whl/cu121
Write-Host "[+] Anaconda environment 'ais' set up complete." -ForegroundColor Green

# Create GitHub folders in Documents
$githubDir = "~\Documents\GitHub"
if (-not (Test-Path $githubDir)) {
    New-Item -ItemType Directory -Path $githubDir
}
$githubSubDirs = @("AIS", "Scripts", "Portfolios", "School")
foreach ($subDir in $githubSubDirs) {
    $subDirPath = "$githubDir\$subDir"
    if (-not (Test-Path $subDirPath)) {
        New-Item -ItemType Directory -Path $subDirPath
    }
}
Write-Host "[+] GitHub folders created." -ForegroundColor Green

# End of script
Write-Host "[=] Setup Script Execution Complete!" -ForegroundColor DarkMagenta
