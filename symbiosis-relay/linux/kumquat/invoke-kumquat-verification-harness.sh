#!/usr/bin/env bash
# Linux mirror stub for Invoke-KumquatVerificationHarness.ps1 (WA verifies contract exists)
# Full dual-run harness is Oregon-only; WA runs ritual capture + checks this file + README section.
set -euo pipefail
echo "=== KUMQUAT VERIFICATION HARNESS (Linux mirror stub) ==="
echo "ENTRY: symbiosis-relay/linux/kumquat/invoke-kumquat-verification-harness.sh"
echo "CONTRACT: Oregon runs Invoke-KumquatVerificationHarness.ps1 for dual-run + evidence bundle"
echo "VERIFY: test -f ~/grok-hermes-symbiosis/symbiosis-relay/windows/kumquat/Invoke-KumquatVerificationHarness.ps1"
REPO="${HOME}/grok-hermes-symbiosis"
HARNESS="${REPO}/symbiosis-relay/windows/kumquat/Invoke-KumquatVerificationHarness.ps1"
if [[ -f "$HARNESS" ]]; then
  echo "CROSS_ARTIFACT_OK: Invoke-KumquatVerificationHarness.ps1"
  exit 0
else
  echo "CROSS_ARTIFACT_MISSING: Invoke-KumquatVerificationHarness.ps1"
  exit 1
fi