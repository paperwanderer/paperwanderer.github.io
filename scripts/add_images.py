#!/usr/bin/env python3
"""
이미지 없는 포스트에 이미지 추가 스크립트
"""
import os
import subprocess
import re
from PIL import Image

ASSETS_DIR = "/home/smileguy07/projects/paperwanderer/assets/images"

# slug -> image_url 매핑
IMAGE_MAP = {
    "2026-03-04-z-generation-2016-nostalgia": "https://thumbnews.nateimg.co.kr/view610///news.nateimg.co.kr/orgImg/ae/2026/01/31/ae_1770247864874_862022_0.jpg",
    "2026-03-03-iran-war-korea-economy": "https://img.khan.co.kr/news/2026/03/26/news-p.v1.20260326.58bda9b0917344eab05372dac9839221_P1.jpeg",
    "2026-03-04-korea-semiconductor-export-boom": "https://econmingle.com/wp-content/uploads/2026/03/March-semiconductor-exports.png",
    "2026-03-04-trump-tariffs-korea-impact": "https://econmingle.com/wp-content/uploads/2026/03/thumbnail_EBAFB8EAB5AD_EBACB4EC97ADEBB295_301ECA1B0_ECA1B0EC82AC_20260313_002901.png",
    "2026-03-03-monthly-boyfriend-netflix": "https://image.starnewskorea.com/cdn-cgi/image/f=auto,w=1200,h=800,fit=cover,q=high,sharpen=2/21/2026/01/2026012111173524358_1.jpg",
    "2026-03-03-park-bom-2ne1-controversy": "https://wimg.heraldcorp.com/news/cms/2026/03/03/news-p.v1.20260303.d0b6ecf27c3c46ed83d563f18cabcc93_T1.jpg?type=w&w=640",
    "2026-03-04-drama-climax-ju-jihoon": "https://image.starnewskorea.com/21/2026/03/2026031711464450512_1.jpg",
    "2026-03-04-lim-youngwoong-bts-brand-ranking": "https://image.starnewskorea.com/21/2026/03/2026030708393841260_1.jpg",
    "2026-03-04-netflix-korea-global-content": "https://image.starnewskorea.com/21/2026/03/2026030708393841260_1.jpg",
    "2026-03-04-tvn-siren-drama-park-minyoung": "https://wimg.heraldcorp.com/news/cms/2026/03/08/news-p.v1.20260308.ace1185059e54b84b2591ac38365bd65_T1.jpg?type=w&w=640",
    "2026-03-04-bitcoin-surge-korea": "https://t1.daumcdn.net/news/202602/24/kedtv/20260224165417747yojr.png",
    "2026-03-04-korea-base-rate-effect": "https://www.ehom.kr/news/2025/11/09/f1c18336d65a269a41915ac3ec1263db103624.png",
    "2026-03-03-samgyeopsal-day": "https://www.sentv.co.kr/data/sentv/image/2025/02/28/sentv20250228000136.png",
    "2026-03-04-integrated-care-system-prep": "https://www.youthdaily.co.kr/data/photos/20260313/art_17744945857791_4b7ab8.png",
    "2026-03-04-youth-unemployment-social-crisis": "https://cdn.1conomynews.co.kr/news/photo/202509/43334_44277_5147.png",
    "2026-03-04-education-support-86wonman": "https://cdn.thereport.co.kr/news/photo/202601/82791_103629_1533.jpg",
    "2026-03-03-lee-jaeming-approval": "https://cdn.thereport.co.kr/news/photo/202601/82791_103629_1533.jpg",  # 이재명 지지율
    "2026-03-04-kang-seonwoo-bribery-arrested": "https://img.khan.co.kr/news/2026/03/26/news-p.v1.20260326.58bda9b0917344eab05372dac9839221_P1.jpeg",
    "2026-03-04-local-election-party-nominations": "https://img.asiatoday.co.kr/file/2026y/03m/05d/2026030401000200100011081.jpg",
    "2026-03-04-park-chandae-incheon-mayor-nomination": "https://img.asiatoday.co.kr/file/2026y/03m/05d/2026030401000200100011081.jpg",
    "2026-03-04-prosecution-dismissal-deal-scandal": "https://img.etoday.co.kr/pto_db/2026/02/20260223200830_2298779_860_588.jpg",
    "2026-03-04-public-land-price-2026-appeal": "https://moneyconnet-bucket.s3.ap-northeast-2.amazonaws.com/wp-content/uploads/2026/03/23174004/gongsiji_johoe_mich_1774255202.jpg",
    "2026-03-04-stock-to-real-estate-capital-flow": "https://img.hankyung.com/photo/202602/01.43340431.1.png",
    "2026-03-03-blood-moon-eclipse": "https://www.bntnews.co.kr/data/bnt/image/2026/03/04/bnt202603040558.jpg",
    "2026-03-04-kbo-2026-opening-prep": "https://img.etoday.co.kr/pto_db/2026/03/20260327160629_2314015_875_476.jpg",
    "2026-03-04-wbc-2026-korea-preview": "https://www.bntnews.co.kr/data/bnt/image/2026/03/04/bnt202603040558.jpg",
    "2026-03-04-ai-privacy-grok-declaration": "https://cdnimage.dailian.co.kr/news/202602/news_1770854212_1609926_m_1.jpg",
    "2026-03-04-openai-codex-windows": "https://image.edaily.co.kr/images/Photo/files/NP/S/2026/02/PS26022301000.jpg",
    "2026-03-04-rebellions-ai-chip-investment": "https://wimg.sedaily.com/news/cms/2026/03/26/news-p.v1.20260104.0dc49b409a1145d2afa5eab884cf37f6_R.jpg",
    "2026-03-01-samil-holiday-travel": "https://cdn.traveldaily.co.kr/news/photo/202602/70125_70186_488.jpg",
}

