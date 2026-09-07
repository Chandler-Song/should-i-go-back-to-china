$ErrorActionPreference = 'SilentlyContinue'
Get-Process python | Stop-Process -Force
Start-Sleep 1
Set-Location 'C:\Users\Administrator\IDEProjects\gotochina'
python -m http.server 8080