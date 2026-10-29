# รวมรายชื่อแพทย์ นนทบุรี+กทม.+ปริมณฑล จากเว็บ รพ. → Desktop/sick/doctors.js
import re, html, json, glob, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
T = lambda s: re.sub(r'^นายแพทย์', 'นพ.', re.sub(r'^แพทย์หญิง', 'พญ.', re.sub(r'^ทันตแพทย์หญิง', 'ทพญ.', s.strip()))).replace('  ', ' ')
H = [  # id, ชื่อ, ประเภท, อำเภอ, โทร, แหล่ง
 ['nv', 'โรงพยาบาลนนทเวช', 'เอกชน', 'เมืองนนทบุรี', '02-596-7888', 'https://www.nonthavej.co.th/medical-services/doctors'],
 ['ccit', 'สถาบันโรคทรวงอก', 'รัฐ (กรมการแพทย์) เฉพาะทางหัวใจ-ปอด', 'เมืองนนทบุรี', '02-547-0999', 'https://www.ccit.go.th/doctor/search.php'],
 ['pcmc', 'ศูนย์การแพทย์ปัญญานันทภิกขุ ชลประทาน', 'รัฐ (มศว)', 'ปากเกร็ด', '02-502-2345', 'https://pcmc.swu.ac.th/doctor-time.html'],
 ['bidi', 'สถาบันบำราศนราดูร', 'รัฐ (กรมควบคุมโรค)', 'เมืองนนทบุรี', '', 'https://ddc.moph.go.th/bidi/'],
 ['st', 'โรงพยาบาลศรีธัญญา', 'รัฐ (กรมสุขภาพจิต) จิตเวช', 'เมืองนนทบุรี', '02-528-7800', 'https://www.srithanya.go.th/'],
 ['kr', 'โรงพยาบาลเกษมราษฎร์ อินเตอร์เนชั่นแนล รัตนาธิเบศร์', 'เอกชน', 'บางใหญ่', '', 'https://www.kasemrad.co.th/th/rattanatibeth/doctor'],
 ['vbp', 'โรงพยาบาลวิภารามปากเกร็ด', 'เอกชน', 'ปากเกร็ด', '', 'https://www.vibharampakkred.com/doctor-list.php'],
]
D = []  # [hid, ชื่อ, แผนก, สาขา/ความเชี่ยวชาญ, วันออกตรวจ]
for o in json.load(open('nv.json', encoding='utf8')):
    D.append(['nv', o['n'], o['dept'] or '', '' if o['sp'] in ('-', '') else o['sp'], ''])
for l in open('ccit/list.txt', encoding='utf8').read().split('\n'):
    if l.strip(): n, d, e = l.split('|'); D.append(['ccit', T(n), d, e, ''])
for l in open('pcmc/list.txt', encoding='utf8').read().split('\n'):
    if l.strip(): d, n, e = l.split('|'); D.append(['pcmc', T(n), d, e, ''])
for l in open('st/list.txt', encoding='utf8').read().split('\n'):
    if l.strip(): n, w = l.split('|'); D.append(['st', n, 'จิตเวช', '', w])
for l in open('vbp.txt', encoding='utf8').read().split('\n'):
    if l.strip(): n, e = l.split('|'); D.append(['vbp', n, '', e, ''])
