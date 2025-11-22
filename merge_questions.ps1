$all = @()
Get-ChildItem ".\datasets\*.json" | ForEach-Object {
    try {
        $content = Get-Content $_.FullName -Raw | ConvertFrom-Json
        $all += $content
    } catch {
        Write-Host "Error reading $($_.Name): $_"
    }
}
$all | ConvertTo-Json -Depth 10 | Out-File "all_questions.json" -Encoding utf8
