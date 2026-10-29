from decimal import Decimal, ROUND_HALF_UP
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.graphics.shapes import Drawing, Rect, String
from reportlab.lib.colors import HexColor
from reportlab.pdfgen.canvas import Canvas
import os

OUT = r'C:\Dev\Learning\1.Company\1.Apero\Bao_cao_hieu_suat_so_voi_gia_goi_AI_2026.pdf'
CHECK = '29/10/2026'
pdfmetrics.registerFont(TTFont('Arial', r'C:\Windows\Fonts\arial.ttf'))
pdfmetrics.registerFont(TTFont('Arial-Bold', r'C:\Windows\Fonts\arialbd.ttf'))

NAVY = HexColor('#102A43'); BLUE = HexColor('#1976D2'); TEAL = HexColor('#00897B')
ORANGE = HexColor('#F59E0B'); LIGHT = HexColor('#F4F7FB'); MID = HexColor('#D9E2EC')
INK = HexColor('#243B53'); MUTED = HexColor('#52606D')

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='VNTitle', parent=styles['Title'], fontName='Arial-Bold', fontSize=22, leading=28, textColor=NAVY, alignment=TA_CENTER, spaceAfter=6))
styles.add(ParagraphStyle(name='VNSub', parent=styles['Normal'], fontName='Arial', fontSize=11, leading=15, textColor=HexColor('#486581'), alignment=TA_CENTER))
styles.add(ParagraphStyle(name='H1VN', parent=styles['Heading1'], fontName='Arial-Bold', fontSize=16, leading=21, textColor=NAVY, spaceBefore=4, spaceAfter=6))
styles.add(ParagraphStyle(name='H2VN', parent=styles['Heading2'], fontName='Arial-Bold', fontSize=12, leading=16, textColor=BLUE, spaceBefore=6, spaceAfter=4))
styles.add(ParagraphStyle(name='BodyVN', parent=styles['BodyText'], fontName='Arial', fontSize=9.2, leading=13.2, textColor=INK, spaceAfter=4))
styles.add(ParagraphStyle(name='SmallVN', parent=styles['BodyText'], fontName='Arial', fontSize=7.4, leading=10, textColor=MUTED))
styles.add(ParagraphStyle(name='Callout', parent=styles['BodyText'], fontName='Arial-Bold', fontSize=10, leading=14.5, textColor=NAVY, backColor=HexColor('#E8F1FB'), borderColor=BLUE, borderWidth=0.7, borderPadding=8, spaceBefore=4, spaceAfter=6))
styles.add(ParagraphStyle(name='Th', parent=styles['BodyText'], fontName='Arial-Bold', fontSize=6.5, leading=8.2, textColor=colors.white))
styles.add(ParagraphStyle(name='Td', parent=styles['BodyText'], fontName='Arial', fontSize=6.5, leading=8.2, textColor=INK))
styles.add(ParagraphStyle(name='Td8', parent=styles['BodyText'], fontName='Arial', fontSize=8, leading=11, textColor=INK))

P = lambda t, s='BodyVN': Paragraph(t, styles[s])
Q = ROUND_HALF_UP
PLAN = Decimal('20')
RATIO = Decimal('0.2')


def money(n):
    q = n.quantize(Decimal('0.01'), rounding=Q)
    sign = '-' if q < 0 else ''
    whole, frac = f'{abs(q):.2f}'.split('.')
    grouped = f'{int(whole):,}'.replace(',', '.')
    return f'{sign}${grouped},{frac}'


def millions(n):
    q = n.quantize(Decimal('0.01'), rounding=Q)
    whole, frac = f'{q:.2f}'.split('.')
    grouped = f'{int(whole):,}'.replace(',', '.')
    return f'{grouped},{frac}'


def cost(pin, pout, in_m, out_m):
    return (pin * in_m + pout * out_m).quantize(Decimal('0.01'), rounding=Q)


def break_even(pin, pout):
    unit = pin + RATIO * pout
    inn = PLAN / unit
    return inn, RATIO * inn


def judge(pin, pout):
    light = cost(pin, pout, Decimal('1'), Decimal('0.2'))
    std = cost(pin, pout, Decimal('10'), Decimal('2'))
    heavy = cost(pin, pout, Decimal('50'), Decimal('10'))
    inn, out = break_even(pin, pout)
    point = f'{millions(inn)}M input + {millions(out)}M output'
    if light > PLAN:
        text = 'Vượt $20 ngay ở mức nhẹ'
    elif light == PLAN:
        text = 'Bằng $20 ngay ở mức nhẹ'
    elif std < PLAN and heavy <= PLAN:
        text = 'Cả ba mức đều dưới $20'
    elif std < PLAN and heavy > PLAN:
        text = 'Nhẹ và chuẩn dưới $20; nặng vượt $20'
    elif std == PLAN:
        text = 'Đúng $20 ở mức chuẩn'
    else:
        text = 'Vượt $20 sau mốc này'
    return light, std, heavy, text, point


