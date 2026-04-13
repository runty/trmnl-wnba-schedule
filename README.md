# TRMNL WNBA Team Schedule

A TRMNL recipe that displays a visual calendar and schedule of upcoming games for a selected WNBA team.

![WNBA](https://a.espncdn.com/i/teamlogos/wnba/500/ind.png)

## Features

- **Monthly calendar grid** with game days highlighted — wins (black), losses (red), upcoming (black with opponent abbreviation)
- **Upcoming games list** with team logos, aligned table columns, and opponent W-L records
- **Next game detail** — bold first game with venue/city and game preview (season series + last 5 form with 🟢❌ emojis)
- **Injury report** for your team displayed at the bottom of the screen
- **Filter** by home games, away games, or all games
- **All 15 WNBA teams** supported (2026 season including expansion teams)
- **All 4 TRMNL layouts**: full, half horizontal, half vertical, quadrant
- **Sans-serif font** (Inter via Google Fonts)
- **Zero inline styles** — uses TRMNL Framework classes + minimal custom CSS
- Team logos from ESPN CDN (500x500 PNG, full color, transparent background)
- Data updated **twice daily** via GitHub Actions (8am/8pm UTC)

## Layouts

### Full (800x480)
Left side: monthly calendar grid with team logo and W-L record. Game days show opponent abbreviation (upcoming) or opponent + score (completed — black for wins, red for losses). Right side: next game featured with venue, city, and preview line, followed by compact upcoming games list. Injury report spans full width at the bottom.

### Half Horizontal (800x240)
Aligned game table on the left with dates, team logos, short names, records, and times. Large team logo on the right with injury list below. Team name and record in the title bar.

### Half Vertical (400x480)
Team logo centered at top. Next game featured with venue and preview. Compact upcoming games table below. Injury report at the bottom. Team name and record in the title bar.

### Quadrant (400x240)
Compact aligned table of 4 upcoming games with 24px team logos, opponent abbreviations, records, and times. Team name and record in the title bar.

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
│   ├── pages.yml              # Deploy to GitHub Pages (with success check)
│   └── update-data.yml        # Fetch schedules twice daily (8am/8pm UTC)
├── api/teams/                 # Generated JSON (one file per team)
├── scripts/
│   └── fetch_schedule.py      # ESPN API fetcher + calendar builder + preview
├── templates/
│   ├── shared.liquid          # Google Fonts, custom CSS classes, filter logic
│   ├── full.liquid            # Full screen: calendar + upcoming + injuries
│   ├── half_horizontal.liquid # Wide split: game table + logo + injuries
│   ├── half_vertical.liquid   # Tall split: logo + featured game + list + injuries
│   └── quadrant.liquid        # Quarter: compact 4-game table
├── form_fields.yml            # Team selector and game filter
├── settings.yml               # Plugin metadata
└── README.md
```

## WNBA Teams (2026)

Atlanta Dream, Chicago Sky, Connecticut Sun, Dallas Wings, Golden State Valkyries, Indiana Fever, Las Vegas Aces, Los Angeles Sparks, Minnesota Lynx, New York Liberty, Phoenix Mercury, Portland Fire, Seattle Storm, Toronto Tempo, Washington Mystics

## Data Source

Schedule data is fetched from the ESPN public API (`site.api.espn.com`). This is an unofficial, free API that does not require authentication. Data includes:

- Game dates, times, and venues
- Opponent team names, short names, logos, and W-L records
- Home/away designation
- Win/loss results and scores (completed games)
- Season series and last 5 form (next game preview)
- Current team injuries (name, position, status)

## Form Fields

| Field | Type | Description |
|-------|------|-------------|
| Team | Select | All 15 WNBA teams (slug format) |
| Game Filter | Select | All Games / Home Only / Away Only |

## Plugin Icon

Use the WNBA league logo: `https://a.espncdn.com/i/teamlogos/leagues/500/wnba.png`

## Technical Notes

- **Zero inline styles** across all templates — uses TRMNL Framework utility classes (`bg--black`, `text--white`, `text--center`, `image--contain`, `p--`, `gap--`, `flex--`, etc.) with minimal custom CSS in `shared.liquid` only for things the Framework doesn't cover (calendar grid layout, cell sizing, border specifics, table layout)
- Calendar dates are parsed from ESPN's local-time display strings to avoid UTC/local timezone mismatch
- Score result computation is guarded against non-numeric values via `_compute_result()` helper
- Exception handling is per-team (`except Exception`) so one ESPN failure doesn't block other teams
- The `shown == 0` counter pattern is used instead of `forloop.first` to correctly handle filtered game lists
- Pages deployment only triggers on successful data updates (`workflow_run.conclusion == 'success'`)
- Non-WNBA opponents (exhibition games) use the WNBA league logo as fallback
