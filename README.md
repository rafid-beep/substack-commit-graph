# Substack commit graph

A GitHub-style contribution heatmap for your Substack writing. Own posts show green, guest posts on other Substacks show purple.

Fully client-side. Hosted free on GitHub Pages. No backend, no cron, no API keys.

## Quick start (fork-and-go)

1. **Fork** this repo.
2. Edit `config.json`:
   ```json
   {
     "byline": "Your Name",
     "own_publications": ["https://you.substack.com"],
     "guest_publications": ["https://someone.substack.com"]
   }
   ```
3. In your fork: **Settings → Pages → Source: "Deploy from a branch" → Branch: `main`, folder: `/ (root)`**.
4. Wait ~1 minute, then open the URL shown under Settings → Pages.

That's it. Every page load pulls the latest posts from your feeds.

## How it works

The browser calls Substack's `/api/v1/archive` endpoint (paginated, full history) via [allorigins.win](https://allorigins.win/) — a free public CORS proxy. Results are cached in your browser's `localStorage` for 6 hours so reloads are instant.

- **Own posts** (anything from `own_publications`) show green
- **Guest posts** (anything from `guest_publications` where you appear in `publishedBylines` matching your `byline`) show purple

Full archive — not just the most recent 20.

## Run locally

Just open `index.html` over a local server (file:// will block fetch):
```bash
python3 -m http.server 8000
# open http://localhost:8000
```

## Limitations

- **rss2json free tier**: 10 requests per hour per IP. Plenty for personal use. If you hit the limit the page will show a partial result.
- **One byline string per repo**. Fork twice if you write under multiple names.
- **Guest posts require manual entry**: there's no automatic discovery — you list each publication you've contributed to.
- **RSS history is shallow**: Substack returns ~20 most recent items per feed.

## Roadmap

- Medium support
- Personal site / Ghost support
- Year selector (currently shows trailing 52 weeks)
