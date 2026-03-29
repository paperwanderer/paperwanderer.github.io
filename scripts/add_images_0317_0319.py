#!/usr/bin/env python3
"""
03-17~03-19 누락 이미지 보강 스크립트
"""
import subprocess
import os
import sys
from pathlib import Path
from PIL import Image

BASE = Path("/home/smileguy07/projects/paperwanderer")
IMG_DIR = BASE / "assets" / "images"

# (slug, image_url, md_file)
TASKS = [
    # autos
    ("2026-03-17-usdkrw-auto-import-price-hike",
     "https://cdn.speconomy.com/news/photo/202603/412129_408942_2256.jpg",
     "content/_trend-topics/autos/2026-03-17-usdkrw-auto-import-price-hike.md"),

    # books
    ("2026-03-17-project-hail-mary-novel-bestseller",
     "https://upload.wikimedia.org/wikipedia/en/3/3b/Project_Hail_Mary_poster.jpg",
     "content/_trend-topics/books/2026-03-17-project-hail-mary-novel-bestseller.md"),
    ("2026-03-18-project-hail-mary-novel-bestseller",
     "https://upload.wikimedia.org/wikipedia/en/3/3b/Project_Hail_Mary_poster.jpg",
     "content/_trend-topics/books/2026-03-18-project-hail-mary-novel-bestseller.md"),

    # business
    ("2026-03-17-cheongung2-middle-east-export-expansion",
     "https://thumb.mt.co.kr/cdn-cgi/image/w=784,h=441,f=auto,fit=crop,g=face/21/2026/03/2026030516003677112_1.jpg",
     "content/_trend-topics/business/2026-03-17-cheongung2-middle-east-export-expansion.md"),
    ("2026-03-19-samsung-union-strike-vote",
     "https://image.zdnet.co.kr/2023/07/27/196deb2bffa7cbd9cf9ecf6d9c3ef3d5.jpg",
     "content/_trend-topics/business/2026-03-19-samsung-union-strike-vote.md"),

    # economy
    ("2026-03-17-middle-east-war-korea-gdp-outlook",
     "https://www.fnnews.com/resource/media/image/2026/03/11/202603112206291201_l.jpg",
     "content/_trend-topics/economy/2026-03-17-middle-east-war-korea-gdp-outlook.md"),
    ("2026-03-17-oil-price-surge-gasoline-1800",
     "http://image.imnews.imbc.com/replay/2026/nwdesk/article/__icsFiles/afieldfile/2026/03/04/desk_20260304_201535_1_13_Large_u.jpg",
     "content/_trend-topics/economy/2026-03-17-oil-price-surge-gasoline-1800.md"),
    ("2026-03-18-iran-israel-war-escalation",
     "https://www.fnnews.com/resource/media/image/2026/03/11/202603112206291201_l.jpg",
     "content/_trend-topics/economy/2026-03-18-iran-israel-war-escalation.md"),
    ("2026-03-18-korea-inflation-march",
     "https://cdn.ngonews.kr/news/photo/202603/227164_229414_5354.jpg",
     "content/_trend-topics/economy/2026-03-18-korea-inflation-march.md"),
    ("2026-03-18-oil-price-stabilization",
     "https://www.fnnews.com/resource/media/image/2026/03/11/202603112206291201_l.jpg",
     "content/_trend-topics/economy/2026-03-18-oil-price-stabilization.md"),
    ("2026-03-19-engel-coefficient-30-percent",
     "https://img.khan.co.kr/news/2026/03/28/news-p.v1.20260327.30b562dd1e7a4767abd7b84e266aa064_P1.png",
     "content/_trend-topics/economy/2026-03-19-engel-coefficient-30-percent.md"),
    ("2026-03-19-oil-supply-middle-east-crisis",
     "http://image.imnews.imbc.com/replay/2026/nwdesk/article/__icsFiles/afieldfile/2026/03/04/desk_20260304_201535_1_13_Large_u.jpg",
     "content/_trend-topics/economy/2026-03-19-oil-supply-middle-east-crisis.md"),
    ("2026-03-19-war-supplementary-budget-order",
     "https://www.fnnews.com/resource/media/image/2026/03/11/202603112206291201_l.jpg",
     "content/_trend-topics/economy/2026-03-19-war-supplementary-budget-order.md"),

    # entertainment
    ("2026-03-17-bts-arirang-comeback-preparation",
     "https://cdn.careyounews.org/news/photo/202603/8954_16407_339.jpg",
     "content/_trend-topics/entertainment/2026-03-17-bts-arirang-comeback-preparation.md"),
    ("2026-03-18-wang-saneun-namja-film",
     "https://upload.wikimedia.org/wikipedia/ko/c/c4/%EC%99%95%EA%B3%BC_%EC%82%AC%EB%8A%94_%EB%82%A8%EC%9E%90.jpg",
     "content/_trend-topics/entertainment/2026-03-18-wang-saneun-namja-film.md"),

    # finance
    ("2026-03-17-kospi-mixed-market-march17",
     "https://www.fnnews.com/resource/media/image/2026/03/11/202603112206291201_l.jpg",
     "content/_trend-topics/finance/2026-03-17-kospi-mixed-market-march17.md"),
    ("2026-03-17-skhynix-us-adr-listing",
     "https://skhynix-prd-data.s3.ap-northeast-2.amazonaws.com/wp-content/uploads/2026/03/SK%ED%95%98%EC%9D%B4%EB%8B%89%EC%8A%A4-GTC-2026%EC%84%9C-%EC%97%94%EB%B9%84%EB%94%94%EC%95%84%EC%99%80-%ED%8C%8C%ED%8A%B8%EB%84%88%EC%8B%AD-%EC%9E%AC%ED%99%95%EC%9D%B8%E2%80%A6%EC%B5%9C%EC%8B%A0-AI-%EB%A9%94%EB%AA%A8%EB%A6%AC-%EC%A0%9C%ED%92%88-%ED%8F%AC%ED%8A%B8%ED%8F%B4%EB%A6%AC%EC%98%A4%EB%8F%84-%EA%B3%B5%EA%B0%9C_07_%ED%96%89%EC%82%AC_2026.jpg",
     "content/_trend-topics/finance/2026-03-17-skhynix-us-adr-listing.md"),
    ("2026-03-18-fomc-rate-hold-sec-crypto",
     "https://www.fnnews.com/resource/media/image/2026/03/11/202603112206291201_l.jpg",
     "content/_trend-topics/finance/2026-03-18-fomc-rate-hold-sec-crypto.md"),
    ("2026-03-18-kospi-weekly-4pct-surge",
     "https://www.fnnews.com/resource/media/image/2026/03/11/202603112206291201_l.jpg",
     "content/_trend-topics/finance/2026-03-18-kospi-weekly-4pct-surge.md"),
    ("2026-03-18-skhynix-stock-surge",
     "https://skhynix-prd-data.s3.ap-northeast-2.amazonaws.com/wp-content/uploads/2026/03/SK%ED%95%98%EC%9D%B4%EB%8B%89%EC%8A%A4-GTC-2026%EC%84%9C-%EC%97%94%EB%B9%84%EB%94%94%EC%95%84%EC%99%80-%ED%8C%8C%ED%8A%B8%EB%84%88%EC%8B%AD-%EC%9E%AC%ED%99%95%EC%9D%B8%E2%80%A6%EC%B5%9C%EC%8B%A0-AI-%EB%A9%94%EB%AA%A8%EB%A6%AC-%EC%A0%9C%ED%92%88-%ED%8F%AC%ED%8A%B8%ED%8F%B4%EB%A6%AC%EC%98%A4%EB%8F%84-%EA%B3%B5%EA%B0%9C_07_%ED%96%89%EC%82%AC_2026.jpg",
     "content/_trend-topics/finance/2026-03-18-skhynix-stock-surge.md"),
    ("2026-03-19-korea-t1-stock-settlement-reform",
     "https://www.fnnews.com/resource/media/image/2026/03/11/202603112206291201_l.jpg",
     "content/_trend-topics/finance/2026-03-19-korea-t1-stock-settlement-reform.md"),

    # gaming
    ("2026-03-18-lck-t1-match",
     "https://www.ddaily.co.kr/photos/2026/03/26/2026032616113051908_l.jpg",
     "content/_trend-topics/gaming/2026-03-18-lck-t1-match.md"),

    # health
    ("2026-03-17-seoul-capsule-hotel-fire-safety",
     "https://t1.daumcdn.net/news/202603/15/donga/20260315194826350lyho.jpg",
     "content/_trend-topics/health/2026-03-17-seoul-capsule-hotel-fire-safety.md"),
    ("2026-03-18-uk-meningococcal-emergency",
     "https://www.ehom.kr/news/2026/03/22/37b17de6d87935b8fc072c6b5a66ebaa101508.jpg",
     "content/_trend-topics/health/2026-03-18-uk-meningococcal-emergency.md"),
    ("2026-03-19-medical-korea-2026-open",
     "https://www.medifonews.com/data/photos/20260312/art_1773885470386_7ef88b.jpg",
     "content/_trend-topics/health/2026-03-19-medical-korea-2026-open.md"),

    # history-society
    ("2026-03-18-canada-eu-membership-talks",
     "https://www.fnnews.com/resource/media/image/2026/03/11/202603112206291201_l.jpg",
     "content/_trend-topics/history-society/2026-03-18-canada-eu-membership-talks.md"),
    ("2026-03-19-busan-pilot-murder-investigation",
     "http://image.imnews.imbc.com/replay/2026/nwdesk/article/__icsFiles/afieldfile/2026/03/18/desk_20260318_203052_1_22_Large.jpg",
     "content/_trend-topics/history-society/2026-03-19-busan-pilot-murder-investigation.md"),

    # hobbies
    ("2026-03-18-ravelball-knitting-trend",
     "https://img.khan.co.kr/news/2026/03/28/news-p.v1.20260327.30b562dd1e7a4767abd7b84e266aa064_P1.png",
     "content/_trend-topics/hobbies/2026-03-18-ravelball-knitting-trend.md"),

    # jobs-education
    ("2026-03-17-samsung-2026-job-application-deadline",
     "https://image.ajunews.com/content/image/2026/03/17/20260317160440903293.jpg",
     "content/_trend-topics/jobs-education/2026-03-17-samsung-2026-job-application-deadline.md"),

    # law-government
    ("2026-03-17-gangbuk-motel-serial-murder",
     "https://image.imnews.imbc.com/news/2026/society/article/__icsFiles/afieldfile/2026/03/09/joo260309_6.jpg",
     "content/_trend-topics/law-government/2026-03-17-gangbuk-motel-serial-murder.md"),
    ("2026-03-17-stalking-punishment-law-reform",
     "https://source.inblog.dev/featured_image/2026-03-26T04:26:37.994Z-64b8f086-14bc-488b-b878-cda645e84ed0",
     "content/_trend-topics/law-government/2026-03-17-stalking-punishment-law-reform.md"),
    ("2026-03-18-illegal-marine-oil-crackdown",
     "https://www.fnnews.com/resource/media/image/2026/03/11/202603112206291201_l.jpg",
     "content/_trend-topics/law-government/2026-03-18-illegal-marine-oil-crackdown.md"),
    ("2026-03-18-pension-reform-debate",
     "https://www.koreadaily.com/data/photo/thumbnail/2026/03/18/b9e91cbd-7c9d-49f1-9d2a-c3c68307bfd1.jpg",
     "content/_trend-topics/law-government/2026-03-18-pension-reform-debate.md"),
    ("2026-03-19-kim-gunhee-doitch-abetment",
     "https://www.koreadaily.com/data/photo/thumbnail/2026/03/18/b9e91cbd-7c9d-49f1-9d2a-c3c68307bfd1.jpg",
     "content/_trend-topics/law-government/2026-03-19-kim-gunhee-doitch-abetment.md"),
    ("2026-03-19-law-distortion-crime-chaos",
     "https://cdn.lawtimes.co.kr/news/photo/202603/218075_123323_5831.jpg",
     "content/_trend-topics/law-government/2026-03-19-law-distortion-crime-chaos.md"),
    ("2026-03-19-prosecution-reform-gongso-law",
     "https://cdn.lawtimes.co.kr/news/photo/202603/218075_123323_5831.jpg",
     "content/_trend-topics/law-government/2026-03-19-prosecution-reform-gongso-law.md"),

    # online-community
    ("2026-03-17-gangbuk-murder-chatgpt-digital-evidence",
     "https://t1.daumcdn.net/news/202602/20/YTN/20260220181012825nnsc.jpg",
     "content/_trend-topics/online-community/2026-03-17-gangbuk-murder-chatgpt-digital-evidence.md"),

    # politics
    ("2026-03-17-middle-east-iran-war-korea",
     "https://www.fnnews.com/resource/media/image/2026/03/11/202603112206291201_l.jpg",
     "content/_trend-topics/politics/2026-03-17-middle-east-iran-war-korea.md"),
    ("2026-03-18-local-election-2026-poll",
     "http://image.imnews.imbc.com/replay/2026/nwdesk/article/__icsFiles/afieldfile/2026/02/14/desk_20260214_200847_1_2_Large.jpg",
     "content/_trend-topics/politics/2026-03-18-local-election-2026-poll.md"),
    ("2026-03-18-north-korea-supreme-assembly-election",
     "https://t1.daumcdn.net/news/202603/16/imbc/20260316091611075bhae.jpg",
     "content/_trend-topics/politics/2026-03-18-north-korea-supreme-assembly-election.md"),
    ("2026-03-19-oh-sehun-law-distortion-special-prosecutor",
     "https://wimg.heraldcorp.com/news/cms/2026/03/18/rcv.YNA.20260318.PYH2026031804740001300_T1.jpg?type=w&w=640",
     "content/_trend-topics/politics/2026-03-19-oh-sehun-law-distortion-special-prosecutor.md"),
    ("2026-03-19-taiwan-korea-south-korea-label",
     "https://image.ajunews.com/content/image/2026/03/18/20260318160212563046.jpg",
     "content/_trend-topics/politics/2026-03-19-taiwan-korea-south-korea-label.md"),

    # real-estate
    ("2026-03-17-lee-jeongmyeong-farmland-real-estate-policy",
     "https://econmingle.com/wp-content/uploads/2026/03/Rise-in-officially-assessed-real-estate-prices.png",
     "content/_trend-topics/real-estate/2026-03-17-lee-jeongmyeong-farmland-real-estate-policy.md"),
    ("2026-03-17-real-estate-policy-survey",
     "https://econmingle.com/wp-content/uploads/2026/03/Rise-in-officially-assessed-real-estate-prices.png",
     "content/_trend-topics/real-estate/2026-03-17-real-estate-policy-survey.md"),
    ("2026-03-18-housing-price-index-korea",
     "https://econmingle.com/wp-content/uploads/2026/03/Rise-in-officially-assessed-real-estate-prices.png",
     "content/_trend-topics/real-estate/2026-03-18-housing-price-index-korea.md"),

    # science
    ("2026-03-17-iran-war-energy-dependency-korea",
     "https://www.fnnews.com/resource/media/image/2026/03/11/202603112206291201_l.jpg",
     "content/_trend-topics/science/2026-03-17-iran-war-energy-dependency-korea.md"),
    ("2026-03-18-joseon-fortress-excavation",
     "https://seoulcitywall.seoul.go.kr/resources/images/content/sub/1_1_2.jpg",
     "content/_trend-topics/science/2026-03-18-joseon-fortress-excavation.md"),

    # sports
    ("2026-03-17-kbo-games-march17-results",
     "https://image.mediapen.com/news/202603/news_1086322_1773196399_m.jpg",
     "content/_trend-topics/sports/2026-03-17-kbo-games-march17-results.md"),
    ("2026-03-17-kbo-spring-training-2026",
     "https://image.mediapen.com/news/202603/news_1086322_1773196399_m.jpg",
     "content/_trend-topics/sports/2026-03-17-kbo-spring-training-2026.md"),
    ("2026-03-18-kbo-spring-training",
     "https://image.mediapen.com/news/202603/news_1086322_1773196399_m.jpg",
     "content/_trend-topics/sports/2026-03-18-kbo-spring-training.md"),
    ("2026-03-19-psg-lee-kangin-ucl-quarterfinal",
     "https://thumb.mt.co.kr/cdn-cgi/image/w=1200,h=675,fit=cover,bg=whilte,f=auto,quality=high,sharpen=2,g=face/21/2026/03/2026031807424527056_3.jpg",
     "content/_trend-topics/sports/2026-03-19-psg-lee-kangin-ucl-quarterfinal.md"),
    ("2026-03-19-wbc-venezuela-champion-korea-exit",
     "https://img1.newsis.com/2026/03/18/NISI20260318_0001113336_web.jpg",
     "content/_trend-topics/sports/2026-03-19-wbc-venezuela-champion-korea-exit.md"),

    # tech
    ("2026-03-17-samsung-hbm5-strategy",
     "https://image.ajunews.com/content/image/2026/03/17/20260317160440903293.jpg",
     "content/_trend-topics/tech/2026-03-17-samsung-hbm5-strategy.md"),
    ("2026-03-17-samsung-vs-skhynix-hbm-race",
     "https://image.ajunews.com/content/image/2026/03/17/20260317160440903293.jpg",
     "content/_trend-topics/tech/2026-03-17-samsung-vs-skhynix-hbm-race.md"),
    ("2026-03-18-samsung-amd-mou",
     "https://image.ajunews.com/content/image/2026/03/17/20260317160440903293.jpg",
     "content/_trend-topics/tech/2026-03-18-samsung-amd-mou.md"),
    ("2026-03-19-bigtech-ai-infra-race",
     "https://wimg.heraldcorp.com/news/cms/2025/08/01/news-p.v1.20250801.0a1c781193f140debc04aa0c4750cc3c_T1.jpg?type=w&w=640",
     "content/_trend-topics/tech/2026-03-19-bigtech-ai-infra-race.md"),

    # travel
    ("2026-03-17-seoul-spring-festival-cherry-blossom",
     "https://img.khan.co.kr/news/2026/03/28/news-p.v1.20260327.30b562dd1e7a4767abd7b84e266aa064_P1.png",
     "content/_trend-topics/travel/2026-03-17-seoul-spring-festival-cherry-blossom.md"),
    ("2026-03-17-spring-travel-festival-korea-2026",
     "https://img.khan.co.kr/news/2026/03/28/news-p.v1.20260327.30b562dd1e7a4767abd7b84e266aa064_P1.png",
     "content/_trend-topics/travel/2026-03-17-spring-travel-festival-korea-2026.md"),
    ("2026-03-17-travel-cost-surge-exchange-rate",
     "https://www.imaeil.com/photos/2026/03/09/2026030916500298880_m.jpg",
     "content/_trend-topics/travel/2026-03-17-travel-cost-surge-exchange-rate.md"),
    ("2026-03-18-jeju-cherry-blossom-peak",
     "https://img.khan.co.kr/news/2026/03/28/news-p.v1.20260327.30b562dd1e7a4767abd7b84e266aa064_P1.png",
     "content/_trend-topics/travel/2026-03-18-jeju-cherry-blossom-peak.md"),
]

