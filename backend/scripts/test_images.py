import urllib.request

test_ids = [
    'photo-1576091160399-112ba8d25d1d',
    'photo-1584515979956-d9f6e5d09982',
    'photo-1584467735815-f778f274e296',
    'photo-1576765608535-5f04d1e3f289',
    'photo-1532938911079-1b06ac7ceec7',
    'photo-1622253692010-333f2da6031d',
    'photo-1629909613654-28e377c37b09',
    'photo-1516574187841-cb9cc2ca948b',
    'photo-1581594693702-fbdc51b2763b',
    'photo-1505751172876-fa1923c5c528',
    'photo-1579684385127-1ef15d508118'
]

for pid in test_ids:
    url = f"https://images.unsplash.com/{pid}?auto=format&fit=crop&w=800&q=80"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=5) as r:
            ct = r.headers.get("content-type")
            print(f"{pid}: Status {r.status}, content-type: {ct}")
    except Exception as e:
        print(f"{pid}: Error {e}")
