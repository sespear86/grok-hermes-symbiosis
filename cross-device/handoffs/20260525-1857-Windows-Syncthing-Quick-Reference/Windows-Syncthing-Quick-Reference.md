# Windows Syncthing Quick Reference

**Last Updated:** 2026-05-26  
**Machine:** Oregon Windows (Brother)

## Installation
- **Method:** Portable binary (not installed as a service)
- **Location:** `C:\Tools\Syncthing\`
- **Executable:** `syncthing.exe`
- **How to start:** Double-click `syncthing.exe` (or run from command line)

## Key Shared Folders

| Folder                  | Local Path                                      | Purpose                              | Sync Mode     |
|-------------------------|--------------------------------------------------|--------------------------------------|---------------|
| Symbiosis Repo          | `C:\Users\spear\grok-hermes-symbiosis`           | Main shared codebase & tools         | Send & Receive |
| Handoffs                | `C:\Users\spear\grok-hermes-symbiosis\cross-device\handoffs` | Structured cross-device task handoffs | Send & Receive |

**Dedicated Sync Root (Recommended):**
- `C:\Synced\` — Used as the top-level folder for Syncthing shares to avoid OneDrive conflicts.

## Important .stignore Patterns
- Located in the root of the symbiosis repo
- Protects:
  - `.env` and secret files
  - `.hermes/` and `.grok/` directories
  - `node_modules/`, `.venv/`, `__pycache__/`
  - Build artifacts and large files
- Always keep the `.stignore` in sync between both machines

## Common Issues & Troubleshooting

**"Expected encrypted info" error**
- Usually caused by one side offering the folder as "Receive Encrypted"
- Fix: Remove the folder share on both sides and re-share as normal Send & Receive (unencrypted)

**Commands not working when run through Grok Build TUI**
- The Grok TUI harness is non-interactive
- `hermes model` and interactive setup wizards will fail
- Always run Syncthing-related or Hermes setup commands in a **normal PowerShell** window

**OneDrive interference**
- Never point Syncthing shares directly at OneDrive folders (especially Documents/Desktop)
- Use `C:\Synced\` or another dedicated location outside OneDrive

**Syncthing not starting / UI not loading**
- Check that `syncthing.exe` is running in Task Manager
- UI is available at: `http://127.0.0.1:8384`

## Maintenance & Restart

- **Restart Syncthing:** Close the process (via Task Manager or `taskkill`) and re-run `syncthing.exe`
- **Auto-start:** Can be added later via Task Scheduler or Startup folder
- **Logs:** Available in the Syncthing UI under **Actions → Logs**

## Device Information
- **Device ID:** `ZRADDTT-FNEWXKT-7Q6PAOK-RXBSUGB-TXFHOQT-QSWS7KO-5KDX3FM-VYVSBQ2`
- **GUI Password:** Set (required for remote access and security)
- **Current Connected Device:** Washington Linux

## Tips
- Prefer running Syncthing from a normal terminal/PowerShell rather than through any AI harness
- Keep the portable folder (`C:\Tools\Syncthing`) clean — only the official files
- Use the handoffs folder for any explicit task transfers between machines
- Periodically check for updates on https://syncthing.net/downloads/

---

*This document is intended to be a living reference. Update it as the Windows Syncthing setup evolves.*