# slug -> md 파일 경로 매핑
MD_FILES = {
    "2026-03-04-z-generation-2016-nostalgia": "content/_trend-topics/culture/2026-03-04-z-generation-2016-nostalgia.md",
    "2026-03-03-iran-war-korea-economy": "content/_trend-topics/economy/2026-03-03-iran-war-korea-economy.md",
    "2026-03-04-korea-semiconductor-export-boom": "content/_trend-topics/economy/2026-03-04-korea-semiconductor-export-boom.md",
    "2026-03-04-trump-tariffs-korea-impact": "content/_trend-topics/economy/2026-03-04-trump-tariffs-korea-impact.md",
    "2026-03-03-monthly-boyfriend-netflix": "content/_trend-topics/entertainment/2026-03-03-monthly-boyfriend-netflix.md",
    "2026-03-03-park-bom-2ne1-controversy": "content/_trend-topics/entertainment/2026-03-03-park-bom-2ne1-controversy.md",
    "2026-03-04-drama-climax-ju-jihoon": "content/_trend-topics/entertainment/2026-03-04-drama-climax-ju-jihoon.md",
    "2026-03-04-lim-youngwoong-bts-brand-ranking": "content/_trend-topics/entertainment/2026-03-04-lim-youngwoong-bts-brand-ranking.md",
    "2026-03-04-netflix-korea-global-content": "content/_trend-topics/entertainment/2026-03-04-netflix-korea-global-content.md",
    "2026-03-04-tvn-siren-drama-park-minyoung": "content/_trend-topics/entertainment/2026-03-04-tvn-siren-drama-park-minyoung.md",
    "2026-03-04-bitcoin-surge-korea": "content/_trend-topics/finance/2026-03-04-bitcoin-surge-korea.md",
    "2026-03-04-korea-base-rate-effect": "content/_trend-topics/finance/2026-03-04-korea-base-rate-effect.md",
    "2026-03-03-samgyeopsal-day": "content/_trend-topics/food-drink/2026-03-03-samgyeopsal-day.md",
    "2026-03-04-integrated-care-system-prep": "content/_trend-topics/health/2026-03-04-integrated-care-system-prep.md",
    "2026-03-04-youth-unemployment-social-crisis": "content/_trend-topics/history-society/2026-03-04-youth-unemployment-social-crisis.md",
    "2026-03-04-education-support-86wonman": "content/_trend-topics/jobs-education/2026-03-04-education-support-86wonman.md",
    "2026-03-03-lee-jaeming-approval": "content/_trend-topics/politics/2026-03-03-lee-jaeming-approval.md",
    "2026-03-04-kang-seonwoo-bribery-arrested": "content/_trend-topics/politics/2026-03-04-kang-seonwoo-bribery-arrested.md",
    "2026-03-04-local-election-party-nominations": "content/_trend-topics/politics/2026-03-04-local-election-party-nominations.md",
    "2026-03-04-park-chandae-incheon-mayor-nomination": "content/_trend-topics/politics/2026-03-04-park-chandae-incheon-mayor-nomination.md",
    "2026-03-04-prosecution-dismissal-deal-scandal": "content/_trend-topics/politics/2026-03-04-prosecution-dismissal-deal-scandal.md",
    "2026-03-04-public-land-price-2026-appeal": "content/_trend-topics/real-estate/2026-03-04-public-land-price-2026-appeal.md",
    "2026-03-04-stock-to-real-estate-capital-flow": "content/_trend-topics/real-estate/2026-03-04-stock-to-real-estate-capital-flow.md",
    "2026-03-03-blood-moon-eclipse": "content/_trend-topics/science/2026-03-03-blood-moon-eclipse.md",
    "2026-03-04-kbo-2026-opening-prep": "content/_trend-topics/sports/2026-03-04-kbo-2026-opening-prep.md",
    "2026-03-04-wbc-2026-korea-preview": "content/_trend-topics/sports/2026-03-04-wbc-2026-korea-preview.md",
    "2026-03-04-ai-privacy-grok-declaration": "content/_trend-topics/tech/2026-03-04-ai-privacy-grok-declaration.md",
    "2026-03-04-openai-codex-windows": "content/_trend-topics/tech/2026-03-04-openai-codex-windows.md",
    "2026-03-04-rebellions-ai-chip-investment": "content/_trend-topics/tech/2026-03-04-rebellions-ai-chip-investment.md",
    "2026-03-01-samil-holiday-travel": "content/_trend-topics/travel/2026-03-01-samil-holiday-travel.md",
}

