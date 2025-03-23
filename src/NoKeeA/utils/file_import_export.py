from pathlib import Path
from bs4 import BeautifulSoup
import io
import base64
from typing import Optional

try:
    import fitz  # PyMuPDF
    PYMUPDF_AVAILABLE = True
except ImportError:
    PYMUPDF_AVAILABLE = False

try:
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, \
        Paragraph, Spacer, Image, PageBreak
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False


def get_supported_extensions():
    """Get list of supported file extensions"""
    extensions = [".txt", ".md"]
    if PYMUPDF_AVAILABLE:  # Only check for PyMuPDF for import
        extensions.append(".pdf")
    return extensions


def import_file(file_path):
    """Import content from a file.

    Args:
        file_path (str): Path to the file to import

    Returns:
        dict: Dictionary containing the imported content and metadata
        {
            "name": str,  # Name of the file without extension
            "content": str,  # Content of the file
            "extension": str  # File extension
        }
    """
    try:
        file_path = Path(file_path)
        if not file_path.exists():
            return None

        extension = file_path.suffix.lower()
        if extension not in get_supported_extensions():
            return None

        name = file_path.stem
        content = ""

        if extension == ".pdf":
            content = import_pdf(file_path)
        elif extension in [".txt", ".md"]:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()

        # Clean up content
        content = clean_content(content, extension)

        return {
            "name": name,
            "content": content,
            "extension": extension
        }
    except Exception as e:
        print(f"Error importing file: {e}")
        return None


def import_pdf(file_path):
    """Import content from a
    PDF file with structure preservation using PyMuPDF.

    Args:
        file_path (Path): Path to the PDF file

    Returns:
        str: HTML content with preserved structure
    """
    if not PYMUPDF_AVAILABLE:
        raise ImportError("PDF import requires PyMuPDF to be installed")

    html_content = []
    doc = fitz.open(file_path)

    for page_num, page in enumerate(doc, 1):
        # Get HTML content with preserved structure
        page_html = page.get_text("html")

        # Extract images
        images = []
        for img_index, img in enumerate(doc.get_page_images(page_num - 1)):
            try:
                xref = img[0]
                pix = fitz.Pixmap(doc, xref)

                # Convert to PNG in memory
                img_buffer = io.BytesIO()
                pix.save(img_buffer, "png")
                img_buffer.seek(0)

                # Convert to base64
                image_base64 = base64.b64encode(img_buffer.getvalue()).decode()
                images.append(
                    f'<img src="data:image/png;base64,{image_base64}" class\
                        ="ql-image" style="max-width: 100%; height: auto;">')

                # Clean up
                pix = None
                img_buffer.close()
            except Exception as e:
                print(f"Error extracting image: {e}")
                continue

        # Add page break
        if page_num > 1:
            html_content.append('<div class="page-break"></div>')

        # Add page content
        html_content.append(f'<div class="page" data-page="{page_num}">')
        html_content.append(page_html)

        # Add images if any were found
        if images:
            for img in images:
                html_content.append(img)
                html_content.append('<br>')

        html_content.append('</div>')

    # Clean up
    doc.close()

    # Combine all pages with proper spacing
    return "\n".join(html_content)


def convert_text_to_html(text: str) -> str:
    """Convert text to HTML with structure preservation"""
    lines = text.split('\n')
    html_lines = []

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Handle headings
        if line.isupper() and len(line) > 3:
            if len(line) < 10:  # Short uppercase lines are likely h1
                html_lines.append(f"<h1>{line}</h1>")
            else:  # Longer uppercase lines are likely h2
                html_lines.append(f"<h2>{line}</h2>")
        # Handle bullet points
        elif line.startswith('•'):
            html_lines.append(f"<li>{line[1:].strip()}</li>")
        # Handle numbered lists
        elif line[0].isdigit() and '. ' in line:
            html_lines.append(f"<li>{line}</li>")
        # Regular paragraphs
        else:
            html_lines.append(f"<p>{line}</p>")

    return '\n'.join(html_lines)


def export_file(content: str, file_path: str) -> Optional[str]:
    """Export content to a file"""
    if not file_path:
        return None

    file_path = Path(file_path)
    extension = file_path.suffix.lower()

    if extension not in get_supported_extensions():
        return None

    try:
        if extension == '.pdf':
            if not REPORTLAB_AVAILABLE:
                return None
            return export_to_pdf(content)
        elif extension == '.txt':
            return content
        elif extension == '.md':
            return convert_html_to_markdown(BeautifulSoup(
                content, 'html.parser')
            )
        else:
            return None
    except Exception as e:
        print(f"Error exporting file: {str(e)}")
        return None


