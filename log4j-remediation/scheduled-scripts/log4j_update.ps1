# C:\Scripts\log4j_update.ps1
$repoPath = "C:\remediation-scripts"
$logFile = "C:\Logs\log4j_update.log"

try {
    Set-Location $repoPath
    git pull origin main | Out-File $logFile -Append
    
    # Check if updates available
    $gitStatus = git status --porcelain
    if ($gitStatus -or (Test-Path ".\force_update.flag")) {
        Write-Output "$(Get-Date): Starting Log4j update process" | Out-File $logFile -Append
        
        # Run the update script
        .\scripts\update_log4j.ps1 -LogPath $logFile
        
        # Clean up flag file
        Remove-Item ".\force_update.flag" -ErrorAction SilentlyContinue
    }
} catch {
    Write-Error "Update failed: $_" | Out-File $logFile -Append
}
