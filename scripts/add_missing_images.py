#!/usr/bin/env python3
"""
Add missing images to trend-topic posts for 2026-03-20, 03-21, 03-22
"""

import subprocess
import os
import re
from PIL import Image

BASE_DIR = "/home/smileguy07/projects/paperwanderer"
IMAGES_DIR = os.path.join(BASE_DIR, "assets/images")

# Map: slug -> image URL
IMAGE_MAP = {
    # business
    "2026-03-22-samsung-skhynix-q1-profit": "https://wimg.heraldcorp.com/news/cms/2026/03/18/news-p.v1.20260318.1838dc81f6544e0484d47dfa996706d5_T1.jpg",
    # culture
    "2026-03-21-bts-documentary-the-return": "https://dnm.nflximg.net/api/v6/BvVbc2Wxr2w6QuoANoSpJKEIWjQ/AAAAQQGTKfnTaOtAxnQzW042Y_UQjfoelE9hvhVJenFopOVIaMQvDxEt6HtDzR03YLdLz3-setvCrigBtCZXQmf_xg7jrVFMW3SFnRv7cupuXMRhyA0nQJbJhT0oRO5pnBaYqMZ9FcVwtRGWhtbWcEHsZiTP.jpg?r=c92",
    "2026-03-22-lim-youngwoong-melon-record": "https://wimg.heraldcorp.com/news/cms/2026/03/11/news-p.v1.20260311.e1b534c6ee2544a2bf988a15f7746328_T1.jpg",
    # economy
    "2026-03-21-hormuz-strait-korea-energy": "https://www.greenpeace.org/korea/wp-content/uploads/sites/11/2026/03/hormuz-korea-energy.jpg",
    "2026-03-21-iran-hormuz-toll-controversy": "https://cdn.thepublic.kr/news/photo/202603/297881_300010_2528.jpg",
    "2026-03-21-korea-energy-reserves-200days": "https://img.seoul.co.kr/img/upload/2026/03/05/SSC_20260305100409.jpg",
    "2026-03-21-qatar-lng-supply-disruption": "http://image.imnews.imbc.com/replay/2026/nwdesk/article/__icsFiles/afieldfile/2026/03/25/desk_20260325_200516_1_9_Large.jpg",
    "2026-03-22-hormuz-strait-toll-iran": "https://cdn.thepublic.kr/news/photo/202603/297881_300010_2528.jpg",
    "2026-03-22-oil-price-middle-east-crisis": "https://nimage.g-enews.com/phpwas/restmb_allidxmake.php?idx=999&simg=2026032009182908102fbbec65dfb211211153121.jpg",
    "2026-03-22-supplementary-budget-25t-march": "https://image.imnews.imbc.com/news/2026/politics/article/__icsFiles/afieldfile/2026/03/22/yh_20260322-25.jpg",
    # entertainment
    "2026-03-21-iheartradio-kpop-rose": "https://newsimg.koreatimes.co.kr/2026/03/27/f8762ecc-0db0-4935-9263-1aadb654f9c7.jpg",
    "2026-03-21-kcon-la-2026-lineup": "https://artthreat.net/wp-content/uploads/2026/03/37356-kcon-la-2026-reveals-full-lineup-with-nct-127-txt-zerobaseone.jpg-scaled.png",
    "2026-03-22-project-hail-mary-movie": "https://upload.wikimedia.org/wikipedia/en/thumb/b/b0/Project_Hail_Mary_%28film%29.jpg/220px-Project_Hail_Mary_%28film%29.jpg",
    # finance
    "2026-03-20-kospi-crash-oil-shock": "https://lh3.googleusercontent.com/blogger_img_proxy/AEn0k_s2O_uonHtuZTsShGSw45lgouz-CskylIbr4cSTcCz-3uubNxQ9qWo8JuLbmMQMTfib__nCgM2b4nFWIbeDF1qRUqVT6fNGBZ55RsMbKWqD6G03SasRC-a8PkBLAt6vpbsSR5osqYOqY2qkfvCGBUHtg5MyPXad1ml2D6ZI0haWujKMsc7FjJdOBtU=w1200-h630-p-k-no-nu",
    "2026-03-21-kospi-volatility-march": "https://blogger.googleusercontent.com/img/b/U2hvZWJveA/AVvXsEgfMvYAhAbdHksiBA24JKmb2Tav6K0GviwztID3Cq4VpV96HaJfy0viIu8z1SSw_G9n5FQHZWSRao61M3e58ImahqBtr7LiOUS6m_w59IvDYwjmMcbq3fKW4JSbacqkbxTo8B90dWp0Cese92xfLMPe_tg11g/w1200/",
    "2026-03-21-won-dollar-exchange-rate": "https://cdn.thepublic.kr/news/photo/202603/297881_300010_2528.jpg",
    "2026-03-22-kospi-samsung-hynix-decline": "https://wimg.heraldcorp.com/news/cms/2026/03/24/rcv.YNA.20260322.PYH2026032205400006400_T1.jpg",
    # health
    "2026-03-21-korea-ai-healthcare-startups": "https://thumb.mt.co.kr/cdn-cgi/image/w=1200,h=675,f=auto,fit=crop,g=face/21/2026/03/2026030813581593758_1.jpg",
    "2026-03-21-medical-korea-2026": "https://cdn.weekly.hankooki.com/news/photo/202603/7157117_229507_3939.jpg",
    # history-society
    "2026-03-21-korea-super-aged-society": "https://wimg.heraldcorp.com/news/cms/2026/03/26/news-p.v1.20260326.fdce6b3fdfa249b1a0983c580d9f466f_T1.jpg",
    "2026-03-21-trump-xi-korea-japan-closer": "https://wimg.heraldcorp.com/news/cms/2026/03/18/news-p.v1.20260318.1838dc81f6544e0484d47dfa996706d5_T1.jpg",
    "2026-03-22-daejeon-fire-ceo-verbal-abuse": "https://img.sbs.co.kr/newimg/news/20260324/202168258.jpg",
    # law-government
    "2026-03-21-bts-concert-overmobilization": "https://thumb.mt.co.kr/cdn-cgi/image/w=1200,h=675,fit=cover,bg=whilte,f=auto,quality=high,sharpen=2,g=face/21/2026/03/2026032219451443515_1.jpg",
    "2026-03-21-daejeon-fire-ceo-controversy": "https://wimg.heraldcorp.com/news/cms/2026/03/24/rcv.YNA.20260322.PYH2026032205400006400_T1.jpg",
    # online-community
    "2026-03-21-bts-gwanghwamun-controversy": "https://wimg.heraldcorp.com/news/cms/2026/03/23/news-p.v1.20260323.cfcc7df6885b4d1a9edf928a8a54f2e8_T1.jpg",
    # politics
    "2026-03-21-general-election-prep-satellite-party": "https://wimg.heraldcorp.com/news/cms/2026/03/18/news-p.v1.20260318.1838dc81f6544e0484d47dfa996706d5_T1.jpg",
    "2026-03-21-iran-us-war-middle-east": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/President_Donald_J._Trump_oversees_Operation_Epic_Fury_at_Mar-a-Lago%2C_Palm_Beach%2C_FL%2C_Feb._28%2C_2026._%28White_House_photo_by_Daniel_Torok%29_%2855121599389%29.jpg/250px-President_Donald_J._Trump_oversees_Operation_Epic_Fury_at_Mar-a-Lago%2C_Palm_Beach%2C_FL%2C_Feb._28%2C_2026._%28White_House_photo_by_Daniel_Torok%29_%2855121599389%29.jpg",
    "2026-03-21-lee-jaemyung-csis-speech": "https://wimg.heraldcorp.com/news/cms/2026/03/20/news-p.v1.20260320.5a15d22744eb457898ef2bcd4fdd2df5_T1.jpg",
    "2026-03-21-sbs-lee-jaemyung-apology": "https://image.imnews.imbc.com/news/2026/politics/article/__icsFiles/afieldfile/2026/03/21/jhp_20260321_7.jpg",
    "2026-03-22-local-elections-june-2026": "https://wimg.heraldcorp.com/news/cms/2026/03/18/news-p.v1.20260318.1838dc81f6544e0484d47dfa996706d5_T1.jpg",
    "2026-03-22-north-korea-spa-kim-jong-un": "https://wimg.heraldcorp.com/news/cms/2026/03/23/news-p.v1.20260226.d0b7cf934bcd424e893f97751acaf7fd_T1.jpg",
    # real-estate
    "2026-03-21-korea-real-estate-tenant-market": "https://lh3.googleusercontent.com/blogger_img_proxy/AEn0k_tE4xAJImx5uZGeafT_JqucusNz5llccSqxMTcZPRIqNDneB9ZBElYSrxhGba1Pjte_M1SJFPe9OZRJQIgVpwaAe6o-DG59d0AP3mDLonadR8mRYvFT6xwLdTB-bcfsBuZL-zkSI-F77Dj41uabmz-_rv1Bt7XG28X7HeerTxuMi-Utg7C9JSBnnYE=w1200-h630-p-k-no-nu",
    "2026-03-22-seoul-public-price-surge": "http://image.imnews.imbc.com/replay/2026/nwdesk/article/__icsFiles/afieldfile/2026/03/17/desk_20260317_203541_1_23_Large.jpg",
    # science
    "2026-03-21-spring-high-temperature-drought": "https://cdn.daehanilbo.co.kr/news/photo/202603/65156_67604_481.jpg",
    "2026-03-21-spring-wildfire-risk": "https://cdn.daehanilbo.co.kr/news/photo/202603/65156_67604_481.jpg",
    # sports
    "2026-03-21-kbo-preseason-2026": "https://www.ikbc.co.kr/data/kbc/image/2026/02/04/kbc202602040119.jpg",
    "2026-03-21-wbc-2026-venezuela-champion": "https://sportshub.cbsistatic.com/i/r/2026/03/17/wbc-2026-venezuela.jpg",
    "2026-03-22-hong-myungbo-worldcup-squad": "https://thumb.mt.co.kr/cdn-cgi/image/w=1200,h=675,fit=cover,bg=whilte,f=auto,quality=high,sharpen=2,g=face/21/2026/03/2026032717345163925_3.jpg",
    # tech
    "2026-03-21-kimes-2026-ai-dementia": "https://cdn.dementianews.co.kr/news/photo/202603/10916_22463_1216.jpg",
    "2026-03-21-korea-ai-startup-investment": "https://startuprecipe.co.kr/wp-content/uploads/2026/03/260306_SBVA_500235-1200x799.jpg",
    "2026-03-22-ai-gpu-infrastructure": "https://image.zdnet.co.kr/2025/12/15/618f95745d768e958e642c54ea72e867.jpg",
    "2026-03-22-semiconductor-supply-chain-crisis": "https://nimage.g-enews.com/phpwas/restmb_allidxmake.php?idx=999&simg=20260319162523095810c8c1c064d22114611240.jpg",
    # finance extra
    "2026-03-22-youth-debt-borrow-invest": "https://cdn.thepublic.kr/news/photo/202603/297881_300010_2528.jpg",
    # law-government extra
    "2026-03-22-daejeon-factory-fire": "https://img.sbs.co.kr/newimg/news/20260324/202168258.jpg",
    # history-society extra
    "2026-03-21-daejeon-factory-fire": "https://img.sbs.co.kr/newimg/news/20260324/202168258.jpg",
    # law-government 03-20
    "2026-03-20-daejeon-factory-fire": "https://img.sbs.co.kr/newimg/news/20260324/202168258.jpg",
}