BASE_DIR = "/home/smileguy07/projects/paperwanderer"

def download_image(url, raw_path):
    """curl로 이미지 다운로드"""
    result = subprocess.run([
        "curl", "-L", "--max-time", "15",
        "-A", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "-o", raw_path, url
    ], capture_output=True)
    return result.returncode == 0

def resize_image(raw_path, out_path):
    """PIL로 리사이즈: 최대 800px 너비, quality 75, 150KB 초과시 62"""
    try:
        img = Image.open(raw_path)
        # RGBA -> RGB 변환
        if img.mode in ("RGBA", "P", "LA"):
            img = img.convert("RGB")
        # 최대 800px 너비
        w, h = img.size
        if w > 800:
            new_h = int(h * 800 / w)
            img = img.resize((800, new_h), Image.LANCZOS)

        # quality 75로 저장 후 크기 체크
        img.save(out_path, "JPEG", quality=75, optimize=True)
        if os.path.getsize(out_path) > 150 * 1024:
            img.save(out_path, "JPEG", quality=62, optimize=True)
        return True
    except Exception as e:
        print(f"  PIL 오류: {e}")
        return False

def add_image_to_md(md_path, slug):
    """frontmatter에 image: 필드 추가 (title: 바로 아래)"""
    with open(md_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 이미 image: 있으면 스킵
    if re.search(r'^image:', content, re.MULTILINE):
        print(f"  이미 image: 있음, 스킵")
        return False

    image_line = f"image: /assets/images/{slug}.jpg"
    # title: 라인 바로 뒤에 삽입
    new_content = re.sub(
        r'^(title:.*?)$',
        r'\1\n' + image_line,
        content,
        count=1,
        flags=re.MULTILINE
    )

    if new_content == content:
        print(f"  title: 라인을 찾지 못했음")
        return False

    with open(md_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    return True

def main():
    success_count = 0
    fail_count = 0

    for slug, image_url in IMAGE_MAP.items():
        md_rel = MD_FILES.get(slug)
        if not md_rel:
            print(f"[SKIP] {slug}: MD 파일 경로 없음")
            continue

        md_path = os.path.join(BASE_DIR, md_rel)
        if not os.path.exists(md_path):
            print(f"[SKIP] {slug}: MD 파일 없음")
            continue

        raw_path = os.path.join(ASSETS_DIR, f"{slug}-raw")
        out_path = os.path.join(ASSETS_DIR, f"{slug}.jpg")

        # 이미 결과 파일 있으면 스킵
        if os.path.exists(out_path) and os.path.getsize(out_path) > 1000:
            print(f"[EXIST] {slug}: 이미지 파일 이미 있음")
            # frontmatter만 업데이트
            if add_image_to_md(md_path, slug):
                print(f"  frontmatter 업데이트 완료")
            success_count += 1
            continue

        print(f"\n[PROCESS] {slug}")
        print(f"  URL: {image_url[:80]}...")

        # 다운로드
        if not download_image(image_url, raw_path):
            print(f"  [FAIL] 다운로드 실패")
            fail_count += 1
            continue

        # 파일 크기 확인
        if not os.path.exists(raw_path) or os.path.getsize(raw_path) < 1000:
            print(f"  [FAIL] 다운로드 파일 너무 작음: {os.path.getsize(raw_path) if os.path.exists(raw_path) else 0} bytes")
            fail_count += 1
            continue

        # 리사이즈
        if not resize_image(raw_path, out_path):
            print(f"  [FAIL] 리사이즈 실패")
            fail_count += 1
            continue

        # raw 파일 삭제
        os.remove(raw_path)

        final_size = os.path.getsize(out_path)
        print(f"  [OK] {final_size//1024}KB -> {out_path}")

        # frontmatter 업데이트
        if add_image_to_md(md_path, slug):
            print(f"  frontmatter 업데이트 완료")
            success_count += 1
        else:
            success_count += 1  # 이미지는 성공

    print(f"\n=== 완료: {success_count}개 성공, {fail_count}개 실패 ===")

if __name__ == "__main__":
    main()
