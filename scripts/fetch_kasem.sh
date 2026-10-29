#!/bin/bash
# เครือเกษมราษฎร์: หน้ารายชื่อ /th/<สาขา>/doctor?page=N (เรนเดอร์จากเซิร์ฟเวอร์ ชื่อ+เลข ว.+แผนก) → ksm/<สาขา>_<N>.html
# จำนวนหน้า = ceil("ผลการค้นหา N รายการ" / 12) + 1 เผื่อ
cd "$(dirname "$0")"; mkdir -p ksm
get() { [ -s "$2" ] || { curl -s -L --max-time 30 "$1" -o "$2"; sleep 0.6; }; }
for b in bangkae chachoengsao maesai pathumthani prachachuen prachinburi ramkhamhaeng rattanatibeth saraburi sriburin; do
  get "https://www.kasemrad.co.th/th/$b/doctor?page=1" "ksm/${b}_1.html"
  t=$(grep -o 'ผลการค้นหา<!-- --> <!-- -->[0-9]*' "ksm/${b}_1.html" | grep -o '[0-9]*$' | head -1)
  for n in $(seq 2 $(( (t + 11) / 12 + 1 ))); do get "https://www.kasemrad.co.th/th/$b/doctor?page=$n" "ksm/${b}_$n.html"; done
  echo "$b $t $(cat ksm/${b}_*.html | grep -o '[นทพ]*[พญ]\. [^<]*' | sort -u | wc -l)"
done
