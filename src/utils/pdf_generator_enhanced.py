"""
Enhanced PDF Report Generator
Multi-page professional PDF generation for tax incentive reports
"""
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, 
    PageBreak, ListFlowable, ListItem, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from datetime import datetime
from typing import List, Dict, Any
import io


class EnhancedPDFReportGenerator:
    """Generate enhanced multi-page professional PDF reports"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles"""
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Subtitle style
        self.styles.add(ParagraphStyle(
            name='CustomSubtitle',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#666666'),
            spaceAfter=20,
            alignment=TA_CENTER
        ))
        
        # Section header
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#2c5aa0'),
            spaceAfter=12,
            spaceBefore=20,
            fontName='Helvetica-Bold'
        ))
        
        # Page title
        self.styles.add(ParagraphStyle(
            name='PageTitle',
            parent=self.styles['Heading1'],
            fontSize=20,
            textColor=colors.HexColor('#2c5aa0'),
            spaceAfter=20,
            fontName='Helvetica-Bold'
        ))
        
        # Highlight box
        self.styles.add(ParagraphStyle(
            name='HighlightBox',
            parent=self.styles['Normal'],
            fontSize=12,
            textColor=colors.HexColor('#2c5aa0'),
            fontName='Helvetica-Bold',
            spaceAfter=6
        ))
        
        # Body text with justify
        self.styles.add(ParagraphStyle(
            name='BodyJustify',
            parent=self.styles['Normal'],
            fontSize=11,
            alignment=TA_JUSTIFY,
            spaceAfter=12
        ))
        
        # Bullet points
        self.styles.add(ParagraphStyle(
            name='BulletPoint',
            parent=self.styles['Normal'],
            fontSize=11,
            leftIndent=20,
            spaceAfter=8
        ))
    
    def generate_comparison_report(
        self,
        production_title: str,
        budget: float,
        comparisons: List[Dict[str, Any]],
        best_option: Dict[str, Any]
    ) -> bytes:
        """Generate enhanced 4-page jurisdiction comparison report"""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=50
        )
        
        story = []
        
        # ============================================
        # PAGE 1: EXECUTIVE SUMMARY
        # ============================================
        story.append(Paragraph("Tax Incentive Comparison Report", self.styles['CustomTitle']))
        story.append(Paragraph(
            f"Generated on {datetime.now().strftime('%B %d, %Y')}",
            self.styles['CustomSubtitle']
        ))
        story.append(Spacer(1, 0.5 * inch))
        
        # Production Info
        story.append(Paragraph("Production Information", self.styles['SectionHeader']))
        prod_data = [
            ['Production Title:', production_title],
            ['Total Budget:', f'${budget:,.0f}'],
            ['Analysis Date:', datetime.now().strftime('%B %d, %Y')],
            ['Jurisdictions Analyzed:', str(len(comparisons))]
        ]
        prod_table = Table(prod_data, colWidths=[2*inch, 4*inch])
        prod_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#333333')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        story.append(prod_table)
        story.append(Spacer(1, 0.3 * inch))
        
        # Recommended Location (Highlighted)
        if best_option:
            story.append(Paragraph("RECOMMENDED LOCATION", self.styles['SectionHeader']))
            rec_data = [
                ['Jurisdiction:', best_option['jurisdiction']],
                ['Estimated Credit:', f"${best_option['estimatedCredit']:,.0f}"],
                ['Rate:', f"{best_option['percentage']}%" if best_option.get('percentage') else 'N/A']
            ]
            rec_table = Table(rec_data, colWidths=[2*inch, 4*inch])
            rec_table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 12),
                ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#2c5aa0')),
                ('TEXTCOLOR', (1, 0), (1, -1), colors.HexColor('#28a745')),
                ('FONTNAME', (1, 0), (1, -1), 'Helvetica-Bold'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f0f8ff')),
                ('BOX', (0, 0), (-1, -1), 2, colors.HexColor('#2c5aa0')),
            ]))
            story.append(rec_table)
            story.append(Spacer(1, 0.3 * inch))
        
        # Quick Comparison Table
        story.append(Paragraph("Jurisdiction Comparison", self.styles['SectionHeader']))
        
        table_data = [['Rank', 'Jurisdiction', 'Program', 'Rate', 'Estimated Credit']]
        for comp in comparisons:
            table_data.append([
                str(comp['rank']),
                comp['jurisdiction'],
                comp['ruleName'][:30] + '...' if len(comp['ruleName']) > 30 else comp['ruleName'],
                f"{comp['percentage']}%" if comp.get('percentage') else 'N/A',
                f"${comp['estimatedCredit']:,.0f}"
            ])
        
        comp_table = Table(table_data, colWidths=[0.6*inch, 1.5*inch, 2.2*inch, 0.8*inch, 1.3*inch])
        comp_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c5aa0')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor('#e8f4f8')),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#cccccc')),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f8f8')])
        ]))
        story.append(comp_table)
        
        # PAGE BREAK
        story.append(PageBreak())
        
        # ============================================
        # PAGE 2: DETAILED JURISDICTION ANALYSIS
        # ============================================
        story.append(Paragraph("Detailed Jurisdiction Analysis", self.styles['PageTitle']))
        story.append(Spacer(1, 0.2 * inch))
        
        for i, comp in enumerate(comparisons, 1):
            # Jurisdiction header
            story.append(Paragraph(
                f"{i}. {comp['jurisdiction']} - {comp['ruleName']}", 
                self.styles['SectionHeader']
            ))
            
            # Details table
            details_data = [
                ['Program:', comp['ruleName']],
                ['Type:', comp.get('incentiveType', 'tax_credit').replace('_', ' ').title()],
                ['Base Rate:', f"{comp['percentage']}%" if comp.get('percentage') else 'Fixed Amount'],
                ['Estimated Credit:', f"${comp['estimatedCredit']:,.0f}"],
                ['Your Budget:', f"${budget:,.0f}"],
                ['Effective Rate:', f"{(comp['estimatedCredit']/budget*100):.2f}%"]
            ]
            
            details_table = Table(details_data, colWidths=[1.5*inch, 4.5*inch])
            details_table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dddddd')),
            ]))
            story.append(details_table)
            story.append(Spacer(1, 0.2 * inch))
        
        # PAGE BREAK
        story.append(PageBreak())
        
        # ============================================
        # PAGE 3: REQUIREMENTS & ELIGIBILITY
        # ============================================
        story.append(Paragraph("Requirements & Eligibility Criteria", self.styles['PageTitle']))
        story.append(Spacer(1, 0.2 * inch))
        
        story.append(Paragraph(
            "Understanding the qualification requirements for each jurisdiction is critical for maximizing your tax incentive benefits. Below are the key requirements for each location analyzed.",
            self.styles['BodyJustify']
        ))
        story.append(Spacer(1, 0.2 * inch))
        
        for comp in comparisons:
            story.append(Paragraph(f"{comp['jurisdiction']}", self.styles['SectionHeader']))
            
            # Common requirements (you can customize these based on actual data)
            requirements = [
                f"<b>Minimum Spend:</b> Varies by program (typically ${500000:,.0f} - ${1000000:,.0f})",
                "<b>Local Hiring:</b> May require minimum percentage of local crew",
                "<b>Shoot Days:</b> Minimum number of production days in jurisdiction",
                "<b>Application:</b> Must apply before production begins",
                "<b>Documentation:</b> Detailed expense tracking and reporting required",
                "<b>Promotional:</b> May include promotional logo requirements for bonus credits"
            ]
            
            for req in requirements:
                story.append(Paragraph(f"• {req}", self.styles['BulletPoint']))
            
            story.append(Spacer(1, 0.15 * inch))
        
        story.append(Paragraph(
            "<b>Note:</b> Requirements vary by program and are subject to change. Always consult with the specific film office for current requirements and application procedures.",
            self.styles['BodyJustify']
        ))
        
        # PAGE BREAK
        story.append(PageBreak())
        
        # ============================================
        # PAGE 4: RECOMMENDATIONS & ACTION PLAN
        # ============================================
        story.append(Paragraph("Recommendations & Action Plan", self.styles['PageTitle']))
        story.append(Spacer(1, 0.2 * inch))
        
        if best_option and len(comparisons) > 1:
            # Financial Analysis
            story.append(Paragraph("Financial Impact Analysis", self.styles['SectionHeader']))
            savings = comparisons[0]['estimatedCredit'] - comparisons[-1]['estimatedCredit']
            
            story.append(Paragraph(
                f"<b>Best Financial Option:</b> {best_option['jurisdiction']} offers the highest tax credit of <font color='#28a745'>${best_option['estimatedCredit']:,.0f}</font>, representing {(best_option['estimatedCredit']/budget*100):.1f}% of your total budget.",
                self.styles['BodyJustify']
            ))
            
            if savings > 0:
                story.append(Paragraph(
                    f"<b>Potential Savings:</b> Filming in {best_option['jurisdiction']} saves <font color='#28a745'>${savings:,.0f}</font> compared to the lowest incentive option ({comparisons[-1]['jurisdiction']}). This represents significant additional capital that can be reinvested into production quality.",
                    self.styles['BodyJustify']
                ))
            
            story.append(Spacer(1, 0.2 * inch))
            
            # Strategic Recommendations
            story.append(Paragraph("Strategic Recommendations", self.styles['SectionHeader']))
            
            recommendations = [
                f"<b>Primary Recommendation:</b> Pursue tax credit application in {best_option['jurisdiction']} for maximum financial benefit",
                "<b>Timeline:</b> Begin application process 60-90 days before principal photography",
                "<b>Documentation:</b> Establish detailed expense tracking system from day one",
                "<b>Compliance:</b> Designate production accountant familiar with local requirements",
                f"<b>Backup Plan:</b> Have contingency plans for {comparisons[1]['jurisdiction'] if len(comparisons) > 1 else 'alternative jurisdictions'} if primary application is delayed"
            ]
            
            for rec in recommendations:
                story.append(Paragraph(f"• {rec}", self.styles['BulletPoint']))
            
            story.append(Spacer(1, 0.2 * inch))
            
            # Next Steps
            story.append(Paragraph("Immediate Next Steps", self.styles['SectionHeader']))
            
            next_steps = [
                f"<b>Week 1:</b> Contact {best_option['jurisdiction']} Film Office to request application package",
                "<b>Week 2:</b> Review detailed compliance requirements and eligibility checklist",
                "<b>Week 3:</b> Assemble required documentation (script, budget, production schedule)",
                "<b>Week 4:</b> Submit preliminary application and schedule pre-production meeting",
                "<b>Ongoing:</b> Maintain detailed expense records and comply with all reporting requirements"
            ]
            
            for step in next_steps:
                story.append(Paragraph(f"{step}", self.styles['BulletPoint']))
            
            story.append(Spacer(1, 0.3 * inch))
            
            # Contact Information
            story.append(Paragraph("Key Contacts", self.styles['SectionHeader']))
            story.append(Paragraph(
                f"<b>{best_option['jurisdiction']} Film Office:</b> Contact local film commission for application assistance and compliance guidance. Visit their official website for current contact information and office hours.",
                self.styles['BodyJustify']
            ))
            
            story.append(Spacer(1, 0.2 * inch))
            
            # Disclaimer
            story.append(Paragraph("Disclaimer", self.styles['SectionHeader']))
            story.append(Paragraph(
                "This report provides general guidance based on publicly available information about tax incentive programs. Tax incentive rules and regulations are subject to change. Consult with qualified tax professionals and the specific jurisdiction's film office for current requirements and application procedures. This analysis does not constitute tax or legal advice.",
                self.styles['BodyJustify']
            ))
        
        # Build PDF
        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()


# Create global instance
enhanced_pdf_generator = EnhancedPDFReportGenerator()