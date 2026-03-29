#!/bin/bash
# 매일 오전 11시 / 오후 5시 — 당일 트렌드 포스트 추가 생성 (시간별 스냅샷)
# cron: 0 11 * * *  /  0 17 * * *

PROJECT="/home/smileguy07/projects/paperwanderer"
LOG="$HOME/.claude/trend_cron.log"
CLAUDE="/home/smileguy07/.local/bin/claude"

cd "$PROJECT" || exit 1

TODAY=$(TZ=Asia/Seoul date +%Y-%m-%d)
TS=$(TZ=Asia/Seoul date '+%Y-%m-%d %H:%M')
HOUR=$(TZ=Asia/Seoul date '+%H')

echo "[$TS] [${HOUR}시 트렌드] /trend-post $TODAY 시작" >> "$LOG"

"$CLAUDE" -p "/trend-post $TODAY" \
  --dangerously-skip-permissions \
  --model claude-sonnet-4-6 \
  >> "$LOG" 2>&1

echo "[$(TZ=Asia/Seoul date '+%Y-%m-%d %H:%M')] [${HOUR}시 트렌드] 완료" >> "$LOG"
echo "---" >> "$LOG"