KR = """นพ.เธียร ขัตตินานนท์|แผนกกระดูกและข้อ
นพ.ปิยณัฐ รัตนเดช|แผนกอายุรกรรม
นพ.รักษิต หริจันทนะวงศ์|แผนกกุมารเวชกรรมทั่วไป
นพ.สิทธิคมน์ สัตยารักษ์|แผนกสูตินรีเวชกรรม
พญ.ปวรา อุตราภรณ์|แผนกสูตินรีเวชกรรม
นพ.กฤษณะ ธนะชาญพัฒนา|แผนกอายุรกรรม
พญ.พลอยนภัส ศิริเอี่ยมแสง|แผนกอายุรกรรม
นพ.จิรายุ พันทอง|คลินิคตรวจสุขภาพ
นพ.สายัณ ม่วงน้อยเจริญ|ศัลยกรรมทั่วไปอุบัติเหตุ
นพ.สถิต กุลนรัตน์|ศัลยกรรมทั่วไปอุบัติเหตุ"""
for l in KR.split('\n'): n, d = l.split('|'); D.append(['kr', n, d, '', ''])
# บำราศฯ: หน้าแผนก → ชื่อแพทย์ + หัวข้อย่อย (อนุสาขา) ที่อยู่ก่อนหน้า
for f in sorted(glob.glob('bidi/*.html')):
    s = open(f, encoding='utf8').read()
    t = re.sub(r'<script.*?</script>|<style.*?</style>|<!--.*?-->', '', s, flags=re.S)
    L = [x.strip() for x in html.unescape(re.sub(r'<[^>]+>', '\n', t)).split('\n') if x.strip()]
    i = next(k for k, x in enumerate(L) if 'กรุณาโทร.สอบถาม' in x)
    dept = next(x for x in L[i-12:i] if x.startswith('แผนก'))
    tel = next((re.search(r'โทร\.?\s*([\d\-, ]+)', x).group(1).strip(' ,') for x in L[i-12:i] if 'โทร' in x), '')
    sub = ''
    for x in L[i+1:]:
        if x in ('*', '-->'): continue
        if x == 'กลุ่มโรค': break
        if re.match(r'^(นายแพทย์|แพทย์หญิง|ทันตแพทย์|ว่าที่)', x): D.append(['bidi', T(x), dept + (' โทร ' + tel if tel else ''), sub, ''])
        else: sub = x
for h in H: h.append('นนทบุรี')  # คอลัมน์ 7 = จังหวัด

# ── กทม.+ปริมณฑล (29ต.ค.69) ดึงจาก sitemap ด้วย fetch_sitemap.sh ──
def lines(f):
    if not os.path.exists(f): return []  # ไฟล์ .html ถูกแปลงเป็น .txt ระหว่างที่ตัวดึงยังวิ่งอยู่
    s = open(f, encoding='utf8', errors='replace').read()
    if f.endswith('.txt'): return s.split('\n')
    t = re.sub(r'<script.*?</script>|<style.*?</style>|<!--.*?-->', '', s, flags=re.S)
    return [x.strip() for x in html.unescape(re.sub(r'<[^>]+>', '\n', t)).split('\n') if x.strip()]
DAY = re.compile(r'^(วัน)?(จันทร์|อังคาร|พุธ|พฤหัสบดี|ศุกร์|เสาร์|อาทิตย์)$')
TIME = re.compile(r'\d{1,2}[:.]\d{2}\s*-\s*\d{1,2}[:.]\d{2}')
def days(L):  # วันที่มีเวลาตามหลัง
    out, cur = [], None
    for x in L:
        m = DAY.match(x)
        if m: cur = m.group(2); continue
        if cur and TIME.search(x) and cur not in out: out.append(cur)
    return ', '.join(out)
