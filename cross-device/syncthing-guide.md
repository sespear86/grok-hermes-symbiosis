# Syncthing Setup for Grok-Hermes Cross-Device Sync

This is the recommended live file sync layer between the Oregon Linux machine and the Windows 11 machine.

## Why Syncthing

- Near real-time bidirectional sync
- Excellent conflict handling (rename conflicts instead of silent loss)
- Selective per-folder control
- Works reliably across Windows ↔ Linux
- No cloud dependency

## Recommended Initial Folder Shares

Share these from the Linux machine to Windows (and vice versa where it makes sense):

1. `grok-hermes-symbiosis` (the entire integration repo)
2. Your main joint project folder(s) — with proper ignore patterns
3. `cross-device/handoffs` (or a dedicated handoff exchange folder)

## Ignore Patterns (`.stignore` file in each shared folder root)

```
# Build artifacts & caches
node_modules
.venv
__pycache__
dist
build
*.log
.cache

# Secrets & machine-specific
.env*
secrets/
**/.git
**/.ssh
**/.grok
**/.hermes
**/%LOCALAPPDATA%/hermes

# Large / unnecessary
*.mp4
*.iso
models/
downloads/
```

## Setup Steps (Windows Side)

1. Download the Windows version of Syncthing (portable zip is fine): https://syncthing.net/downloads/
2. Extract and run `syncthing.exe`.
3. It should open the web UI at http://127.0.0.1:8384
4. On first run, set a GUI password in the UI (Actions → Settings).
5. Go to "Actions → Show ID" and send your Device ID to your brother (or vice versa).
6. Accept the incoming folder shares from the Linux machine.
7. For each folder, review the "Ignore Patterns" and add the content above.

## Setup Steps (Linux Side)

Your brother will do the symmetric steps.

## Best Practices

- Start with small, important folders only.
- Always review what is being shared before enabling "Send & Receive" on sensitive material.
- Use "Receive Only" folders in some cases if you want one side as the source of truth.
- For very large folders, consider separate shares with different sync schedules.
- Periodically run "Rescan" or let the watcher do its job.

## Integration with the Symbiosis

Once Syncthing is running:
- Both sides should have the latest `grok-hermes-symbiosis` at all times (or pull frequently).
- New skills, scripts, and docs appear on both machines automatically.
- Handoff packages created on one machine become visible on the other shortly after.

This + Git + Hermes gateway in the shared chat gets us extremely close to the "one extended machine" goal.

We can later add watchers or Hermes cron jobs that react to changes in the synced folders.
