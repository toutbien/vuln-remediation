param([string]$LogPath = "C:\Logs\log4j_update.log")

# Import inventory of vulnerable locations
$inventory = Get-Content ".\data\$env:COMPUTERNAME.json" | ConvertFrom-Json

foreach ($app in $inventory.applications) {
    Write-Output "Processing $($app.name)..." | Out-File $LogPath -Append
    
    # Stop services
    $app.services | ForEach-Object {
        Stop-Service $_ -Force -ErrorAction SilentlyContinue
    }
    
    # Backup and replace JARs
    $app.jar_locations | ForEach-Object {
        if (Test-Path $_) {
            Copy-Item $_ "$_.backup.$(Get-Date -Format 'yyyyMMdd')"
            Copy-Item ".\files\log4j-core-2.17.1.jar" $_
        }
    }
    
    # Restart services
    $app.services | ForEach-Object {
        Start-Service $_ -ErrorAction SilentlyContinue
    }
}