N0 = lambda s: re.sub(r'(นพ|พญ|ทพ|ทพญ|ศ|รศ|ผศ|อ)[.]\s+', lambda m: m.group(1) + '.', re.sub(r'\s+', ' ', T(s)))
# รหัสคลินิกนำหน้า "(PBC) " ออก · ยศทหาร "พันโท แพทย์หญิง" → "พันโท พญ." · "พ. ต. ต." → "พ.ต.ต."
N = lambda s: re.sub(r'(?<=[ก-๙]\.)\s+(?=[ก-๙]{1,4}\.)', '', N0(re.sub(r'\s(นายแพทย์|แพทย์หญิง)\s*', lambda m: ' ' + {'นายแพทย์': 'นพ.', 'แพทย์หญิง': 'พญ.'}[m.group(1)], re.sub(r'^\([A-Z]+\)\s*', '', s.strip()))))
H += [
 ['pl_rs', 'โรงพยาบาลเปาโล รังสิต', 'เอกชน', 'ธัญบุรี', '1772', 'https://www.paolohospital.com/th-TH/rangsit/', 'ปทุมธานี'],
 ['pl_sp', 'โรงพยาบาลเปาโล สมุทรปราการ', 'เอกชน', 'เมืองสมุทรปราการ', '1772', 'https://www.paolohospital.com/th-TH/samutprakarn/', 'สมุทรปราการ'],
 ['pl_pd', 'โรงพยาบาลเปาโล พระประแดง', 'เอกชน', 'พระประแดง', '1772', 'https://www.paolohospital.com/th-TH/phrapradaeng/', 'สมุทรปราการ'],
 ['pl_kc', 'โรงพยาบาลเปาโล โชคชัย 4', 'เอกชน', 'ลาดพร้าว', '1772', 'https://www.paolohospital.com/th-TH/chokchai4/', 'กรุงเทพฯ'],
 ['pl_ks', 'โรงพยาบาลเปาโล เกษตร', 'เอกชน', 'จตุจักร', '1772', 'https://www.paolohospital.com/th-TH/kaset/', 'กรุงเทพฯ'],
 ['tb', 'โรงพยาบาลธนบุรี', 'เอกชน', 'บางกอกน้อย', '02-487-2000', 'https://www.thonburihospital.com/doctor/', 'กรุงเทพฯ'],
 ['vbd', 'โรงพยาบาลวิภาวดี', 'เอกชน', 'จตุจักร', '02-561-1111', 'https://www.vibhavadi.com/th/doctor', 'กรุงเทพฯ'],
 ['tu', 'โรงพยาบาลธรรมศาสตร์เฉลิมพระเกียรติ', 'รัฐ (มหาวิทยาลัยธรรมศาสตร์)', 'คลองหลวง', '02-926-9999', 'https://hospital.tu.ac.th/th/doctors', 'ปทุมธานี'],
]
PL = {'เปาโล รังสิต': 'pl_rs', 'เปาโล สมุทรปราการ': 'pl_sp', 'เปาโล พระประแดง': 'pl_pd', 'เปาโล โชคชัย4': 'pl_kc', 'เปาโล เกษตร': 'pl_ks'}
for f in sorted(glob.glob('paolo/*')):
    L = lines(f)
    if 'แพทย์ทั้งหมด' not in L: continue
    i = L.index('แพทย์ทั้งหมด'); hid = PL.get(L[L.index('สาขา', i) + 1])
    if not hid: print('?สาขา', f, L[L.index('สาขา', i) + 1]); continue
    spec = L[i + 3] if L[i + 3] not in ('นัดหมายแพทย์', 'สาขา') else ''
    tel = next((m.group(0) for k, x in enumerate(L) if x == 'เบอร์โทร' and L[k + 1] != '1772' for m in [re.search(r'0[\d\-]{8,}(\s*ต่อ\s*[\d ,]+)?', L[k + 1])] if m), '').strip(' ,')
    D.append([hid, N(L[i + 1]), L[i + 2] + (' โทร ' + tel if tel else ''), spec, ''])
for f in sorted(glob.glob('thonburi/*')):
    L = lines(f)
    if 'ศูนย์:' not in L: continue
    i = L.index('ศูนย์:'); sp = L[i + 3].replace('แพทย์ผู้ชำนาญการทางด้าน', '') if L[i + 2] == 'ผู้ชำนาญการ:' else ''
    D.append(['tb', N(L[i - 1]), L[i + 1], sp, ''])
for f in sorted(glob.glob('vibhavadi/*')):
    L = lines(f)
    if 'สาขาที่เชี่ยวชาญ' not in L: continue
    k = L.index('นัดหมายเเพทย์'); s = L.index('สาขาที่เชี่ยวชาญ')
    sch = L[L.index('ตารางแพทย์ออกตรวจ'):] if 'ตารางแพทย์ออกตรวจ' in L else []
    D.append(['vbd', N(L[k - 3]), L[k - 1], L[s + 1] if L[s + 1] != 'ประวัติแพทย์' else '', days(sch[:40])])
