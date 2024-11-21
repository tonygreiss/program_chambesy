from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
import io

class DocumentGenerator:
    """Handles the generation of church program documents"""
    
    def __init__(self):
        """Initialize the document generator"""
        self.doc = Document()
        self._setup_document()
    
    def _setup_document(self):
        """Configure initial document settings"""
        # Set up margins
        sections = self.doc.sections
        for section in sections:
            section.top_margin = Inches(1)
            section.bottom_margin = Inches(1)
            section.left_margin = Inches(1)
            section.right_margin = Inches(1)
    
    def generate(self, year: int, month: int, dates: list, french_verse: str, arabic_verse: str) -> bytes:
        """
        Generate a church program document
        
        Parameters:
        -----------
        year : int
            The year for the program
        month : int
            The month for the program (1-12)
        dates : list
            List of dates with Synaxaire entries
        french_verse : str
            The verse in French
        arabic_verse : str
            The verse in Arabic
            
        Returns:
        --------
        bytes
            The generated document as bytes
        """
        # Add title
        title = self.doc.add_heading(f'Programme du mois {month}/{year}', 0)
        title.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        # Add verses
        verse_para = self.doc.add_paragraph()
        verse_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        verse_para.add_run(french_verse).bold = True
        verse_para.add_run('\n')
        verse_para.add_run(arabic_verse).bold = True
        
        # Add dates and events
        self.doc.add_heading('Dates importantes:', level=1)
        for date_entry in dates:
            p = self.doc.add_paragraph(style='List Bullet')
            p.add_run(f"{date_entry['date']}: {date_entry['event']}")
        
        # Save to memory buffer
        doc_buffer = io.BytesIO()
        self.doc.save(doc_buffer)
        doc_buffer.seek(0)
        
        return doc_buffer.getvalue() 