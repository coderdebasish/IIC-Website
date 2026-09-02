# IIC – IEM Website & Management System
## Master Implementation Plan

> **Project Start:** 2026-09-02 | **Lead:** Antigravity AI Agent
> **Repository:** `d:\Programming Project\IIC Website`
> **Current Phase:** Phase 1 – Architecture & Foundation

---

## Project Vision

Build a modern, premium, production-ready website and management system for the **Institution's Innovation Council (IIC) of IEM**. The system combines a stunning public-facing website with a powerful admin panel, enabling IIC councils to manage all content without developer intervention.

---

## Technology Decisions & Rationale

| Layer | Technology | Reason |
|---|---|---|
| Backend | **Python 3.14 + Django 5.x** | Mature, batteries-included, excellent ORM, strong auth |
| Database | **PostgreSQL 16** | Robust relational DB, excellent with Django |
| Frontend | **Django Templates + Tailwind CSS v4 (CDN)** | Fast development, no build step needed initially |
| Rich Editor | **django-ckeditor-5** (or TipTap via JS) | Block-based rich content for event pages |
| Interactivity | **HTMX** | Lightweight, Django-native, avoids full SPA complexity |
| File Storage | **Django Media (local dev) → Cloudflare R2 or S3 (prod)** | Abstracted via `django-storages` |
| Auth | **Django built-in auth** + custom user model | Extend AbstractUser for roles |
| QR Scanning | **html5-qrcode** (JS library via CDN) | No backend dependency, client-side scanning |
| CSV/Excel Import | **pandas + openpyxl** | Robust import/validation |
| Deployment | **Docker Compose** | Nginx + Gunicorn + Django + PostgreSQL |
| Static Files | **WhiteNoise** (dev/staging) → Nginx (prod) | |

> **Note on Tailwind:** Using Tailwind CSS v4 via CDN `@tailwindcss/browser` for development, then switching to CLI build for production. No node build pipeline required for initial development.

---

## Project Structure (Final Target)

```
iic_website/                    ← Django project root
├── manage.py
├── requirements.txt
├── requirements-dev.txt
├── .env.example
├── .env                        ← local secrets (gitignored)
├── .gitignore
├── IMPLEMENTATION_PLAN.md      ← this file (copy in repo)
│
├── config/                     ← Django project package
│   ├── __init__.py
│   ├── settings/
│   │   ├── __init__.py
│   │   ├── base.py             ← shared settings
│   │   ├── development.py      ← dev overrides
│   │   └── production.py       ← prod overrides
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── apps/
│   ├── core/                   ← Base templates, site settings, utilities
│   ├── users/                  ← Custom user model, auth, admin management
│   ├── events/                 ← Event system, lifecycle, content, gallery, reports
│   ├── certificates/           ← Certificate records, verification, bulk import
│   ├── council/                ← Council members, council years
│   ├── achievements/           ← IIC achievements & milestones
│   ├── gallery/                ← General gallery albums & images
│   └── announcements/          ← Site announcements
│
├── templates/
│   ├── base.html               ← Master public layout
│   ├── admin_base.html         ← Master admin layout
│   ├── core/
│   ├── users/
│   ├── events/
│   ├── certificates/
│   ├── council/
│   ├── achievements/
│   ├── gallery/
│   └── announcements/
│
├── static/
│   ├── css/
│   │   └── custom.css
│   ├── js/
│   │   ├── main.js
│   │   ├── qr-scanner.js
│   │   └── htmx.min.js
│   └── images/
│       └── logo_placeholder.png
│
├── media/                      ← Uploaded files (gitignored)
│
├── docker/
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── docker-compose.prod.yml
│   ├── nginx/
│   │   └── nginx.conf
│   └── entrypoint.sh
│
└── docs/
    └── IMPLEMENTATION_PLAN.md  ← Symlink or copy
```

---

## Database Schema (Core Tables)

### `users_customuser` (extends AbstractUser)
| Field | Type | Notes |
|---|---|---|
| id | PK | |
| username | CharField(unique) | |
| email | EmailField(unique) | |
| role | CharField | choices: `admin`, `super_admin` |
| is_active | BooleanField | |
| date_joined | DateTimeField | |

