# TRMNL WNBA Team Schedule

A TRMNL recipe that displays a visual calendar and schedule of upcoming games for a selected WNBA team. Choose to see home games only, away games only, or all games.

Data sourced from ESPN and updated twice daily via GitHub Actions.

## Features

- Monthly calendar grid showing game days (full layout)
- Upcoming games list with home/away indicators
- Filter by home, away, or all games
- All 15 WNBA teams supported
- All 4 TRMNL layout sizes (full, half horizontal, half vertical, quadrant)

## Setup

### 1. Fork this repository

### 2. Enable GitHub Pages
- Go to Settings > Pages
- Set source to **GitHub Actions**

### 3. Run the data fetch
- Go to Actions > "Update WNBA Schedule Data" > Run workflow
- This will populate the `api/teams/` directory and deploy to Pages

### 4. Create a Private Plugin on TRMNL
- Go to your TRMNL dashboard > Plugins > New Private Plugin
- Strategy: **Polling**
- Polling URL: `https://YOUR_USERNAME.github.io/trmnl-wnba-schedule/teams/{{ team }}.json`
- Paste the form fields from `form_fields.yml`
- Paste each template from `templates/` into the corresponding layout tab
- Paste `templates/shared.liquid` into the Shared tab

### 5. Test and publish
- Select a team, preview in the editor
- Add to your playlist and verify on your device
- Click "Publish as a Recipe" when ready

## Project Structure

```
trmnl-wnba-schedule/
├── .github/workflows/
│   ├── pages.yml              # Deploy to GitHub Pages
│   └── update-data.yml        # Fetch schedules twice daily
├── api/teams/                 # Generated JSON (one per team)
├── scripts/
│   └── fetch_schedule.py      # ESPN API fetcher
├── templates/
│   ├── shared.liquid          # Common styles and components
│   ├── full.liquid            # Full screen (calendar + list)
│   ├── half_horizontal.liquid # Top/bottom split (compact list)
│   ├── half_vertical.liquid   # Left/right split (compact list)
│   └── quadrant.liquid        # Quarter screen (next game + 3 more)
├── form_fields.yml            # Custom form field definitions
├── settings.yml               # Plugin metadata
└── README.md
```

## WNBA Teams

Atlanta Dream, Chicago Sky, Connecticut Sun, Dallas Wings, Golden State Valkyries, Indiana Fever, Las Vegas Aces, Los Angeles Sparks, Minnesota Lynx, New York Liberty, Phoenix Mercury, Portland Fire, Seattle Storm, Toronto Tempo, Washington Mystics

## Data Source

Schedule data is fetched from the ESPN public API (`site.api.espn.com`). This is an unofficial API that does not require authentication. Data includes game dates, opponents, home/away status, venues, and scores.
