# TRMNL WNBA Team Schedule

A TRMNL recipe that displays a visual calendar and schedule of upcoming games for a selected WNBA team.

![WNBA](https://a.espncdn.com/i/teamlogos/leagues/500/wnba.png)

## Features

- **Monthly calendar grid** with game days highlighted — wins (black), losses (red), upcoming (black with opponent)
- **Upcoming games list** with team logos, aligned columns, and opponent records
- **Next game detail** with bold formatting, venue/city, and game preview (season series + last 5 form with ✅❌ emojis)
- **Injury report** for your team shown at the bottom
- **Filter** by home games, away games, or all
- **All 15 WNBA teams** supported
- **All 4 TRMNL layouts**: full, half horizontal, half vertical, quadrant
- Team logos from ESPN CDN (500x500 PNG, full color, transparent background)
- Data updated **twice daily** via GitHub Actions

## Layouts

### Full (800x480)
Calendar grid on the left with team logo and record. Upcoming games on the right with next game detail (venue, preview), followed by compact game list. Injuries at the bottom spanning full width.

### Half Horizontal (800x240)
Aligned game list on the left, large team logo on the right with injuries below.

### Half Vertical (400x480)
Team logo at top, next game detail with venue and preview, compact game list, injuries at the bottom.

### Quadrant (400x240)
Compact aligned table of 4 upcoming games with team logos and records.

## Setup

### 1. Fork this repository

### 2. Enable GitHub Pages
- Go to Settings > Pages
- Set source to **GitHub Actions**

### 3. Run the data fetch
- Go to Actions > "Update WNBA Schedule Data" > Run workflow
- This populates `api/teams/` and deploys to Pages

### 4. Create a Private Plugin on TRMNL
1. Go to your TRMNL dashboard > Plugins > Private Plugin
2. Strategy: **Polling**
3. Polling URL: `https://YOUR_USERNAME.github.io/trmnl-wnba-schedule/teams/{{team}}.json`
4. Paste the YAML from `form_fields.yml` into Custom Fields
5. Click **Edit Markup** and paste each template:
   - `templates/shared.liquid` → **Shared** tab
   - `templates/full.liquid` → **Full** tab
   - `templates/half_horizontal.liquid` → **Half Horizontal** tab
   - `templates/half_vertical.liquid` → **Half Vertical** tab
   - `templates/quadrant.liquid` → **Quadrant** tab
6. Select your team, save, and **Force Refresh**

### 5. Publish as a Recipe (optional)
- Click the publish icon on your plugin settings
- Choose **Public** (reviewed in 1-2 days) or **Unlisted** (instant link)

## Project Structure

```
trmnl-wnba-schedule/
├── .github/workflows/
│   ├── pages.yml              # Deploy to GitHub Pages
│   └── update-data.yml        # Fetch schedules twice daily (8am/8pm UTC)
├── api/teams/                 # Generated JSON (one file per team)
├── scripts/
│   └── fetch_schedule.py      # ESPN API fetcher + calendar builder
├── templates/
│   ├── shared.liquid          # Common styles (sans-serif font, calendar, layout)
│   ├── full.liquid            # Full screen: calendar + upcoming + injuries
│   ├── half_horizontal.liquid # Wide split: game list + logo + injuries
│   ├── half_vertical.liquid   # Tall split: logo + game list + injuries
│   └── quadrant.liquid        # Quarter: compact 4-game table
├── form_fields.yml            # Team selector, game filter, timezone
├── settings.yml               # Plugin metadata
└── README.md
```

## WNBA Teams

Atlanta Dream, Chicago Sky, Connecticut Sun, Dallas Wings, Golden State Valkyries, Indiana Fever, Las Vegas Aces, Los Angeles Sparks, Minnesota Lynx, New York Liberty, Phoenix Mercury, Portland Fire, Seattle Storm, Toronto Tempo, Washington Mystics

## Data Source

Schedule data is fetched from the ESPN public API (`site.api.espn.com`). This is an unofficial API that does not require authentication. Data includes:

- Game dates, times, and venues
- Opponent team names, logos, and records
- Home/away designation
- Win/loss results and scores (completed games)
- Season series and last 5 form (next game preview)
- Current team injuries

## Form Fields

| Field | Type | Description |
|-------|------|-------------|
| Team | Select | All 15 WNBA teams |
| Game Filter | Select | All Games / Home Only / Away Only |
| Time Zone | Timezone | Local timezone for game times |

## Plugin Icon

Use the WNBA league logo: `https://a.espncdn.com/i/teamlogos/leagues/500/wnba.png`
