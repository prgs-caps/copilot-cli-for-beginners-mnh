<#
.SYNOPSIS
    Run the book-app-project test suite.

.DESCRIPTION
    Installs pytest if needed, then runs pytest -v from the correct directory.
    Exit code mirrors pytest: 0 = all passed, non-zero = failures.

.EXAMPLE
    pwsh -File samples/book-app-project/run-tests.ps1
#>

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

Write-Host "Installing/verifying pytest..." -ForegroundColor Cyan
pip install "pytest>=9.0,<10" --quiet

Write-Host "Running tests..." -ForegroundColor Cyan
pytest -v

exit $LASTEXITCODE
