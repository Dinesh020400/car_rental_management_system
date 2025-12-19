from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch, cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image as RLImage
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT, TA_JUSTIFY
from reportlab.pdfgen import canvas
from datetime import datetime
import os

class ProfessionalInvoiceGenerator:
    def __init__(self):
        self.invoice_folder = 'static/invoices'
        if not os.path.exists(self.invoice_folder):
            os.makedirs(self.invoice_folder)
    
    def generate_invoice(self, booking_data, payment_data, user_data):
        """Generate professional PDF invoice"""
        
        invoice_id = f"INV-{booking_data['id'][:8].upper()}"
        filename = f"{invoice_id}.pdf"
        filepath = os.path.join(self.invoice_folder, filename)
        
        # Create PDF
        doc = SimpleDocTemplate(
            filepath,
            pagesize=A4,
            rightMargin=1.5*cm,
            leftMargin=1.5*cm,
            topMargin=1.5*cm,
            bottomMargin=1.5*cm
        )
        
        elements = []
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'InvoiceTitle',
            parent=styles['Heading1'],
            fontSize=28,
            textColor=colors.HexColor('#1a237e'),
            spaceAfter=5,
            alignment=TA_RIGHT,
            fontName='Helvetica-Bold'
        )
        
        company_style = ParagraphStyle(
            'Company',
            parent=styles['Normal'],
            fontSize=20,
            textColor=colors.HexColor('#3f51b5'),
            spaceAfter=2,
            alignment=TA_LEFT,
            fontName='Helvetica-Bold'
        )
        
        section_header = ParagraphStyle(
            'SectionHeader',
            parent=styles['Heading2'],
            fontSize=11,
            textColor=colors.white,
            backColor=colors.HexColor('#3f51b5'),
            spaceBefore=10,
            spaceAfter=5,
            leftIndent=5,
            fontName='Helvetica-Bold'
        )
        
        # Header Section
        header_data = [
            [
                Paragraph('<b>PREMIUM CAR RENTALS</b>', company_style),
                Paragraph('INVOICE', title_style)
            ],
            [
                Paragraph(
                    'Near Katpadi Junction, Vellore<br/>Tamil Nadu, India - 632006<br/>'
                    'Phone: +91 98765 43210<br/>Email: info@carrentals.com<br/>'
                    'GSTIN: 33AABCU9603R1ZM',
                    ParagraphStyle('Address', parent=styles['Normal'], fontSize=9, textColor=colors.HexColor('#546e7a'))
                ),
                Paragraph(
                    f'<b>Invoice #:</b> {invoice_id}<br/>'
                    f'<b>Date:</b> {datetime.now().strftime("%B %d, %Y")}<br/>'
                    f'<b>Booking ID:</b> {booking_data["id"][:12]}',
                    ParagraphStyle('InvoiceInfo', parent=styles['Normal'], fontSize=9, alignment=TA_RIGHT, textColor=colors.HexColor('#546e7a'))
                )
            ]
        ]
        
        header_table = Table(header_data, colWidths=[9*cm, 9*cm])
        header_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ]))
        elements.append(header_table)
        elements.append(Spacer(1, 0.3*cm))
        
        # Divider line
        line_table = Table([['']], colWidths=[18*cm], rowHeights=[2])
        line_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#3f51b5')),
        ]))
        elements.append(line_table)
        elements.append(Spacer(1, 0.5*cm))
        
        # Bill To Section
        bill_to_data = [
            [
                Paragraph('<b>BILL TO:</b>', ParagraphStyle('BoldLabel', parent=styles['Normal'], fontSize=10, textColor=colors.HexColor('#1a237e'), fontName='Helvetica-Bold')),
                ''
            ],
            [
                Paragraph(
                    f'<b>{user_data.get("username", "Customer")}</b><br/>'
                    f'{user_data.get("email", "N/A")}<br/>'
                    f'Phone: {user_data.get("phone", "N/A")}',
                    ParagraphStyle('BillTo', parent=styles['Normal'], fontSize=10, textColor=colors.HexColor('#37474f'))
                ),
                Paragraph(
                    f'<b>PAYMENT METHOD:</b><br/>{payment_data.get("method", "N/A").upper()}<br/>'
                    f'<b>Status:</b> <font color="#2e7d32">PAID</font><br/>'
                    f'<b>Transaction ID:</b> {payment_data.get("transaction_id", "N/A")[:16]}',
                    ParagraphStyle('Payment', parent=styles['Normal'], fontSize=9, alignment=TA_RIGHT, textColor=colors.HexColor('#37474f'))
                )
            ]
        ]
        
        bill_table = Table(bill_to_data, colWidths=[9*cm, 9*cm])
        bill_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('SPAN', (0, 0), (1, 0)),
        ]))
        elements.append(bill_table)
        elements.append(Spacer(1, 0.6*cm))
        
        # Rental Details Section
        car_name = f"{booking_data.get('car_brand', '')} {booking_data.get('car_model', 'Vehicle')}".strip()
        
        rental_header = Paragraph('  RENTAL DETAILS', section_header)
        elements.append(rental_header)
        elements.append(Spacer(1, 0.2*cm))
        
        rental_data = [
            ['Vehicle', car_name],
            ['Rental Period', f"{booking_data.get('start_date', 'N/A')} to {booking_data.get('end_date', 'N/A')}"],
            ['Duration', f"{booking_data.get('total_days', 0)} days"],
            ['Pickup Location', booking_data.get('pickup_location', 'Not specified')],
            ['Drop Location', booking_data.get('drop_location', 'Not specified')],
            ['Pickup Time', booking_data.get('pickup_time', 'N/A')],
        ]
        
        rental_table = Table(rental_data, colWidths=[5*cm, 13*cm])
        rental_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#eceff1')),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#37474f')),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cfd8dc')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        elements.append(rental_table)
        elements.append(Spacer(1, 0.6*cm))
        
        # Charges Section
        charges_header = Paragraph('  CHARGES', section_header)
        elements.append(charges_header)
        elements.append(Spacer(1, 0.2*cm))
        
        base_amount = booking_data.get('total_price', 0) / 1.18  # Remove GST
        gst_amount = booking_data.get('total_price', 0) - base_amount
        
        charges_data = [
            ['Description', 'Rate', 'Days', 'Amount'],
            ['Vehicle Rental', f"Rs. {base_amount/booking_data.get('total_days', 1):,.2f}", str(booking_data.get('total_days', 0)), f"Rs. {base_amount:,.2f}"],
        ]
        
        # Add location charge if different locations
        if booking_data.get('pickup_location') != booking_data.get('drop_location'):
            charges_data.append(['Different Drop Location Fee', 'Rs. 200.00', '1', 'Rs. 200.00'])
        
        charges_table = Table(charges_data, colWidths=[8*cm, 3.5*cm, 2.5*cm, 4*cm])
        charges_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3f51b5')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cfd8dc')),
            ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        elements.append(charges_table)
        elements.append(Spacer(1, 0.3*cm))
        
        # Summary Section
        summary_data = [
            ['Subtotal', f"Rs. {base_amount:,.2f}"],
            ['GST (18%)', f"Rs. {gst_amount:,.2f}"],
            ['TOTAL AMOUNT', f"Rs. {booking_data.get('total_price', 0):,.2f}"],
        ]
        
        summary_table = Table(summary_data, colWidths=[14*cm, 4*cm])
        summary_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 1), 'Helvetica'),
            ('FONTNAME', (0, 2), (-1, 2), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 1), 10),
            ('FONTSIZE', (0, 2), (-1, 2), 12),
            ('TEXTCOLOR', (0, 0), (-1, 1), colors.HexColor('#546e7a')),
            ('TEXTCOLOR', (0, 2), (-1, 2), colors.white),
            ('BACKGROUND', (0, 2), (-1, 2), colors.HexColor('#2e7d32')),
            ('LINEABOVE', (0, 0), (-1, 0), 1, colors.HexColor('#cfd8dc')),
            ('LINEABOVE', (0, 2), (-1, 2), 1.5, colors.HexColor('#1b5e20')),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ]))
        elements.append(summary_table)
        elements.append(Spacer(1, 0.8*cm))
        
        # Terms and Footer
        terms_style = ParagraphStyle(
            'Terms',
            parent=styles['Normal'],
            fontSize=8,
            textColor=colors.HexColor('#78909c'),
            alignment=TA_JUSTIFY,
            leading=10
        )
        
        terms_text = """
        <b>TERMS & CONDITIONS:</b><br/>
        1. The renter is responsible for any damage to the vehicle during the rental period.<br/>
        2. Late return charges: Rs. 500 per hour after scheduled return time.<br/>
        3. Fuel should be refilled before returning the vehicle.<br/>
        4. Valid driving license and ID proof required at pickup.<br/>
        5. No refund for early returns. Cancellation charges apply.<br/>
        """
        elements.append(Paragraph(terms_text, terms_style))
        elements.append(Spacer(1, 0.4*cm))
        
        # Footer
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=9,
            textColor=colors.HexColor('#3f51b5'),
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        elements.append(Paragraph('Thank you for choosing Premium Car Rentals!', footer_style))
        elements.append(Paragraph(
            '<font size=8 color="#90a4ae">This is a computer-generated invoice and does not require a signature.</font>',
            ParagraphStyle('FooterSmall', parent=styles['Normal'], fontSize=7, alignment=TA_CENTER, textColor=colors.HexColor('#90a4ae'))
        ))
        
        # Build PDF
        doc.build(elements)
        
        return {
            'invoice_id': invoice_id,
            'filename': filename,
            'filepath': filepath,
            'download_url': f'/static/invoices/{filename}'
        }
