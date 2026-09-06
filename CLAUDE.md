# Totally Wanderlost — website

Travel blog and interactive trip maps for [totallywanderlost.com](https://totallywanderlost.com).
Static site built with **Jekyll**, hosted on **Cloudflare Pages**. All data is baked in at
build time — there is no runtime/client data fetching.

## Common commands

| Command | What it does |
|---|---|
| `make setup` | One-time: installs `mise`, then Ruby/Python/Node toolchains + all deps |
| `make build` | `jekyll build` → `build/` (set `env=dev` to skip minification) |
| `make run` | Build + watch + serve on [localhost:8080](http://localhost:8080) via `wrangler pages dev` (`port=1337` to override) |
| `make deploy` | Manual `wrangler pages publish` (CI does this automatically) |
| `make fetch` | Refresh trip data from Polarsteps for every trip in the manifest (see below) |
| `bundle exec jekyll build` | Build directly without the Makefile wrapper |

Toolchain versions are pinned in `.tool-versions` (Ruby 3.2.2, Python 3.10.3, Node 24) and
installed with `mise`. Ruby deps: `bundle`. Python deps: `pipenv`.

## Deployment

- Push to `main` → auto-deploy to production (`.github/workflows/website.yml`).
- Push to any branch → preview at `${branch}.totallywanderlost.pages.dev`.
- `.github/workflows/data.yml` is **manual only** (`workflow_dispatch`); it runs `make fetch`
  and commits any changed trip data.

## Architecture

### Rendering

- `_config.yml`: `source: src`, `destination: build`. Plugins: `jekyll-minifier`,
  `jekyll-sitemap`, plus local plugins in `src/_plugins/`.
- `src/_layouts/default.liquid` — HTML shell, `<head>`, OG/meta tags. The OG block keys off
  `page.layout` (`post` / `step`) and otherwise falls back to site defaults.
- Pages: `src/index.html` (full-bleed map), `src/trips.html` (`/trips` index),
  `src/photos.html` (`/photos` — all photos across all trips), `src/blog.html`,
  `src/about.md`, `src/contact.html`. Blog posts: `src/_posts/*.md` → `/blog/:slug`.
- Styling: `src/assets/css/normalise.css` + `main.css`, with page-specific `<style>` blocks
  inline in layouts/pages. Dark mode via `prefers-color-scheme`. Font Awesome 4.7 from CDN.

### Local plugins (`src/_plugins/`)

- `photo.rb` — Liquid filters `photo_url` / `photo_tag` / `avatar_url` that build ImageKit
  transform URLs. Used for blog featured images and author avatars.
- `trip_pages.rb` — **generator** that builds the trip and step pages from the trip manifest
  + per-trip step data. Replaces the old `jekyll-datapage-generator`. Emits:
  - `/trips/<slug>/` — layout `trip`
  - `/trips/<slug>/<step-key>/` — layout `step`, one per step where
    `state != 'planned' && photos.size > 0`

### Trips & journey data

Each **trip** is one Polarsteps trip. Data is split into:

- **`src/_data/trips.yml`** — hand-authored manifest. List order = display order. Fields:
  `slug`, `polarsteps_id`, `title`, `summary`, `hero` (optional ImageKit path; else the
  first step photo is used), `published` (false → fetched but not built).
- **`src/_data/journeys/<slug>.json`** — one flat array of step objects per trip, written by
  `data/fetch.py`. Auto-loaded by Jekyll as `site.data.journeys.<slug>`. The trip is implied
  by the filename; `trip_pages.rb` stamps `trip_slug`/`trip_title` onto each step page, and
  `map.liquid` stamps `trip_slug` from the manifest when it flattens trips together.

Step object shape (produced by `data/fetch.py`):
`id` (UPPER uuid), `key` (lower uuid — the URL segment), `name`, `description`,
`country`, `arrived` (unix seconds, or `false` for planned), `location` `[lat, lon]`,
`photos[]`, `state` (`visited` | `stopped` | `current` | `planned`).
Photo: `id`, `source_url` (Polarsteps S3), `r2_url`, `url` (ImageKit base), `location`.

`src/_data/flags.yml` maps country name (exactly as it appears in the step data) → flag emoji,
used on step page headings and prev/next labels. Add entries when a new trip introduces new
countries.

### The map (`src/_includes/map.liquid`)

Self-contained: MapLibre GL from unpkg, Jawg vector tiles (light/dark chosen from
`prefers-color-scheme`; access token is in the file). All trip data is inlined at build time.

Include params:
- `mode` — `steps` (default: pins + route) or `photos` (pins per photo).
- `trip` — a slug; limits the map to that one trip. Omitted → every published trip is drawn,
  each as its own colour-graded route (`addTripRoute(coords, suffix)` namespaces the
  sources/layers so routes never join across trips). Markers still merge places within ~100 m
  into one pageable popup, including across trips.
- `step` — a step id; filter to that step (used by the per-step mini-map).
- `height`, `zoom`, `drag`, `trim`.

Route rendering: great-circle arcs, a faint "wandering" line through every step + a bold
"trunk" through legs ≥200 km, direction arrows, green→amber→red gradient across trip progress
(resets per trip), collision-thinned pins. Step popups link to `/trips/<slug>/<key>`.

### Images

Originals live in the Cloudflare **R2** bucket `totally-wanderlost` under
`images/journey/step/<STEP_ID>/<PHOTO_ID>` (no trip namespace — Polarsteps step UUIDs are
globally unique). All display goes through **ImageKit** transforms
(`https://ik.imagekit.io/totallywanderlost/r2/...?tr=w-,h-,fo-`).

### Data pipeline (`data/fetch.py`)

`make fetch` → `python data/fetch.py --manifest src/_data/trips.yml --out-dir src/_data/journeys`.
For each manifest entry it:
1. `GET https://api.polarsteps.com/trips/<polarsteps_id>` (public, unauthenticated).
2. Parses visited + planned steps, marks the last visited step `current`.
3. Diffs against the existing `journeys/<slug>.json` and uploads new / deletes removed photos
   in R2 (`sync_images_to_r2`, boto3 S3 API, creds from `CLOUDFLARE_*` env vars).
4. Rewrites `journeys/<slug>.json`.

Adding a trip: append an entry to `src/_data/trips.yml` (start with `published: false`), run
`make fetch`, commit the new `src/_data/journeys/<slug>.json`. No template/config changes needed.

### URLs & redirects

- `/trips`, `/trips/<slug>/`, `/trips/<slug>/<step-key>/`.
- `src/_redirects` is a plain static file: `/where`, `/journey`, `/journey/*` all `301` to
  `/trips`. Old per-step links are not preserved individually.

## Conventions

- Keep new Liquid/JS in the style of the surrounding file (the map and lightbox are vanilla
  JS, no build step, no framework).
- Everything a published page needs must be self-contained or build-time-inlined; there is no
  client-side data fetching.
- Prefer reusing the shared includes: `map.liquid`, `photo_grid.liquid`,
  `photo_lightbox.liquid`, and the `photo_url` filter.

## Recent work

**Multi-trip support** (Sept 2026). The site was previously hard-wired to a single Polarsteps
trip (`src/_data/journey.json`, one `page_gen` block, `/journey/<key>` pages). Changed to:

- Per-trip data (`src/_data/trips.yml` manifest + `src/_data/journeys/<slug>.json`); a step's
  trip is implied by the filename, not stored on the step.
- `data/fetch.py` loops the manifest; `make fetch` / `data.yml` take no trip args.
- New `src/_plugins/trip_pages.rb` generator replaces `jekyll-datapage-generator`
  (removed from `Gemfile` / `_config.yml`).
- `src/_layouts/journey.html` → `src/_layouts/step.html`, scoped to one trip; new
  `src/_layouts/trip.html` and `src/trips.html`.
- `src/_includes/map.liquid` draws one route per trip; new `trip=` param.
- `src/journey.html` removed; `src/_redirects` sends the old `/journey` paths to `/trips`.
