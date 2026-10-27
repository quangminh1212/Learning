from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from xml.sax.saxutils import escape
import re
from pathlib import Path

md = Path('bao-cao-repo-giam-token-llm.md').read_text(encoding='utf-8')
out = 'bao-cao-repo-giam-token-llm.pdf'
pdfmetrics.registerFont(TTFont('DejaVu', r'C:\\Windows\\Fonts\\DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DejaVu-Bold', r'C:\\Windows\\Fonts\\DejaVuSans-Bold.ttf'))
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='TitleVN', parent=styles['Title'], fontName='DejaVu-Bold', fontSize=18, leading=23, alignment=TA_CENTER, spaceAfter=14))
styles.add(ParagraphStyle(name='H2VN', parent=styles['Heading2'], fontName='DejaVu', fontSize=13, leading=16, spaceBefore=10, spaceAfter=6, textColor='#17365d'))
styles.add(ParagraphStyle(name='H3VN', parent=styles['Heading3'], fontName='DejaVu', fontSize=11, leading=14, spaceBefore=7, spaceAfter=4, textColor='#24527a'))
styles.add(ParagraphStyle(name='BodyVN', parent=styles['BodyText'], fontName='DejaVu', fontSize=8.5, leading=11, spaceAfter=5))
story = []
para = []
in_code = False

def flush():
    global para
    if para:
        text = ' '.join(para).strip()
        text = escape(text)
        text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<link href="\2" color="#1155cc">\1</link>', text)
        text = text.replace('**', '<b>', 1).replace('**', '</b>', 1).replace('`', '')
        story.append(Paragraph(text, styles['BodyVN']))
        para = []

for line in md.splitlines():
    if line.startswith('```'):
        flush(); in_code = not in_code; continue
    if in_code:
        para.append(line); continue
    if line.startswith('# '):
        flush(); story.append(Paragraph(escape(line[2:]), styles['TitleVN']))
    elif line.startswith('## '):
        flush(); story.append(Paragraph(escape(line[3:]), styles['H2VN']))
    elif line.startswith('### '):
        flush(); story.append(Paragraph(escape(line[4:]), styles['H3VN']))
    elif line.startswith('|') or line.startswith('---'):
        flush(); continue
    elif not line.strip():
        flush(); story.append(Spacer(1, 3))
    else:
        para.append(line)
flush()
SimpleDocTemplate(out, pagesize=A4, rightMargin=1.7*cm, leftMargin=1.7*cm, topMargin=1.7*cm, bottomMargin=1.7*cm, title='Báo cáo repo giảm token LLM', author='Claude-Fable / Anthropic').build(story)
print(out)
