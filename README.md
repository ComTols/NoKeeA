# NoKeeA - Eine moderne Notiz-App mit KI-Funktionen

NoKeeA ist eine moderne Notiz-Anwendung mit erweiterten KI-Funktionen. Die App kombiniert klassische Notizfunktionen mit fortschrittlichen KI-Fähigkeiten wie Video-zu-Text-Konvertierung und automatischer Bildbeschreibung.

## Features

### Notiz-Funktionen
- 📝 Rich Text Editor mit umfangreichen Formatierungsoptionen
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

### Lokale Installation

1. Klonen Sie das Repository:
   ```bash
   git clone https://github.com/ComTols/NoKeeA.git
   cd NoKeeA
   ```

2. Erstellen Sie eine virtuelle Umgebung:
   ```bash
   python -m venv venv
   # Unter Windows:
   .\venv\Scripts\activate
   # Unter Linux/Mac:
   source venv/bin/activate
   ```

3. Installieren Sie die Abhängigkeiten:
   ```bash
   pip install -r requirements.txt
   ```

4. Starten Sie die Anwendung:
   ```bash
   streamlit run src/NoKeeA/main.py
   ```
   alternativ mit "poetry run ..."

### Docker-Installation

1. Bauen Sie das Docker-Image:
   ```bash
   docker build -t nokeea .
   ```

2. Starten Sie den Container:
   ```bash
   docker run -p 8501:8501 nokeeA
   ```

3. Öffnen Sie die Anwendung im Browser:
   ```
   http://localhost:8501
   ```

## Verwendung

### Notizen verwalten

1. **Neue Notiz erstellen**:
   - Klicken Sie auf "📝 Neue Notiz" in der Seitenleiste
   - Geben Sie einen Namen ein
   - Beginnen Sie mit der Bearbeitung

2. **Notizen bearbeiten**:
   - Nutzen Sie den Rich Text Editor für Formatierung
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

## Entwicklung

### Projektstruktur