for f in sorted(glob.glob('tu/*')):
    L = lines(f)
    if 'กลับสู่หน้าค้นหาแพทย์' not in L: continue
    i = L.index('กลับสู่หน้าค้นหาแพทย์'); seg = L[i:i + 80]
    dept = seg[seg.index('หน่วยตรวจ') + 1] if 'หน่วยตรวจ' in seg else ''
    sp = seg[seg.index('ความชำนาญเฉพาะทางสาขา') + 1] if 'ความชำนาญเฉพาะทางสาขา' in seg else ''
    end = seg.index('โรงพยาบาลธรรมศาสตร์เฉลิมพระเกียรติ') if 'โรงพยาบาลธรรมศาสตร์เฉลิมพระเกียรติ' in seg else len(seg)
    D.append(['tu', N(L[i + 1]), dept, sp if sp != 'ตารางออกตรวจ' else '', days(seg[:end])])
# พญาไท (29ต.ค.69 ลูกพี่อนุญาต) ดึงหน้าแพทย์จาก sitemap content-doctor-th-1..7 (robots ห้าม /api/ เลยไม่ใช้ API) · ตัดศรีราชา (ชลบุรี)
H += [
 ['pyt1', 'โรงพยาบาลพญาไท 1', 'เอกชน', 'ราชเทวี', '1772, 02-201-4600', 'https://www.phyathai.com/th/pyt1/doctor', 'กรุงเทพฯ'],
 ['pyt2', 'โรงพยาบาลพญาไท 2', 'เอกชน', 'พญาไท', '1772, 02-617-2444', 'https://www.phyathai.com/th/pyt2/doctor', 'กรุงเทพฯ'],
 ['pyt3', 'โรงพยาบาลพญาไท 3', 'เอกชน', 'ภาษีเจริญ', '1772, 02-467-1111', 'https://www.phyathai.com/th/pyt3/doctor', 'กรุงเทพฯ'],
 ['pytn', 'โรงพยาบาลพญาไท นวมินทร์', 'เอกชน', 'บึงกุ่ม', '1772, 02-944-7111', 'https://www.phyathai.com/th/pytn/doctor', 'กรุงเทพฯ'],
 ['pytp', 'โรงพยาบาลพญาไท พหลโยธิน', 'เอกชน', 'พญาไท', '1772, 02-271-7000', 'https://www.phyathai.com/th/pytp/doctor', 'กรุงเทพฯ'],
]
for f in sorted(glob.glob('pyt/*')):
    L = lines(f); hid = re.search(r'_(pyt[123np])_doctor_', f).group(1)
    if 'พญาไท ศรีราชา' not in L: continue
    st = L.index('พญาไท ศรีราชา')
    get = lambda lab: next((L[k + 1] for k in range(st, min(len(L) - 1, st + 40)) if L[k] == lab), '')
    sp = get('ความชำนาญพิเศษเฉพาะทาง') or get('ความชำนาญ')
    D.append([hid, N(L[0].split(' - ')[0]), get('ศูนย์'), sp, ''])

# รามาธิบดี: experts/index.php?keyword= (ว่าง) คืนตารางออกตรวจทุกหน่วยตรวจในหน้าเดียว → หน่วยตรวจ + [บทบาท] + วัน
H.append(['rama', 'โรงพยาบาลรามาธิบดี', 'รัฐ (โรงเรียนแพทย์ ม.มหิดล)', 'ราชเทวี', '02-201-1000', 'https://www.rama.mahidol.ac.th/experts/', 'กรุงเทพฯ'])
RM = {}
for sec in re.split(r'class="tabtitle-opd"', open('rama/all.html', encoding='utf8').read())[1:]:
    clinic = re.sub(r'\s*(ศูนย์การแพทย์สมเด็จพระเทพรัตน์|อาคาร\s*\d|ชั้น\s*\d).*$', '', html.unescape(re.sub(r'<[^>]+>', '', sec.split('</h4>')[0])).strip(' >'))
    for row in sec.split('class="opd-schedule-tr"')[1:]:
        day = (re.search(r'cn_day">([^<]*)', row) or [None, ''])[1].strip()
        for eid, n, role in re.findall(r'eid=(\d+)[^>]*>([^<]*)</a>\[([^\]]*)\]', row):
            r = RM.setdefault(eid, [N(html.unescape(n)), [], [], []])
            for lst, x in ((r[1], clinic), (r[2], role.strip()), (r[3], day)):
                if x and x not in lst: lst.append(x)
