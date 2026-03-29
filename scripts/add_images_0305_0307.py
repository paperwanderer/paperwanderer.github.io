#!/usr/bin/env python3
"""
2026-03-05~03-07 이미지 없는 포스트에 이미지 추가 스크립트
"""
import os
import subprocess
import re
from PIL import Image

ASSETS_DIR = "/home/smileguy07/projects/paperwanderer/assets/images"

# slug -> image_url 매핑
IMAGE_MAP = {
    # economy
    "2026-03-05-iran-hormuz-oil-shock":
        "https://www.aljazeera.com/wp-content/uploads/2026/03/2026-03-26T032610Z_1054992894_RC2YBKAEGEE4_RTRMADP_3_IRAN-CRISIS-FUEL-THAILAND-1774498329.jpg?resize=1200%2C630",
    "2026-03-05-won-dollar-1500-exchange-rate":
        "https://thumb.mt.co.kr/cdn-cgi/image/w=1200,h=675,f=auto,fit=crop,g=face/21/2026/03/2026030404481096676_1.jpg",
    "2026-03-07-current-account-surplus":
        "https://wimg.heraldcorp.com/news/cms/2026/03/06/news-p.v1.20251226.366e3cde29b249a5bf88c330c38270d0_T1.jpg?type=w&w=640",
    "2026-03-07-onion-price-collapse":
        "https://cdn.agrinet.co.kr/news/photo/202603/402396_92410_3830.jpg",
    # entertainment
    "2026-03-05-bts-march-comeback-confirmed":
        "https://img1.newsis.com/2026/03/05/NISI20260305_0021197147_web.jpg",
    "2026-03-05-h1key-mini5-comeback":
        "https://kpopofficial.com/wp-content/uploads/2026/02/H1-KEY-LOVECHAPTER-Album-Cover.webp",
    "2026-03-05-kcon-la-2026-lineup":
        "https://0.soompi.io/wp-content/uploads/2026/03/26155945/KCON-LA-2026.jpg",
    "2026-03-07-kpop-march-comeback-rush":
        "https://0.soompi.io/wp-content/uploads/2026/03/26155945/KCON-LA-2026.jpg",
    "2026-03-07-netflix-monthly-boyfriend":
        "https://d3h3k01ny8mjr.cloudfront.net/tv-report/2026/02/05095223/CP-2022-0227-34909055-thumb.jpg",
    # finance
    "2026-03-05-circuit-breaker-kospi-kosdaq":
        "http://image.imnews.imbc.com/replay/2026/nw1200/article/__icsFiles/afieldfile/2026/03/04/noon_20260304_120344_1_1_Large.jpg",
    "2026-03-05-defense-stocks-surge":
        "https://t1.daumcdn.net/news/202603/03/mk/20260303102703962nbky.jpg",
    "2026-03-05-samsung-200k-breach":
        "https://thumb.mt.co.kr/cdn-cgi/image/w=1200,h=675,f=auto,fit=crop,g=face/21/2026/03/2026030409531893083_1.jpg",
    "2026-03-07-oil-shock-korea-economy":
        "https://thumb.mt.co.kr/cdn-cgi/image/w=1200,h=675,f=auto,fit=crop,g=face/21/2026/03/2026030911085852370_1.jpg",
    # health
    "2026-03-05-spring-fine-dust":
        "https://www.korea.kr/newsWeb/resources/attaches/2026.03/04/01bdad842da04eb1725934ef05cba4cb.jpg",
    # history-society
    "2026-03-05-gangbuk-motel-serial-murder-psychopath":
        "https://thumb.mt.co.kr/cdn-cgi/image/w=1200,h=675,f=auto,fit=crop,g=face/21/2026/03/2026030409531893083_1.jpg",
    "2026-03-05-low-birthrate-parental-leave-policy":
        "https://www.korea.kr/newsWeb/resources/attaches/2024.12/17/ea38207bb3c7c754106ea30bebd68c16.jpg",
    # hobbies
    "2026-03-07-lotto-1214":
        "https://thumb.mt.co.kr/cdn-cgi/image/w=1200,h=675,fit=cover,bg=whilte,f=auto,quality=high,sharpen=2,g=face/21/2026/03/2026030722445157554_1.jpg",
    # jobs-education
    "2026-03-07-neulbom-school-launch":
        "https://www.korea.kr/newsWeb/resources/attaches/2026.03/04/01bdad842da04eb1725934ef05cba4cb.jpg",
    # law-government
    "2026-03-05-lawmaker-car-rationing":
        "https://www.sisa-news.com/data/photos/20260313/art_177440480252_d3d2e1.jpg",
    "2026-03-05-park-wangyeol-extradited":
        "https://image.imnews.imbc.com/news/2026/politics/article/__icsFiles/afieldfile/2026/03/25/lyj_260325_7_1.jpg",
    # politics
    "2026-03-05-moon-jaein-us-visit":
        "https://image.imnews.imbc.com/news/2026/politics/article/__icsFiles/afieldfile/2026/03/07/ggm_20260307_2.jpg",
    "2026-03-05-north-korea-cruise-missile-destroyer":
        "https://img.khan.co.kr/news/2026/03/05/news-p.v1.20260305.dac820ed48f3478ca306fe1893bf595e_P1.jpeg",
    "2026-03-05-prosecution-reform-public-prosecution":
        "https://image.imnews.imbc.com/news/2026/politics/article/__icsFiles/afieldfile/2026/03/09/yh_20260309-1.jpg",
    "2026-03-05-us-investment-special-act":
        "https://image.imnews.imbc.com/news/2026/politics/article/__icsFiles/afieldfile/2026/03/09/yh_20260309-1.jpg",
    "2026-03-07-democratic-union-launch":
        "https://image.imnews.imbc.com/news/2026/politics/article/__icsFiles/afieldfile/2026/03/07/ggm_20260307_2.jpg",
    "2026-03-07-iran-war-antiwar-protest":
        "https://assets.ws.or.kr/resized/2026/03/ff99fcb66f7fd3a0e9fbdd885e6e85c1.webp",
    "2026-03-07-local-election-ppp-chaos":
        "https://image.imnews.imbc.com/news/2026/politics/article/__icsFiles/afieldfile/2026/03/07/ggm_20260307_2.jpg",
    # real-estate
    "2026-03-05-apartment-public-price-rise":
        "http://image.imnews.imbc.com/replay/2026/nwdesk/article/__icsFiles/afieldfile/2026/03/17/desk_20260317_203541_1_23_Large.jpg",
    "2026-03-05-seoul-housing-supply-shock":
        "http://image.imnews.imbc.com/replay/2026/nwdesk/article/__icsFiles/afieldfile/2026/03/17/desk_20260317_203541_1_23_Large.jpg",
    # science
    "2026-03-05-kf21-first-production-rollout":
        "https://www.korea.kr/newsWeb/resources/attaches/2026.03/04/01bdad842da04eb1725934ef05cba4cb.jpg",
    # sports
    "2026-03-05-lee-junghoo-wbc-ankle-injury":
        "https://img1.newsis.com/2026/03/05/NISI20260305_0021197142_web.jpg",
    "2026-03-05-moon-bogyeong-grand-slam-wbc":
        "https://img1.newsis.com/2026/03/05/NISI20260305_0021197147_web.jpg",
    "2026-03-05-soh-hyungjun-wbc-pitching":
        "https://thumb.mt.co.kr/cdn-cgi/image/w=1200,h=675,fit=cover,bg=whilte,f=auto,quality=high,sharpen=2,g=face/21/2026/03/2026030521042063217_1.jpg",
    "2026-03-05-wbc-korea-japan-preview":
        "https://img1.newsis.com/2026/03/05/NISI20260305_0021197147_web.jpg",
    "2026-03-07-paralympics-korea-day1":
        "https://www.paralympic.org/sites/default/files/2026-03/1-Milano%20Cortina%202026%20Paralympic%20Opening%20Ceremony.jpg",
    # tech
    "2026-03-05-openai-nato-military-ai":
        "https://www.techzine.eu/wp-content/uploads/2026/03/OpenAI.jpg",
    "2026-03-05-skhynix-1m-breach":
        "https://thumb.mt.co.kr/cdn-cgi/image/w=1200,h=675,f=auto,fit=crop,g=face/21/2026/03/2026030911085852370_1.jpg",
    "2026-03-05-trump-semiconductor-tariff-100":
        "https://www.aljazeera.com/wp-content/uploads/2025/08/2025-03-03T200456Z_1507691846_RC2Q5DAGI615_RTRMADP_3_USA-TRUMP-1755660040.jpg?resize=1200%2C630&quality=80",
}