# Standard, input mới, không cache. USD / 1M token.
MODELS = [
    ('luna', 'GPT-6 Luna', '0.10', '0.50', 'OpenAI Standard. Cache read $0,01.', 'Luna'),
    ('terra', 'GPT-6.1 Terra', '1', '5', 'OpenAI Standard. Cache read $0,05.', 'Terra'),
    ('sol', 'GPT-6.1 Sol', '2', '10', 'OpenAI Standard. Cache read $0,10.', 'Sol'),
    ('astra', 'GPT-6 Astra', '10', '50', 'OpenAI Standard. Cache read $1,00. Prompt trên 272.000 token input: cả request tính 2 lần input/cache và 1,5 lần output.', 'Astra'),
    ('haiku_lo', 'Claude Haiku 5.5, request đến 100.000 token', '0.10', '0.50', 'Claude API, Standard Global. Cache read $0,01. Ngưỡng tính trên từng request.', None),
    ('haiku_hi', 'Claude Haiku 5.5, request trên 100.000 token', '0.50', '2.50', 'Cùng model, bậc cao hơn. Cache read $0,05. Cả tháng ở mức này khi mọi request đều vượt ngưỡng.', None),
    ('sonnet', 'Claude Sonnet 5.5', '2', '10', 'Standard Global, mọi độ dài. Cache read $0,10. Cache write 5 phút $2,50.', None),
    ('opus', 'Claude Opus 5.5', '4', '20', 'Standard Global. Cache read $0,20. Cache write 5 phút $5,00.', 'Opus'),
    ('fable', 'Claude Fable 5.1', '10', '50', 'Standard Global. Cache read $0,25. Fable 5 vẫn $10 / $50 nhưng cache read $1,00.', None),
    ('gflash', 'Gemini 3.8 Flash, đến 31/12/2026', '0.75', '3.75', 'gemini-3.8-flash, giá mở cửa. Từ 1/1/2027: $1,50 / $7,50. Output đã gồm thinking.', 'Gem. Flash'),
    ('argon', 'Gemini 4 Argon, đến 30/11/2026', '2', '10', 'gemini-4-argon, giá mở cửa. Từ 1/12/2026: $4,00 / $20,00. Cache $0,10 rồi $0,20. Chỉ implicit cache.', None),
    ('dsflash', 'DeepSeek Flash, giờ cao điểm, cache miss', '0.30', '1.20', 'deepseek-flash, bản DeepSeek-V4.1-Flash-1017. Giờ thấp điểm bằng một nửa. Cache hit cao điểm $0,006, không dùng làm mốc.', 'DS Flash'),
    ('dspro', 'DeepSeek V4-Pro, giờ cao điểm, cache miss', '1.32', '3.96', 'Bảng giá 19/10/2026 vẫn niêm yết id này. Thông báo 10/9 nói từ 14/9 id deepseek-v4-pro chuyển sang Flash đến khi có V4.1-Pro. Xác nhận id trước khi mua lượng lớn.', None),
]

LATER = [
    ('Gemini 4 Argon từ 1/12/2026', '4', '20'),
    ('Gemini 3.8 Flash từ 1/1/2027', '1.50', '7.50'),
    ('DeepSeek Flash, giờ thấp điểm, cache miss', '0.15', '0.60'),
    ('DeepSeek V4-Pro, giờ thấp điểm, cache miss', '0.66', '1.98'),
]

ROWS = []
for key, name, pin_s, pout_s, note, chart in MODELS:
    pin, pout = Decimal(pin_s), Decimal(pout_s)
    light, std, heavy, text, point = judge(pin, pout)
    ROWS.append(dict(key=key, name=name, pin=pin, pout=pout, note=note, chart=chart,
                      light=light, std=std, heavy=heavy, text=text, point=point))

BY = {r['key']: r for r in ROWS}
assert BY['luna']['std'] == Decimal('2.00')
assert BY['terra']['std'] == Decimal('20.00') and BY['terra']['text'].startswith('Đúng')
assert BY['sol']['std'] == BY['sonnet']['std'] == BY['argon']['std'] == Decimal('40.00')
assert BY['astra']['light'] == BY['fable']['light'] == Decimal('20.00')
assert BY['astra']['std'] == BY['fable']['std'] == Decimal('200.00')
assert BY['opus']['std'] == Decimal('80.00')
assert BY['gflash']['std'] == Decimal('15.00')
assert BY['haiku_lo']['std'] == Decimal('2.00')
assert BY['haiku_hi']['std'] == Decimal('10.00')
assert BY['dsflash']['std'] == Decimal('5.40') and BY['dsflash']['heavy'] == Decimal('27.00')
assert BY['dspro']['std'] == Decimal('21.12')
assert millions(break_even(Decimal('0.75'), Decimal('3.75'))[0]) == '13,33'
assert millions(break_even(Decimal('1.32'), Decimal('3.96'))[0]) == '9,47'


