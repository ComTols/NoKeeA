import json
from pathlib import Path
from typing import Optional, Dict, List

# Define the notes directory
NOTES_DIR = Path.home() / "NoKeeA_Notes"


def ensure_notes_directory() -> None:
    """Ensure the notes directory exists"""
    NOTES_DIR.mkdir(parents=True, exist_ok=True)


def save_note(name: str, content: str) -> bool:
    """
    Save a note with the given name and content.

    Args:
        name: The name of the note (without file extension)
        content: The content of the note

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        ensure_notes_directory()

        # Create parent directories if they don't exist
        note_path = NOTES_DIR / f"{name}.json"
        note_path.parent.mkdir(parents=True, exist_ok=True)

        note_data = {
            "name": name,
            "content": content,
            "last_modified": str(note_path.stat().st_mtime)
            if note_path.exists() else None
        }

        with open(note_path, 'w', encoding='utf-8') as f:
            json.dump(note_data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Error saving note: {str(e)}")
        return False


def load_note(name: str) -> Optional[Dict]:
    """
    Load a note with the given name.

    Args:
        name: The name of the note (without file extension)

    Returns:
        Optional[Dict]: The note data if found, None otherwise
    """
    try:
        note_path = NOTES_DIR / f"{name}.json"
        if not note_path.exists():
            return None

        with open(note_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading note: {str(e)}")
        return None


def delete_note(name: str) -> bool:
    """
    Delete a note with the given name.

    Args:
        name: The name of the note (without file extension)

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        note_path = NOTES_DIR / f"{name}.json"
        if note_path.exists():
            note_path.unlink()
            return True
        return False
    except Exception as e:
        print(f"Error deleting note: {str(e)}")
        return False


def list_notes() -> List[str]:
    """
    List all available notes.

    Returns:
        List[str]: List of note names
    """
    try:
        ensure_notes_directory()
        return [f.stem for f in NOTES_DIR.glob("**/*.json")]
    except Exception as e:
        print(f"Error listing notes: {str(e)}")
        return []