DAYS = 'จันทร์ อังคาร พุธ พฤหัสบดี ศุกร์ เสาร์ อาทิตย์'.split()
for n, cl, ro, dy in RM.values():
    D.append(['rama', n, ' · '.join(cl), ' · '.join(ro), ', '.join(sorted(dy, key=lambda d: DAYS.index(d) if d in DAYS else 9))])

# ── รอบ 2 (29ต.ค.69 บ่าย) สมิติเวช / บำรุงราษฎร์ / เวชธานี / เครือ รพ.กรุงเทพ — sitemap ของแต่ละเว็บ ──
H += [
 ['smt_sk', 'โรงพยาบาลสมิติเวช สุขุมวิท', 'เอกชน', 'วัฒนา', '02-022-2222', 'https://www.samitivejhospitals.com/th/doctor', 'กรุงเทพฯ'],
 ['smt_sn', 'โรงพยาบาลสมิติเวช ศรีนครินทร์', 'เอกชน', 'ประเวศ', '', 'https://www.samitivejhospitals.com/th/doctor', 'กรุงเทพฯ'],
 ['smt_cs', 'โรงพยาบาลเด็กสมิติเวช (สุขุมวิท)', 'เอกชน เฉพาะเด็ก', 'วัฒนา', '', 'https://www.samitivejhospitals.com/th/doctor', 'กรุงเทพฯ'],
 ['smt_cn', 'โรงพยาบาลเด็กสมิติเวช (ศรีนครินทร์)', 'เอกชน เฉพาะเด็ก', 'ประเวศ', '', 'https://www.samitivejhospitals.com/th/doctor', 'กรุงเทพฯ'],
 ['smt_tb', 'โรงพยาบาลสมิติเวช ธนบุรี', 'เอกชน', 'ธนบุรี', '', 'https://www.samitivejhospitals.com/th/doctor', 'กรุงเทพฯ'],
 ['smt_ct', 'โรงพยาบาลสมิติเวช ไชน่าทาวน์', 'เอกชน', 'สัมพันธวงศ์', '', 'https://www.samitivejhospitals.com/th/doctor', 'กรุงเทพฯ'],
 ['smt_sr', 'โรงพยาบาลสมิติเวช ศรีราชา', 'เอกชน', 'ศรีราชา', '', 'https://www.samitivejhospitals.com/th/doctor', 'ชลบุรี'],
 ['smt_x', 'โรงพยาบาลสมิติเวช (เว็บไม่ระบุสาขา)', 'เอกชน · สุขุมวิท/ศรีนครินทร์/ธนบุรี ฯลฯ โทรถามสาขาก่อนไป', 'ไม่ระบุเขต', '02-022-2222', 'https://www.samitivejhospitals.com/th/doctor', 'กรุงเทพฯ'],
 ['smt_cb', 'โรงพยาบาลสมิติเวช ชลบุรี', 'เอกชน', 'เมืองชลบุรี', '', 'https://www.samitivejhospitals.com/th/doctor', 'ชลบุรี'],
 ['bh', 'โรงพยาบาลบำรุงราษฎร์', 'เอกชน', 'วัฒนา', '1378', 'https://www.bumrungrad.com/th/doctors', 'กรุงเทพฯ'],
 ['vj', 'โรงพยาบาลเวชธานี', 'เอกชน', 'บางกะปิ', '02-734-0000', 'https://www.vejthani.com/th/', 'กรุงเทพฯ'],
 ['bkh', 'โรงพยาบาลกรุงเทพ สำนักงานใหญ่', 'เอกชน', 'ห้วยขวาง', '1719', 'https://www.bangkokhospital.com/th/bangkok/doctor', 'กรุงเทพฯ'],
 ['bkh_heart', 'โรงพยาบาลหัวใจกรุงเทพ', 'เอกชน เฉพาะทางหัวใจ', 'ห้วยขวาง', '1719', 'https://www.bangkokhospital.com/th/bangkok-heart/doctor', 'กรุงเทพฯ'],
 ['bkh_sanamchan', 'โรงพยาบาลกรุงเทพสนามจันทร์', 'เอกชน', 'เมืองนครปฐม', '1719', 'https://www.bangkokhospital.com/th/sanamchan/doctor', 'นครปฐม'],
]
SMB = [('เด็กสมิติเวช อินเตอร์เนชั่นแนล (สุขุมวิท)', 'smt_cs'), ('เด็กสมิติเวช อินเตอร์เนชั่นแนล (ศรีนครินทร์)', 'smt_cn'), ('สุขุมวิท', 'smt_sk'), ('ศรีนครินทร์', 'smt_sn'),
       ('ธนบุรี', 'smt_tb'), ('ไชน่าทาวน์', 'smt_ct'), ('ศรีราชา', 'smt_sr'), ('ชลบุรี', 'smt_cb')]
