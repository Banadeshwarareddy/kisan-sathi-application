from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor, white
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer,
    Table, TableStyle
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from django.db.models import Sum
from decimal import Decimal
from io import BytesIO
from datetime import datetime
import os
from django.conf import settings
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Register DejaVu Sans font for Unicode Indian Rupee symbol (₹) support
FONT_DIR = os.path.join(str(settings.BASE_DIR), 'static', 'fonts')
pdfmetrics.registerFont(TTFont('DejaVuSans', os.path.join(FONT_DIR, 'DejaVuSans.ttf')))
pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', os.path.join(FONT_DIR, 'DejaVuSans-Bold.ttf')))
pdfmetrics.registerFontFamily('DejaVuSans', normal='DejaVuSans', bold='DejaVuSans-Bold')



# Colors matching dark theme
GREEN = HexColor('#22c55e')
GREEN_DARK = HexColor('#16a34a')
BLUE = HexColor('#3b82f6')
ORANGE = HexColor('#f97316')
GRAY = HexColor('#6b7280')
WHITE = white


def make_header(farmer_name, title, subtitle=''):
    """Generate PDF header banner"""
    data = [[
        Paragraph(
            f'<font color="white" size="16"><b>KISAN SATHI</b></font>',
            ParagraphStyle('h', fontName='DejaVuSans-Bold', fontSize=16, textColor=WHITE)
        ),
        Paragraph(
            f'<font color="white" size="11"><b>{title}</b></font>'
            f'<br/><font color="white" size="9">{subtitle}</font>'
            f'<br/><font color="white" size="8">'
            f'Farmer: {farmer_name} | '
            f'Generated: {datetime.now().strftime("%d %b %Y %I:%M %p")}'
            f'</font>',
            ParagraphStyle('h2', fontName='DejaVuSans', fontSize=11, textColor=WHITE, alignment=TA_RIGHT)
        )
    ]]
    t = Table(data, colWidths=[90*mm, 100*mm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), HexColor('#1b4332')),
        ('PADDING', (0,0), (-1,-1), 12),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    return t


def section_title(text, color=None):
    color = color or GREEN_DARK
    data = [[Paragraph(
        f'<font color="white"><b>{text}</b></font>',
        ParagraphStyle('st', fontName='DejaVuSans-Bold', fontSize=11, textColor=WHITE)
    )]]
    t = Table(data, colWidths=[190*mm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), color),
        ('PADDING', (0,0), (-1,-1), 7),
    ]))
    return t


