from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from datetime import datetime
import os

class PDFReport:
    def __init__(self, output_dir=None):
        """Initialize PDF Report generator.
        
        Args:
            output_dir (str, optional): Directory to save PDF reports. Defaults to 'reports' in current directory.
        """
        self.output_dir = output_dir or os.path.join(os.path.dirname(os.path.dirname(__file__)), 'reports')
        os.makedirs(self.output_dir, exist_ok=True)
        self.styles = getSampleStyleSheet()
        
        # Create custom styles
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=16,
            spaceAfter=30
        ))
        self.styles.add(ParagraphStyle(
            name='PolicyName',
            parent=self.styles['Normal'],
            fontSize=12,
            textColor=colors.HexColor('#000066'),
            spaceAfter=5
        ))

    def create_compliance_report(self, report_data, level):
        """Create a PDF compliance report.
        
        Args:
            report_data (dict): Dictionary containing compliance check results
            level (str): Hardening level used for the check
        """
        # Create filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = os.path.join(self.output_dir, f'protego_compliance_{timestamp}.pdf')
        
        # Create PDF document
        doc = SimpleDocTemplate(
            filename,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        # Build content
        content = []
        
        # Add title
        title = Paragraph(
            f"Protego Compliance Report: CHECK",
            self.styles['CustomTitle']
        )
        content.append(title)
        
        # Add metadata
        content.append(Paragraph(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", self.styles['Normal']))
        content.append(Paragraph(f"Hardening Level: {level}", self.styles['Normal']))
        content.append(Spacer(1, 20))
        
        # Add separator
        content.append(Paragraph("="*50, self.styles['Normal']))
        content.append(Spacer(1, 20))
        
        # Add policy details
        for policy_name, details in report_data.items():
            # Policy name
            content.append(Paragraph(f"POLICY: {policy_name}", self.styles['PolicyName']))
            
            # Create policy details table
            status_color = colors.green if details['status'] == 'SUCCESS' else colors.red
            data = [
                ["Status:", details['status']],
                ["Previous/State:", details.get('previous', 'N/A')],
                ["Current/Final:", details.get('current', 'N/A')],
                ["Target Value:", details['target']]
            ]
            
            t = Table(data, colWidths=[1.5*inch, 4*inch])
            t.setStyle(TableStyle([
                ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
                ('FONTSIZE', (0,0), (-1,-1), 10),
                ('TEXTCOLOR', (0,0), (0,-1), colors.grey),
                ('TEXTCOLOR', (1,0), (1,0), status_color),  # Color the status
                ('ALIGN', (0,0), (-1,-1), 'LEFT'),
                ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ]))
            content.append(t)
            content.append(Spacer(1, 10))
            
            # Add separator
            content.append(Paragraph("-"*50, self.styles['Normal']))
            content.append(Spacer(1, 10))
        
        # Add summary
        content.append(Spacer(1, 20))
        content.append(Paragraph("--- Summary ---", self.styles['Heading2']))
        
        # Calculate statistics
        total = len(report_data)
        success = sum(1 for details in report_data.values() if details['status'] == 'SUCCESS')
        failure = total - success
        
        summary_data = [
            ["Total Checks:", str(total)],
            ["Compliant/Success:", str(success)],
            ["Non-Compliant/Failure:", str(failure)]
        ]
        
        summary_table = Table(summary_data, colWidths=[2*inch, 1*inch])
        summary_table.setStyle(TableStyle([
            ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,-1), 11),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ]))
        content.append(summary_table)
        
        # Build PDF
        doc.build(content)
        return filename