
text
# 🎯 Gerber to DXF Converter - GUI Edition

Eine **moderne, benutzerfreundliche Desktop-Anwendung** zur Konvertierung von Gerber-Dateien (`.gbr`) in DXF-Format (`.dxf`) mit grafischer Benutzeroberfläche.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![PyQt6](https://img.shields.io/badge/PyQt6-GUI-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)

## ✨ Features

- 🎨 **Moderne GUI** - Intuitive Benutzeroberfläche mit PyQt6
- 📂 **Dateiauswahl** - Einfacher Dialog zur Auswahl von Gerber-Dateien
- 🔄 **Intelligente Ausgabe** - Automatische Übernahme des Dateinamens und Speicherung im selben Verzeichnis
- 📊 **Live-Protokoll** - Echtzeit-Feedback während der Konvertierung
- ⚙️ **Hintergrund-Verarbeitung** - Non-blocking UI, keine Einfrierungen
- 📐 **Automatische Einheiten** - Konvertierung inch/mil → mm
- 🚀 **Eigenständige App** - PyInstaller-kompilierbar für Windows/macOS/Linux
- 💾 **Robust** - Fehlerbehandlung und aussagekräftige Fehlermeldungen

## 🚀 Quick Start

### Installation

```bash
# Abhängigkeiten installieren
pip install PyQt6 ezdxf

# Anwendung starten
python gerber_to_dxf_gui.py
Verwendung
Klicke auf "📂 GBR-Datei auswählen"

Wähle deine Gerber-Datei aus

Klicke auf "🔄 Konvertieren"

Die DXF-Datei wird automatisch im selben Verzeichnis gespeichert

📦 Als eigenständige EXE kompilieren
bash
# PyInstaller installieren
pip install pyinstaller

# EXE erstellen
pyinstaller --onefile --windowed --exclude-module=PyQt5 gerber_to_dxf_gui.py

# Fertig! Die EXE findest du unter: dist/gerber_to_dxf_gui.exe
Die kompilierte EXE benötigt kein Python und kann überall verteilt werden! 🎉

🛠️ Systemanforderungen
Python: 3.8 oder höher (nur für .py Version)

OS: Windows, macOS, Linux

RAM: Mindestens 512 MB

Speicherplatz: ca. 100 MB (mit Abhängigkeiten)

📋 Abhängigkeiten
Paket	Version	Zweck
PyQt6	≥6.0	GUI Framework
ezdxf	≥1.0	DXF Dateigenerierung
pyinstaller	≥6.0	(Optional) EXE-Kompilierung
🔧 Technische Details
Gerber-Format Support
✅ RS-274X (Extended Gerber)

✅ Aperture Definitionen (Circle, Rectangle)

✅ D01 (Interpolate), D02 (Move), D03 (Flash) Kommandos

✅ Automatische Einheiten-Erkennung

DXF-Ausgabe
✅ AutoCAD 2010 Format (R2010)

✅ Einheiten in Millimetern

✅ Linien und Kreise aus Gerber-Entities

✅ Rechtecke als geschlossene Polylines

💡 Verwendungsbeispiele
bash
# Einfache Verwendung
python gerber_to_dxf_gui.py

# Oder die kompilierte Version
./gerber_to_dxf_gui.exe    # Windows
./gerber_to_dxf_gui.app    # macOS
./gerber_to_dxf_gui        # Linux
🐛 Troubleshooting
PyQt5/PyQt6 Konflikt bei PyInstaller
bash
pip uninstall PyQt5 -y
pip install --upgrade pyinstaller
pyinstaller --onefile --windowed --exclude-module=PyQt5 gerber_to_dxf_gui.py
Module nicht gefunden
bash
pip install --upgrade PyQt6 ezdxf
DXF-Datei lässt sich nicht öffnen
Überprüfe, dass die GBR-Datei valides Gerber-Format hat

Schau in das Protokoll-Fenster für Fehlermeldungen

Versuche die Datei in LibreCAD oder einem anderen CAD-Programm zu öffnen

📖 Dokumentation
Code-Struktur
GerberParser - Parst Gerber RS-274X Dateien

DXFConverter - Konvertiert geparste Entities zu DXF

GerberConverterGUI - PyQt6 GUI mit Thread-Support

WorkerSignals - Signal-System für Hintergrund-Verarbeitung

Erweitern des Codes
Neue Aperture-Shapes hinzufügen in DXFConverter.add_flash():

python
elif aperture['shape'] == 'P':  # Polygon
    sides = int(aperture['params'])
    # Implementiere Polygon-Handling
🤝 Beiträge
Beiträge sind willkommen!

Mögliche Verbesserungen:

 Mehrfach-Datei-Konvertierung

 Batch-Processing

 Vorschau der Konvertierung

 Support für weitere Aperture-Shapes

 Layer-Management

 3D-Visualisierung

💰 Unterstütze das Projekt
Gefällt dir dieses Projekt? Du kannst mich gerne unterstützen! Jede Spende hilft bei der Weiterentwicklung und verbesserter Unterstützung. 🙏

🎁 Spende-Optionen
Plattform	Beschreibung
☕ Ko-fi	Kleine schnelle Spende - perfekt für einen Kaffee ☕
❤️ Buy Me a Coffee	Regelmäßige Unterstützung - für Entwickler, von Entwicklern
🌍 GoFundMe	Größere Spendenkampagne für spezielle Features
💳 PayPal	Direkte und sichere Überweisung
🪙 Crypto	Bitcoin -> 
⭐ GitHub Sponsor	Werde GitHub Sponsor und erhalte exklusive Vorteile!
💡 Wofür deine Spende genutzt wird:
🔧 Weiterentwicklung - Neue Features und Aperture-Shapes (Polygon, Oval, etc.)

🐛 Bug-Fixes - Schnellere und prioritäre Fehlerbehebung

📚 Dokumentation - Bessere Guides, Video-Tutorials und API-Dokumentation

🌐 Community Support - Schnellere Antworten auf Issues und Support

🚀 Performance - Optimierung für große Dateien und Batch-Processing

🎨 UI/UX Verbesserungen - Noch bessere Benutzeroberfläche und User Experience

🧪 Testing - Umfangreichere Unit-Tests und Quality Assurance

📦 Distribution - Kostenlose Windows/macOS/Linux Build-Server

🌟 Sponsorship-Vorteile
Mit einer Spende erhältst du:

✅ Deinen Namen im README (Gold/Platinum Sponsor)

✅ Early Access zu neuen Features

✅ Persönlichen Support

✅ Danksagung in den Release Notes

✅ Badge auf deinem GitHub Profil (GitHub Sponsor)

🏆 Sponsoren & Unterstützer
Vielen Dank an alle, die dieses Projekt unterstützen! ❤️

🥇 Platinsponsoren ($500+):

(Dein Name hier! 👑)

🥈 Goldsponsoren ($100+):

(Bald hier verfügbar 🎯)

🥉 Silbersponsoren ($25+):

(Community Heroes)

Community Supporter:

Du? 😊 Jede noch so kleine Spende zählt!

📧 Support & Fragen
Hast du Fragen oder Probleme?

🐛 Öffne ein Issue

💬 Schau in den Discussions Bereich

📖 Lies die FAQ

🎯 Kontaktiere mich direkt

📝 Lizenz
MIT License - Frei verwendbar für private und kommerzielle Projekte.

text
MIT License

Copyright (c) 2026

Hiermit wird jeder Person, die eine Kopie dieser Software 
und der zugehörigen Dokumentationsdateien erhält, 
hierdurch kostenlos die Nutzung dieser Software ohne 
Einschränkung gestattet...
🙏 Danksagungen
PyQt6 - Für die großartige GUI-Library

ezdxf - Für die robuste DXF-Dateigenerierung

PyInstaller - Für die Möglichkeit, eigenständige Executables zu erstellen

Community - Für die Unterstützung und das Feedback

📊 Project Stats
⭐ Stars: ?

🔀 Forks: ?

👀 Watchers: ?

📥 Downloads: ?

💰 Gesamt gespendete: $0 (Hilf uns, das zu ändern! 🚀)

Viel Spaß beim Konvertieren! 🚀

Made with ❤️ für Elektronik-Enthusiasten und PCB-Designer

⬆ zurück nach oben