def download_and_resize(slug, url, md_file):
    raw_path = os.path.join(IMAGES_DIR, f"{slug}-raw")
    jpg_path = os.path.join(IMAGES_DIR, f"{slug}.jpg")

    # Skip if already done
    if os.path.exists(jpg_path):
        print(f"  [SKIP] {slug}.jpg already exists")
        return True

    print(f"  Downloading {slug}...")
    result = subprocess.run(
        ["curl", "-L", "--max-time", "15", "-A", "Mozilla/5.0", "-o", raw_path, url],
        capture_output=True
    )

    if result.returncode != 0 or not os.path.exists(raw_path) or os.path.getsize(raw_path) < 1000:
        print(f"  [FAIL] Download failed for {slug}: {result.stderr.decode()[:100]}")
        if os.path.exists(raw_path):
            os.remove(raw_path)
        return False

    try:
        img = Image.open(raw_path)
        img = img.convert("RGB")

        # Resize: max 800px width
        w, h = img.size
        if w > 800:
            ratio = 800 / w
            img = img.resize((800, int(h * ratio)), Image.LANCZOS)

        # Save with quality 75
        img.save(jpg_path, "JPEG", quality=75, optimize=True)

        # Check size: if > 150KB, re-save with quality 62
        if os.path.getsize(jpg_path) > 150 * 1024:
            img.save(jpg_path, "JPEG", quality=62, optimize=True)

        size_kb = os.path.getsize(jpg_path) / 1024
        print(f"  [OK] {slug}.jpg saved ({size_kb:.1f}KB)")
        os.remove(raw_path)
        return True

    except Exception as e:
        print(f"  [FAIL] Image processing failed for {slug}: {e}")
        if os.path.exists(raw_path):
            os.remove(raw_path)
        return False