MD_FILES = {
    "2026-03-05-iran-hormuz-oil-shock":
        "/home/smileguy07/projects/paperwanderer/content/_trend-topics/economy/2026-03-05-iran-hormuz-oil-shock.md",
    "2026-03-05-won-dollar-1500-exchange-rate":
        "/home/smileguy07/projects/paperwanderer/content/_trend-topics/economy/2026-03-05-won-dollar-1500-exchange-rate.md",
    "2026-03-07-current-account-surplus":
        "/home/smileguy07/projects/paperwanderer/content/_trend-topics/economy/2026-03-07-current-account-surplus.md",
    "2026-03-07-onion-price-collapse":
        "/home/smileguy07/projects/paperwanderer/content/_trend-topics/economy/2026-03-07-onion-price-collapse.md",
    "2026-03-05-bts-march-comeback-confirmed":
        "/home/smileguy07/projects/paperwanderer/content/_trend-topics/entertainment/2026-03-05-bts-march-comeback-confirmed.md",
    "2026-03-05-h1key-mini5-comeback":
        "/home/smileguy07/projects/paperwanderer/content/_trend-topics/entertainment/2026-03-05-h1key-mini5-comeback.md",
    "2026-03-05-kcon-la-2026-lineup":
        "/home/smileguy07/projects/paperwanderer/content/_trend-topics/entertainment/2026-03-05-kcon-la-2026-lineup.md",
    "2026-03-07-kpop-march-comeback-rush":
        "/home/smileguy07/projects/paperwanderer/content/_trend-topics/entertainment/2026-03-07-kpop-march-comeback-rush.md",
    "2026-03-07-netflix-monthly-boyfriend":
        "/home/smileguy07/projects/paperwanderer/content/_trend-topics/entertainment/2026-03-07-netflix-monthly-boyfriend.md",
    "2026-03-05-circuit-breaker-kospi-kosdaq":
        "/home/smileguy07/projects/paperwanderer/content/_trend-topics/finance/2026-03-05-circuit-breaker-kospi-kosdaq.md",
    "2026-03-05-defense-stocks-surge":
        "/home/smileguy07/projects/paperwanderer/content/_trend-topics/finance/2026-03-05-defense-stocks-surge.md",
    "2026-03-05-samsung-200k-breach":
        "/home/smileguy07/projects/paperwanderer/content/_trend-topics/finance/2026-03-05-samsung-200k-breach.md",
    "2026-03-07-oil-shock-korea-economy":
        "/home/smileguy07/projects/paperwanderer/content/_trend-topics/finance/2026-03-07-oil-shock-korea-economy.md",
    "2026-03-05-spring-fine-dust":
        "/home/smileguy07/projects/paperwanderer/content/_trend-topics/health/2026-03-05-spring-fine-dust.md",
    "2026-03-05-gangbuk-motel-serial-murder-psychopath":
        "/home/smileguy07/projects/paperwanderer/content/_trend-topics/history-society/2026-03-05-gangbuk-motel-serial-murder-psychopath.md",
    "2026-03-05-low-birthrate-parental-leave-policy":
        "/home/smileguy07/projects/paperwanderer/content/_trend-topics/history-society/2026-03-05-low-birthrate-parental-leave-policy.md",
    "2026-03-07-lotto-1214":
        "/home/smileguy07/projects/paperwanderer/content/_trend-topics/hobbies/2026-03-07-lotto-1214.md",
    "2026-03-07-neulbom-school-launch":
        "/home/smileguy07/projects/paperwanderer/content/_trend-topics/jobs-education/2026-03-07-neulbom-school-launch.md",
    "2026-03-05-lawmaker-car-rationing":
        "/home/smileguy07/projects/paperwanderer/content/_trend-topics/law-government/2026-03-05-lawmaker-car-rationing.md",
    "2026-03-05-park-wangyeol-extradited":
        "/home/smileguy07/projects/paperwanderer/content/_trend-topics/law-government/2026-03-05-park-wangyeol-extradited.md",
    "2026-03-05-moon-jaein-us-visit":
        "/home/smileguy07/projects/paperwanderer/content/_trend-topics/politics/2026-03-05-moon-jaein-us-visit.md",
    "2026-03-05-north-korea-cruise-missile-destroyer":
        "/home/smileguy07/projects/paperwanderer/content/_trend-topics/politics/2026-03-05-north-korea-cruise-missile-destroyer.md",
    "2026-03-05-prosecution-reform-public-prosecution":
        "/home/smileguy07/projects/paperwanderer/content/_trend-topics/politics/2026-03-05-prosecution-reform-public-prosecution.md",
    "2026-03-05-us-investment-special-act":
        "/home/smileguy07/projects/paperwanderer/content/_trend-topics/politics/2026-03-05-us-investment-special-act.md",
    "2026-03-07-democratic-union-launch":
        "/home/smileguy07/projects/paperwanderer/content/_trend-topics/politics/2026-03-07-democratic-union-launch.md",
    "2026-03-07-iran-war-antiwar-protest":
        "/home/smileguy07/projects/paperwanderer/content/_trend-topics/politics/2026-03-07-iran-war-antiwar-protest.md",
    "2026-03-07-local-election-ppp-chaos":
        "/home/smileguy07/projects/paperwanderer/content/_trend-topics/politics/2026-03-07-local-election-ppp-chaos.md",
    "2026-03-05-apartment-public-price-rise":
        "/home/smileguy07/projects/paperwanderer/content/_trend-topics/real-estate/2026-03-05-apartment-public-price-rise.md",
    "2026-03-05-seoul-housing-supply-shock":
        "/home/smileguy07/projects/paperwanderer/content/_trend-topics/real-estate/2026-03-05-seoul-housing-supply-shock.md",
    "2026-03-05-kf21-first-production-rollout":
        "/home/smileguy07/projects/paperwanderer/content/_trend-topics/science/2026-03-05-kf21-first-production-rollout.md",
    "2026-03-05-lee-junghoo-wbc-ankle-injury":
        "/home/smileguy07/projects/paperwanderer/content/_trend-topics/sports/2026-03-05-lee-junghoo-wbc-ankle-injury.md",
    "2026-03-05-moon-bogyeong-grand-slam-wbc":
        "/home/smileguy07/projects/paperwanderer/content/_trend-topics/sports/2026-03-05-moon-bogyeong-grand-slam-wbc.md",
    "2026-03-05-soh-hyungjun-wbc-pitching":
        "/home/smileguy07/projects/paperwanderer/content/_trend-topics/sports/2026-03-05-soh-hyungjun-wbc-pitching.md",
    "2026-03-05-wbc-korea-japan-preview":
        "/home/smileguy07/projects/paperwanderer/content/_trend-topics/sports/2026-03-05-wbc-korea-japan-preview.md",
    "2026-03-07-paralympics-korea-day1":
        "/home/smileguy07/projects/paperwanderer/content/_trend-topics/sports/2026-03-07-paralympics-korea-day1.md",
    "2026-03-05-openai-nato-military-ai":
        "/home/smileguy07/projects/paperwanderer/content/_trend-topics/tech/2026-03-05-openai-nato-military-ai.md",
    "2026-03-05-skhynix-1m-breach":
        "/home/smileguy07/projects/paperwanderer/content/_trend-topics/tech/2026-03-05-skhynix-1m-breach.md",
    "2026-03-05-trump-semiconductor-tariff-100":
        "/home/smileguy07/projects/paperwanderer/content/_trend-topics/tech/2026-03-05-trump-semiconductor-tariff-100.md",
}


