#!/bin/bash
# ดึงหน้าแพทย์จาก sitemap ทีละหน้าด้วย curl (UA ของ curl เอง ไม่ปลอม) เว้น 0.6 วิ · แคชใน <โฟลเดอร์>/ ข้ามไฟล์ที่มี
# ใช้: bash fetch_sitemap.sh <sitemap url> <โฟลเดอร์> [grep -E กรอง url]
mkdir -p "$2"; n=0
curl -s -L --max-time 30 "$1" | grep -o '<loc>[^<]*' | sed 's/<loc>//; s/[[:space:]]//g' | grep -E "${3:-.}" | while read -r u; do
  f="$2/$(echo "${u#*://}" | sed 's/[^A-Za-z0-9._-]/_/g' | tail -c 150).html"
  [ -s "$f" ] && continue; [ -s "${f%.html}.txt" ] && continue
  curl -s -L --max-time 30 "$u" -o "$f" || echo "ERR $u"; [ -n "$STRIP" ] && python totext.py "$f"
  n=$((n+1)); [ $((n % 50)) = 0 ] && echo "$n"
  sleep 0.6
done; echo done
