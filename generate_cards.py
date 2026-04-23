#!/usr/bin/env python3
"""Generate stylish SVG cards for profile analytics."""
import json
import math

COLORS = {
    "bg": "#0d1117",
    "card_bg": "#161b22", 
    "border": "#30363d",
    "green": "#2ea043",
    "blue": "#58a6ff",
    "purple": "#a371f7",
    "orange": "#f0883e",
    "red": "#f85149",
    "text": "#c9d1d9",
    "text_secondary": "#8b949e",
    "subtext": "#6e7681"
}

FLAGS = {
    "US": "🇺🇸", "DE": "🇩🇪", "GB": "🇬🇧", "FR": "🇫🇷", "CA": "🇨🇦",
    "AU": "🇦🇺", "JP": "🇯🇵", "IN": "🇮🇳", "BR": "🇧🇷", "NL": "🇳🇱",
    "Unknown": "🌐"
}

def card_svg(width, height, title, value, subtitle="", color="#58a6ff", icon=""):
    return f'''<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    .title {{ font-family: 'Inter', sans-serif; font-size: 11px; fill: #{COLORS['text_secondary']}; text-transform: uppercase; letter-spacing: 0.5px; }}
    .value {{ font-family: 'Inter', sans-serif; font-size: 28px; font-weight: 700; fill: {color}; }}
    .subtitle {{ font-family: 'Inter', sans-serif; font-size: 10px; fill: #{COLORS['subtext']}; }}
  </style>
  <rect width="{width}" height="{height}" rx="8" fill="{COLORS['card_bg']}"/>
  <rect width="{width}" height="{height}" rx="8" fill="none" stroke="{COLORS['border']}" stroke-width="1"/>
  {icon}
  <text x="12" y="22" class="title">{title}</text>
  <text x="12" y="48" class="value">{value}</text>
  <text x="12" y="62" class="subtitle">{subtitle}</text>
</svg>'''

def bar_svg(width, height, data, title=""):
    if not data:
        return f'''<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">
  <rect width="{width}" height="{height}" rx="8" fill="{COLORS['card_bg']}"/>
  <text x="{width//2}" y="{height//2+4}" text-anchor="middle" fill="{COLORS['text_secondary']}" font-size="12">No data yet</text>
</svg>'''
    
    max_val = max(data.values()) if data else 1
    bar_w = (width - 24) / max(len(data), 1)
    bars = ""
    x = 12
    for k, v in sorted(data.items()):
        h = max(4, int((v / max_val) * (height - 40)))
        bars += f'<rect x="{x}" y="{height - 16 - h}" width="{max(2, bar_w - 2)}" height="{h}" rx="2" fill="{COLORS['blue']}"/>'
        x += bar_w
    
    title_el = f'<text x="12" y="18" font-family="Inter, sans-serif" font-size="11" fill="{COLORS["text_secondary"]}">{title}</text>' if title else ""
    
    return f'''<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">
  <rect width="{width}" height="{height}" rx="8" fill="{COLORS['card_bg']}"/>
  <rect width="{width}" height="{height}" rx="8" fill="none" stroke="{COLORS['border']}" stroke-width="1"/>
  {title_el}
  {bars}
</svg>'''

def list_svg(width, height, items, title, color="#58a6ff"):
    lines = ""
    y = 28
    for label, value in items:
        lines += f'''<text x="12" y="{y}" font-family="Inter, sans-serif" font-size="12" fill="{COLORS['text']}">{label}</text>
<text x="{width-12}" y="{y}" font-family="Inter, sans-serif" font-size="12" fill="{color}" text-anchor="end">{value}</text>'''
        y += 18
    
    title_el = f'<text x="12" y="18" font-family="Inter, sans-serif" font-size="11" fill="{COLORS["text_secondary"]}" text-transform="uppercase">{title}</text>' if title else ""
    
    return f'''<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">
  <rect width="{width}" height="{height}" rx="8" fill="{COLORS['card_bg']}"/>
  <rect width="{width}" height="{height}" rx="8" fill="none" stroke="{COLORS['border']}" stroke-width="1"/>
  {title_el}
  {lines}
</svg>'''

def render():
    with open("analytics_data.json") as f:
        data = json.load(f)
    
    # Cards
    count_card = card_svg(180, 70, "Total Views", data['count'], f"{data['hourly']} views/hour", COLORS['blue'])
    sources_card = card_svg(180, 70, "Top Source", data['sources'][0][0] if data['sources'] else "N/A", f"{data['sources'][0][1] if data['sources'] else 0} visits", COLORS['green'])
    country_card = card_svg(180, 70, "Top Country", FLAGS.get(data['countries'][0][0], "🌐") + " " + data['countries'][0][0] if data['countries'] else "🌐 Unknown", f"{data['countries'][0][1] if data['countries'] else 0} visits", COLORS['purple'])
    
    with open("cards/total_views.svg", "w") as f: f.write(count_card)
    with open("cards/sources.svg", "w") as f: f.write(sources_card)
    with open("cards/country.svg", "w") as f: f.write(country_card)
    
    # Bar chart
    bar = bar_svg(540, 120, data['hours'], "24-Hour Activity")
    with open("cards/hourly.svg", "w") as f: f.write(bar)
    
    # Lists
    devices_list = [(d.title(), str(v)) for d, v in data['devices']]
    browsers_list = [(b, str(v)) for b, v in data['browsers']]
    
    devices_svg = list_svg(260, 100, devices_list, "Devices", COLORS['orange'])
    browsers_svg = list_svg(260, 100, browsers_list, "Browsers", COLORS['red'])
    
    with open("cards/devices.svg", "w") as f: f.write(devices_svg)
    with open("cards/browsers.svg", "w") as f: f.write(browsers_svg)
    
    print("Cards generated!")

if __name__ == "__main__":
    render()
