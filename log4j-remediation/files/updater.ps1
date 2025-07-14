$hosts = Import-Csv "C:\scripts\log4j_hosts.csv"
$latestVersion = "2.21.0"
$latestJarPath = "\\yourserver\log4j\log4j-core-$latestVersion.jar"
$outputReport = "C:\scripts\log4j_update_results.csv"

"Host,CurrentVersion,Updated,Message" | Out-File $outputReport

foreach ($entry in $hosts) {
    $host = $entry.Host
    $log4jPath = $entry.Log4jPath

    try {
        Invoke-Command -ComputerName $host -Credential (Get-Credential) -ScriptBlock {
            param ($log4jPath, $latestVersion, $latestJarPath)

            if (-Not (Test-Path $log4jPath)) {
                return "$env:COMPUTERNAME,,False,Log4j path not found"
            }

            if ($log4jPath -match "log4j-core-(\d+\.\d+\.\d+)\.jar") {
                $currentVersion = $matches[1]
            } else {
                return "$env:COMPUTERNAME,,False,Unable to parse version from filename"
            }

            if ($currentVersion -eq $latestVersion) {
                return "$env:COMPUTERNAME,$currentVersion,False,Already up to date"
            }

            # Backup and replace
            Copy-Item -Path $log4jPath -Destination "$log4jPath.bak" -Force
            Copy-Item -Path $latestJarPath -Destination $log4jPath -Force

            return "$env:COMPUTERNAME,$currentVersion,True,Updated to $latestVersion"
        } -ArgumentList $log4jPath, $latestVersion, $latestJarPath | Out-File $outputReport -Append
    }
    catch {
        "$host,,False,Error: $_" | Out-File $outputReport -Append
    }
}
