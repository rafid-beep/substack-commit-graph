# Substack commit graph

A GitHub-style contribution heatmap for your Substack writing. Own posts show green, guest posts on other Substacks show purple.

Hosted free on GitHub Pages, refreshes daily via GitHub Actions.

## Quick start (fork-and-go)

1. **Fork** this repo.
2. Edit `config.yml`:
   ```yaml
   byline: "Your Name"          # how your name appears in author bylines
   own_publications:
     - https://you.substack.com
   guest_publications:           # other Substacks you've contributed to
     - https://someone.substack.com
   ```
3. In your fork, go to **Settings → Pages** and set **Source: GitHub Actions**.
4. Go to **Actions**, enable workflows, and run **Update writing activity** once manually.
5. Open the URL shown under Settings → Pages.

That's it. The cron runs daily at 06:00 UTC and republishes the site.

## How guest-post detection works

For each `guest_publications` entry, the fetcher pulls that Substack's RSS feed and keeps only posts whose author matches your `byline` (case-insensitive, exact match). Substack RSS exposes `<author>` and `<dc:creator>`, both are checked.

You need to add the publication to the list manually — there's no automatic discovery. Submit a PR if you want to add a contribution.

## Run locally

```bash
pip install -r requirements.txt
python3 fetch.py
python3 -m http.server 8000
# open http://localhost:8000
```

## Limitations

- Substack RSS typically returns only the ~20 most recent posts per publication, so the heatmap fills in gradually as you publish — historical archives further back than that won't appear.
- One byline string per repo. If you write under multiple names, fork twice.
