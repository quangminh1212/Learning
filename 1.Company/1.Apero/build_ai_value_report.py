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


def cost_bars(items):
    d = Drawing(500, 214)
    max_v = Decimal('240')
    left, bottom, width, height = 46, 46, 436, 140
    d.add(Rect(left, bottom, width, height, fillColor=colors.white, strokeColor=MID, strokeWidth=0.4))
    for step in (0, 40, 80, 120, 160, 200, 240):
        y = bottom + float(height * Decimal(step) / max_v)
        d.add(String(left - 3, y - 2, str(step), fontName='Arial', fontSize=6.5, fillColor=MUTED, textAnchor='end'))
        if step:
            d.add(Rect(left, y, width, 0.3, fillColor=MID, strokeColor=MID, strokeWidth=0))
    palette = [BLUE, TEAL, HexColor('#0F766E'), HexColor('#1D4ED8'), ORANGE, HexColor('#B45309'), HexColor('#9F1239')]
    n = len(items)
    gap = 8
    bw = (width - gap * (n + 1)) / n
    for i, (label, value) in enumerate(items):
        x = left + gap + i * (bw + gap)
        bh = float(height * value / max_v)
        d.add(Rect(x, bottom, bw, max(bh, 1), fillColor=palette[i], strokeColor=colors.white, strokeWidth=0.4))
        d.add(String(x + bw / 2, bottom + bh + 3, money(value), fontName='Arial-Bold', fontSize=6.2, fillColor=NAVY, textAnchor='middle'))
        d.add(String(x + bw / 2, 28, label, fontName='Arial', fontSize=6.5, fillColor=INK, textAnchor='middle'))
    return d


story = []
story += [Spacer(1, 16 * mm), P('HIỆU SUẤT SO VỚI GIÁ', 'VNTitle')]
story += [P('API theo token hay thuê bao tháng: phương án nào kinh tế hơn?', 'VNSub'), Spacer(1, 5 * mm)]
story += [P(f'Báo cáo thực hành cho Apero. Giá kiểm tra {CHECK}, nguồn từ tháng 9/2026.', 'Callout')]

intro = [
    ['Mục tiêu', 'Cùng một lượng token, so chi phí API với giá thuê bao.'],
    ['Phạm vi', 'OpenAI GPT-6, Claude Sonnet 5.5 / Opus 5.5 / Haiku 5.5 / Fable 5.1, Gemini 4 Argon, Gemini 3.8 Flash, DeepSeek V4, và các gói ChatGPT, Claude, Gemini, Perplexity, Copilot.'],
    ['Kịch bản chuẩn', '10 triệu token input + 2 triệu token output mỗi tháng. Thêm mức nhẹ (1M + 0,2M) và nặng (50M + 10M), cùng tỷ lệ 5:1.'],
    ['Kết luận nhanh', 'Ở mức chuẩn, Luna khoảng $2, Terra đúng $20, Sol / Sonnet / Argon ưu đãi $40, Opus $80, Astra và Fable 5.1 $200. Gói $20 chỉ rẻ hơn khi gói đó mở đúng model và hạn mức cho phép lượng token ấy.'],
]
story.append(table(
    [cells(['Thông tin', 'Tóm tắt'], 'Th')] + [cells(pair, 'Td8') for pair in intro],
    [32 * mm, 146 * mm],
))
story += [Spacer(1, 4 * mm), P(
    '<b>Thước đo của báo cáo này là tiền cho cùng một lượng sử dụng.</b> Đây là phép so kinh tế, tách khỏi bảng xếp hạng benchmark. '
    'API tính theo token. Thuê bao có giao diện, công cụ và hạn mức riêng, và không cam kết một số token cố định.',
    'BodyVN')]
story += [P('Mục 1: cách tính. Mục 2: giá API. Mục 3: hòa vốn. Mục 4: giá thuê bao. Mục 5: khuyến nghị. Mục 6: nguồn.', 'BodyVN'), PageBreak()]

