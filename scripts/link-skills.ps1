[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$TargetDirectory,

    [string]$SourceDirectory = (Join-Path (Split-Path -Parent $PSScriptRoot) 'skills'),

    [ValidateSet('Auto', 'SymbolicLink', 'Junction')]
    [string]$LinkType = 'Auto'
)

$ErrorActionPreference = 'Stop'

$sourceRoot = (Resolve-Path -LiteralPath $SourceDirectory).Path
if (-not (Test-Path -LiteralPath $TargetDirectory)) {
    New-Item -ItemType Directory -Path $TargetDirectory | Out-Null
}
$targetRoot = (Resolve-Path -LiteralPath $TargetDirectory).Path

$skills = @(
    Get-ChildItem -LiteralPath $sourceRoot -Directory |
        Where-Object { Test-Path -LiteralPath (Join-Path $_.FullName 'SKILL.md') } |
        Sort-Object Name
)

if ($skills.Count -eq 0) {
    throw "No skills with SKILL.md found under $sourceRoot"
}

$linked = 0
foreach ($skill in $skills) {
    $linkPath = Join-Path $targetRoot $skill.Name
    $existing = Get-Item -LiteralPath $linkPath -Force -ErrorAction SilentlyContinue

    if ($existing) {
        if (-not ($existing.Attributes -band [IO.FileAttributes]::ReparsePoint)) {
            throw "Refusing to replace real path: $linkPath"
        }

        $storedTarget = @($existing.Target)[0]
        if ($storedTarget) {
            if ([IO.Path]::IsPathRooted($storedTarget)) {
                $actualTarget = [IO.Path]::GetFullPath($storedTarget)
            } else {
                $actualTarget = [IO.Path]::GetFullPath((Join-Path $targetRoot $storedTarget))
            }

            if ($actualTarget -eq [IO.Path]::GetFullPath($skill.FullName)) {
                $linked++
                continue
            }
        }

        Remove-Item -LiteralPath $linkPath -Force
    }

    $created = $false
    if ($LinkType -ne 'Junction') {
        $relativeTarget = [IO.Path]::GetRelativePath($targetRoot, $skill.FullName)
        Push-Location $targetRoot
        try {
            New-Item -ItemType SymbolicLink -Path $skill.Name -Target $relativeTarget -ErrorAction Stop | Out-Null
            $created = $true
        } catch {
            if ($LinkType -eq 'SymbolicLink' -or -not $IsWindows) {
                throw
            }
        } finally {
            Pop-Location
        }
    }

    if (-not $created) {
        New-Item -ItemType Junction -Path $linkPath -Target $skill.FullName | Out-Null
    }
    $linked++
}

Write-Output "Linked $linked skills from $sourceRoot into $targetRoot"
