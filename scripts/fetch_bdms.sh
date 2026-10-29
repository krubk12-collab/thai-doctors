#!/bin/bash
# เครือ รพ.กรุงเทพ ทุกสาขา: sitemap-<สาขา>.xml → หน้า sitemap แพทย์ภาษาไทย → fetch_sitemap.sh (STRIP=1 เก็บ .txt ใน bkh/)
cd "$(dirname "$0")"
for b in "$@"; do
  curl -s -L --max-time 30 "https://www.bangkokhospital.com/sitemap-$b.xml" | grep -o '<loc>[^<]*post/doctor?locale=th[^<]*' | sed 's/<loc>//; s/&amp;/\&/g' | while read -r u; do
    echo "== $b $u"; STRIP=1 bash fetch_sitemap.sh "$u" bkh
  done
done; echo ALLDONE