def resize_image(raw_path, out_path):
    """리사이즈: 최대 800px 너비, quality 75, 150KB 초과 시 quality 62"""
    try:
        img = Image.open(raw_path)
        # RGBA → RGB 변환
        if img.mode in ("RGBA", "P", "LA"):
            img = img.convert("RGB")
        # 리사이즈
        w, h = img.size
        if w > 800:
            ratio = 800 / w
            img = img.resize((800, int(h * ratio)), Image.LANCZOS)
        # 저장 quality 75
        img.save(out_path, "JPEG", quality=75, optimize=True)
        # 150KB 초과면 quality 62로 재저장
        if os.path.getsize(out_path) > 150 * 1024:
            img.save(out_path, "JPEG", quality=62, optimize=True)
        return True
    except Exception as e:
        print(f"  [리사이즈 오류] {e}")
        return False

def download_and_process(slug, url, rel_md):
    raw_path = IMG_DIR / f"{slug}-raw"
    out_path = IMG_DIR / f"{slug}.jpg"
    md_path = BASE / rel_md

    # 이미 이미지가 있으면 스킵
    if out_path.exists():
        print(f"  [스킵] 이미 존재: {slug}.jpg")
        return True

    # 다운로드
    print(f"  다운로드 중: {url[:80]}...")
    result = subprocess.run(
        ["curl", "-L", "--max-time", "15", "-A", "Mozilla/5.0", "-o", str(raw_path), url],
        capture_output=True
    )
    if result.returncode != 0 or not raw_path.exists() or raw_path.stat().st_size < 1000:
        print(f"  [실패] 다운로드 실패 (returncode={result.returncode}, size={raw_path.stat().st_size if raw_path.exists() else 0})")
        if raw_path.exists():
            raw_path.unlink()
        return False

    # 리사이즈
    ok = resize_image(raw_path, out_path)
    raw_path.unlink(missing_ok=True)
    if not ok:
        return False

    print(f"  [성공] {slug}.jpg ({out_path.stat().st_size // 1024}KB)")
    return True

