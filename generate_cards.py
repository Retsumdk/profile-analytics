FLAGS = {
    'US': 'US', 'DE': 'DE', 'GB': 'GB', 'FR': 'FR', 'CA': 'CA',
    'AU': 'AU', 'JP': 'JP', 'IN': 'IN', 'BR': 'BR', 'NL': 'NL',
    'Unknown': 'UN'
}

#!/usr/bin/env python3
import json

def card_svg(width, height, title, value, subtitle="", color="#58a6ff"):
    fill_color = color.lstrip('#')
    return f'''<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">
  <rect width="{width}" height="{height}" rx="8" fill="#161b22"/>
  <rect width="{width}" height="{height}" rx="8" fill="none" stroke="#30363d" stroke-width="1"/>
  <text x="12" y="22" font-family="Arial, sans-serif" font-size="11" fill="#8b949e" text-transform="uppercase">{title}</text>
  <text x="12" y="48" font-family="Arial, sans-serif" font-size="28" font-weight="700" fill="#{fill_color}">{value}</text>
  <text x="12" y="62" font-family="Arial, sans-serif" font-size="10" fill="#6e7681">{subtitle}</text>
</svg>'''

def bar_svg(width, height, data, title=""):
    if not data:
        return f'''<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">
  <rect width="{width}" height="{height}" rx="8" fill="#161b22"/>
  <text x="{width//2}" y="{height//2+4}" text-anchor="middle" fill="#8b949e" font-size="12">No data yet</text>
</svg>'''
    
    max_val = max(data.values()) if data else 1
    bar_w = (width - 24) / max(len(data), 1)
    bars = ""
    x = 12
    for k, v in sorted(data.items()):
        h = max(4, int((v / max_val) * (height - 40)))
        bars += f'<rect x="{int(x)}" y="{height - 16 - h}" width="{max(2, bar_w - 2)}" height="{h}" rx="2" fill="#3498db"/>'
        x += bar_w
    
    title_el = f'<text x="12" y="18" font-family="Arial, sans-serif" font-size="11" fill="#8b949e">{title}</text>' if title else ""
    
    return f'''<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">
  <rect width="{width}" height="{height}" rx="8" fill="#161b22"/>
  <rect width="{width}" height="{height}" rx="8" fill="none" stroke="#30363d" stroke-width="1"/>
  {title_el}
  {bars}
</svg>'''

def list_svg(width, height, items, title, color="#58a6ff"):
    lines = ""
    y = 28
    fill_color = color.lstrip('#')
    for label, value in items:
        lines += f'<text x="12" y="{y}" font-family="Arial, sans-serif" font-size="12" fill="#c9d1d9">{label}</text>'
        lines += f'<text x="{width-12}" y="{y}" font-family="Arial, sans-serif" font-size="12" fill="#{fill_color}" text-anchor="end">{value}</text>'
        y += 18
    
    title_el = f'<text x="12" y="18" font-family="Arial, sans-serif" font-size="11" fill="#8b949e">{title}</text>' if title else ""
    
    return f'''<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">
  <rect width="{width}" height="{height}" rx="8" fill="#161b22"/>
  <rect width="{width}" height="{height}" rx="8" fill="none" stroke="#30363d" stroke-width="1"/>
  {title_el}
  {lines}
</svg>'''

def render():
    with open("analytics_data.json") as f:
        data = json.load(f)
    
    # Cards
    count_card = card_svg(180, 70, "Total Views", data['count'], f"{data['hourly']} views/hour", "#3498db")
    sources_card = card_svg(180, 70, "Top Source", data['sources'][0][0] if data['sources'] else "N/A", f"{data['sources'][0][1] if data['sources'] else 0} visits", "#2ea043")
    country_card = card_svg(180, 70, "Top Country", FLAGS.get(data['countries'][0][0], "UN") + " " + data['countries'][0][0] if data['countries'] else "UN Unknown", f"{data['countries'][0][1] if data['countries'] else 0} visits", "#a371f7")
    
    with open("cards/total_views.svg", "w") as f: f.write(count_card)
    with open("cards/sources.svg", "w") as f: f.write(sources_card)
    with open("cards/country.svg", "w") as f: f.write(country_card)
    
    # Bar chart
    bar = bar_svg(540, 120, data.get('hours', {}), "24-Hour Activity")
    with open("cards/hourly.svg", "w") as f: f.write(bar)
    
    # Lists
    devices_list = [(d.title(), str(v)) for d, v in data['devices']]
    browsers_list = [(b, str(v)) for b, v in data['browsers']]
    
    devices_svg = list_svg(260, 100, devices_list, "Devices", "#f0883e")
    browsers_svg = list_svg(260, 100, browsers_list, "Browsers", "#f85149")
    
    with open("cards/devices.svg", "w") as f: f.write(devices_svg)
    with open("cards/browsers.svg", "w") as f: f.write(browsers_svg)
    
    print("Cards generated!")

if __name__ == "__main__":
    render()