def add_image_to_frontmatter(md_file, slug):
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if image already exists
    if re.search(r'^image:', content, re.MULTILINE):
        print(f"  [SKIP] {md_file} already has image field")
        return

    image_value = f"/assets/images/{slug}.jpg"

    # Insert image after description field
    new_content = re.sub(
        r'(^description:.*$)',
        r'\1\nimage: ' + image_value,
        content,
        count=1,
        flags=re.MULTILINE
    )

    if new_content == content:
        # Try inserting before the closing ---
        lines = content.split('\n')
        # Find second ---
        dashes = [i for i, l in enumerate(lines) if l.strip() == '---']
        if len(dashes) >= 2:
            insert_pos = dashes[1]
            lines.insert(insert_pos, f'image: {image_value}')
            new_content = '\n'.join(lines)

    with open(md_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"  [OK] Added image field to {os.path.basename(md_file)}")


# Find all target files missing image
import glob

target_files = []
for md_file in sorted(glob.glob(f"{BASE_DIR}/content/_trend-topics/**/*.md", recursive=True)):
    basename = os.path.basename(md_file)
    if not any(basename.startswith(d) for d in ['2026-03-20', '2026-03-21', '2026-03-22']):
        continue
    with open(md_file, 'r') as f:
        content = f.read()
    if 'image:' not in content:
        slug = os.path.splitext(basename)[0]
        target_files.append((slug, md_file))

print(f"Found {len(target_files)} files missing image field\n")

success_count = 0
skip_count = 0
fail_count = 0

for slug, md_file in target_files:
    print(f"\nProcessing: {slug}")
    url = IMAGE_MAP.get(slug)
    if not url:
        print(f"  [SKIP] No image URL mapped for {slug}")
        skip_count += 1
        continue

    ok = download_and_resize(slug, url, md_file)
    if ok:
        add_image_to_frontmatter(md_file, slug)
        success_count += 1
    else:
        fail_count += 1

print(f"\n\nDone! Success: {success_count}, Skipped: {skip_count}, Failed: {fail_count}")