def add_image_to_md(md_path, slug):
    """frontmatter에 image: 필드 추가"""
    content = md_path.read_text(encoding="utf-8")
    if "image:" in content[:500]:
        print(f"  [스킵] 이미 image 필드 있음")
        return
    # date: 줄 뒤에 image: 삽입
    lines = content.split("\n")
    new_lines = []
    inserted = False
    for line in lines:
        new_lines.append(line)
        if not inserted and line.startswith("date:"):
            new_lines.append(f"image: /assets/images/{slug}.jpg")
            inserted = True
    if not inserted:
        # date가 없으면 두 번째 --- 앞에 삽입
        for i, line in enumerate(new_lines):
            if i > 0 and line.strip() == "---":
                new_lines.insert(i, f"image: /assets/images/{slug}.jpg")
                break
    md_path.write_text("\n".join(new_lines), encoding="utf-8")
    print(f"  [MD 업데이트] image 필드 추가됨")

success_count = 0
fail_count = 0
skip_count = 0

for slug, url, rel_md in TASKS:
    print(f"\n[{slug}]")
    md_path = BASE / rel_md
    if not md_path.exists():
        print(f"  [경고] MD 파일 없음: {rel_md}")
        fail_count += 1
        continue

    out_path = IMG_DIR / f"{slug}.jpg"
    if out_path.exists():
        # 이미지는 있는데 MD에 image 필드가 없는 경우 처리
        if not any("image:" in l for l in md_path.read_text().split("\n")[:20]):
            add_image_to_md(md_path, slug)
        skip_count += 1
        continue

    ok = download_and_process(slug, url, rel_md)
    if ok:
        add_image_to_md(md_path, slug)
        success_count += 1
    else:
        fail_count += 1

print(f"\n=== 완료 ===")
print(f"성공: {success_count}, 스킵(기존): {skip_count}, 실패: {fail_count}")
