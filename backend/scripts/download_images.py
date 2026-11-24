import os
from pathlib import Path
import urllib.request

DEST = Path(r"C:\Users\abhis\.gemini\antigravity\brain\fb716a5a-1847-430b-a2a9-d314fda779f8\workspace\oncosathi\frontend\public\images")
DEST.mkdir(parents=True, exist_ok=True)

images_to_fetch = [
    # Hero image: Authentic Indian community health consultation / awareness
    {
        "name": "asha_hero.jpg",
        "urls": [
            "https://images.unsplash.com/photo-1584515979956-d9f6e5d09982?auto=format&fit=crop&w=1200&q=85",
            "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?auto=format&fit=crop&w=1200&q=85"
        ]
    },
    # Community health discussion
    {
        "name": "community_health.jpg",
        "urls": [
            "https://images.unsplash.com/photo-1576765608535-5f04d1e3f289?auto=format&fit=crop&w=800&q=85",
            "https://images.unsplash.com/photo-1584467735815-f778f274e296?auto=format&fit=crop&w=800&q=85"
        ]
    },
    # Healthcare worker explaining document
    {
        "name": "doctor_explaining.jpg",
        "urls": [
            "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?auto=format&fit=crop&w=800&q=85",
            "https://images.unsplash.com/photo-1629909613654-28e377c37b09?auto=format&fit=crop&w=800&q=85"
        ]
    },
    # Indian female healthcare professional
    {
        "name": "asha_worker_portrait.jpg",
        "urls": [
            "https://images.unsplash.com/photo-1622253692010-333f2da6031d?auto=format&fit=crop&w=800&q=85",
            "https://images.unsplash.com/photo-1532938911079-1b06ac7ceec7?auto=format&fit=crop&w=800&q=85"
        ]
    },
    # Calm healthcare consultation setting
    {
        "name": "clinic_consultation.jpg",
        "urls": [
            "https://images.unsplash.com/photo-1584467735815-f778f274e296?auto=format&fit=crop&w=800&q=85",
            "https://images.unsplash.com/photo-1505751172876-fa1923c5c528?auto=format&fit=crop&w=800&q=85"
        ]
    }
]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

for item in images_to_fetch:
    out_file = DEST / item["name"]
    downloaded = False
    for url in item["urls"]:
        try:
            print(f"Downloading {item['name']} from {url[:60]}...")
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = resp.read()
                if len(data) > 5000:
                    out_file.write_bytes(data)
                    print(f"Saved {item['name']} ({len(data):,} bytes)")
                    downloaded = True
                    break
        except Exception as e:
            print(f"Failed {url}: {e}")
    if not downloaded:
        print(f"Warning: Could not download {item['name']}")

print("\nFiles in images directory:")
for f in DEST.iterdir():
    print(f"  {f.name} - {f.stat().st_size:,} bytes")
