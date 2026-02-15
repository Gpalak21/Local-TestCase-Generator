#!/bin/bash
echo "🚀 Starting Deployment..."

# 1. Kill any existing manual server processes to free up ports
pkill -f "python server.py" || true
pkill -f "python3 server.py" || true

# 2. Start Services with PM2 (installs if missing via npx)
# --yes accepts installation prompts automatically
npx --yes pm2 start ecosystem.config.js

# 3. Save the process list (so they can be resurrected)
npx --yes pm2 save

echo ""
echo "✅ Deployment Successful!"
echo "---------------------------------------------------"
echo "🖥️  Frontend: http://localhost:8081"
echo "⚙️  Backend:  http://localhost:8000"
echo "---------------------------------------------------"
echo "👉 To stop:    npx pm2 stop all"
echo "👉 To restart: npx pm2 restart all"
echo "👉 To logs:    npx pm2 logs"
