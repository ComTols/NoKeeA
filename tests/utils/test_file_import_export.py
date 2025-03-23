import pytest
import tempfile
from pathlib import Path
import base64
from PIL import Image
import io
from NoKeeA.utils.file_import_export import\
    import_file, export_file, get_supported_extensions, convert_text_to_html, \
    convert_html_to_markdown, clean_content
from bs4 import BeautifulSoup
from unittest.mock import patch


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files"""
    with tempfile.TemporaryDirectory() as tmpdirname:
        yield tmpdirname


@pytest.fixture
def sample_image():
    """Create a sample image for testing"""
    img = Image.new('RGB', (100, 100), color='red')
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    return buffer.getvalue()


def test_get_supported_extensions():
    """Test getting supported file extensions"""
    extensions = get_supported_extensions()
    assert '.txt' in extensions
    assert '.md' in extensions
    assert '.pdf' in extensions


def test_import_txt_file(temp_dir):
    """Test importing a text file"""
    # Create test file
    test_content = "Test content\nLine 2"
    test_file = Path(temp_dir) / "test.txt"
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write(test_content)

    # Import file
    result = import_file(str(test_file))
    assert result is not None
    assert result["name"] == "test"
    assert result["content"] == test_content
    assert result["extension"] == ".txt"


def test_import_md_file(temp_dir):
    """Test importing a markdown file"""
    test_content = "# Test\n## Subtitle\nContent"
    test_file = Path(temp_dir) / "test.md"

    # Write test content
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write(test_content)

    # Import file
    result = import_file(str(test_file))
    assert result is not None
    assert result["name"] == "test"
    assert result["extension"] == ".md"
    assert result["content"] == test_content


def test_import_nonexistent_file():
    """Test importing a nonexistent file"""
    result = import_file("nonexistent.txt")
    assert result is None


def test_import_unsupported_file(temp_dir):
    """Test importing an unsupported file type"""
    test_file = Path(temp_dir) / "test.xyz"
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write("Test content")

    result = import_file(str(test_file))
    assert result is None


def test_export_txt_file(temp_dir):
    """Test exporting to a text file"""
    test_content = "Test content\nLine 2"
    test_file = Path(temp_dir) / "export.txt"

    # Export content
    export_content = export_file(test_content, str(test_file))
    assert export_content is not None

    # Write content to file
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write(export_content)

    # Verify file content
    with open(test_file, 'r', encoding='utf-8') as f:
        assert f.read() == test_content


def test_export_md_file(temp_dir):
    """Test exporting to a markdown file"""
    test_content = "<h1>Test</h1><h2>Subtitle</h2><p>Content</p>"
    test_file = Path(temp_dir) / "export.md"

    # Export content
    export_content = export_file(test_content, str(test_file))
    assert export_content is not None

    # Write content to file
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write(export_content)

    # Verify file content
    with open(test_file, 'r', encoding='utf-8') as f:
        assert f.read() == "# Test\n## Subtitle\nContent\n\n"


def test_export_pdf_with_images(temp_dir, sample_image):
    """Test exporting to PDF with images"""
    # Create HTML content with an image
    img_base64 = base64.b64encode(sample_image).decode()
    test_content = f"""
    <h1>Test PDF</h1>
    <p>This is a test paragraph.</p>
    <img src="data:image/png;base64,{img_base64}" class="ql-image">
    <p>Another paragraph after the image.</p>
    """

    # Export to PDF
    pdf_content = export_file(test_content, "test.pdf")
    assert pdf_content is not None

    # Save PDF for verification
    test_file = Path(temp_dir) / "test.pdf"
    with open(test_file, 'wb') as f:
        f.write(pdf_content)

    # Verify PDF exists and has content
    assert test_file.exists()
    assert test_file.stat().st_size > 0


def test_export_unsupported_file(temp_dir):
    """Test exporting to an unsupported file type"""
    test_content = "Test content"
    test_file = Path(temp_dir) / "export.xyz"

    # Export content
    success = export_file(test_content, str(test_file))
    assert success is None


def test_export_to_nonexistent_directory():
    """Test exporting to a nonexistent directory"""
    test_content = "Test content"
    test_file = "nonexistent/dir/export.txt"

    # Export content
    success = export_file(test_content, test_file)
    # Should still return content even if directory doesn't exist
    assert success is not None


def test_convert_text_to_html():
    """Test converting text to HTML with structure preservation"""
    text = """HEADING
    SUBHEADING
    • List item 1
    • List item 2
    1. Numbered item 1
    2. Numbered item 2
    Regular paragraph
    """

    html = convert_text_to_html(text)
    assert "<h1>HEADING</h1>" in html
    assert "<h2>SUBHEADING</h2>" in html
    assert "<li>List item 1</li>" in html
    assert "<li>List item 2</li>" in html
    assert "<li>1. Numbered item 1</li>" in html
    assert "<li>2. Numbered item 2</li>" in html
    assert "<p>Regular paragraph</p>" in html


def test_convert_html_to_markdown():
    """Test converting HTML to Markdown"""
    html = """
    <h1>Test Heading</h1>
    <h2>Subheading</h2>
    <p>Regular paragraph</p>
    <li>List item</li>
    <br>
    """

    markdown = convert_html_to_markdown(BeautifulSoup(html, 'html.parser'))
    assert "# Test Heading" in markdown
    assert "## Subheading" in markdown
    assert "Regular paragraph" in markdown
    assert "- List item" in markdown


def test_clean_content_with_html():
    """Test cleaning HTML content"""
    html_content = """
    <h1>Test</h1>
    <p>Content</p>
    """

    # Test cleaning for different file types
    txt_content = clean_content(html_content, ".txt", is_import=False)
    assert txt_content == "Test\nContent"

    md_content = clean_content(html_content, ".md", is_import=False)
    assert md_content == "# Test\nContent\n\n"

    pdf_content = clean_content(html_content, ".pdf", is_import=False)
    assert pdf_content == html_content


def test_export_pdf_without_reportlab():
    """Test PDF export when reportlab is not available"""
    with patch("NoKeeA.utils.file_import_export.REPORTLAB_AVAILABLE", False):
        test_content = "<h1>Test</h1>"
        result = export_file(test_content, "test.pdf")
        assert result is None
