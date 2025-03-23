import pytest
import tempfile
from NoKeeA.utils.file_operations import save_note, \
    load_note, delete_note, list_notes


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files"""
    with tempfile.TemporaryDirectory() as tmpdirname:
        yield tmpdirname


def test_save_and_load_note(temp_dir):
    """Test saving and loading a note"""
    # Setup
    note_name = "test_note"
    note_content = "Test content"

    # Save note
    success = save_note(note_name, note_content)
    assert success

    # Load note
    loaded_note = load_note(note_name)
    assert loaded_note is not None
    assert loaded_note["name"] == note_name
    assert loaded_note["content"] == note_content


def test_save_note_with_special_chars(temp_dir):
    """Test saving a note with special characters in name"""
    note_name = "test/note/with/slashes"
    note_content = "Test content"

    success = save_note(note_name, note_content)
    assert success

    loaded_note = load_note(note_name)
    assert loaded_note is not None
    assert loaded_note["content"] == note_content


def test_load_nonexistent_note():
    """Test loading a nonexistent note"""
    result = load_note("nonexistent_note")
    assert result is None


def test_delete_note(temp_dir):
    """Test deleting a note"""
    # Setup
    note_name = "test_note"
    note_content = "Test content"
    save_note(note_name, note_content)

    # Delete note
    success = delete_note(note_name)
    assert success

    # Verify note is deleted
    loaded_note = load_note(note_name)
    assert loaded_note is None


def test_delete_nonexistent_note():
    """Test deleting a nonexistent note"""
    success = delete_note("nonexistent_note")
    assert not success


def test_list_notes(temp_dir):
    """Test listing notes"""
    # Create some test notes
    notes = ["note1", "note2", "note3"]
    for note in notes:
        save_note(note, f"Content for {note}")

    # List notes
    available_notes = list_notes()
    assert len(available_notes) >= len(notes)
    for note in notes:
        assert note in available_notes


def test_save_note_with_empty_content(temp_dir):
    """Test saving a note with empty content"""
    note_name = "empty_note"
    note_content = ""

    success = save_note(note_name, note_content)
    assert success

    loaded_note = load_note(note_name)
    assert loaded_note is not None
    assert loaded_note["content"] == ""


def test_save_note_with_unicode_content(temp_dir):
    """Test saving a note with unicode content"""
    note_name = "unicode_note"
    note_content = "Test content with unicode: äöüß"

    success = save_note(note_name, note_content)
    assert success

    loaded_note = load_note(note_name)
    assert loaded_note is not None
    assert loaded_note["content"] == note_content
