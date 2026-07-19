---
name: droxul
version: "1.0.0"
tags:
  - dropbox
  - backup
  - upload
  - storage
  - maintenance
description: >
  Dropbox CLI uploader (dropbox_uploader.sh) available as `droxul` on this device.
  Use for off-device backup, file sharing, and cloud staging of tarballs and artifacts.
---

# Droxul — Dropbox CLI Upload/Download Skill

## What It Is

`droxul` is a Bash-based Dropbox CLI client (based on Andrea Fabrizi's dropbox_uploader.sh) installed at `$PREFIX/bin/droxul`. It authenticates via OAuth token stored in `~/.dropbox_uploader`.

## Available Commands

| Command | Usage | Description |
|---------|-------|-------------|
| `upload` | `droxul upload <LOCAL> <REMOTE_DIR>` | Upload file or directory to Dropbox |
| `download` | `droxul download <REMOTE> [LOCAL]` | Download file or directory |
| `list` | `droxul list [REMOTE_DIR]` | List contents of a Dropbox directory |
| `mkdir` | `droxul mkdir <REMOTE_DIR>` | Create remote directory |
| `delete` | `droxul delete <REMOTE>` | Delete remote file or directory |
| `move` | `droxul move <SRC> <DST>` | Move/rename remote item |
| `copy` | `droxul copy <SRC> <DST>` | Copy remote item |
| `share` | `droxul share <REMOTE_FILE>` | Get share link |
| `search` | `droxul search <QUERY>` | Search Dropbox |
| `info` | `droxul info` | Account info |
| `space` | `droxul space` | Storage usage |

## Flags

- `-s` — Skip existing files (don't overwrite)
- `-q` — Quiet mode
- `-p` — Show progress meter
- `-h` — Human-readable file sizes
- `-x <NAME>` — Exclude file/dir from sync

## Backup Conventions on This Device

- **Staging tmp**: `/data/data/com.termux/files/usr/tmp/`
- **Dropbox target**: `/BackupsRoot/Ilex/YYMM/` (year-month subfolder)
- **Naming**: `<namespace>.<user>.<hostname>.<tlid-timestamp>.tar`
- **Utility**: `tlid min` generates a compact timestamp (`YYMMDDhhmm`)

## Example: Backup a Directory

```bash
namespace=my-project
_TMP=/data/data/com.termux/files/usr/tmp
_TAR=$_TMP/$namespace.$USER.$HOSTNAME.$(tlid min).tar
_DEST=/BackupsRoot/Ilex/$(date +%y%m)

tar -cf "$_TAR" /path/to/source
droxul upload "$_TAR" "$_DEST/"
rm -f "$_TAR"
```

## Example: List and Download

```bash
droxul list /BackupsRoot/Ilex/2607
droxul download /BackupsRoot/Ilex/2607/some-file.tar /local/path/
```

## Known Dropbox Structure

- `/BackupsRoot/Ilex/` — Device backups (YYMM subfolders)
- `/MuSiK/` — Music
- `/ART/` — Art assets
- `/Mobile Uploads/` — Camera auto-uploads

## Important Notes

- Max chunk size: 50MB per request (large files are chunked automatically)
- Config: `~/.dropbox_uploader` (OAuth token — never expose)
- Temp dir used internally: `/data/data/com.termux/files/usr/tmp/`
- Trailing `/` on remote path matters for upload (means "into this directory")