miss = 0
for f in sorted(glob.glob('smt/*')):
    L = lines(f)
    if 'Doctors Listing' not in L: continue
    i = L.index('Doctors Listing'); seg = L[i + 1:i + 6]
    br = seg[1] if not seg[1].startswith(('สาขา', 'อนุสาขา')) else ''
    sp = ' · '.join(x for x in seg[1:4] if x.startswith(('สาขา', 'อนุสาขา')))
    hids = []
    for b in br.split(', '):
        h = next((k for s, k in SMB if s in b), None)
        if h and h not in hids: hids.append(h)
    if not hids: miss += 1; hids = ['smt_x']  # หน้าเว็บไม่บอกสาขา → ไม่เดา
    for h in hids: D.append([h, N(seg[0]), '', sp, ''])
print('สมิติเวชไม่ระบุสาขา รพ.', miss)
for f in sorted(glob.glob('bh/*')):
    L = lines(f)
    if not L or ' | โรงพยาบาลบำรุงราษฎร์' not in L[0]: continue
    n, _, sp = L[0].split(' | ')[0].partition(' - ')
    D.append(['bh', N(n), '', sp, ''])
for f in sorted(glob.glob('vj/*')):
    L = lines(f)
    if not L or 'อนุสาขา' not in L: continue
    i = L.index('อนุสาขา'); g = L[i + 3] if L[i + 2] == 'กลุ่มสาขา' else ''
    D.append(['vj', N(L[0].split(' - ')[0]), g, L[i + 1], ''])
for f in sorted(glob.glob('bkh/*')):
    L = lines(f); m = re.search(r'_th_([a-z-]+)_doctor_', f)
    if not L or not m or 'ความชำนาญเฉพาะทางสาขา' not in L: continue
    hid = {'bangkok': 'bkh', 'bangkok-heart': 'bkh_heart', 'sanamchan': 'bkh_sanamchan'}.get(m.group(1))
    if not hid: continue
    get = lambda lab: L[L.index(lab) + 1] if lab in L else ''
    sub = get('อนุสาขา') if get('อนุสาขา') not in ('ภาษา', 'การศึกษา') else ''
    D.append([hid, N(L[0].split(' | ')[0]), get('ศูนย์และคลินิก'), ' · '.join(x for x in (get('ความชำนาญเฉพาะทางสาขา'), sub) if x), ''])

