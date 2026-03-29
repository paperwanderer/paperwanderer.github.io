#!/bin/bash
# 매일 오전 11시 / 오후 5시 — 당일 트렌드 포스트 업데이트
# cron: 0 11 * * *  /  0 17 * * *

PROJECT="/home/smileguy07/projects/paperwanderer"
LOG="$HOME/.claude/trend_cron.log"
CLAUDE="/home/smileguy07/.local/bin/claude"

cd "$PROJECT" || exit 1

TODAY=$(TZ=Asia/Seoul date +%Y-%m-%d)
TS=$(TZ=Asia/Seoul date '+%Y-%m-%d %H:%M')
HOUR=$(TZ=Asia/Seoul date '+%H')

# 포스트가 없으면 업데이트 불가
COUNT=$(find "$PROJECT/content/_trend-topics" -name "${TODAY}-*.md" 2>/dev/null | wc -l)
if [ "$COUNT" -eq 0 ]; then
  echo "[$TS] [${HOUR}시 업데이트] 스킵 — ${TODAY} 포스트 없음 (먼저 생성 필요)" >> "$LOG"
  exit 0
fi

echo "[$TS] [${HOUR}시 업데이트] /trend-post-update $TODAY 시작 (포스트 ${COUNT}개)" >> "$LOG"

"$CLAUDE" -p "/trend-post-update $TODAY" \
  --dangerously-skip-permissions \
  --model claude-sonnet-4-6 \
  >> "$LOG" 2>&1

echo "[$(TZ=Asia/Seoul date '+%Y-%m-%d %H:%M')] [${HOUR}시 업데이트] 완료" >> "$LOG"
echo "---" >> "$LOG"
