Describe "Get-SymbiosisMemorySync (7eb7d1b7 mirror)" {
  It "emits json for bundle dry-run" {
    $out = & "$PSScriptRoot\Get-SymbiosisMemorySync.ps1" -Cmd bundle -Agent grok -Device "Oregon Windows" -DryRun
    $out | Should -Not -BeNullOrEmpty
  }
}
