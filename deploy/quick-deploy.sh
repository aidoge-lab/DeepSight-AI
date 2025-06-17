#!/bin/bash

# Quick deployment script - for frequent updates

echo "🚀 Quick deploying to GitHub Pages..."

# Create temporary branch and push
git subtree split --prefix=insights -b temp-deploy-$(date +%s)
TEMP_BRANCH=$(git branch | grep temp-deploy | tail -1 | sed 's/* //')
git push pages $TEMP_BRANCH:main --force

# Clean up temporary branch
git branch -D $TEMP_BRANCH

echo "✅ Deployment complete! Visit: https://aidoge-lab.github.io/"