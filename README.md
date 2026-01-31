# Andy2244's Kodi Repository

A personal Kodi addon repository for Jellyfin-related addons.

## Installation Guide

### Step 1: Install the Repository

1. Download the repository addon: [repository.andy2244-1.0.0.zip](https://github.com/Andy2244/kodi-repo/raw/main/zips/repository.andy2244/repository.andy2244-1.0.0.zip)
2. In Kodi, go to **Settings** → **Add-ons** → **Install from zip file**
3. Navigate to your downloads folder and select `repository.andy2244-1.0.0.zip`
4. Wait for the "Add-on installed" notification

> **CoreELEC/LibreELEC Users:** If installation fails with an error, go to **Power** → **Restart Kodi** and try again. This is a known caching issue.

### Step 2: Install Jellyskip

1. Go to **Settings** → **Add-ons** → **Install from repository**
2. Select **Andy2244's Repository**
3. Go to **Services** → **Jellyskip**
4. Click **Install**

### Step 3: Configure Jellyskip

Jellyskip works automatically with Jellyfin once installed. For additional options:

1. Go to **Settings** → **Add-ons** → **My add-ons** → **Services** → **Jellyskip**
2. Click **Configure**

#### Settings

| Setting | Description |
|---------|-------------|
| **Auto Skip** | When enabled, automatically skips intro/outro segments without showing a button. A brief notification will appear instead. On initial playback, there's a 5-second delay to allow your TV to sync before skipping. |

## Requirements

- **Kodi 21 (Omega) or newer**
- **Jellyfin for Kodi addon** (must be installed and configured)
- **Jellyfin server 10.9+** with the [Intro Skipper plugin](https://github.com/intro-skipper/intro-skipper) installed and configured to detect intros/outros

## How It Works

Jellyskip monitors your Jellyfin playback and detects when you enter a marked segment (intro, outro, etc.). It then:

- **Auto Skip OFF:** Shows a "Skip Intro" / "Skip Outro" button that disappears when the segment ends
- **Auto Skip ON:** Automatically skips the segment with a brief notification

## Troubleshooting

### Skip button doesn't appear
- Ensure the [Intro Skipper plugin](https://github.com/intro-skipper/intro-skipper) is installed on your Jellyfin server
- Check that the media file has detected segments (visible in Jellyfin web UI under media info)
- Verify the Jellyfin for Kodi addon is properly configured and synced

### Installation fails on CoreELEC/LibreELEC
- Go to **Power** → **Restart Kodi**
- Try the installation again after restart

### Auto Skip not working after changing settings
- Settings take effect immediately, no restart needed
- If issues persist, restart Kodi

---

## Available Addons

| Addon | Version | Description |
|-------|---------|-------------|
| Jellyskip | 1.1.0 | Skip Jellyfin media segments (intros/outros) |

## For Developers

### Updating the Repository

After adding or updating addons, run:

```bash
python _tools/generate_repo.py
```

This will regenerate `addons.xml` and `addons.xml.md5`.
