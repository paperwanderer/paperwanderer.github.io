#!/bin/bash
# 매일 1회 — 최근 2주 트렌드 포스트 누락 날짜 감지 후 Claude에 지시 주입
# UserPromptSubmit 훅으로 실행됨

LOCK_FILE="$HOME/.claude/trend_last_run_paperwanderer"
TODAY=$(TZ=Asia/Seoul date +%Y-%m-%d)
PROJECT="/home/smileguy07/projects/paperwanderer/content/_trend-topics"

# 오늘 이미 실행됐으면 조용히 종료
if [ -f "$LOCK_FILE" ] && [ "$(cat "$LOCK_FILE")" = "$TODAY" ]; then
  exit 0
fi

# 최근 2주 누락 날짜 수집
MISSING=()
for i in $(seq 13 -1 0); do
  D=$(TZ=Asia/Seoul date -d "$i days ago" +%Y-%m-%d 2>/dev/null)
  [ -z "$D" ] && continue
  COUNT=$(find "$PROJECT" -name "${D}-*.md" 2>/dev/null | wc -l)
  if [ "$COUNT" -eq 0 ]; then
    MISSING+=("$D")
  fi
done

# 락 파일 업데이트 (누락 없어도 오늘은 여기서 끝)
echo "$TODAY" > "$LOCK_FILE"

if [ ${#MISSING[@]} -eq 0 ]; then
  exit 0
fi

# 누락 날짜 범위 계산 (oldest~newest)
OLDEST="${MISSING[${#MISSING[@]}-1]}"
NEWEST="${MISSING[0]}"

if [ "$OLDEST" = "$NEWEST" ]; then
  RANGE="$OLDEST"
else
  RANGE="${OLDEST}~${NEWEST}"
fi

# Claude에 주입할 지시 출력
echo "🔔 [자동 감지] 최근 2주 트렌드 포스트 누락: ${MISSING[*]}"
echo "지금 바로 /trend-post ${RANGE} 를 실행해주세요."