story += [P('1. Cách tính API so với thuê bao', 'H1VN')]
story += [P('Hai phương án được đặt lên cùng một lượng token input và output trong một tháng. Số tiền API được so với phí thuê bao. Chất lượng model nằm ngoài phép tính này.', 'BodyVN')]
criteria = [
    ['Hạng mục', 'Giả định chuẩn', 'Cách tính'],
    ['Input', '10 triệu token/tháng', 'Số triệu token input × giá input'],
    ['Output', '2 triệu token/tháng', 'Số triệu token output × giá output'],
    ['Tỷ lệ', '5 input : 1 output', 'Mức nhẹ và nặng giữ cùng tỷ lệ'],
    ['Baseline', 'Input mới, không cache', 'Không gồm batch, fast mode, context dài, web search'],
    ['Thuê bao', 'Giá niêm yết', 'Chỉ so được khi gói mở đúng model và hạn mức chấp nhận lượng đó'],
]
story.append(table([cells(r, 'Th' if i == 0 else 'Td') for i, r in enumerate(criteria)], [32 * mm, 52 * mm, 94 * mm]))
story += [P('Công thức', 'H2VN')]
story += [P('<b>Chi phí API = (input, triệu token × giá input) + (output, triệu token × giá output).</b><br/>Với tỷ lệ 5:1, mỗi 1 triệu token input kéo theo 0,2 triệu token output. Lượng input để chạm $20 = 20 / (giá input + 0,2 × giá output).', 'BodyVN')]
story += [P('Những khoản nằm ngoài số headline', 'H2VN')]
story += [P(
    'Cache read, batch (thường giảm 50% với các model này), fast mode và context dài làm hóa đơn lệch khỏi bảng. '
    'Với Claude và Gemini, token suy nghĩ nằm trong giá output: 2 triệu output của kịch bản là phần được tính tiền, gồm thinking nếu nhà cung cấp tính thinking như output. '
    'Web search, grounding và tool tính riêng. US-only inference của Claude nhân 1,1 lần giá input và output. Endpoint regional và FedRAMP của OpenAI cộng 10% với model ra từ 5/3/2026.',
    'BodyVN')]
story += [P('Ba kịch bản chỉ là mô hình. Token thật lấy từ log API.', 'SmallVN'), PageBreak()]

story += [P('2. Giá API đang niêm yết', 'H1VN')]
story += [P(f'USD cho 1 triệu token, mức Standard, chưa thuế. OpenAI: trang giá ngày {CHECK}. Claude: rate card hiệu lực 22/10/2026. Gemini: trang giá cập nhật 28/10/2026. DeepSeek: docs 19/10/2026.', 'BodyVN')]
price_head = ['Model', 'Input / 1M', 'Output / 1M', 'Điều kiện của đơn giá']
price_body = [[r['name'], money(r['pin']), money(r['pout']), r['note']] for r in ROWS]
story.append(table(
    [cells(price_head, 'Th')] + [cells(r, 'Td') for r in price_body],
    [52 * mm, 22 * mm, 24 * mm, 80 * mm],
))
story += [P('Mốc đổi giá và giờ thấp điểm', 'H2VN')]
later_head = ['Mốc', 'Input / 1M', 'Output / 1M', 'Kịch bản chuẩn']
later_body = []
for name, pin_s, pout_s in LATER:
    pin, pout = Decimal(pin_s), Decimal(pout_s)
    later_body.append([name, money(pin), money(pout), money(cost(pin, pout, Decimal('10'), Decimal('2')))])
story.append(table(
    [cells(later_head, 'Th')] + [cells(r, 'Td') for r in later_body],
    [78 * mm, 28 * mm, 32 * mm, 40 * mm],
))
story += [P(
    'Giờ cao điểm DeepSeek, theo docs 19/10/2026: thứ Hai đến thứ Sáu, 01:00–04:00 và 06:00–10:00 UTC, trừ ngày lễ Trung Quốc. Giờ còn lại, cả ngày thứ Bảy, Chủ nhật và ngày lễ, tính một nửa. '
    'Search và Fetch $0,75 / 1.000 request thành công. Tool phía server qua DeepSeek Harness, Claude Code và Codex được miễn đến 00:00 giờ Bắc Kinh ngày 1/11/2026.',
    'BodyVN')]
story += [P(
    'Haiku 5.5 đổi giá theo từng request. Tổng 10 triệu token trong tháng vẫn ở mức $0,10 / $0,50 nếu mọi request đứng dưới 100.000 token. Một request vượt ngưỡng thì request đó tính $0,50 / $2,50. '
    'Trang Gemini còn các thẻ giá khác (batch, context, model ảnh). Báo cáo chỉ lấy thẻ Standard của Argon và của Gemini 3.8 Flash.',
    'BodyVN')]
