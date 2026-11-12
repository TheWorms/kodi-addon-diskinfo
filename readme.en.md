<!-- logo:start -->
<!-- logo:end -->

[Français](README.md) · **English**

# Disk Info

<!-- version:auto -->
**Version : 1.0.0**
<!-- /version:auto -->

Small Kodi service that publishes the **disk usage of the data partition** for
skins. Kodi only measures `/`: on **CoreELEC / LibreELEC** that is the read-only
system image (`loop0`), always 100 % full. This service measures the partition
holding the Kodi folder (`/storage` on CoreELEC) and makes it readable by the skin.

Built for the **Arctic: Worms** skin, usable by any skin. For Kodi 19
"Matrix" and later.

- **Repository**: `github.com/TheWorms/kodi-addon-diskinfo`
- **Kodi id**: `service.worms.diskinfo`
- **Display name**: Disk Info · **License**: MIT

---

## What it does

When Kodi starts, then at a regular interval (60 s by default), the service reads
the partition usage and publishes it as home window properties:

| Property | Example | Content |
|---|---|---|
| `Window(Home).Property(DiskInfo.UsedPercent)` | `25` | used percentage, computed like `df` |
| `Window(Home).Property(DiskInfo.FreePercent)` | `75` | free percentage |
| `Window(Home).Property(DiskInfo.Total)` | `32 GB` | partition size |
| `Window(Home).Property(DiskInfo.Used)` | `8.0 GB` | used space |
| `Window(Home).Property(DiskInfo.Free)` | `24 GB` | available space |
| `Window(Home).Property(DiskInfo.Path)` | `/storage/.kodi/` | measured folder |

It has no user interface: nothing shows until the skin reads these properties.
**Arctic: Worms** shows them in the **Storage** tile of the system info and falls
back to Kodi's value when the service is missing.

To use it in another skin, for example:

```xml
<label>$INFO[Window(Home).Property(DiskInfo.UsedPercent)] % used of $INFO[Window(Home).Property(DiskInfo.Total)]</label>
```

## Install

### Via the TheWorms repository (recommended, auto-updates)

1. Install the repository:
   `https://raw.githubusercontent.com/TheWorms/kodi-repo/main/zips/repository.theworms/repository.theworms.zip`
2. Add-ons → **Install from repository** → *TheWorms Repository* → *Services* →
   **Disk Info** → Install.

### Manual (zip)

1. Get `service.worms.diskinfo-x.y.z.zip`.
2. System → Add-ons → enable **Unknown sources**.
3. Add-ons → **Install from zip file**.

The service starts right away, no Kodi restart needed.

## Settings

| Setting | Default | Description |
|---|---|---|
| Folder to measure | empty | Empty: the partition of the Kodi folder (`/storage` on CoreELEC). Otherwise any folder (USB drive, mounted NAS…) |
| Refresh interval | 60 s | How often the usage is read again (10 to 600 s) |

## Troubleshooting

- **The skin still shows 100 %**: check that the service is enabled, then over SSH:
  ```bash
  grep worms.diskinfo /storage/.kodi/temp/kodi.log
  ```
  A line `/storage/.kodi/ : … utilisés sur … (… %)` confirms the measurement. If
  it is there, the skin is not reading the properties.
- **"lecture impossible" in the log**: the folder chosen in the settings does not
  exist or is not mounted. The service falls back to the Kodi folder.

## License

MIT — see `LICENSE.txt`.
