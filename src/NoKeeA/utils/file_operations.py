import json
from pathlib import Path
from typing import Optional, Dict, List

# Define the notes directory
NOTES_DIR = Path.home() / "NoKeeA_Notes"


def ensure_notes_directory() -> None:
    """Ensure the notes directory exists in the user's home directory.

    This function creates the NoKeeA_Notes directory if it doesn't already exist.
    The directory is created with all necessary parent directories.

    Returns:
        None: The function creates the directory but does not return any values.

    Note:
        The notes directory is created in the user's home directory under
        the name 'NoKeeA_Notes'. This is the central location for storing
        all application notes.
    """
    NOTES_DIR.mkdir(parents=True, exist_ok=True)


def save_note(name: str, content: str) -> bool:
    """Save a note with the given name and content to the filesystem.

    This function saves a note as a JSON file in the notes directory. The note
    is stored with metadata including the name, content, and last modification time.

    Args:
        name (str): The name of the note (without file extension)
        content (str): The content of the note to be saved

    Returns:
        bool: True if the note was successfully saved, False if an error occurred

    Note:
        - The note is saved as a JSON file with UTF-8 encoding
        - The file is created in the NoKeeA_Notes directory
        - If the note already exists, its last_modified timestamp is preserved
        - Any errors during saving are logged to the console
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
    """Load a note with the given name from the filesystem.

    This function retrieves a note from the notes directory and returns its
    contents as a dictionary containing the note's metadata and content.

    Args:
        name (str): The name of the note to load (without file extension)

    Returns:
        Optional[Dict]: A dictionary containing the note data if found, None if
                       the note doesn't exist or if an error occurred. The dictionary
                       includes:
                       - name: The name of the note
                       - content: The note's content
                       - last_modified: Timestamp of last modification

    Note:
        - The function attempts to load the note as a JSON file
        - If the note doesn't exist or can't be loaded, None is returned
        - Any errors during loading are logged to the console
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
    """Delete a note with the given name from the filesystem.

    This function removes a note file from the notes directory if it exists.

    Args:
        name (str): The name of the note to delete (without file extension)

    Returns:
        bool: True if the note was successfully deleted or didn't exist,
              False if an error occurred during deletion

    Note:
        - The function only deletes the note if it exists
        - If the note doesn't exist, the function returns True (as the desired
          state is achieved)
        - Any errors during deletion are logged to the console
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
    """List all available notes in the notes directory.

    This function retrieves a list of all note names from the NoKeeA_Notes
    directory, including notes in subdirectories.

    Returns:
        List[str]: A list of note names (without file extensions). If an error
                  occurs, an empty list is returned.

    Note:
        - The function searches recursively through all subdirectories
        - Only files with the .json extension are considered as notes
        - The returned names do not include the file extension
        - If an error occurs during listing, an empty list is returned
        - Any errors during listing are logged to the console
    """
    try:
        ensure_notes_directory()
        return [f.stem for f in NOTES_DIR.glob("**/*.json")]
    except Exception as e:
        print(f"Error listing notes: {str(e)}")
        return []
