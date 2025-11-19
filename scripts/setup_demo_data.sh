#!/bin/bash
# Setup script to populate the database with comprehensive demo data

echo "========================================"
echo "TRAJECT DEMO DATA SETUP"
echo "========================================"
echo ""

echo "Step 1: Populating initial demo data..."
python scripts/populate_demo_data.py

echo ""
echo "Step 2: Enhancing demo data with more users..."
python scripts/update_demo_data.py

echo ""
echo "Step 3: Adding portfolio checklists to users..."
python scripts/add_portfolio_checklists.py

echo ""
echo "========================================"
echo "DEMO DATA SETUP COMPLETE!"
echo "========================================"
echo ""
echo "You can now login with any of these accounts (password: demo123):"
echo "  - demo_student"
echo "  - alice_chen"
echo "  - grace_park"
echo "  - henry_brown"
echo ""
echo "Start the server with: python manage.py runserver"
echo ""