def header_footer(canvas: Canvas, doc):
    canvas.saveState()
    w, h = A4
    if doc.page > 1:
        canvas.setFillColor(NAVY)
        canvas.rect(0, h - 13 * mm, w, 13 * mm, fill=1, stroke=0)
        canvas.setFont('Arial-Bold', 8)
        canvas.setFillColor(colors.white)
        canvas.drawString(16 * mm, h - 8.5 * mm, 'Apero | Hiệu suất so với giá của các gói AI')
    canvas.setStrokeColor(MID)
    canvas.line(16 * mm, 13 * mm, w - 16 * mm, 13 * mm)
    canvas.setFont('Arial', 7)
    canvas.setFillColor(HexColor('#7B8794'))
    canvas.drawString(16 * mm, 8 * mm, f'Bản tham khảo quyết định mua | Dữ liệu kiểm tra: {CHECK}')
    canvas.drawRightString(w - 16 * mm, 8 * mm, f'{doc.page}')
    canvas.restoreState()


def table(data, widths):
    t = Table(data, colWidths=widths, repeatRows=1, hAlign='LEFT')
    cmds = [
        ('FONTNAME', (0, 0), (-1, -1), 'Arial'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.35, MID),
        ('LEFTPADDING', (0, 0), (-1, -1), 3),
        ('RIGHTPADDING', (0, 0), (-1, -1), 3),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
        ('BACKGROUND', (0, 0), (-1, 0), NAVY),
    ]
    for r in range(1, len(data)):
        if r % 2 == 0:
            cmds.append(('BACKGROUND', (0, r), (-1, r), LIGHT))
    t.setStyle(TableStyle(cmds))
    return t


def cells(row, style):
    return [P(x, style) for x in row]


def times(value, price):
    return millions(value / price) + '×'


def month_from_weeks(week, price, weeks=Decimal('4')):
    month = (week * weeks).quantize(Decimal('0.01'), rounding=Q)
    return month, times(month, price)


# Rate card Codex, Standard, 29/10/2026. Credit / giá API Standard.
# Luna, Terra, GPT-6.1 Sol, Astra lấy từ bảng API của báo cáo này.
# GPT-6 Sol cache $0,20 và GPT-5.6 Sol $4 / $0,40 / $20 lấy từ rate card Enterprise tính bằng đô la.
CREDIT_PAIRS = [
    (Decimal('0.10'), Decimal('0.01'), Decimal('0.50'), Decimal('2.5'), Decimal('0.25'), Decimal('12.5')),
    (Decimal('1'), Decimal('0.05'), Decimal('5'), Decimal('25'), Decimal('1.25'), Decimal('125')),
    (Decimal('2'), Decimal('0.10'), Decimal('10'), Decimal('50'), Decimal('2.5'), Decimal('250')),
    (Decimal('2'), Decimal('0.20'), Decimal('10'), Decimal('50'), Decimal('5'), Decimal('250')),
    (Decimal('10'), Decimal('1'), Decimal('50'), Decimal('250'), Decimal('25'), Decimal('1250')),
    (Decimal('4'), Decimal('0.40'), Decimal('20'), Decimal('100'), Decimal('10'), Decimal('500')),
]
_ratios = set()
for _pin, _cache, _pout, _cin, _cc, _co in CREDIT_PAIRS:
    _ratios.add(_cin / _pin)
    _ratios.add(_cc / _cache)
    _ratios.add(_co / _pout)
assert _ratios == {Decimal('25')}
CREDITS_PER_API_DOLLAR = Decimal('25')


def credits_of(dollars):
    n = (Decimal(dollars) * CREDITS_PER_API_DOLLAR).quantize(Decimal('1'), rounding=Q)
    return f'{int(n):,}'.replace(',', '.')


def credits_span(lo, hi):
    return f'{credits_of(lo)}–{credits_of(hi)}'