### `core_sitesettings` (singleton)
| Field | Type | Notes |
|---|---|---|
| site_name | CharField | |
| tagline | CharField | |
| logo | ImageField | |
| favicon | ImageField | |
| contact_email | EmailField | |
| contact_phone | CharField | |
| address | TextField | |
| facebook_url | URLField | |
| instagram_url | URLField | |
| twitter_url | URLField | |
| linkedin_url | URLField | |
| youtube_url | URLField | |
| footer_text | TextField | |
| hero_tagline | CharField | |
| hero_description | TextField | |
| updated_at | DateTimeField | |

### `events_event`
| Field | Type | Notes |
|---|---|---|
| id | PK | |
| title | CharField | |
| slug | SlugField(unique) | URL-safe identifier |
| short_description | TextField | |
| poster | ImageField | |
| start_date | DateTimeField | |
| end_date | DateTimeField(null) | |
| status | CharField | `draft`, `upcoming`, `ongoing`, `completed`, `archived` |
| registration_link | URLField(null) | External Google Form link |
| is_featured | BooleanField | Show on homepage |
| created_at | DateTimeField | |
| updated_at | DateTimeField | |
| created_by | FK(User) | |

### `events_eventcontent`
| Field | Type | Notes |
|---|---|---|
| id | PK | |
| event | FK(Event, one-to-one) | |
| content | TextField | Rich HTML content (CKEditor5) |
| updated_at | DateTimeField | |

### `events_eventstage` (lifecycle)
| Field | Type | Notes |
|---|---|---|
| id | PK | |
| event | FK(Event) | |
| name | CharField | e.g., "Registration Open" |
| stage_order | PositiveIntegerField | ordering |
| start_date | DateField(null) | informational |
| end_date | DateField(null) | informational |
| is_current | BooleanField | manually set by admin |
| is_completed | BooleanField | |
| description | CharField(null) | optional note |

### `events_eventreport`
| Field | Type | Notes |
|---|---|---|
| id | PK | |
| event | FK(Event, one-to-one) | |
| content | TextField | Rich text report |
| pdf_file | FileField(null) | optional PDF upload |
| external_link | URLField(null) | Google Drive, etc. |
| updated_at | DateTimeField | |

### `events_eventgalleryimage`
| Field | Type | Notes |
|---|---|---|
| id | PK | |
| event | FK(Event) | |
| image | ImageField | |
| caption | CharField(null) | |
| order | PositiveIntegerField | |
| uploaded_at | DateTimeField | |

### `certificates_certificate`
| Field | Type | Notes |
|---|---|---|
| id | PK | |
| certificate_id | CharField(unique, indexed) | e.g., IIC-IEM-2026-IDEA-001 |
| event | FK(Event, null) | |
| recipient_name | CharField | |
| certificate_type | CharField | e.g., Participant, Winner, Volunteer |
| issue_date | DateField | |
| status | CharField | `valid`, `revoked`, `expired` |
| notes | TextField(null) | internal admin notes |
| created_at | DateTimeField | |
| updated_at | DateTimeField | |

### `council_councilyear`
| Field | Type | Notes |
|---|---|---|
| id | PK | |
| year_label | CharField | e.g., "2025-2026" |
| is_current | BooleanField | |
| description | TextField(null) | |

### `council_councilmember`
| Field | Type | Notes |
|---|---|---|
| id | PK | |
| council_year | FK(CouncilYear) | |
| name | CharField | |
| role | CharField | e.g., "President", "Faculty Advisor" |
| designation | CharField | |
| member_type | CharField | `faculty`, `student` |
| photo | ImageField(null) | |
| email | EmailField(null) | |
| order_no | PositiveIntegerField | display order |
| is_active | BooleanField | |

### `achievements_achievement`
| Field | Type | Notes |
|---|---|---|
| id | PK | |
| title | CharField | |
| description | TextField | |
| image | ImageField(null) | |
| date | DateField(null) | |
| category | CharField | `award`, `recognition`, `milestone` |
| is_featured | BooleanField | show on homepage |
| created_at | DateTimeField | |

