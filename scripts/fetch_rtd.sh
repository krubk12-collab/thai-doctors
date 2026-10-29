#!/bin/bash
# ทะเบียนผู้เชี่ยวชาญราชวิทยาลัยทันตแพทย์ฯ ทั้งประเทศ: dent/all_ids.txt → dent/i_<id>.html (ข้ามไฟล์ที่มี เว้น 0.6 วิ)
cd "$(dirname "$0")/dent"; n=0
for id in $(tr -d '\r' < all_ids.txt); do
  [ -s "i_$id.html" ] && continue
  curl -s -L --max-time 30 "https://www.royalthaident.org/specialist/info/$id" -o "i_$id.html" || echo "ERR $id"
  n=$((n+1)); [ $((n % 100)) = 0 ] && echo "$n"; sleep 0.6
done; echo ALLDONE