def ratio_bars(items):
    d = Drawing(500, 168)
    max_v = Decimal('2.5')
    left, bottom, width, height = 42, 40, 440, 108
    d.add(Rect(left, bottom, width, height, fillColor=colors.white, strokeColor=MID, strokeWidth=0.4))
    for step in (Decimal('0'), Decimal('0.5'), Decimal('1'), Decimal('1.5'), Decimal('2'), Decimal('2.5')):
        y = bottom + float(height * step / max_v)
        d.add(String(left - 3, y - 2, millions(step), fontName='Arial', fontSize=6.5, fillColor=MUTED, textAnchor='end'))
        if step:
            d.add(Rect(left, y, width, 0.3, fillColor=MID, strokeColor=MID, strokeWidth=0))
    palette = [BLUE, TEAL, HexColor('#1D4ED8'), ORANGE]
    n = len(items)
    gap = 16
    bw = (width - gap * (n + 1)) / n
    for i, (label, value) in enumerate(items):
        x = left + gap + i * (bw + gap)
        bh = float(height * value / max_v)
        d.add(Rect(x, bottom, bw, max(bh, 1), fillColor=palette[i], strokeColor=colors.white, strokeWidth=0.4))
        d.add(String(x + bw / 2, bottom + bh + 3, times(value, Decimal('1')), fontName='Arial-Bold', fontSize=8, fillColor=NAVY, textAnchor='middle'))
        d.add(String(x + bw / 2, 22, label, fontName='Arial', fontSize=7, fillColor=INK, textAnchor='middle'))
    return d


PLUS_WEEK = Decimal('67')
PRO100_WEEK = Decimal('175')
PLUS_MONTH, PLUS_X = month_from_weeks(PLUS_WEEK, Decimal('20'))
PRO100_MONTH, PRO100_X = month_from_weeks(PRO100_WEEK, Decimal('100'))
assert PLUS_MONTH == Decimal('268.00') and PLUS_X == '13,40×'
assert PRO100_MONTH == Decimal('700.00') and PRO100_X == '7,00×'
assert credits_of(PLUS_WEEK) == '1.675' and credits_of(PLUS_MONTH) == '6.700'
assert credits_of(PRO100_WEEK) == '4.375' and credits_of(PRO100_MONTH) == '17.500'
assert credits_of(66) == '1.650' and credits_of(285) == '7.125'
assert credits_span(330, 380) == '8.250–9.500' and credits_span(1440, 1640) == '36.000–41.000'
assert credits_span(641, 670) == '16.025–16.750' and credits_span(2800, 2900) == '70.000–72.500'
assert credits_of(1300) == '32.500'
assert times(Decimal('15'), Decimal('10')) == '1,50×'
assert times(Decimal('70'), Decimal('39')) == '1,79×'
assert times(Decimal('200'), Decimal('100')) == '2,00×'


story = []
story += [Spacer(1, 14 * mm), P('HIỆU SUẤT SO VỚI GIÁ', 'VNTitle')]
story += [P('Giá trị API của lượng dùng trong gói, chia cho phí subscription', 'VNSub'), Spacer(1, 4 * mm)]
story += [P(f'Báo cáo thực hành cho Apero. Giá API kiểm tra {CHECK}. Phép đo lấy từ tháng 9/2026.', 'Callout')]

intro = [
    ['Câu hỏi', 'Một gói subscription mua được lượng dùng model trị giá bao nhiêu đô la API, và hệ số đó so với phí là bao nhiêu.'],
    ['Công thức', 'Hiệu suất = giá trị API của phần dùng được / phí gói. Trên 1: phần quy ra API lớn hơn phí. Bằng 1: phí mua đúng số đô la API đó.'],
    ['Hai khoản', 'Credit ghi trên giá (Copilot, credit API của Claude Max). Và hạn mức app đo từ log, quy ra đô la API rồi sang credit của đúng hãng. Hai khoản đứng riêng, không cộng vào một hệ số.'],
    ['Kết luận nhanh', f'Credit Copilot: Pro {times(Decimal("15"), Decimal("10"))}, Pro+ {times(Decimal("70"), Decimal("39"))}, Max {times(Decimal("200"), Decimal("100"))}. Credit Claude Max đúng 1,00×. Log Codex: Plus {credits_of(PLUS_WEEK)} credit/tuần, {credits_of(PLUS_MONTH)} credit/tháng ({PLUS_X}). Pro $100 từ {credits_of(PRO100_WEEK)} credit/tuần trở lên, tùy bài đo.'],
]
story.append(table(
    [cells(['Thông tin', 'Tóm tắt'], 'Th')] + [cells(pair, 'Td8') for pair in intro],
    [32 * mm, 146 * mm],
))
story += [P('Mục 1: cách tính. Mục 2: đơn giá API để quy đổi. Mục 3: hiệu suất credit. Mục 4: hiệu suất hạn mức đã đo. Mục 5: cách chọn gói. Mục 6: nguồn.', 'BodyVN'), PageBreak()]

