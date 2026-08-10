# djangocms-ndthemev4

Django **6.1** + django CMS **5.1** base template with Notre Dame Web Theme v4 integration (in progress).

## Quick start (Docker)

Requires Docker Desktop running.

```bash
docker compose -f local.yml build
docker compose -f local.yml up
```

App: http://localhost:8000  
Mailhog: http://localhost:8025

Create a superuser:

```bash
docker compose -f local.yml run --rm django python manage.py createsuperuser
```

## Database

**PostgreSQL 17** (Compose service `postgres`). SQLite is not used.

`DATABASE_URL` is required and is assembled by the Django entrypoint from `POSTGRES_*` in `.envs/.local/.postgres`.

## Quick start (local venv against Compose Postgres)

```bash
docker compose -f local.yml up -d postgres redis
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements/local.txt
export DATABASE_URL=postgres://debug:debug@127.0.0.1:5432/djangocms_ndthemev4
# Publish Postgres to the host first (see local.yml ports) or use Docker-only workflow above.
python manage.py migrate
```

## Stack

- Local: django, postgres, mailhog, redis, celeryworker, celerybeat
- Production: nginx, django, postgres, redis, celeryworker, celerybeat
- Optional Okta via `OKTA_AUTH=True` (see plan / later milestones)

## M6 goirish demo site (local QA)

Reset the database and seed a full browsable demo site:

```bash
docker compose -f local.yml down -v
docker compose -f local.yml up -d
docker compose -f local.yml exec django python manage.py migrate
docker compose -f local.yml exec django python manage.py goirish --fresh --demo-superuser
```

Demo login: **admin** / **changeme**

`goirish` creates Home (NDT banner + stats), News/Events/People landings with sample content, About, Archive, and the plugin/component showcase pages. Use `--no-showcases` for a faster seed, or `--combined` for a single News & Events landing page.

Re-run on an existing database with `--fresh` to wipe pages and rebuild.

## M4 plugin showcase (local QA)

After `goirish`, the plugin review pages are included automatically. To rebuild showcases only:

```bash
docker compose -f local.yml exec django python manage.py seed_plugin_showcase
```

Pages:

- http://localhost:8000/en/plugin-showcase/
- http://localhost:8000/en/plugin-showcase-side-nav/

Re-run safely; showcase placeholders are cleared and rebuilt each time.

## M5 component showcase (local QA)

The component review page is included in `goirish`. To rebuild it only:

```bash
docker compose -f local.yml exec django python manage.py seed_components_showcase
```

Page:

- http://localhost:8000/en/component-showcase/

Re-run safely; the showcase placeholder is cleared and rebuilt each time.

**M5 component plugins** — full stable [NDT4 Components](https://webtheme.nd.edu/?path=/docs/components-about-components--docs) library:

| Category | Plugins |
|----------|---------|
| **NDT / Content** | Accordion (+ item), Notice, Heading, Quote, Stat list (+ stat), Tabs (+ panel), List (+ item), Table, Timeline (+ item), FAQ (+ item), Dialog, Footnote list (+ item), Button, Byline, Icon, Sticker, Social share, Video button |
| **NDT / Layout** | Banner (+ image, accordion panel, cards, gallery child), Page header, Nav anchor (+ item), Pagination (+ item), Button group/list (+ item), Icon button, Lede button |
| **NDT / Cards** | Card list; Default, News, Event, Featured, People, Media mention, Media mention (quoted), Byline item |
| **NDT / Media** | Gallery (+ item), Image single, Image multiple (+ item), Video, Avatar |
| **NDT / Forms** | Form (+ field), Search form |

**P0 chrome** (template-level, not duplicate plugins): breadcrumb, page title placeholder, primary/sidebar navigation, site header/footer.

**Deferred** (Storybook `coming` or unstable): Banner group, button group border/active variants, news card image-right.

After adding new plugin classes, restart the Django container so they register in the plugin pool.

## Theme assets (NDT 4.0)

- CSS: `https://conductor.nd.edu/stylesheets/themes/ndt/4.0/ndt.css`
- JS: `https://conductor.nd.edu/javascripts/themes/ndt/4.0/ndt.js`
- Docs: https://webtheme.nd.edu/