def export_to_pdf(content):
    """Export content to PDF with proper formatting.

    Args:
        content (str): HTML content to export

    Returns:
        bytes: PDF content
    """
    if not REPORTLAB_AVAILABLE:
        raise ImportError("PDF export requires reportlab to be installed")

    # Create a PDF buffer
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=72,
                            leftMargin=72, topMargin=72, bottomMargin=72)
    styles = getSampleStyleSheet()
    story = []

    # Create custom styles
    styles.add(ParagraphStyle(
        name='CustomNormal',
        parent=styles['Normal'],
        fontSize=11,
        leading=14,
        spaceBefore=6,
        spaceAfter=6
    ))

    styles.add(ParagraphStyle(
        name='CustomHeading1',
        parent=styles['Heading1'],
        fontSize=16,
        leading=20,
        spaceBefore=12,
        spaceAfter=6
    ))

    styles.add(ParagraphStyle(
        name='CustomHeading2',
        parent=styles['Heading2'],
        fontSize=14,
        leading=18,
        spaceBefore=10,
        spaceAfter=4
    ))

    # Parse HTML content
    soup = BeautifulSoup(content, 'html.parser')

    # Process each element
    for element in soup.find_all(
        ['h1', 'h2', 'h3', 'p', 'li', 'br', 'div', 'img']
    ):
        if element.name == 'div' and 'page-break' in element.get('class', []):
            story.append(PageBreak())
            continue

        if element.name == 'img':
            try:
                # Extract image data from base64
                img_src = element.get('src', '')
                if img_src.startswith('data:'):
                    img_data = img_src.split(',')[1]
                    img_bytes = base64.b64decode(img_data)

                    # Create a BytesIO object for the image
                    img_buffer = io.BytesIO(img_bytes)

                    # Create ReportLab image directly from the buffer
                    img = Image(img_buffer)
                    page_width = letter[0] - 144  # Account for margins
                    img_width, img_height = img.imageWidth, \
                        img.imageHeight
                    scale = page_width / img_width
                    img.drawWidth = page_width
                    img.drawHeight = img_height * scale

                    story.append(img)
                    story.append(Spacer(1, 12))

                    # Keep the buffer open until the PDF is built
                    img_buffer.seek(0)

            except Exception as e:
                print(f"Error processing image: {e}")
                continue

        text = element.get_text().strip()
        if not text:
            if element.name == 'br':
                story.append(Spacer(1, 12))
            continue

        # Create appropriate style
        if element.name == 'h1':
            style = styles['CustomHeading1']
        elif element.name == 'h2':
            style = styles['CustomHeading2']
        elif element.name == 'h3':
            style = styles['Heading3']
        elif element.name == 'li':
            style = styles['CustomNormal']
            text = f"• {text}"
        else:
            style = styles['CustomNormal']

        # Handle long text by splitting into paragraphs
        paragraphs = text.split('\n')
        for para in paragraphs:
            if para.strip():
                story.append(Paragraph(para.strip(), style))
                story.append(Spacer(1, 6))

    try:
        # Build PDF
        doc.build(story)

        # Get PDF content
        pdf_content = buffer.getvalue()
        buffer.close()

        return pdf_content
    except Exception as e:
        print(f"Error building PDF: {e}")
        buffer.close()
        return None


def clean_content(content: str, extension: str, is_import: bool = True) -> str:
    """Clean content based on file type.

    Args:
        content: The content to clean
        extension: The file extension
        is_import: Whether this is an import
          operation (True) or export/cleanup (False)

    Returns:
        str: The cleaned content
    """
    if extension == ".pdf":
        return content

    if extension == ".md" and is_import:
        return content  # Return Markdown content as is during import

    soup = BeautifulSoup(content, 'html.parser')

    if extension == ".txt":
        # Extract text content without HTML tags
        return soup.get_text(separator='\n', strip=True)
    elif extension == ".md" and not is_import:
        # Convert HTML to Markdown during export/cleanup
        return convert_html_to_markdown(soup)
    else:
        return content


def convert_html_to_markdown(soup):
    """Convert HTML to Markdown format.

    Args:
        soup (BeautifulSoup): Parsed HTML content

    Returns:
        str: Markdown formatted content
    """
    markdown = []

    for element in soup.find_all(['h1', 'h2', 'h3', 'p', 'li', 'br']):
        text = element.get_text().strip()
        if not text:
            continue

        if element.name == 'h1':
            markdown.append(f'# {text}\n')
        elif element.name == 'h2':
            markdown.append(f'## {text}\n')
        elif element.name == 'h3':
            markdown.append(f'### {text}\n')
        elif element.name == 'li':
            markdown.append(f'- {text}\n')
        elif element.name == 'br':
            markdown.append('\n')
        else:
            markdown.append(f'{text}\n\n')

    return ''.join(markdown)
