#!/bin/bash
set -e

cd "/Users/olekzhyrko/Desktop/fps tester"

# Remove old git
rm -rf .git 2>/dev/null || true

# Initialize fresh repo
git init

# Configure git
git config user.email "olekzhyrko@test.com"
git config user.name "Olek Zhyrko"

# Add all files
git add .

# Create commit
git commit -m "FPS Tester - Complete desktop and web performance analysis tool"

# Add remote
git remote add origin https://github.com/zhirkoalexander-maker/kuper.git

# Rename branch
git branch -M main

# Push
git push --force -u origin main

echo "✅ Successfully pushed to GitHub!"
