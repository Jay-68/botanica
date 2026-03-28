# 🌿 Botanica

A Django project combining two connected apps:
- **The Journal** — a narrative blog for botanical essays and field notes
- **The Grimoire** — a structured living archive of plant knowledge

---

## Quick Start

```bash
# 1. Clone / place the project folder
cd botanica

# 2. Create a virtual environment
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 3. Run setup (installs deps, migrates, seeds data, starts server)
bash setup_and_run.sh
```

Or manually:
```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_data
python manage.py runserver
```

- Admin: http://127.0.0.1:8000/admin/ — `admin / botanica2024`
- Journal: http://127.0.0.1:8000/blog/
- Grimoire: http://127.0.0.1:8000/grimoire/

---

## Project Structure

```
botanica/
├── botanica/           # Project config (settings, urls, wsgi)
├── blog/               # Blog app
│   ├── models.py       # Post, Category, Tag, Series
│   ├── views.py
│   ├── urls.py
│   └── admin.py
├── grimoire/           # Grimoire app
│   ├── models.py       # Plant, PlantFamily, PlantProperty, PlantImage, ObservationLog
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   └── management/commands/seed_data.py
├── templates/
│   ├── base/           # base.html, home.html
│   ├── blog/           # post_list, post_detail, category, tag, series
│   └── grimoire/       # plant_list, plant_detail, property
├── static/
│   ├── css/main.css    # Full design system
│   └── js/main.js
├── media/              # Uploaded images (created at runtime)
├── requirements.txt
└── setup_and_run.sh
```

---

## Features Built

### ✅ Blog App
| Feature | Status |
|---|---|
| Posts with title, body, excerpt, featured image | ✅ |
| Publish / Draft control | ✅ |
| Categories & filtering | ✅ |
| Tags & filtering | ✅ |
| Author attribution | ✅ |
| Series (Field Reflections, Plant Studies…) | ✅ |
| Estimated reading time | ✅ |
| Related posts | ✅ |
| Full-text search | ✅ |
| Post tone: Essay / Journal / Article | ✅ |

### ✅ Grimoire App
| Feature | Status |
|---|---|
| Plant entries with scientific + common names | ✅ |
| Plant family taxonomy | ✅ |
| Full taxonomy (kingdom, order, genus, species) | ✅ |
| Layer 1: Scientific (morphology, habitat, distribution) | ✅ |
| Layer 2: Practical (medicinal, culinary, other uses) | ✅ |
| Layer 3: Observational (field notes, locations, seasonal patterns) | ✅ |
| Layer 4: Symbolic / personal reflections | ✅ |
| Preparation methods | ✅ |
| Warnings & contraindications | ✅ |
| Image gallery (per plant) | ✅ |
| Observation logs (dated, with coordinates) | ✅ |
| Alphabetical browsing | ✅ |
| Filter by edibility / use | ✅ |
| Filter by properties (tag-like attributes) | ✅ |
| Full-text search | ✅ |
| Random plant discovery | ✅ |
| Related species links | ✅ |

### ✅ Blog–Grimoire Connection
| Feature | Status |
|---|---|
| Blog posts can reference multiple plants | ✅ |
| "Referenced Plants" section in post detail | ✅ |
| "From the Journal" section in plant detail | ✅ |
| Navigation between blog ↔ grimoire | ✅ |

---

## Design System

- **Serif**: Cormorant Garamond — for the grimoire, plant pages, body text
- **Sans-serif**: Jost — for navigation, labels, metadata
- **Palette**: cream/parchment base, charcoal text, deep green accents, muted gold
- **Grimoire feel**: section markers (✦ I, ✦ II…), taxonomy tables, manuscript-like sections
- **Blog feel**: clean, breathable, generous white space, subtle hover effects

---

## Adding Content

### Via Admin
Go to http://127.0.0.1:8000/admin/ and create:
- **Plants** (Grimoire → Plants) — add all 5 knowledge layers
- **Plant Images** (inline on plant form)
- **Observation Logs** (inline on plant form)
- **Posts** (Blog → Posts) — link to plants via "Referenced Plants"

### Via the seed command
```bash
python manage.py seed_data
```
Creates sample plants, posts, observations, categories, and tags.

---

## Extending

- **Add a map**: ObservationLog stores lat/lon — integrate Leaflet.js
- **Add rich text**: Install `django-ckeditor` or `django-markdownx` for body fields
- **Add image optimization**: Use `easy-thumbnails` or `Pillow` resizing
- **Add RSS feed**: Django's `django.contrib.syndication` for the blog
- **Add newsletter**: Integrate Mailchimp or a simple email model
- **Deploy**: Add `gunicorn`, `whitenoise`, set `DEBUG=False`, configure `SECRET_KEY` from env
