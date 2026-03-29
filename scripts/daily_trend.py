#!/usr/bin/env python3
"""
paperWanderer Daily Trend Bot - TOP 3
Google Trends KR TOP 3 -> Claude AI -> MD + SVG -> GitHub commit
"""
import os, re, time
from datetime import datetime, timezone, timedelta
from pathlib import Path
import anthropic, requests
from pytrends.request import TrendReq

KST = timezone(timedelta(hours=9))
TODAY = datetime.now(KST).strftime('%Y-%m-%d')
REPO_ROOT = Path(__file__).parent.parent
TREND_DIR = REPO_ROOT / 'content' / '_trend-topics'
IMAGES_DIR = REPO_ROOT / 'assets' / 'images'
IMAGES_DIR.mkdir(parents=True, exist_ok=True)
client = anthropic.Anthropic(api_key=os.environ['ANTHROPIC_API_KEY'])

TOP_N = 3

COLORS = [
    ('#1a1a2e','#e84393'),
    ('#0a1628','#2980b9'),
    ('#0d0a1a','#9b59b6'),
]

def get_trends(n=TOP_N):
    print(f'Fetching Google Trends KR TOP {n}...')
    try:
        pt = TrendReq(hl='ko', tz=-540)
        df = pt.trending_searches(pn='south_korea')
        topics = df[0].tolist()[:n]
        print(f'Got: {topics}')
        return topics
    except Exception as e:
        print(f'Trends failed: {e}')
        return [f'trend_{i}' for i in range(1, n+1)]

def search_news(topic, k=8):
    try:
        q = requests.utils.quote(topic + ' 뉴스 오늘')
        r = requests.get(
            f'https://html.duckduckgo.com/html/?q={q}&kl=kr-ko',
            headers={'User-Agent':'Mozilla/5.0'}, timeout=8)
        titles   = re.findall(r'class="result__a"[^>]*>(.*?)</a>', r.text, re.S)
        snippets = re.findall(r'class="result__snippet"[^>]*>(.*?)</a>', r.text, re.S)
        out = []
        for t, s in zip(titles[:k], snippets[:k]):
            out.append({
                't': re.sub(r'<[^>]+>', '', t).strip(),
                's': re.sub(r'<[^>]+>', '', s).strip()
            })
        return out
    except:
        return []

def make_slug(topic, rank):
    s = re.sub(r'[^a-z0-9]+', '-', topic.lower()).strip('-')[:40]
    return f'{TODAY}-rank{rank:02d}-{s}'