### `gallery_album`
| Field | Type | Notes |
|---|---|---|
| id | PK | |
| title | CharField | |
| description | TextField(null) | |
| cover_image | ImageField(null) | |
| created_at | DateTimeField | |

### `gallery_image`
| Field | Type | Notes |
|---|---|---|
| id | PK | |
| album | FK(Album) | |
| image | ImageField | |
| caption | CharField(null) | |
| order | PositiveIntegerField | |
| uploaded_at | DateTimeField | |

### `announcements_announcement`
| Field | Type | Notes |
|---|---|---|
| id | PK | |
| title | CharField | |
| content | TextField | |
| link | URLField(null) | optional CTA link |
| is_active | BooleanField | publish/unpublish |
| show_on_home | BooleanField | |
| created_at | DateTimeField | |
| expires_at | DateTimeField(null) | auto-hide after date |

### `users_adminactivitylog`
| Field | Type | Notes |
|---|---|---|
| id | PK | |
| admin_user | FK(User) | |
| action | CharField | |
| model_name | CharField | |
| object_id | CharField | |
| details | TextField | |
| created_at | DateTimeField | |

---

## Public URL Structure

```
/                               → Homepage
/about/                         → About IIC
/events/                        → Events list (upcoming + past)
/events/<slug>/                 → Event detail page
/council/                       → Council members (current)
/council/<year>/                → Council members (by year)
/achievements/                  → Achievements list
/gallery/                       → Gallery albums
/gallery/<album-id>/            → Album detail
/certificates/                  → Certificate verification page
/contact/                       → Contact & social
```

## Admin URL Structure

```
/admin-panel/                   → Dashboard
/admin-panel/login/             → Admin login
/admin-panel/events/            → Events list
/admin-panel/events/create/     → Create event
/admin-panel/events/<id>/edit/  → Edit event (basic info)
/admin-panel/events/<id>/content/ → Edit rich content
/admin-panel/events/<id>/stages/  → Manage lifecycle stages
/admin-panel/events/<id>/report/  → Manage report
/admin-panel/events/<id>/gallery/ → Manage gallery
/admin-panel/certificates/      → Certificate management
/admin-panel/certificates/<event>/ → Certificates by event
/admin-panel/certificates/import/ → Bulk import
/admin-panel/council/           → Council management
/admin-panel/achievements/      → Achievements
/admin-panel/gallery/           → General gallery
/admin-panel/announcements/     → Announcements
/admin-panel/settings/          → Site settings
/admin-panel/users/             → Admin user management (super admin only)
```

---

## Implementation Modules & Status

| # | Module | Status | Priority |
|---|---|---|---|
| 1 | Project Setup & Architecture | ✅ IN PROGRESS | CRITICAL |
| 2 | PostgreSQL + Django Configuration | 🔲 NOT STARTED | CRITICAL |
| 3 | Custom User Model + Auth + Roles | 🔲 NOT STARTED | CRITICAL |
| 4 | Core App + Site Settings | 🔲 NOT STARTED | HIGH |
| 5 | Base Templates + Design System | 🔲 NOT STARTED | HIGH |
| 6 | Event System (models + admin CRUD) | 🔲 NOT STARTED | HIGH |
| 7 | Event Rich Content (CKEditor5) | 🔲 NOT STARTED | HIGH |
| 8 | Event Lifecycle / Progress Bar | 🔲 NOT STARTED | HIGH |
| 9 | Event Registration Links | 🔲 NOT STARTED | MEDIUM |
| 10 | Event Reports & Galleries | 🔲 NOT STARTED | MEDIUM |
| 11 | Certificate Database & Bulk Import | 🔲 NOT STARTED | HIGH |
| 12 | Certificate Verification (Public) | 🔲 NOT STARTED | HIGH |
| 13 | QR Code Scanning (Client-side) | 🔲 NOT STARTED | HIGH |
| 14 | Council Management | 🔲 NOT STARTED | MEDIUM |
| 15 | Achievements Module | 🔲 NOT STARTED | MEDIUM |
| 16 | General Gallery Module | 🔲 NOT STARTED | MEDIUM |
| 17 | Announcements Module | 🔲 NOT STARTED | MEDIUM |
| 18 | Homepage Integration | 🔲 NOT STARTED | HIGH |
| 19 | Public Pages Design Refinement | 🔲 NOT STARTED | MEDIUM |
| 20 | Security Review | 🔲 NOT STARTED | HIGH |
| 21 | Performance Optimization | 🔲 NOT STARTED | MEDIUM |
| 22 | Docker / Deployment Preparation | 🔲 NOT STARTED | HIGH |

