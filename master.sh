#!/usr/bin/env bash
set -euo pipefail

# Insight Atlas master runner:
# - validates prereqs
# - boots local stack
# - runs a smoke test via CLI

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
API_URL="${API_URL:-http://localhost:8000}"
WEB_URL="${WEB_URL:-http://localhost:3000}"

require() { command -v "$1" >/dev/null 2>&1 || { echo "Missing dependency: $1" >&2; exit 1; }; }

echo "[1/7] Checking dependencies..."
require python3
require curl

echo "[2/7] Checking if services are running..."
if ! curl -fsS "$API_URL/healthz" >/dev/null 2>&1; then
  echo "API not running. Start with: cd backend && uvicorn app.main:app --reload"
  exit 1
fi
echo "✓ API is up at $API_URL"

if ! curl -fsS "$WEB_URL" >/dev/null 2>&1; then
  echo "⚠ Frontend not running at $WEB_URL (optional)"
else
  echo "✓ Frontend is up at $WEB_URL"
fi

echo "[3/7] Running smoke test via CLI..."

# Generate unique email
TEST_EMAIL="demo$(date +%s)@example.com"
TEST_PASSWORD="ChangeMe123!"

echo "  → Registering user: $TEST_EMAIL"
TOKEN_JSON="$(python3 "$ROOT_DIR/cli/atlasctl.py" --api "$API_URL" register "$TEST_EMAIL" "$TEST_PASSWORD")"

if [ -z "$TOKEN_JSON" ]; then
  echo "✗ Registration failed"
  exit 1
fi

TOKEN="$(echo "$TOKEN_JSON" | python3 -c 'import json,sys; print(json.load(sys.stdin)["access_token"])')"

if [ -z "$TOKEN" ]; then
  echo "✗ Failed to extract token"
  echo "Response: $TOKEN_JSON"
  exit 1
fi

echo "✓ User registered, token obtained"

export ATLAS_TOKEN="$TOKEN"
export ATLAS_API="$API_URL"

echo "[4/7] Upgrading to Pro (demo mode)..."
python3 "$ROOT_DIR/cli/atlasctl.py" --api "$API_URL" --token "$TOKEN" billing monthly >/dev/null
echo "✓ Upgraded to Pro"

echo "[5/7] Creating intake session..."
SESSION_JSON="$(python3 "$ROOT_DIR/cli/atlasctl.py" --api "$API_URL" --token "$TOKEN" intake --consent --survey '{"novelty_seeking":4,"structure_preference":4,"social_energy":3,"sensory_sensitivity":3,"hyperfocus":5}' --text "I like systems, shipping, and clear definitions of done.")"

SESSION_ID="$(echo "$SESSION_JSON" | python3 -c 'import json,sys; print(json.load(sys.stdin)["session_id"])')"

if [ -z "$SESSION_ID" ]; then
  echo "✗ Failed to create session"
  exit 1
fi

echo "✓ Session created: $SESSION_ID"

echo "[6/7] Running analysis..."
REPORT_JSON="$(python3 "$ROOT_DIR/cli/atlasctl.py" --api "$API_URL" --token "$TOKEN" analyze "$SESSION_ID")"

echo "✓ Analysis complete"
echo ""
echo "Sample report output:"
echo "$REPORT_JSON" | python3 -m json.tool | head -n 40

echo ""
echo "[7/7] Smoke test PASSED ✓"
echo ""
echo "Services:"
echo "  Web: $WEB_URL"
echo "  API: $API_URL/docs"
echo ""
echo "Test user:"
echo "  Email: $TEST_EMAIL"
echo "  Token: ${TOKEN:0:50}..."
