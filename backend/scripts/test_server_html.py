# -*- coding: utf-8 -*-
import urllib.request

req = urllib.request.Request("http://127.0.0.1:8000/")
with urllib.request.urlopen(req) as resp:
    html = resp.read().decode("utf-8")
    print("HTTP Status:", resp.status)
    print("Title in HTML:", "OncoSathi AI" in html)
    print("Brand in HTML:", "OncoSathi" in html and "AI" in html)
    print("No purple gradient:", "from-purple" not in html)
    print("Hind Siliguri included:", "Hind+Siliguri" in html)
    print("Healthcare primary #176B63:", "#176B63" in html)
