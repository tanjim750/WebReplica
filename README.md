# WebReplica

WebReplica is a small Python CLI that clones a website's HTML pages into a local `output/<domain>` folder. It crawls same-domain links, saves each HTML page, and rewrites internal links to point to the saved files so you can browse the snapshot locally.

## How It Works

- Validates the starting URL.
- Crawls same-domain pages via `href` links.
- Saves each page as an `.html` file in `output/<domain>`.
- Rewrites internal links to the local filenames.

Note: The current implementation only saves HTML. CSS, JS, and other assets are discovered but not downloaded yet.

## Requirements

- Python 3.9+
- Packages: `requests`, `beautifulsoup4`, `colorama`

## Setup

1. Create and activate a virtual environment.
2. Install dependencies.

```bash
python -m venv .venv
source .venv/bin/activate
pip install requests beautifulsoup4 colorama
```

## Usage

Run the CLI and enter a full URL (including `http` or `https`).

```bash
python manage.py
```

Or use the helper script:

```bash
bash replicate.sh
```

Output is written to `output/<domain>`, with the first page saved as `index.html`.

## Project Layout

- `manage.py`: CLI entrypoint and URL validation.
- `replicator/__replica.py`: Crawl loop and page tracking.
- `replicator/__request.py`: HTTP requests and link parsing.
- `replicator/__output.py`: Output directory and HTML rewriting.
- `output/`: Generated snapshots.

## Known Limitations

- Assets (CSS, JS, images, fonts) are not downloaded.
- JavaScript-rendered content is not captured.
- Crawl scope is restricted to the same base domain.

## License

No license file is currently included. Add one if you plan to distribute or reuse this project.