def generate_expense_pdf(expenses, farmer) -> BytesIO:
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A4,
        rightMargin=10*mm, leftMargin=10*mm,
        topMargin=10*mm, bottomMargin=10*mm
    )
    story = []

    total = sum(e.amount for e in expenses)
    farmer_name = farmer.get_full_name() or farmer.username

    # Header
    story.append(make_header(farmer_name, 'Expense Report', f'Total Expenses: ₹{total:,.2f}'))
    story.append(Spacer(1, 5*mm))

    # Summary stats
    stats_data = [[
        Paragraph(
            f'<b>Total Expenses</b><br/>'
            f'<font size="14" color="#3b82f6">₹{total:,.2f}</font>',
            ParagraphStyle('s', fontName='DejaVuSans', fontSize=9, alignment=TA_CENTER)
        ),
        Paragraph(
            f'<b>Total Records</b><br/>'
            f'<font size="14" color="#22c55e">{expenses.count()}</font>',
            ParagraphStyle('s', fontName='DejaVuSans', fontSize=9, alignment=TA_CENTER)
        ),
        Paragraph(
            f'<b>Report Date</b><br/>'
            f'<font size="11">{datetime.now().strftime("%d %b %Y")}</font>',
            ParagraphStyle('s', fontName='DejaVuSans', fontSize=9, alignment=TA_CENTER)
        ),
    ]]
    stats = Table(stats_data, colWidths=[63*mm, 63*mm, 64*mm])
    stats.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), HexColor('#dbeafe')),
        ('BACKGROUND', (1,0), (1,0), HexColor('#dcfce7')),
        ('BACKGROUND', (2,0), (2,0), HexColor('#f3f4f6')),
        ('PADDING', (0,0), (-1,-1), 10),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOX', (0,0), (-1,-1), 0.5, HexColor('#e5e7eb')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, HexColor('#e5e7eb')),
    ]))
    story.append(stats)
    story.append(Spacer(1, 5*mm))

    # Expenses Table
    story.append(section_title('Expense Records', BLUE))
    story.append(Spacer(1, 2*mm))

    table_data = [['#', 'Category', 'Amount (₹)', 'Date', 'Notes']]
    for i, e in enumerate(expenses, 1):
        table_data.append([
            str(i),
            e.get_category_display(),
            f'₹{e.amount:,.2f}',
            e.date.strftime('%d %b %Y'),
            (e.notes[:40] + '...') if len(e.notes) > 40 else e.notes
        ])
    
    # Total row
    table_data.append(['', 'TOTAL', f'₹{total:,.2f}', '', ''])

    t = Table(table_data, colWidths=[10*mm, 45*mm, 35*mm, 30*mm, 70*mm])
    t.setStyle(TableStyle([
        ('FONTNAME', (0,0), (-1,-1), 'DejaVuSans'),
        ('BACKGROUND', (0,0), (-1,0), HexColor('#1b4332')),
        ('TEXTCOLOR', (0,0), (-1,0), WHITE),
        ('FONTNAME', (0,0), (-1,0), 'DejaVuSans-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('PADDING', (0,0), (-1,-1), 6),
        ('ROWBACKGROUNDS', (0,1), (-1,-2), [WHITE, HexColor('#f9fafb')]),
        ('GRID', (0,0), (-1,-1), 0.5, HexColor('#e5e7eb')),
        ('BACKGROUND', (0,-1), (-1,-1), HexColor('#dbeafe')),
        ('FONTNAME', (0,-1), (-1,-1), 'DejaVuSans-Bold'),
        ('ALIGN', (2,0), (2,-1), 'RIGHT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t)

    # Footer
    story.append(Spacer(1, 10*mm))
    story.append(Paragraph(
        'Kisan Sathi AI - Smart Farming Platform | This is a system generated report.',
        ParagraphStyle('ft', fontName='DejaVuSans', fontSize=7, textColor=GRAY, alignment=TA_CENTER)
    ))

    doc.build(story)
    buffer.seek(0)
    return buffer


def generate_income_pdf(incomes, farmer) -> BytesIO:
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A4,
        rightMargin=10*mm, leftMargin=10*mm,
        topMargin=10*mm, bottomMargin=10*mm
    )
    story = []

    total = sum(i.total_amount or 0 for i in incomes)
    farmer_name = farmer.get_full_name() or farmer.username

    story.append(make_header(farmer_name, 'Income Report', f'Total Income: ₹{total:,.2f}'))
    story.append(Spacer(1, 5*mm))

    # Stats
    pending = sum(1 for i in incomes if i.payment_status == 'pending')
    received = sum(1 for i in incomes if i.payment_status == 'received')

    stats_data = [[
        Paragraph(
            f'<b>Total Income</b><br/>'
            f'<font size="14" color="#22c55e">₹{total:,.2f}</font>',
            ParagraphStyle('s', fontName='DejaVuSans', fontSize=9, alignment=TA_CENTER)
        ),
        Paragraph(
            f'<b>Received</b><br/>'
            f'<font size="14" color="#22c55e">{received}</font>',
            ParagraphStyle('s', fontName='DejaVuSans', fontSize=9, alignment=TA_CENTER)
        ),
        Paragraph(
            f'<b>Pending</b><br/>'
            f'<font size="14" color="#f97316">{pending}</font>',
            ParagraphStyle('s', fontName='DejaVuSans', fontSize=9, alignment=TA_CENTER)
        ),
    ]]
    stats = Table(stats_data, colWidths=[63*mm, 63*mm, 64*mm])
    stats.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), HexColor('#dcfce7')),
        ('BACKGROUND', (1,0), (1,0), HexColor('#dbeafe')),
        ('BACKGROUND', (2,0), (2,0), HexColor('#fff7ed')),
        ('PADDING', (0,0), (-1,-1), 10),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 0.5, HexColor('#e5e7eb')),
    ]))
    story.append(stats)
    story.append(Spacer(1, 5*mm))

    story.append(section_title('Income Records', GREEN_DARK))
    story.append(Spacer(1, 2*mm))

    table_data = [['#', 'Crop', 'Qty', 'Rate/Unit', 'Total (₹)', 'Buyer', 'Date', 'Status']]
    for i, inc in enumerate(incomes, 1):
        status_text = inc.payment_status.title()
        table_data.append([
            str(i),
            inc.crop,
            f'{inc.quantity} {inc.unit}' if inc.quantity else '-',
            f'₹{inc.rate_per_unit:,.2f}' if inc.rate_per_unit else '-',
            f'₹{inc.total_amount:,.2f}' if inc.total_amount else '-',
            inc.buyer_name or '-',
            inc.sale_date.strftime('%d %b %Y'),
            status_text
        ])

    table_data.append(['', '', '', 'TOTAL', f'₹{total:,.2f}', '', '', ''])

    t = Table(table_data, colWidths=[8*mm, 30*mm, 20*mm, 20*mm, 25*mm, 30*mm, 22*mm, 18*mm])
    t.setStyle(TableStyle([
        ('FONTNAME', (0,0), (-1,-1), 'DejaVuSans'),
        ('BACKGROUND', (0,0), (-1,0), HexColor('#1b4332')),
        ('TEXTCOLOR', (0,0), (-1,0), WHITE),
        ('FONTNAME', (0,0), (-1,0), 'DejaVuSans-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 7),
        ('PADDING', (0,0), (-1,-1), 5),
        ('ROWBACKGROUNDS', (0,1), (-1,-2), [WHITE, HexColor('#f9fafb')]),
        ('GRID', (0,0), (-1,-1), 0.5, HexColor('#e5e7eb')),
        ('BACKGROUND', (0,-1), (-1,-1), HexColor('#dcfce7')),
        ('FONTNAME', (0,-1), (-1,-1), 'DejaVuSans-Bold'),
        ('ALIGN', (4,0), (4,-1), 'RIGHT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t)
    
    # Footer
    story.append(Spacer(1, 10*mm))
    story.append(Paragraph(
        'Kisan Sathi AI - Smart Farming Platform | This is a system generated report.',
        ParagraphStyle('ft', fontName='DejaVuSans', fontSize=7, textColor=GRAY, alignment=TA_CENTER)
    ))

    doc.build(story)
    buffer.seek(0)
    return buffer


def generate_full_report_pdf(farmer) -> BytesIO:
    """Complete farm financial report PDF"""
    from .models import Expense, Income, Livestock

    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A4,
        rightMargin=10*mm, leftMargin=10*mm,
        topMargin=10*mm, bottomMargin=10*mm
    )
    story = []

    farmer_name = farmer.get_full_name() or farmer.username

    expenses = Expense.objects.filter(farmer=farmer, is_deleted=False)
    incomes = Income.objects.filter(farmer=farmer, is_deleted=False)
    livestock = Livestock.objects.filter(farmer=farmer, is_active=True)

    total_exp = sum(e.amount for e in expenses) or Decimal('0')
    total_inc = sum(i.total_amount or 0 for i in incomes) or Decimal('0')
    net_profit = total_inc - total_exp

    # Header
    story.append(make_header(farmer_name, 'Complete Farm Report', f'Net Profit: ₹{net_profit:,.2f}'))
    story.append(Spacer(1, 5*mm))

    # Financial Summary
    story.append(section_title('Financial Summary'))
    story.append(Spacer(1, 2*mm))

    fin_data = [
        ['Total Income', f'₹{total_inc:,.2f}', 'Total Expenses', f'₹{total_exp:,.2f}'],
        ['Net Profit/Loss', f'₹{net_profit:,.2f}', '', ''],
    ]
    fin_t = Table(fin_data, colWidths=[45*mm, 50*mm, 45*mm, 50*mm])
    fin_t.setStyle(TableStyle([
        ('FONTNAME', (0,0), (-1,-1), 'DejaVuSans'),
        ('FONTNAME', (0,0), (0,-1), 'DejaVuSans-Bold'),
        ('FONTNAME', (2,0), (2,-1), 'DejaVuSans-Bold'),
        ('BACKGROUND', (1,0), (1,0), HexColor('#dcfce7')),
        ('BACKGROUND', (3,0), (3,0), HexColor('#fff7ed')),
        ('BACKGROUND', (1,1), (1,1), HexColor('#dcfce7') if net_profit >= 0 else HexColor('#fee2e2')),
        ('PADDING', (0,0), (-1,-1), 8),
        ('GRID', (0,0), (-1,-1), 0.5, HexColor('#e5e7eb')),
        ('FONTSIZE', (0,0), (-1,-1), 9),
    ]))
    story.append(fin_t)
    story.append(Spacer(1, 5*mm))

    # Expenses section
    if expenses.exists():
        story.append(section_title('Expenses', BLUE))
        story.append(Spacer(1, 2*mm))

        exp_data = [['Category', 'Amount', 'Date', 'Notes']]
        for e in expenses[:20]:
            exp_data.append([
                e.get_category_display(),
                f'₹{e.amount:,.2f}',
                e.date.strftime('%d %b %Y'),
                (e.notes[:35]+'...') if len(e.notes) > 35 else e.notes
            ])
        exp_data.append(['TOTAL', f'₹{total_exp:,.2f}', '', ''])

        et = Table(exp_data, colWidths=[50*mm, 35*mm, 30*mm, 75*mm])
        et.setStyle(TableStyle([
            ('FONTNAME', (0,0), (-1,-1), 'DejaVuSans'),
            ('BACKGROUND', (0,0), (-1,0), BLUE),
            ('TEXTCOLOR', (0,0), (-1,0), WHITE),
            ('FONTNAME', (0,0), (-1,0), 'DejaVuSans-Bold'),
            ('FONTSIZE', (0,0), (-1,-1), 8),
            ('PADDING', (0,0), (-1,-1), 5),
            ('ROWBACKGROUNDS', (0,1), (-1,-2), [WHITE, HexColor('#f9fafb')]),
            ('GRID', (0,0), (-1,-1), 0.5, HexColor('#e5e7eb')),
            ('BACKGROUND', (0,-1), (-1,-1), HexColor('#dbeafe')),
            ('FONTNAME', (0,-1), (-1,-1), 'DejaVuSans-Bold'),
        ]))
        story.append(et)
        story.append(Spacer(1, 5*mm))

    # Income section
    if incomes.exists():
        story.append(section_title('Income', GREEN_DARK))
        story.append(Spacer(1, 2*mm))

        inc_data = [['Crop', 'Quantity', 'Total', 'Buyer', 'Date']]
        for i in incomes[:20]:
            inc_data.append([
                i.crop,
                f'{i.quantity} {i.unit}' if i.quantity else '-',
                f'₹{i.total_amount:,.2f}' if i.total_amount else '-',
                i.buyer_name or '-',
                i.sale_date.strftime('%d %b %Y'),
            ])
        inc_data.append(['TOTAL', '', f'₹{total_inc:,.2f}', '', ''])

        it = Table(inc_data, colWidths=[40*mm, 35*mm, 35*mm, 40*mm, 30*mm])
        it.setStyle(TableStyle([
            ('FONTNAME', (0,0), (-1,-1), 'DejaVuSans'),
            ('BACKGROUND', (0,0), (-1,0), GREEN_DARK),
            ('TEXTCOLOR', (0,0), (-1,0), WHITE),
            ('FONTNAME', (0,0), (-1,0), 'DejaVuSans-Bold'),
            ('FONTSIZE', (0,0), (-1,-1), 8),
            ('PADDING', (0,0), (-1,-1), 5),
            ('ROWBACKGROUNDS', (0,1), (-1,-2), [WHITE, HexColor('#f9fafb')]),
            ('GRID', (0,0), (-1,-1), 0.5, HexColor('#e5e7eb')),
            ('BACKGROUND', (0,-1), (-1,-1), HexColor('#dcfce7')),
            ('FONTNAME', (0,-1), (-1,-1), 'DejaVuSans-Bold'),
        ]))
        story.append(it)
        story.append(Spacer(1, 5*mm))

    # Footer
    story.append(Paragraph(
        f'Kisan Sathi AI | Smart Farming Platform | System Generated Report | {datetime.now().strftime("%d %B %Y")}',
        ParagraphStyle('ft', fontName='DejaVuSans', fontSize=7, textColor=GRAY, alignment=TA_CENTER)
    ))

    doc.build(story)
    buffer.seek(0)
    return buffer