def download_image(url, raw_path):
    cmd = [
        "curl", "-L", "--max-time", "20",
        "-A", "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120.0",
        "--referer", "https://www.google.com/",
        "-o", raw_path,
        url
    ]
    result = subprocess.run(cmd, capture_output=True, timeout=30)
    return result.returncode == 0


def resize_and_save(raw_path, output_path):
    try:
        img = Image.open(raw_path)
        img = img.convert("RGB")
        w, h = img.size
        if w > 800:
            ratio = 800 / w
            new_h = int(h * ratio)
            img = img.resize((800, new_h), Image.LANCZOS)
        img.save(output_path, "JPEG", quality=75, optimize=True)
        if os.path.getsize(output_path) > 150 * 1024:
            img.save(output_path, "JPEG", quality=62, optimize=True)
        return True
    except Exception as e:
        print(f"  PIL 오류: {e}")
        return False


def add_image_to_frontmatter(md_path, image_path):
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
    if re.search(r'^image:', content, re.MULTILINE):
        return False
    new_content = re.sub(
        r'(^title:.*$)',
        r'\1\nimage: ' + image_path,
        content,
        count=1,
        flags=re.MULTILINE
    )
    if new_content == content:
        return False
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    return True


def process_slug(slug, image_url, md_path):
    print(f"\n처리 중: {slug}")
    raw_path = os.path.join(ASSETS_DIR, f"{slug}-raw")
    output_path = os.path.join(ASSETS_DIR, f"{slug}.jpg")
    image_front = f"/assets/images/{slug}.jpg"

    if os.path.exists(output_path) and os.path.getsize(output_path) > 1000:
        print(f"  이미지 이미 존재, frontmatter만 업데이트")
        result = add_image_to_frontmatter(md_path, image_front)
        print(f"  frontmatter {'업데이트됨' if result else '이미 있음'}")
        return True

    print(f"  다운로드: {image_url[:80]}...")
    if not download_image(image_url, raw_path):
        print(f"  다운로드 실패!")
        return False

    if not os.path.exists(raw_path) or os.path.getsize(raw_path) < 1000:
        print(f"  파일 없거나 크기 너무 작음")
        if os.path.exists(raw_path):
            os.remove(raw_path)
        return False

    print(f"  리사이즈 중...")
    if not resize_and_save(raw_path, output_path):
        if os.path.exists(raw_path):
            os.remove(raw_path)
        return False

    if os.path.exists(raw_path):
        os.remove(raw_path)

    size_kb = os.path.getsize(output_path) / 1024
    print(f"  저장완료: {output_path} ({size_kb:.1f}KB)")

    result = add_image_to_frontmatter(md_path, image_front)
    print(f"  frontmatter {'업데이트됨' if result else '이미 있음'}")
    return True


def main():
    success = 0
    fail = 0
    failed_slugs = []

    for slug, image_url in IMAGE_MAP.items():
        md_path = MD_FILES.get(slug)
        if not md_path or not os.path.exists(md_path):
            print(f"경고: {slug} md 파일 없음")
            continue
        try:
            ok = process_slug(slug, image_url, md_path)
            if ok:
                success += 1
            else:
                fail += 1
                failed_slugs.append(slug)
        except Exception as e:
            print(f"  예외: {e}")
            fail += 1
            failed_slugs.append(slug)

    print(f"\n=== 완료 === 성공:{success} 실패:{fail}")
    if failed_slugs:
        print("실패 목록:")
        for s in failed_slugs:
            print(f"  - {s}")


if __name__ == "__main__":
    main()
