# NoKeeA - Eine moderne Notiz-App mit KI-Funktionen

NoKeeA ist eine moderne Notiz-Anwendung mit erweiterten KI-Funktionen. Die App kombiniert klassische Notizfunktionen mit
fortschrittlichen KI-Fähigkeiten wie Video-zu-Text-Konvertierung und automatischer Bildbeschreibung.

## Features

### Notiz-Funktionen

- 📝 Rich-Text-Editor mit umfangreichen Formatierungsoptionen
- 🔍 Wikipedia-Integration für schnelle Recherchen
- 💾 Automatisches Speichern von Notizen
- 📤 Import/Export von Notizen in verschiedenen Formaten
- 🎨 Moderne, benutzerfreundliche Oberfläche

### KI-Funktionen

- 🎥 Video-zu-Text-Konvertierung mit Whisper
- 📸 Automatische Bildbeschreibung mit BLIP
- 🔍 Texterkennung in Bildern mit Tesseract
- 🤖 KI-gestützte Zusammenfassungen mit DeepSeek
- 🎯 Intelligente Frame-Extraktion aus Videos

## Installation

### Docker (empfohlen)

Um die Anwendung in Docker auszuführen, verwende folgenden Befehl:
> [!CAUTION]
> Beim Ausführen ohne die Umgebungsvariable `OPENAI_API_KEY` wird das DeepSeek Model heruntergeladen!
> Das setzt extrem viel Festplattenspeicher und RAM voraus!

```bash
docker run -p 8501:8501 comtols/nokeea:latest
```

Dies startet einen Docker-Container mit der aktuell stable Version.
Das Image umfasst ca. 15 GB. Enthalten sind die basic KI-Modelle.
Beim Starten des Containers wird das `Blip2` Model nachgeladen.
Dies umfasst weitere 10 GB. Es ist entsprechender Festplattenspeicher nötig.

Das Image ist mit Nvidia Treibern ausgestattet, um Hardwarebeschleunigung zu unterstützen.
Es wird empfohlen, diese zu verwenden.
Eventuell muss der Docker-Host mit den Erweiterungen entsprechend dem Host-Betriebssystem erweitert werden.

Um einen Openai-API Key zu verwenden, starte den Container mit der entsprechenden Umgebungsvariable:

```bash
docker run -p 8501:8501 -e OPENAI_API_KEY=<key> comtols/nokeea:latest
```

### Lokale Umgebung

Das Projekt unterstützt die Paketverwaltung `poetry`. Es wird empfohlen, diese zu verwenden.
Für genauere Informationen zur Installation von `poetry`, lies bitte in
der [Dokumentation](https://python-poetry.org/docs/#installation) nach.

Es wird Python in der Version `3.9.9` vorausgesetzt. Installiere die entsprechende Python version und passe dein
`poetry`-Umgebung entsprechend an.

```bash
poetry env use /full/path/to/python
```

Nach dem Einrichten von `poetry` musst du im Projektordner lediglich die Abhängigkeiten installieren.

```bash
poetry install
```

Nun kannst du das Programm starten:

```bash
poetry run streamlit run src/NoKeeA/UI/streamlit_ui.py
```

## Verwendung

### Notizen verwalten

1. **Neue Notiz erstellen**:
    - Klicken Sie auf "📝 Neue Notiz" in der Seitenleiste
    - Geben Sie einen Namen ein
    - Beginnen Sie mit der Bearbeitung

2. **Notizen bearbeiten**:
    - Nutzen Sie den Rich-Text-Editor für Formatierung
    - Fügen Sie Bilder, Links und Code-Blöcke ein
    - Ihre Änderungen werden automatisch gespeichert

3. **Notizen importieren/exportieren**:
    - Nutzen Sie den Datei-Upload in der Seitenleiste
    - Wählen Sie das Export-Format (TXT, MD, PDF)
    - Klicken Sie auf "📥 Exportieren"

### KI-Funktionen nutzen

1. **Video-zu-Text-Konvertierung**:
    - Laden Sie ein Video hoch
    - Warten Sie auf die Verarbeitung
    - Die Transkription wird automatisch in Ihre Notiz eingefügt

2. **Bildbeschreibung**:
    - Laden Sie ein Bild hoch
    - Die KI generiert automatisch eine Beschreibung
    - Die Beschreibung wird in Ihre Notiz eingefügt

3. **Texterkennung**:
    - Laden Sie ein Bild mit Text hoch
    - Der Text wird automatisch erkannt und extrahiert
