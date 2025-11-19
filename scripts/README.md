# Demo Data Setup Scripts

This directory contains scripts to populate the Traject application with comprehensive demo data.

## Quick Setup

Run all scripts at once:
```bash
bash scripts/setup_demo_data.sh
```

Or run individually in this order:

1. **populate_demo_data.py** - Creates initial users, careers, portfolio items, clubs, courses
2. **update_demo_data.py** - Adds more diverse users and enhanced career/portfolio data
3. **add_portfolio_checklists.py** - Adds portfolio checklist items to demo users with realistic progress

## Demo Accounts

All accounts use password: `demo123`

- **demo_student** - Intermediate level student (33% portfolio complete)
- **alice_chen** - CS Senior at MIT (60% complete)
- **grace_park** - CS Junior at Stanford (100% complete)
- **henry_brown** - CS Senior at UC Berkeley (80% complete)
- **david_kim** - Data Science Junior (60% complete)
- **bob_martinez** - EE Junior (50% complete)
- **carol_johnson** - Business Sophomore (40% complete)
- **emma_wilson** - ME Freshman (0% complete, just started)

## What Gets Created

- **18 users** with diverse profiles and career goals
- **18 careers** across tech, data science, product, design, etc.
- **24 portfolio items** (projects, certifications, internships, competitions)
- **45 clubs** across 4 colleges
- **8 courses** from top universities
- **37 portfolio checklist entries** showing realistic progress

## Features Demonstrated

- AI-powered career recommendations with multi-factor scoring
- Portfolio progress tracking
- Course recommendations based on major
- Club suggestions based on interests
- Personalized dashboard with insights