# ศูนย์การแพทย์กาญจนาภิเษก (ม.มหิดล ศาลายา) หน้า /main/doctor/ รายชื่อทั้งหมดหน้าเดียว: ชื่อ · "ตารางออกตรวจ" · แผนก
# หัวเฉียว เว็บใหม่ hc-hospital.com (huachiewhospital.com ถูกปล่อยขายแล้ว) wp-sitemap-posts-doctors-1
H += [['gj', 'ศูนย์การแพทย์กาญจนาภิเษก (ม.มหิดล)', 'รัฐ (ม.มหิดล)', 'พุทธมณฑล', '', 'https://www.gj.mahidol.ac.th/main/doctor/', 'นครปฐม'],
      ['hc', 'โรงพยาบาลหัวเฉียว', 'เอกชน (มูลนิธิ)', 'ป้อมปราบศัตรูพ่าย', '', 'https://www.hc-hospital.com/doctor-appointment/', 'กรุงเทพฯ']]
L = lines('gj/list.html')
for k in range(len(L) - 2):
    if L[k + 1] == 'ตารางออกตรวจ' and re.search(r'(นพ|พญ|ทพ|ทพญ)\.', L[k]): D.append(['gj', N(L[k]), L[k + 2], '', ''])
for f in sorted(glob.glob('hc/*')):
    L = lines(f)
    if 'ร่วมงานกับ รพ.หัวเฉียว' not in L or 'การศึกษา' not in L: continue
    j = L.index('การศึกษา'); i = max(k for k in range(j) if L[k] == 'ร่วมงานกับ รพ.หัวเฉียว') + 1  # เมนูซ้ำหลายจุด เอาตัวก่อนหัวข้อการศึกษา
    sch = L[L.index('ตารางการออกตรวจแพทย์'):] if 'ตารางการออกตรวจแพทย์' in L else []
    D.append(['hc', N(L[i]), '', ' · '.join(L[i + 1:j][:2]), days([x.replace('–', '-') for x in sch[:30]])])

# รพ.ศูนย์บริการการแพทย์นนทบุรี (ห้าแยกพระราม 5) nmc.moph.go.th/ค้นหาแพทย์/ — ลงไว้ 4 คน · หน้าแผนไทย/จีนมีแต่เบอร์ ไม่มีรายชื่อ
H.append(['nmc', 'โรงพยาบาลศูนย์บริการการแพทย์นนทบุรี', 'รัฐ (สธ.) · มีแพทย์แผนไทย (ชั้น 5 ต่อ 5010) และแผนจีน (ต่อ 6000)', 'บางกรวย', '02-432-6167-8', 'https://nmc.moph.go.th/', 'นนทบุรี'])
L = lines('nmc/find.html'); L = L[L.index('แพทย์เฉพาะทาง') + 1:next(k for k, x in enumerate(L) if 'เลขที่ 155' in x)]
idx = [k for k, x in enumerate(L) if re.match(r'(นพ|พญ)\.', x)] + [len(L)]
for a, b in zip(idx, idx[1:]):
    seg = L[a:b]; t = ' '.join(seg[1:])
    dy = [d for d in DAYS if 'วัน' + d in t or (d == 'พุธ' and 'วันพุทธ' in t)]
    D.append(['nmc', N(seg[0]), seg[1], seg[2] if seg[2] != 'ตารางแพทย์ออกตรวจ' else '', ', '.join(dy)])