story += [P('Cache làm hóa đơn agent thấp hơn bảng', 'H2VN')]
story += [P(
    'Phiên agent đọc lại prefix đã cache. Sonnet 5.5 cache read $0,10 so với input $2,00. Fable 5.1 cache read $0,25 so với input $10,00. '
    'Bảng headline là trường hợp input mới toàn bộ. Hóa đơn thật có thể thấp hơn nhiều khi phần lớn input là cache read. Báo cáo không giả định một tỷ lệ cache để tính lại cả bảng.',
    'BodyVN'), PageBreak()]

story += [P('3. Hòa vốn với gói $20', 'H1VN')]
story += [P('Số tiền dưới đây là chi phí API của đúng kịch bản. Cột cuối là lượng token, theo tỷ lệ 5:1, để API chạm $20.', 'BodyVN')]
be_head = ['Model', 'Nhẹ', 'Chuẩn', 'Nặng', 'So với gói $20']
be_body = [[r['name'], money(r['light']), money(r['std']), money(r['heavy']), f"{r['text']}. Mốc $20: {r['point']}."] for r in ROWS]
story.append(table(
    [cells(be_head, 'Th')] + [cells(r, 'Td') for r in be_body],
    [46 * mm, 20 * mm, 22 * mm, 22 * mm, 68 * mm],
))
story += [Spacer(1, 2 * mm), P('USD, kịch bản chuẩn, input mới không cache. Trục đến $240 để cột Astra $200 còn nằm trong hình. Sol đại diện cho Sonnet 5.5 và Argon ưu đãi (cùng $40). Astra đại diện cho Fable 5.1 (cùng $200).', 'SmallVN')]
chart_items = sorted(((r['chart'], r['std']) for r in ROWS if r['chart']), key=lambda item: item[1])
story.append(cost_bars(chart_items))
story += [P('Cách đọc', 'H2VN')]
story += [P(
    f"Terra chạm đúng {money(BY['terra']['std'])} ở mức chuẩn, tức 10M input + 2M output. "
    f"Luna, Haiku khi mọi request dưới 100.000 token, và DeepSeek Flash giờ cao điểm đều dưới $20 ở mức chuẩn "
    f"({money(BY['luna']['std'])}, {money(BY['haiku_lo']['std'])}, {money(BY['dsflash']['std'])}). "
    f"DeepSeek Flash giờ cao điểm ở mức nặng là {money(BY['dsflash']['heavy'])}. "
    f"Sol, Sonnet 5.5 và Argon ưu đãi vượt $20 sau 5,00M input + 1,00M output. "
    f"Opus 5.5, và Argon từ 1/12/2026, vượt sau 2,50M input + 0,50M output. "
    f"Astra và Fable 5.1 bằng $20 ngay ở mức nhẹ.",
    'BodyVN')]
story += [P(
    'Phép so với $20 chỉ đúng khi gói $20 mở đúng model đó và hạn mức thật sự cho phép lượng token đó. '
    'Astra đầy đủ hơn ở ChatGPT Pro. Fable 5.1 nằm ở nhóm Max của Perplexity. Google AI Plus $4,99 có ghi Gemini 4 Argon, nhưng hạn mức là bội số của gói miễn phí.',
    'BodyVN'), PageBreak()]