story += [P('1. Cách tính hiệu suất của gói', 'H1VN')]
story += [P('Phí gói mua quyền dùng model trong ứng dụng, kèm hạn mức. Hiệu suất ở đây là số đô la API tương đương của phần dùng đó, chia cho phí. Đây là thước đo tiền, tách khỏi điểm benchmark.', 'BodyVN')]
method = [
    ['Hạng mục', 'Cách làm'],
    ['Tử số', 'Lượng token đã dùng hoặc được cấp, nhân đơn giá API của đúng model, đúng loại token (input mới, cache read, output).'],
    ['Mẫu số', 'Phí subscription của tháng đó. Giá năm được quy về tháng khi nguồn đã quy.'],
    ['Credit chính thức', 'Copilot: 1 AI credit = $0,01. Claude Max: credit API ghi bằng đô la. ChatGPT: credit mua thêm sau khi hết hạn mức, rate card Codex tính 25 credit cho mỗi $1 API Standard.'],
    ['Hạn mức app', 'Nhà cung cấp không cấp một số credit cố định trong phí Plus hay Pro. Log đã định giá theo API đổi sang credit ChatGPT bằng đô la × 25. Một tuần nhân 4 là giả định của báo cáo này khi nguồn chỉ có số tuần.'],
    ['Đơn giá', 'Mức Standard, input mới, chưa thuế. Cache, batch, fast mode và context dài làm cùng một log ra số đô la khác.'],
]
story.append(table([cells(r, 'Th' if i == 0 else 'Td') for i, r in enumerate(method)], [36 * mm, 142 * mm]))
story += [P(
    'Cùng một hạn mức gói đổi ra số đô la rất khác nhau theo model. Ở kịch bản 10 triệu input và 2 triệu output, Luna và Haiku dưới 100.000 token là $2,00, Sol và Sonnet 5.5 là $40,00, Astra và Fable 5.1 là $200,00. '
    'Vì vậy một hệ số đo trên Sonnet không mang sang Fable, và một hệ số đo trên Codex không mang sang chat thường.',
    'BodyVN'), PageBreak()]

story += [P('2. Đơn giá API dùng để quy đổi', 'H1VN')]
story += [P(f'USD / 1 triệu token, Standard, input mới. OpenAI ngày {CHECK}. Claude rate card 22/10/2026. Gemini cập nhật 28/10/2026. DeepSeek docs 19/10/2026.', 'BodyVN')]
price_head = ['Model trong phép quy đổi', 'Input / 1M', 'Output / 1M', 'Ghi chú khi đổi log ra đô la']
price_body = [[r['name'], money(r['pin']), money(r['pout']), r['note']] for r in ROWS]
story.append(table(
    [cells(price_head, 'Th')] + [cells(r, 'Td') for r in price_body],
    [52 * mm, 22 * mm, 24 * mm, 80 * mm],
))
story += [P(
    'Argon lên $4 / $20 từ 1/12/2026. Gemini 3.8 Flash lên $1,50 / $7,50 từ 1/1/2027. DeepSeek giờ thấp điểm bằng một nửa giá cao điểm. '
    'Prompt GPT-6 Astra trên 272.000 token input tính 2 lần input và 1,5 lần output cho cả request. Haiku 5.5 nhảy bậc khi một request vượt 100.000 token.',
    'BodyVN'), PageBreak()]

story += [P('3. Hiệu suất của credit ghi trên giá', 'H1VN')]
story += [P('Khoản này đọc được từ bảng giá, không cần log. Tử số là số đô la credit. Mẫu số là phí gói.', 'BodyVN')]
credits = [
    ('Copilot Pro', '10', '15', '1.500 AI credit. Completion và NES không trừ credit, nên 1,50× là sàn của phần chat và agent.'),
    ('Copilot Pro+', '39', '70', '7.000 credit. Cùng quy tắc trừ theo giá token của model.'),
    ('Copilot Max', '100', '200', '20.000 credit. Auto giảm 10% giá model. Fusion giảm 30% đến 30/11/2026. Hai mức giảm làm cùng một credit đi được xa hơn, chưa cộng vào hệ số.'),
    ('Copilot Business', '19', '19', '1.900 credit gộp mỗi ghế. Base credit bằng đúng phí ghế.'),
    ('Copilot Enterprise', '39', '39', '3.900 credit gộp mỗi ghế.'),
    ('Claude Pro', '20', '0', 'Phí mua hạn mức Claude và Claude Code. Credit API bằng 0.'),
    ('Claude Max 5x', '100', '100', 'Credit API $100 mỗi kỳ, nếu liên kết Console. Đứng riêng với hạn mức app ở mục 4.'),
    ('Claude Max 20x', '200', '200', 'Credit API $200 mỗi kỳ. Credit không trả cho Claude Code chạy trực tiếp.'),
]
credit_rows = []
for name, price_s, value_s, note in credits:
    price, value = Decimal(price_s), Decimal(value_s)
    credit_rows.append([name, money(price), money(value), times(value, price), note])
