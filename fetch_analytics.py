#!/usr/bin/env python3
"""Fetch profile analytics from Zo Space and generate card data."""
import urllib.request
import json
from datetime import datetime

ZO_API = "https://thebookmaster.zo.space/api/profile-views"
USERNAME = "Retsumdk"

def fetch():
    url = f"{ZO_API}?readOnly=true&limit=1000"
    req = urllib.request.Request(url, headers={"User-Agent": "GitHub-Actions"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read())

def generate_cards(data):
    count = data.get("count", 0)
    detailed = data.get("detailed", [])

    sources = {"Google": 0, "Twitter/X": 0, "LinkedIn": 0, "Reddit": 0, "GitHub": 0, "YouTube": 0, "Direct": 0}
    countries = {}
    devices = {"desktop": 0, "mobile": 0, "tablet": 0}
    browsers = {}
    hours = {}

    for v in detailed:
        src = v.get("referrer", "direct")
        if "google" in src.lower(): sources["Google"] += 1
        elif "twitter" in src.lower() or "t.co" in src.lower(): sources["Twitter/X"] += 1
        elif "linkedin" in src.lower(): sources["LinkedIn"] += 1
        elif "reddit" in src.lower(): sources["Reddit"] += 1
        elif "github" in src.lower(): sources["GitHub"] += 1
        elif "youtube" in src.lower(): sources["YouTube"] += 1
        else: sources["Direct"] += 1

        country = v.get("country", "Unknown")
        countries[country] = countries.get(country, 0) + 1

        device = v.get("device", "desktop")
        devices[device] = devices.get(device, 0) + 1

        browser = v.get("browser", "other")
        browsers[browser] = browsers.get(browser, 0) + 1

        # Hour buckets - use "time" field (ISO timestamp), not "timestamp"
        ts_str = v.get("time", "")
        if ts_str:
            try:
                dt = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
                hour = dt.strftime("%H:00")
                hours[hour] = hours.get(hour, 0) + 1
            except Exception:
                pass

    top_sources = sorted(sources.items(), key=lambda x: -x[1])[:4]
    top_countries = sorted(countries.items(), key=lambda x: -x[1])[:5]
    top_devices = sorted(devices.items(), key=lambda x: -x[1])
    top_browsers = sorted(browsers.items(), key=lambda x: -x[1])[:4]
    hourly_count = sum(hours.values())

    return {
        "count": count,
        "hourly": hourly_count,
        "sources": top_sources,
        "countries": top_countries,
        "devices": top_devices,
        "browsers": top_browsers,
        "hours": hours
    }

if __name__ == "__main__":
    data = fetch()
    cards = generate_cards(data)
    with open("analytics_data.json", "w") as f:
        json.dump(cards, f, indent=2)
    print("Fetched %d total views, %d hourly" % (cards["count"], cards["hourly"]))
