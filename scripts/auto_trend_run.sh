#!/bin/bash
# 매일 11시 — 최근 2주(어제까지) 누락 트렌드 포스트 자동 생성
# 설치: crontab -e → 0 11 * * * /home/smileguy07/projects/paperwanderer/scripts/auto_trend_run.sh

PROJECT="/home/smileguy07/projects/paperwanderer"
LOG="$HOME/.claude/trend_cron.log"
CLAUDE="/home/smileguy07/.local/bin/claude"

cd "$PROJECT" || exit 1

YESTERDAY=$(TZ=Asia/Seoul date -d "1 day ago" +%Y-%m-%d)

# 최근 2주(어제까지) 누락 날짜 수집 (오래된 날짜부터 → MISSING[0]이 oldest)
MISSING=()
for i in $(seq 13 -1 0); do
  D=$(TZ=Asia/Seoul date -d "$i days ago" +%Y-%m-%d 2>/dev/null)
  [ -z "$D" ] && continue
  [[ "$D" > "$YESTERDAY" ]] && continue  # 오늘은 제외
  COUNT=$(find "$PROJECT/content/_trend-topics" -name "${D}-*.md" 2>/dev/null | wc -l)
  [ "$COUNT" -eq 0 ] && MISSING+=("$D")
done

TS=$(TZ=Asia/Seoul date '+%Y-%m-%d %H:%M')
echo "[$TS] 누락: ${MISSING[*]:-없음}" >> "$LOG"

[ ${#MISSING[@]} -eq 0 ] && exit 0

# 날짜 범위 문자열 생성 (oldest~newest 또는 단일)
OLDEST="${MISSING[0]}"
NEWEST="${MISSING[${#MISSING[@]}-1]}"
[ "$OLDEST" = "$NEWEST" ] && RANGE="$OLDEST" || RANGE="${OLDEST}~${NEWEST}"

echo "[$TS] /trend-post $RANGE 실행 시작" >> "$LOG"

"$CLAUDE" -p "/trend-post $RANGE" \
  --dangerously-skip-permissions \
  --model claude-sonnet-4-6 \
  >> "$LOG" 2>&1

echo "[$(TZ=Asia/Seoul date '+%Y-%m-%d %H:%M')] 완료" >> "$LOG"
echo "---" >> "$LOG"
