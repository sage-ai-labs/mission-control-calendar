# Toggle Calendar Deployment

This repo contains a static calendar page at `index.html`.

## How auto-refresh works

The page now prefers local same-origin data from:

- `data/mission-control.json`

That JSON file is generated from the Google Sheet by:

- `scripts/sync_toggle_calendar.py`

If you push this project to a GitHub repository, the included workflow:

- `.github/workflows/sync-toggle-calendar.yml`

will refresh the JSON file every 30 minutes and commit changes automatically.

## Recommended GitHub Pages setup

1. Create a GitHub repo and push this folder into it.
2. In GitHub, enable Pages for the branch you want to publish from.
3. Publish from the root of the repository.
4. Open `index.html` from the Pages URL.

## Notes

- You do not need PRs for data refreshes if you keep the workflow committing directly to the default branch.
- You will still use normal PRs if you want review for code or design changes.
- The page still has embedded fallback data and a direct Google Sheets fetch fallback, but Pages should usually use the generated local JSON first.
