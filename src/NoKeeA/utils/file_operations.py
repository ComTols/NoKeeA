import json
from pathlib import Path

# Konstanten
NOTES_DIR = Path.home() / "NoKeeA_Notes"


def ensure_notes_directory():
    """Stellt sicher, dass das Notiz-Verzeichnis existiert."""
    if not NOTES_DIR.exists():
        NOTES_DIR.mkdir(parents=True)


def save_note(name: str, content: str) -> None:
    """
    Speichert eine Notiz mit dem gegebenen Namen und Inhalt.

    Args:
        name: Der Name der Notiz (ohne Dateiendung)
        content: Der Inhalt der Notiz

    Raises:
        IOError: Wenn die Notiz nicht gespeichert werden konnte
    """
    ensure_notes_directory()
    note_path = NOTES_DIR / f"{name}.json"

    note_data = {
        "name": name,
        "content": content,
        "last_modified": str(Path(
            note_path
        ).stat().st_mtime) if note_path.exists() else None
    }

    try:
        with open(note_path, 'w', encoding='utf-8') as f:
            json.dump(note_data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        raise IOError(f"Fehler beim Speichern der Notiz: {str(e)}")


def delete_note(name: str) -> bool:
    """
    Löscht eine Notiz mit dem gegebenen Namen.

    Args:
        name: Der Name der Notiz (ohne Dateiendung)

    Returns:
        bool: True wenn die Notiz gelöscht wurde,
        False wenn sie nicht existierte
    """
    note_path = NOTES_DIR / f"{name}.json"
    if note_path.exists():
        note_path.unlink()
        return True
    return False


def load_note(name: str) -> dict:
    """
    Lädt eine Notiz mit dem gegebenen Namen.

    Args:
        name: Der Name der Notiz (ohne Dateiendung)

    Returns:
        dict: Ein Dictionary mit den Notiz-Daten (name, content, last_modified)

    Raises:
        FileNotFoundError: Wenn die Notiz nicht gefunden wurde
    """
    note_path = NOTES_DIR / f"{name}.json"
    if not note_path.exists():
        raise FileNotFoundError(f"Notiz '{name}' nicht gefunden")

    with open(note_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def list_notes() -> list:
    """
    Listet alle verfügbaren Notizen auf.

    Returns:
        list: Eine Liste der Notiz-Namen (ohne Dateiendung)
    """
    ensure_notes_directory()
    return [f.stem for f in NOTES_DIR.glob("*.json")]
