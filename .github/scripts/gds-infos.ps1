param (
    [string]$FilePath
)

if (Test-Path $FilePath) {
    
    $relativePath = Resolve-Path -Relative $file.FullName
    $lastEdited = git log -1 --pretty="format:%ci" -- $relativePath
    $hash = Get-FileHash -Path $FilePath -Algorithm SHA256
    Write-Output "$lastEdited|$($hash.Hash)"
} else {
    throw "File not found: $FilePath"
}
