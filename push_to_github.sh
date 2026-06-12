#!/bin/bash

# Ensure git is installed
if ! command -v git &> /dev/null; then
    echo "Error: git is not installed on your system. Please install it first."
    exit 1
fi

# Initialize git repository if not already initialized
if [ ! -d ".git" ]; then
    git init -b main
    echo "Initialized empty Git repository."
fi

# Add all project files
git add bot.py requirements.txt .github/workflows/daily.yml

# Create initial commit
git commit -m "Add Pulse bot + GitHub Actions workflow"

echo ""
echo "=========================================================="
echo "Project files committed locally!"
echo "=========================================================="
echo "To push this to your GitHub account (sivaramsajeesh):"
echo "1. Go to https://github.com/new and create a repository named 'pulse-daily-summary-bot'."
echo "2. Run the following commands in this directory:"
echo ""
echo "   git remote add origin https://github.com/sivaramsajeesh/pulse-daily-summary-bot.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo "=========================================================="