story.append(table(
    [cells(['Gói', 'Phí', 'Credit quy ra API', 'Hiệu suất', 'Phạm vi của hệ số'], 'Th')] + [cells(r, 'Td') for r in credit_rows],
    [32 * mm, 22 * mm, 32 * mm, 22 * mm, 70 * mm],
))
story += [Spacer(1, 2 * mm), P('Hiệu suất credit = đô la credit / phí. Trục đến 2,50. Claude Max 5x và Max 20x cùng 1,00× nên biểu đồ chỉ vẽ một cột.', 'SmallVN')]
story.append(ratio_bars([
    ('Copilot Pro', Decimal('1.50')),
    ('Copilot Pro+', Decimal('70') / Decimal('39')),
    ('Copilot Max', Decimal('2')),
    ('Claude Max', Decimal('1')),
]))
story += [P(
    'Perplexity Pro và Max không công bố số token để nhân với giá API của OpenAI, Anthropic hay Google. '
    'Gemini AI Plus, Pro và Ultra công bố bội số hạn mức (2×, 4×, 5×, 20× so với gói dưới), không công bố số token. Hai nhóm này chưa có hiệu suất API trong báo cáo. DeepSeek không có gói cá nhân.',
    'BodyVN'), PageBreak()]

story += [P('4. Hiệu suất của hạn mức app, đo từ log', 'H1VN')]
story += [P(
    'Cột giá trị là giá niêm yết API của lượng token trong log, rồi số credit ChatGPT tương đương. '
    f'Rate card Codex ngày {CHECK} tính GPT-6 Astra, GPT-6.1 Sol, Terra, GPT-6 Sol, Luna và GPT-5.6 Sol đúng 25 credit cho mỗi $1 giá API Standard, cùng tỷ lệ ở input, cache read và output. '
    'Credit = đô la API × 25. Đây là credit trên rate card mua thêm sau khi hết hạn mức, không phải số credit được cấp trong phí. Giá mua một credit phụ thuộc gói, OpenAI không niêm một giá cố định.',
    'BodyVN')]
measured = [
    ['ChatGPT Plus, Codex', '$20', f'Tuần: $67, bằng {credits_of(PLUS_WEEK)} credit. Tháng, nhân 4: {money(PLUS_MONTH)}, bằng {credits_of(PLUS_MONTH)} credit, hiệu suất {PLUS_X}.', 'FinOps LLM, 27 cửa sổ từ tháng 8, cập nhật 10/10/2026. Bảy cửa sổ gần nhất $61–$81.'],
    ['ChatGPT Plus, Codex', '$20', f'Tuần: khoảng $66, bằng {credits_of(66)} credit. Tháng theo bài: khoảng $285, bằng {credits_of(285)} credit, khoảng 14×.', 'InventiveHQ, một cửa sổ 26/9, bài 4/10/2026. Số tháng là suy của bài đó, không phải phép nhân 4.'],
    ['ChatGPT Pro 100, Codex', '$100', f'Tuần: $175, bằng {credits_of(PRO100_WEEK)} credit, 2,6× Plus. Tháng, nhân 4: {money(PRO100_MONTH)}, bằng {credits_of(PRO100_MONTH)} credit, hiệu suất {PRO100_X}.', 'FinOps LLM, 6 cửa sổ 27/9–8/10, bài 9/10/2026. Nhãn bán là 5× Plus.'],
    ['ChatGPT Pro 100, Codex', '$100', f'Tuần: $330–$380, bằng {credits_span(330, 380)} credit. Tháng theo bài: $1.440–$1.640, bằng {credits_span(1440, 1640)} credit, khoảng 14–16×.', 'InventiveHQ, hai cửa sổ sạch, reset 30/9 và 3/10.'],
    ['ChatGPT Pro 200, hạn mức mới', '$200', f'Tuần: $641–$670, bằng {credits_span(641, 670)} credit. Tháng theo bài: $2.800–$2.900, bằng {credits_span(2800, 2900)} credit, khoảng 14×.', 'InventiveHQ, hai cửa sổ reset 6/10 và 9/10.'],
    ['ChatGPT Pro 200, hạn mức cũ', '$200', f'Tuần bài suy: khoảng $1.300, bằng {credits_of(1300)} credit, khoảng 28×. Bài không tách một số tháng riêng.', 'Suy đến hết 29/10/2026. Hạn mức cũ của cửa sổ 22–29/9 hết trong ngày này.'],
    ['ChatGPT Pro 500', '$500', 'Chưa có cửa sổ được định giá, nên chưa có credit.', 'OpenAI không công bố bội số token. Ultrafast tiêu hạn mức 8 lần Standard, rồi credit mua thêm ở 6 lần.'],
    ['Claude Max 20x, hết hạn mức', '$200', 'Không đổi sang credit ChatGPT. Credit API của gói vẫn là $200. Giá trị hạn mức app: Sonnet 5.5 $12.529 agent (62,6×) và $7.009 chat (35,0×). Opus 5.5 $11.726 (58,6×) và $9.200 (46,0×). Fable 5.1 khoảng $2.480 (12,4×).', 'SemiAnalysis, 5/10/2026. Anthropic ghi credit bằng đô la. Chưa tính lại sau khi cache read Sonnet xuống $0,10 ngày 7/10. Fable dùng tối đa 50% hạn mức tuần.'],
]
story.append(table(
    [cells(['Gói và phần được đo', 'Phí', 'Giá trị API, credit và hiệu suất', 'Nguồn, từ tháng 9/2026'], 'Th')] + [cells(r, 'Td') for r in measured],
    [38 * mm, 18 * mm, 62 * mm, 60 * mm],
))
story += [P('Cách đọc hai nguồn Codex', 'H2VN')]
story += [P(
    f'FinOps và InventiveHQ cùng đo Codex, cùng lúc, ra hai mức cho Pro $100: {PRO100_X} theo trung vị FinOps sau khi nhân 4 tuần, và khoảng 14–16× theo InventiveHQ. '
    'Báo cáo giữ cả hai. Plus nằm sát nhau, khoảng 13× đến 14×. '
    'Trên mỗi đô la phí, Plus cao hơn Pro $100 trong bài FinOps: họ đo Pro $100 bằng 2,6 lần hạn mức Plus trong khi phí gấp 5. InventiveHQ thấy các gói Pro gần cùng một hệ số khoảng 14×.',
    'BodyVN')]
