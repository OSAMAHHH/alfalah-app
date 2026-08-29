#!/bin/bash
git add src/services/aiService.ts dist/services/aiService.js
git commit -m "Fix Gemini model 404 error by reverting to gemini-3.6-flash"
git push