---

## Phase 1: Project Setup (CURRENT)

### Steps
1. [x] Analyze requirements
2. [x] Create implementation plan
3. [ ] Install Python dependencies (Django, psycopg2, etc.)
4. [ ] Initialize Django project with split settings
5. [ ] Configure PostgreSQL database connection
6. [ ] Set up `.env` pattern with `python-decouple`
7. [ ] Initialize git repository
8. [ ] Create all Django apps
9. [ ] Configure INSTALLED_APPS, MEDIA, STATIC
10. [ ] Create `requirements.txt` and `.gitignore`
11. [ ] Validate project runs with `runserver`

### Python Dependencies (requirements.txt)
```
Django>=5.2,<6.0
psycopg2-binary>=2.9
Pillow>=10.0
python-decouple>=3.8
whitenoise>=6.7
gunicorn>=22.0
django-ckeditor-5>=0.2
pandas>=2.0
openpyxl>=3.1
django-htmx>=1.17
```

---

## Technical Decisions & Notes

1. **Rich Text Editor**: Using `django-ckeditor-5` for event content and reports. CKEditor 5 provides a Word-like editing experience with image upload, tables, links, headings. No separate frontend framework needed.

2. **Tailwind CSS**: Using Tailwind CSS v4 via `@tailwindcss/browser` CDN for development. For production, will set up `tailwindcss` CLI to generate a purged CSS file. This avoids requiring a Node.js build pipeline in the Django container.

3. **QR Scanning**: Client-side only using `html5-qrcode` JavaScript library. The scanned certificate ID is passed to the Django verification endpoint. No server-side QR processing needed.

4. **Certificate PDFs**: NOT stored on server. The system only stores certificate metadata records. Actual PDFs are distributed externally (Google Drive, etc.).

5. **Admin Panel**: Custom-built Django admin panel using our own templates (NOT Django's default admin). This ensures a premium, user-friendly experience appropriate for non-technical council members.

6. **HTMX**: Used for search/filter UIs, certificate verification lookup, and announcement management — anywhere a partial page update improves UX without full-page reload.

7. **File Storage**: Local `MEDIA_ROOT` for development. In production, `django-storages` with S3-compatible storage (Cloudflare R2 preferred) or simply served by Nginx.

8. **Settings Split**: `config/settings/base.py` + `development.py` + `production.py`. `DJANGO_SETTINGS_MODULE` controlled via `.env`.

9. **Slug Generation**: Auto-generated from event title on creation. Admin can override. Must be unique.

10. **Admin Activity Log**: Lightweight custom logging (not a full audit trail library). Key actions logged: event created/deleted, certificate imported/revoked, admin added/disabled.

---

## Open Questions / Decisions Pending

> [!IMPORTANT]
> These items need clarification before or during their respective module implementations.

1. **PostgreSQL Access**: Is PostgreSQL installed locally on the dev machine, or should we use Docker for the DB? (Docker not currently installed)
2. **Logo/Branding**: Should we use a placeholder logo or does the user have an IIC-IEM logo to upload?
3. **Domain**: Final domain for production (e.g., `iic.iem.edu.in`) — needed for allowed hosts config
4. **Email**: SMTP server details for any future email notifications?
5. **Existing Data**: Any existing council member data, events, or certificates to migrate?

---

## Environment Requirements Summary

- Python 3.14 ✅ (confirmed installed)
- PostgreSQL 16 — needs installation or Docker
- Git 2.52 ✅ (confirmed installed)
- Node.js 24 ✅ (available but only needed for Tailwind CLI build, optional in dev)
- Docker — not installed (optional, needed for full deployment prep)

---

*Last Updated: 2026-09-02 | Status: Phase 1 – Architecture & Foundation*