story += [P(
    'Credit ChatGPT và credit Copilot là hai đơn vị. Copilot tính 1 credit = $0,01 và không có log tuần hay tháng trong báo cáo này, nên mục 3 giữ nguyên số credit trên giá. '
    'Không chia đô la Codex cho $0,01 rồi gọi đó là credit Copilot. '
    'Credit API của Claude Max (mục 3, đúng 1,00×) và cột SemiAnalysis (mục 4) là hai khoản. Cộng chúng thành một hệ số sẽ đếm trùng. '
    'Chi tiết log Claude tháng 10 nằm ở báo cáo «3.So sánh Claude Pro Max Enterprise và API - 10.2026».',
    'BodyVN'), PageBreak()]

story += [P('5. Chọn gói theo hiệu suất', 'H1VN')]
recs = [
    ['Cần hệ số đọc được từ giá', 'Copilot Pro hoặc Max', f'Pro {times(Decimal("15"), Decimal("10"))} trên credit, Max {times(Decimal("200"), Decimal("100"))}. Completion không nằm trong tử số.'],
    ['Code nhiều bằng Codex', 'Plus nếu chưa chạm trần tuần', f'Log tháng 9–10: Plus khoảng {credits_of(66)}–{credits_of(PLUS_WEEK)} credit/tuần, khoảng {PLUS_X} đến 14×. Pro $100 mua thêm lượng, từ {credits_of(PRO100_WEEK)} credit/tuần trở lên.'],
    ['Code nhiều bằng Claude', 'Max khi đã chạm trần Pro', 'Credit API đúng bằng phí. Phần app, nếu dùng hết hạn mức tháng 10, từ khoảng 12× với Fable đến vài chục lần với Sonnet và Opus.'],
    ['Chat, file, nghiên cứu', 'Giữ một gói $20', 'Chưa có log chat thường được định giá theo API trong tháng 9–10. Perplexity và Gemini chưa ra được hệ số token.'],
    ['Sản phẩm tự gọi API', 'Trả theo token', 'Gói subscription không cấp một số token cố định cho sản phẩm. Credit Claude Max chỉ bù API khi đủ điều kiện Console.'],
]
story.append(table(
    [cells(['Nhu cầu', 'Điểm vào', 'Vì sao, theo hệ số'], 'Th')] + [cells(r, 'Td') for r in recs],
    [42 * mm, 48 * mm, 88 * mm],
))
story += [Spacer(1, 3 * mm), P(
    'Điểm vào cho Apero: Copilot Pro cho người code khi cần một hệ số credit chắc; Claude Pro hoặc ChatGPT Plus cho việc viết và đọc; chỉ lên Max hoặc Pro 100/200/500 khi log của chính nhóm, định giá theo bảng mục 2, đã vượt phí gói.',
    'Callout'), PageBreak()]

