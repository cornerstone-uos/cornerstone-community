param (
    [string]$FilePath
)

if (Test-Path $FilePath) {
    $lastEdited = git log -1 --pretty="format:%ci" -- $FilePath
    $hash = Get-FileHash -Path $FilePath -Algorithm SHA256
    Write-Output "$lastEdited|$($hash.Hash)"
} else {
    throw "File not found: $FilePath"
}