story += [P('4. Giá thuê bao để đối chiếu', 'H1VN')]
story += [P('Thuê bao không đổi ra một số token cố định. Cột giá dưới đây để biết gói nào đang mở model nào, rồi mới mang về bảng hòa vốn.', 'BodyVN')]
subs = [
    ['ChatGPT Go', '$8/tháng', 'Số này không nằm trên HTML openai.com/chatgpt/pricing đã tải. Nhiều trang theo dõi giá, đối chiếu chatgpt.com ngày 17–28/10/2026, ghi mức này.', 'Đối chiếu'],
    ['ChatGPT Plus', '$20/tháng, trả theo tháng', 'Cùng nhóm trang theo dõi. Họ ghi model chat mặc định là GPT-6.1 Sol từ khoảng 7/10/2026, và Astra bị hạn chế trên Plus.', 'Đối chiếu'],
    ['ChatGPT Pro 100', '$100/tháng', 'Ultrafast không có trong gói.', 'Help Center, bài 9793128'],
    ['ChatGPT Pro 200', '$200/tháng', 'Đăng ký mới ngoài cửa sổ 22–29/9/2026 có hạn mức thấp hơn. Hạn mức cũ giữ đến hết 29/10/2026. Giá vẫn $200. Pro trả theo tháng.', 'Help Center, bài 9793128'],
    ['ChatGPT Pro 500', '$500/tháng', 'Có Ultrafast cho GPT-6 Astra và GPT-6.1 Sol. Hạn mức tiêu hao 8 lần Standard, sau đó credit 6 lần.', 'Help Center, bài 9793128'],
    ['Claude Pro', '$20/tháng, hoặc $17/tháng khi trả $200 trước một năm', 'Ít nhất 5 lần Free mỗi phiên. Hạn mức là phiên 5 giờ và hạn tuần.', 'claude.com/pricing, 29/10/2026'],
    ['Claude Max', 'Từ $100/tháng, mức 5x và 20x so với Pro', 'Kèm credit API $100/tháng (Max 5x) hoặc $200/tháng (Max 20x). Credit không phải tiền mặt và không trả cho Claude Code dùng trực tiếp. Bảng model ghi Fable trên Max ở mức 50% hạn tuần.', 'claude.com/pricing'],
    ['Claude Team', 'Standard $25/ghế/tháng hoặc $20 trả năm. Premium $125 hoặc $100 trả năm.', 'Premium bằng 5 lần ghế Standard. Pool credit API tối đa $500/tháng.', 'claude.com/pricing'],
    ['Claude Enterprise', '$20/ghế/tháng, trả năm, tối thiểu 20 ghế', 'Cộng usage theo giá API. Không có credit API sẵn.', 'claude.com/pricing'],
    ['Google AI Plus', '$4,99/tháng', '2 lần free, có Gemini 4 Argon, 400 GB. Gói gồm lưu trữ.', 'gemini.google/subscriptions/'],
    ['Google AI Pro', '$19,99/tháng', '4 lần free, 5 TB. Một trang Google One ghi năm $199,99. Giá trị nằm ở bộ lưu trữ và ứng dụng Google.', 'gemini.google/subscriptions/'],
    ['Google AI Ultra', '$99,99/tháng (5 lần Pro) và $199,99/tháng (20 lần Pro)', 'Trang Google One cũ vẫn ghi $249,99 và 30 TB. Báo cáo lấy số trên gemini.google/subscriptions/.', 'gemini.google/subscriptions/'],
    ['Perplexity Pro', '$20/tháng hoặc $200/năm', 'Trang help so sánh gói bị Cloudflare khi đọc trực tiếp, nên $20 là đối chiếu trang giá và bundle JS ngày 23–28/10/2026. Help model sửa 27/10/2026: GPT-6.1 Sol, Gemini 3.8 Flash, Sonnet 5.5, Kimi K3, GLM 5.3, Grok 4.7, Nemotron 3.5 Super VL.', 'Đối chiếu + help model'],
    ['Perplexity Max', '$200/tháng hoặc $2.000/năm', 'Thêm GPT-6 Astra, Gemini 4 Argon, Opus 5.5, Fable 5.1. Hạn mức là mức dùng trung bình theo tuần và tháng.', 'Help Max, sửa 14/9/2026'],
    ['Perplexity Enterprise', 'Pro $40/ghế hoặc $400/năm. Max $325/ghế hoặc $3.250/năm.', 'Cùng cách chia model giữa Enterprise Pro và Enterprise Max.', 'Help, cập nhật 8/10/2026'],
    ['GitHub Copilot Pro', '$10/tháng, 1.500 AI credit', '1.000 base + 500 flex. 1 credit = $0,01, tức khoảng $15 usage. Completion và NES không tốn credit.', 'docs.github.com và trang plans'],
    ['Copilot Pro+', '$39/tháng, 7.000 credit', '3.900 + 3.100. Khoảng $70 usage.', 'Cùng nguồn'],
    ['Copilot Max', '$100/tháng, 20.000 credit', '10.000 + 10.000. Khoảng $200 usage.', 'Cùng nguồn'],
    ['Copilot Business / Enterprise', '$19 và $39 mỗi ghế', '1.900 và 3.900 credit gộp. Auto giảm 10%. Fusion giảm 30% đến 30/11/2026. Không đổi credit ra kịch bản 10M + 2M vì không có hạn token công khai.', 'Cùng nguồn'],
    ['DeepSeek', 'Không có gói cá nhân chính thức', 'So bằng API ở mục 2.', 'Docs 19/10/2026'],
]
story.append(table(
    [cells(['Gói', 'Giá', 'Model và hạn mức đã ghi', 'Nguồn'], 'Th')] + [cells(r, 'Td') for r in subs],
    [34 * mm, 42 * mm, 68 * mm, 34 * mm],
))
story += [P(
    'Câu hỏi gói Max của Claude có đáng tiền hơn API, kể cả credit $100–$200, nằm ở hai báo cáo cùng thư mục: '
    '«2.Claude - Quy đổi gói sang giá trị API» và «3.So sánh Claude Pro Max Enterprise và API - 10.2026». Báo cáo này không lặp lại phần đó.',
    'BodyVN'), PageBreak()]