story += [P('6. Nguồn và giới hạn', 'H1VN')]
story += [P(f'Đơn giá kiểm tra {CHECK}. Hệ số log giữ nguyên ngày đo của từng bài.', 'BodyVN')]
sources = [
    ['OpenAI, đơn giá API', 'https://developers.openai.com/api/docs/pricing'],
    ['Codex, rate card credit, 29/10/2026', 'https://learn.chatgpt.com/docs/pricing'],
    ['ChatGPT Plus và Pro, credit mua thêm', 'https://help.openai.com/en/articles/12642688'],
    ['ChatGPT Pro 100 / 200 / 500', 'https://help.openai.com/en/articles/9793128-about-chatgpt-pro-tiers'],
    ['FinOps LLM, Codex Plus và Pro $100', 'https://finopsllm.com/research/chatgpt-pro-100-real-codex-multiplier'],
    ['InventiveHQ, đo Codex trên Plus và Pro', 'https://inventivehq.com/blog/codex-subscription-usage-measured'],
    ['Claude, giá gói và credit API', 'https://claude.com/pricing'],
    ['Claude rate card 22/10/2026', 'https://assets.claude.com/5633dc848caa431115468f31c7085d695bbfb9cc.pdf'],
    ['SemiAnalysis, Max 20x ngày 5/10/2026', 'Dẫn lại từ báo cáo Claude cùng thư mục. Bài gốc có thể yêu cầu tài khoản.'],
    ['Gemini API', 'https://ai.google.dev/gemini-api/docs/pricing'],
    ['Gemini, gói cá nhân', 'https://gemini.google/subscriptions/'],
    ['DeepSeek, 19/10/2026', 'https://api-docs.deepseek.com/quick_start/pricing'],
    ['GitHub Copilot, credit', 'https://docs.github.com/copilot/concepts/billing/usage-based-billing-for-individuals'],
    ['GitHub Copilot, trang gói', 'https://github.com/features/copilot/plans'],
]
story.append(table(
    [cells(['Nguồn', 'Liên kết'], 'Th')] + [cells(r, 'Td') for r in sources],
    [62 * mm, 116 * mm],
))
story += [P('Giới hạn', 'H2VN')]
story += [P(
    'Nhân 4 là giả định của báo cáo khi nguồn chỉ có số tuần. Một tháng lịch có thể hơn hoặc kém 4 cửa sổ. '
    'Hệ số 25 credit trên mỗi đô la API là rate card Standard ngày kiểm tra. Hạn mức có sẵn trong gói không được OpenAI công bố bằng credit, và Fast mode tiêu hạn mức đó ở 2,5 lần trong khi credit mua thêm tính 2 lần. '
    'Hai bài Codex không thống nhất ở Pro $100. SemiAnalysis là phép dùng hết hạn mức ngày 5/10, trước lần giảm giá cache read của Sonnet. '
    'ChatGPT Go $8 và Plus $20 trên trang chat không hiện trong HTML giá chính thức đã tải; phí Plus $20 trong bảng log là mức các bài đo dùng. '
    'Perplexity Max $200 lấy từ bài help sửa 14/9/2026. Pro $20 là đối chiếu 23–28/10/2026.',
    'BodyVN')]
story += [Spacer(1, 3 * mm), P(
    'Hiệu suất một gói là giá trị API của phần dùng được chia cho phí. Credit Copilot nằm từ 1,00× đến 2,00×. Credit Claude Max đúng 1,00×. '
    f'Log Codex tháng 9–10, quy theo rate card ngày {CHECK}: Plus khoảng {credits_of(PLUS_WEEK)} credit một tuần và {credits_of(PLUS_MONTH)} credit cho 4 tuần, tức {PLUS_X}. Cùng một phí mua hệ số khác nhau theo model và theo cách đo.',
    'Callout')]
story += [Spacer(1, 4 * mm), P('Tài liệu tham khảo nội bộ Apero. Định giá lại bằng log của nhóm và bảng đơn giá mục 2 trước khi nâng gói.', 'SmallVN')]

doc = SimpleDocTemplate(
    OUT, pagesize=A4, rightMargin=16 * mm, leftMargin=16 * mm, topMargin=18 * mm, bottomMargin=16 * mm,
    title='Hiệu suất gói AI tính theo giá trị API', author='Apero',
)
doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
print(OUT)
print('bytes', os.path.getsize(OUT))
print('plus', money(PLUS_MONTH), PLUS_X)
print('pro100', money(PRO100_MONTH), PRO100_X)
