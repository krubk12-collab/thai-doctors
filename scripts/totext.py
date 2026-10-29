# html → บรรทัดข้อความ (ตัด script/style) เขียนทับเป็น .txt แล้วลบ html
import re, html, sys, os
for f in sys.argv[1:]:
    s = open(f, encoding='utf8', errors='replace').read()
    t = re.sub(r'<script.*?</script>|<style.*?</style>|<!--.*?-->', '', s, flags=re.S)
    L = [x.strip() for x in html.unescape(re.sub(r'<[^>]+>', '\n', t)).split('\n') if x.strip()]
    open(f[:-5] + '.txt', 'w', encoding='utf8').write('\n'.join(L)); os.remove(f)