story += [P('5. Khuyến nghị theo nhu cầu', 'H1VN')]
recs = [
    ['Văn phòng đa năng', 'ChatGPT Plus hoặc Google AI Pro', 'Claude Pro', 'Plus hợp viết, file và workflow. AI Pro hợp khi đã nằm trong Gmail, Docs, Drive. Kiểm tra lại giá Plus vì HTML chính thức không hiện số.'],
    ['Viết tài liệu dài', 'Claude Pro', 'ChatGPT Plus', 'Sonnet 5.5 ở mức chuẩn là $40 API. Pro $20 có lợi thế tiền nếu hạn mức chịu được lượng viết đó.'],
    ['Nghiên cứu, cần nguồn', 'Perplexity Pro', 'ChatGPT Plus', 'Lấy giá Pro $20 theo đối chiếu 23–28/10/2026. Max $200 mới mở Astra, Argon, Opus 5.5 và Fable 5.1.'],
    ['Lập trình trong IDE', 'Copilot Pro', 'Thêm một ghế Claude hoặc ChatGPT', 'Copilot tính bằng credit, không bằng kịch bản 10M + 2M. Model mạnh dùng cho phân tích kiến trúc nằm ở ghế chat.'],
    ['Sản phẩm gọi API nhiều', 'Luna, Haiku, Gemini Flash hoặc DeepSeek Flash', 'Mua Pro hoặc Max khi chạm hạn ứng dụng', 'Ở mức chuẩn, nhóm này nằm dưới hoặc sát $20 API. Astra và Fable 5.1 đạt $200 ở cùng mức.'],
    ['Nhóm nhỏ', '1–2 ghế Pro để chuẩn hóa việc', 'Business khi cần quản trị và thanh toán', 'Nâng gói sau 30 ngày nếu nhật ký tác vụ chỉ ra giờ tiết kiệm lớn hơn phí.'],
]
story.append(table(
    [cells(['Nhu cầu', 'Lựa chọn đầu', 'Phương án khác', 'Lý do'], 'Th')] + [cells(r, 'Td') for r in recs],
    [32 * mm, 42 * mm, 42 * mm, 62 * mm],
))
story += [P('Thử 30 ngày', 'H2VN')]
story += [P(
    '<b>Tuần 1:</b> ghi 10 tác vụ thường làm và thời gian hiện tại.<br/>'
    '<b>Tuần 2:</b> dùng cùng bộ prompt, đo thời gian, số lần sửa và chất lượng.<br/>'
    '<b>Tuần 3:</b> ghi lúc bị chặn hạn, model thực sự mở được, và tính năng đã dùng.<br/>'
    '<b>Tuần 4:</b> giữ gói có giờ tiết kiệm nhân giá trị giờ lớn hơn phí. Hủy gói trùng việc.',
    'BodyVN')]
story += [P(
    'Điểm vào cho Apero: 1–2 tài khoản Claude Pro hoặc ChatGPT Plus để chuẩn hóa việc viết và đọc tài liệu; Copilot Pro cho người code; Perplexity Pro cho người cần nguồn. '
    'API trả theo token cho phần việc lặp lại, ưu tiên Luna, Haiku, Gemini 3.8 Flash và DeepSeek Flash. Chỉ lên Max hoặc Pro 100/200/500 khi hạn mức ứng dụng là chỗ thật sự.',
    'Callout'), PageBreak()]

