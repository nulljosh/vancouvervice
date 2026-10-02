# Hardware

Unreal runs off an external drive because the Mac's internal SSD has about 20 GB free. The engine is 49 GB and the project 16 GB.

## Why boots take 15 minutes

The current drive, a LaCie Rugged USB-C, is a spinning disk. It reads at 125 MB/s (measured 2026-10-01). Every editor launch reads tens of gigabytes off it.

## What to buy

Anything that says NVMe or SSD and 1,000 MB/s or more. 1 TB fits the engine and the game. Plug it into a back USB-C port on the Mac mini M4 (those are the fast Thunderbolt ports).

- Easiest: Samsung T7 Shield 1 TB, about 1,000 MB/s. https://www.amazon.ca/s?k=Samsung+T7+Shield+1TB
- Fastest and often cheapest: a USB4 NVMe enclosure plus a 1 TB NVMe stick, about 3,000 MB/s.
  - Enclosure: https://www.amazon.ca/s?k=USB4+NVMe+enclosure
  - Drive: https://www.amazon.ca/s?k=1TB+NVMe+SSD+WD+SN850X
  - Memory Express: https://www.memoryexpress.com/Search/Products?Search=USB4+NVMe+enclosure

Best Buy had the T7 Shield 2 TB at $779.99 on 2026-10-01. Skip that.

## Moving off the LaCie

The LaCie also holds Ollama models, Movies and Music through symlinks from the Mac. Copy all of it to the new drive and repoint the symlinks before the LaCie goes back. Then update the paths in `unreal/open.sh`, `unreal/package.sh` and `UNREAL.md` (`/Volumes/LaCie/UE_5.8`, `/Volumes/LaCie/Unreal/VancouverVice`).