# เก็บเฉพาะแพทย์/ทันตแพทย์ (มีคำนำหน้า) ตัดนักกายภาพ นักฝึกพูด ฯลฯ ที่บางเว็บลงปนมา
DR = re.compile(r'^([ก-๙]{1,4}\.|\(พิเศษ\)|(พัน|นาวา|เรือ|ร้อย)[ก-๙]*\s|\s)*(นพ|พญ|ทพ|ทพญ)\.')  # ยศ/ตำแหน่งวิชาการนำหน้าได้ เช่น ผศ.พ.ท.นพ.
ok = lambda d: DR.match(d[1]) or ('ทันต' in d[2] and not re.match(r'^(คุณ|นาง|นาย)', d[1]))  # ทันตแพทย์บางเว็บไม่ใส่คำนำหน้า
drop = [d for d in D if not ok(d)]; D = [d for d in D if ok(d)]
import collections as _c; print('ตัดที่ไม่ใช่แพทย์', len(drop), _c.Counter(d[0] for d in drop), [d[1] for d in drop if d[0] not in ('tb',)][:12])
# หมอคนเดียวหลายแถว (หลายแผนก/หลาย URL) → รวมเป็นแถวเดียว แผนกที่เพิ่มต่อท้ายในช่องสาขา
M = {}
for d in D:
    k = (d[0], d[1])
    if k not in M: M[k] = d; continue
    m = M[k]
    for x in (re.sub(r'\s*โทร.*$', '', d[2]), d[3]):
        if x and x not in m[2] + ' ' + m[3]: m[3] = (m[3] + ' · ' + x).strip(' ·')
D = list(M.values())
# สาขาจาก checkmd.tmc.or.th (29ต.ค.69) สำหรับหมอที่เว็บ รพ.ไม่ระบุ — "ยังไม่มี" = แพทย์เวชปฏิบัติทั่วไป
CMD = {'นพ.ธีระภาพ เสนะวงษ์': 'เวชศาสตร์ป้องกัน แขนงเวชศาสตร์การบิน · นิติเวชศาสตร์', 'นพ.ศุภวาร วงษ์สวัสดิ์': 'เวชศาสตร์ป้องกัน แขนงสาธารณสุขศาสตร์',
       'นพ.ภาณุพงศ์ โควสุรัตน์': 'เวชศาสตร์ป้องกัน แขนงเวชศาสตร์การเดินทางและท่องเที่ยว'}
for n in ['พญ.จิรัศยา ด่านก้าวหน้า', 'พญ.ชลธิชา คุ้มวงศ์', 'พญ.นันทิยา จรรยาประเสริฐ', 'พญ.ภิรญา ศรีวิชัย', 'พญ.สุชัญญา เลาว์วงญาติ', 'นพ.กันติพจน์ ธีรวรวัชร์', 'นพ.พงษ์พสุ พ่วงทอง']: CMD[n] = 'แพทย์เวชปฏิบัติทั่วไป'
for d in D:
    if d[1] in CMD and not d[3]: d[3] = CMD[d[1]] + ' (แพทยสภา)'
H = [h for h in H if any(d[0] == h[0] for d in D)]  # ตัด รพ.ที่ไม่มีรายชื่อ (เช่น เปาโลสมุทรปราการ หน้าแพทย์เด้งหน้าแรกหมด 29ต.ค.69)
# รพ.ที่ตัวดึงยังโหลดไม่ครบ → ยังไม่ปล่อย (กันคนเข้าใจว่ามีหมอแค่นั้น) · ตั้งผ่าน env PENDING="smt_,bh" (คำนำหน้า id)
PEND = tuple(x for x in os.environ.get('PENDING', '').split(',') if x)
if PEND: D = [d for d in D if not d[0].startswith(PEND)]; H = [h for h in H if not h[0].startswith(PEND)]; print('ยังไม่ปล่อย', PEND)
out = {'asof': '2569-10-29', 'hosp': H, 'd': D}
js = '// รายชื่อแพทย์ กทม. ปริมณฑล ภาคกลาง ดึงจากเว็บ รพ. ' + out['asof'] + ' — สร้างโดย build_docs.py ห้ามแก้มือ\nconst DOCS=' + json.dumps(out, ensure_ascii=False) + ';\n'
for p in ('~/Desktop/sick/doctors.js', '~/Desktop/thai-doctors/data/central.js'):  # สำเนาสำรองบนโฮสต์ + repo GitHub (โหลดผ่าน jsDelivr)
    os.makedirs(os.path.dirname(os.path.expanduser(p)), exist_ok=True); open(os.path.expanduser(p), 'w', encoding='utf8').write(js)
import collections; print(len(D), collections.Counter(d[0] for d in D))
