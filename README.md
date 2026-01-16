🎯 Gerber to DXF Converter - GUI Edition
Eine moderne, benutzerfreundliche Desktop-Anwendung zur Konvertierung von Gerber-Dateien (.gbr) in DXF-Format (.dxf) mit grafischer Benutzeroberfläche.

Python
PyQt6
License
Status

✨ Features
🎨 Moderne GUI - Intuitive Benutzeroberfläche mit PyQt6

📂 Dateiauswahl - Einfacher Dialog zur Auswahl von Gerber-Dateien

🔄 Intelligente Ausgabe - Automatische Übernahme des Dateinamens und Speicherung im selben Verzeichnis

📊 Live-Protokoll - Echtzeit-Feedback während der Konvertierung

⚙️ Hintergrund-Verarbeitung - Non-blocking UI, keine Einfrierungen

📐 Automatische Einheiten - Konvertierung inch/mil → mm

🚀 Eigenständige App - PyInstaller-kompilierbar für Windows/macOS/Linux

💾 Robust - Fehlerbehandlung und aussagekräftige Fehlermeldungen

🚀 Quick Start
Installation
bash
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

📝 Lizenz
MIT License - Frei verwendbar für private und kommerzielle Projekte.

text
MIT License

Copyright (c) 2026

Hiermit wird jeder Person, die eine Kopie dieser Software 
und der zugehörigen Dokumentationsdateien erhält, 
hierdurch kostenlos die Nutzung dieser Software ohne 
Einschränkung gestattet, einschließlich...
🙏 Danksagungen
PyQt6 - Für die großartige GUI-Library

ezdxf - Für die robuste DXF-Dateigenerierung

PyInstaller - Für die Möglichkeit, eigenständige Executables zu erstellen

📧 Support & Fragen
Hast du Fragen oder Probleme?

Öffne ein Issue

Schau in den Discussions Bereich

Lies die FAQ

📊 Project Stats
⭐ Stars: ?

🔀 Forks: ?

👀 Watchers: ?

📥 Downloads: ?

Viel Spaß beim Konvertieren! 🚀

Made with ❤️ für Elektronik-Enthusiasten und PCB-Designer
