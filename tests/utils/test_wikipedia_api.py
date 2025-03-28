from unittest.mock import patch, Mock
from NoKeeA.utils.wikipedia_api import get_wikipedia_summary
import wikipedia
import pytest


def test_get_wikipedia_summary_success():
    """Test successful Wikipedia article retrieval."""
    with patch('wikipedia.page') as mock_page, patch('wikipedia.summary') as mock_summary:
        mock_page.return_value = Mock(url="https://test.com")
        mock_summary.return_value = "This is a test article about Python programming."

        result = get_wikipedia_summary("Python")

        assert result is not None
        assert isinstance(result, dict)
        assert "summary" in result
        assert "url" in result
        assert "Python programming" in result["summary"]
        assert result["url"] == "https://test.com"

        mock_summary.assert_called_once_with("Python", sentences=3)


def test_get_wikipedia_summary_disambiguation():
    """Test disambiguation error when the term is ambiguous."""
    with patch('wikipedia.page') as mock_page:
        mock_page.side_effect = wikipedia.exceptions.DisambiguationError(
            "Test", ["Option1", "Option2", "Option3"])

        result = get_wikipedia_summary("AmbiguousTerm")

        assert result is not None
        assert isinstance(result, dict)
        assert "error" in result
        assert "Mehrdeutiger Begriff" in result["error"]
        assert "Option1" in result["error"]


def test_get_wikipedia_summary_page_error():
    """Test page error when the article does not exist."""
    with patch('wikipedia.page') as mock_page:
        mock_page.side_effect = wikipedia.exceptions.PageError(
            "NonexistentArticle123")

        result = get_wikipedia_summary("NonexistentArticle123")

        assert result is not None
        assert isinstance(result, dict)
        assert "error" in result
        assert "Kein Wikipedia-Eintrag gefunden." in result["error"]


def test_get_wikipedia_summary_empty_query():
    """Test behavior when searching with an empty query string."""
    with pytest.raises(wikipedia.exceptions.WikipediaException):
        get_wikipedia_summary("")