story += [P('6. Nguồn, giới hạn, checklist', 'H1VN')]
story += [P(f'Kiểm tra ngày {CHECK}. Giá có thể đổi sau các mốc ghi trong bảng.', 'BodyVN')]
sources = [
    ['OpenAI API', 'https://developers.openai.com/api/docs/pricing'],
    ['GPT-6 Astra, context trên 272K', 'https://platform.openai.com/docs/models/gpt-6-astra'],
    ['ChatGPT Pro 100 / 200 / 500', 'https://help.openai.com/en/articles/9793128-about-chatgpt-pro-tiers'],
    ['ChatGPT, trang giá (HTML không hiện số Plus/Go)', 'https://openai.com/chatgpt/pricing/'],
    ['Claude, giá gói', 'https://claude.com/pricing'],
    ['Claude rate card 22/10/2026', 'https://assets.claude.com/5633dc848caa431115468f31c7085d695bbfb9cc.pdf'],
    ['Gemini API, cập nhật 28/10/2026', 'https://ai.google.dev/gemini-api/docs/pricing'],
    ['Gemini, gói cá nhân', 'https://gemini.google/subscriptions/'],
    ['DeepSeek, 19/10/2026', 'https://api-docs.deepseek.com/quick_start/pricing'],
    ['DeepSeek, thông báo 10/9/2026 về id V4-Pro', 'https://api-docs.deepseek.com/news/news260910'],
    ['Perplexity Max', 'https://www.perplexity.ai/help-center/en/articles/11680686-perplexity-max'],
    ['Perplexity, model trong gói, sửa 27/10/2026', 'https://www.perplexity.ai/help-center/en/articles/10354919-what-advanced-ai-models-are-included-in-my-subscription'],
    ['GitHub Copilot', 'https://github.com/features/copilot/plans'],
    ['GitHub Copilot, tài liệu gói', 'https://docs.github.com/en/copilot/about-github-copilot/subscription-plans-for-github-copilot'],
]
story.append(table(
    [cells(['Nguồn', 'Liên kết'], 'Th')] + [cells(r, 'Td') for r in sources],
    [62 * mm, 116 * mm],
))
story += [P('Mốc cần xem lại', 'H2VN')]
story += [P(
    'Argon hết giá mở cửa ngày 30/11/2026. Gemini 3.8 Flash hết giá mở cửa ngày 31/12/2026. Fusion của Copilot giảm 30% đến 30/11/2026. '
    'Tool phía server của DeepSeek bắt đầu tính sau 00:00 giờ Bắc Kinh ngày 1/11/2026. Hạn mức cũ của ChatGPT Pro 200 giữ đến hết 29/10/2026. '
    'GPT-5.6 Sol còn giá khuyến mãi ít nhất đến 21/11/2026; model này không nằm trong bộ so sánh.',
    'BodyVN')]
story += [P('Giới hạn', 'H2VN')]
story += [P(
    'ChatGPT Go $8 và Plus $20 lấy từ nhiều trang theo dõi giá ngày 17–28/10/2026, vì HTML trang giá OpenAI không hiện con số. '
    'Perplexity Pro $20 lấy từ đối chiếu trang giá và bundle JS ngày 23–28/10/2026; trang help so sánh gói bị chặn khi đọc trực tiếp. Max $200 lấy từ bài help chính thức. '
    'Thuế, khuyến mãi theo nước và cửa hàng Apple hoặc Google Play có thể lệch giá web. Benchmark công khai không được dùng làm hiệu suất trong báo cáo này.',
    'BodyVN')]
story += [P('Checklist trước khi trả tiền', 'H2VN')]
story += [P(
    'Gói có mở đúng model đang cần. Hạn mức tuần cao điểm có đủ. Công việc có dữ liệu nhạy cảm hay không. '
    'Đã có sẵn trong IDE hoặc bộ tài liệu đang dùng. Hủy được và biết ngày gia hạn. Với API, log có tách cache, batch và thinking.',
    'BodyVN')]
story += [Spacer(1, 3 * mm), P(
    'Không có một gói rẻ nhất cho mọi việc. Ở mức chuẩn, model $2 / $10 đã thành $40 API, nên gói $20 có lợi thế tiền khi nó mở đúng model đó và hạn mức chịu được. '
    'Luna, Haiku dưới ngưỡng 100.000 token và DeepSeek Flash giờ cao điểm vẫn dưới $20 ở mức chuẩn. Astra và Fable 5.1 bằng $20 ngay từ mức nhẹ, và chúng nằm ở gói cao hơn gói $20.',
    'Callout')]
story += [Spacer(1, 4 * mm), P('Tài liệu tham khảo nội bộ Apero. Đối chiếu lại giá và điều khoản trên trang chính thức trước khi mua.', 'SmallVN')]

doc = SimpleDocTemplate(
    OUT, pagesize=A4, rightMargin=16 * mm, leftMargin=16 * mm, topMargin=18 * mm, bottomMargin=16 * mm,
    title='Hiệu suất so với giá của các gói AI thông dụng', author='Apero',
)
doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
print(OUT)
print('bytes', os.path.getsize(OUT))
for r in ROWS:
    print(f"{r['key']}\t{money(r['light'])}\t{money(r['std'])}\t{money(r['heavy'])}\t{r['text']}")
