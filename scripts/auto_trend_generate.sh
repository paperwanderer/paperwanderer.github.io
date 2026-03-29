#!/bin/bash
# 매일 오전 7시 — 당일 트렌드 포스트 생성
# cron: 0 7 * * *

PROJECT="/home/smileguy07/projects/paperwanderer"
LOG="$HOME/.claude/trend_cron.log"
CLAUDE="/home/smileguy07/.local/bin/claude"

cd "$PROJECT" || exit 1

TODAY=$(TZ=Asia/Seoul date +%Y-%m-%d)
TS=$(TZ=Asia/Seoul date '+%Y-%m-%d %H:%M')

echo "[$TS] [7시 생성] /trend-post $TODAY 시작" >> "$LOG"

"$CLAUDE" -p "/trend-post $TODAY" \
  --dangerously-skip-permissions \
  --model claude-sonnet-4-6 \
  >> "$LOG" 2>&1

echo "[$(TZ=Asia/Seoul date '+%Y-%m-%d %H:%M')] [7시 생성] 완료" >> "$LOG"
echo "---" >> "$LOG"
