# Andy2244's Kodi Repository

A personal Kodi addon repository.

## Installation

1. Download the repository zip: [repository.andy2244-1.0.0.zip](https://github.com/Andy2244/kodi-repo/raw/main/zips/repository.andy2244/repository.andy2244-1.0.0.zip)
2. In Kodi, go to **Add-ons** → **Install from zip file**
3. Navigate to and select the downloaded zip file
4. Once installed, go to **Install from repository** → **Andy2244's Repository**

## Available Addons

### Jellyskip (service.jellyskip)
Interact with Jellyfin Media Segments API to skip intros/outros.

**Features:**
- Skip intro/outro segments with a button prompt
- Auto Skip mode - automatically skip without interaction
- 5-second delay on initial playback (for TV sync)
- Seek-back detection to re-show skip prompts

## Updating the Repository

To update the repository after adding/updating addons:

```bash
python _tools/generate_repo.py
```

This will:
1. Create zip files for addons in the repo root
2. Scan `zips/` for existing addon zips
3. Generate `addons.xml` and `addons.xml.md5`