def generate(rank, topic, news):
    bg, ac = COLORS[(rank-1) % len(COLORS)]
    slug = make_slug(topic, rank)
    img = f'/assets/images/{slug}.svg'
    date_kr = datetime.now(KST).strftime('%Y년 %m월 %d일')
    news_txt = chr(10).join(
        f"- {n['t']}: {n['s']}" for n in news
    ) or '관련 뉴스 없음'

    prompt = (
        f'오늘({date_kr}) 한국 Google Trends {rank}위 키워드: [{topic}]' + chr(10) +
        f'관련 뉴스 (다양한 시각 포함):{chr(10)}{news_txt}' + chr(10)*2 +
        '다음 세 섹션을 생성해주세요.' + chr(10)*2 +
        '[CATEGORY_START]' + chr(10) +
        '이 토픽의 카테고리를 영어 소문자 하이픈으로 딱 한 단어만 출력하세요.' + chr(10) +
        '(예: entertainment, economy, politics, finance, gaming, sports, tech, history-society, lifestyle, culture)' + chr(10) +
        '[CATEGORY_END]' + chr(10)*2 +
        '[MARKDOWN_START]' + chr(10) +
        f'---{chr(10)}title: "(흥미롭고 클릭하고 싶은 제목)"{chr(10)}trend_date: {TODAY}{chr(10)}trend_rank: {rank}{chr(10)}tags: [태그1, 태그2, 태그3, 태그4]{chr(10)}image: {img}{chr(10)}---{chr(10)}' +
        f'![{topic}]({img}){chr(10)*2}' +
        '# 제목' + chr(10)*2 +
        '## 무슨 일인가' + chr(10) +
        '(3~4문단, 배경과 맥락을 충분히 설명)' + chr(10)*2 +
        '## 핵심 내용' + chr(10) +
        '(중요 사실들을 불릿으로)' + chr(10)*2 +
        '## 다양한 관점' + chr(10) +
        '### 긍정적/지지 시각' + chr(10) +
        '### 비판적/우려 시각' + chr(10) +
        '### 전문가 분석' + chr(10) +
        '### paperWanderer 인사이트' + chr(10) +
        '(깊이 있는 분석 2~3문단)' + chr(10)*2 +
        f'---{chr(10)}*출처: 관련 뉴스 ({date_kr})*' + chr(10) +
        '[MARKDOWN_END]' + chr(10)*2 +
        '[SVG_START]' + chr(10) +
        f'800x420 인포그래픽 SVG (xmlns 포함, 한글 사용):{chr(10)}' +
        f'배경색={bg}, 포인트색={ac}{chr(10)}' +
        f'- 왼쪽 8px 세로 강조바{chr(10)}' +
        f'- 상단: TREND #{rank:02d} 레이블{chr(10)}' +
        f'- 큰 주제명 (48px bold){chr(10)}' +
        f'- 부제목 (22px){chr(10)}' +
        f'- 구분선{chr(10)}' +
        f'- 핵심 정보 3줄{chr(10)}' +
        f'- 하단: 검색량/상승률 뱃지 2개{chr(10)}' +
        f'- 우측 하단: {date_kr} · paperWanderer{chr(10)}' +
        '[SVG_END]'
    )

    print(f'  Claude generating: {topic}...')
    msg = client.messages.create(
        model='claude-sonnet-4-20250514',
        max_tokens=4000,
        messages=[{'role': 'user', 'content': prompt}]
    )
    raw = msg.content[0].text

    cat_m = re.search(r'\[CATEGORY_START\](.*?)\[CATEGORY_END\]', raw, re.S)
    md_m  = re.search(r'\[MARKDOWN_START\](.*?)\[MARKDOWN_END\]', raw, re.S)
    svg_m = re.search(r'\[SVG_START\](.*?)\[SVG_END\]',           raw, re.S)

    category = cat_m.group(1).strip() if cat_m else 'general'
    category = re.sub(r'[^a-z0-9-]', '', category.lower()) or 'general'

    md  = md_m.group(1).strip()  if md_m  else f'---\ntitle: {topic}\ntrend_date: {TODAY}\ntrend_rank: {rank}\n---\n# {topic}'
    svg = svg_m.group(1).strip() if svg_m else (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="800" height="420">'
        f'<rect width="800" height="420" fill="{bg}"/>'
        f'<rect width="8" height="420" fill="{ac}"/>'
        f'<text x="40" y="210" font-size="48" fill="white" font-family="Arial" font-weight="bold">{topic}</text>'
        '</svg>'
    )
    svg = re.sub(r'^```[a-z]*\s*', '', svg.strip())
    svg = re.sub(r'\s*```$',       '', svg.strip())
    return md, svg.strip(), category

def save(rank, topic, md, svg, category):
    slug = make_slug(topic, rank)
    cat_dir = TREND_DIR / category
    cat_dir.mkdir(parents=True, exist_ok=True)
    (cat_dir   / f'{slug}.md' ).write_text(md,  encoding='utf-8')
    (IMAGES_DIR / f'{slug}.svg').write_text(svg, encoding='utf-8')
    print(f'  saved: {category}/{slug}')

def main():
    print(f'paperWanderer Bot (TOP {TOP_N}) - {TODAY}')
    print('=' * 45)
    topics = get_trends(TOP_N)
    for rank, topic in enumerate(topics, 1):
        print(f'[{rank}/{TOP_N}] {topic}')
        news = search_news(topic)
        print(f'  news: {len(news)}개 수집')
        md, svg, category = generate(rank, topic, news)
        print(f'  category: {category}')
        save(rank, topic, md, svg, category)
        time.sleep(3)
    print(f'Done! {TOP_N}개 포스트 생성')

if __name__ == '__main__':
    main()
