#!/usr/bin/env python3
"""
Gerber to DXF Converter - GUI Version
Konvertiert Gerber-Dateien (.gbr) in DXF-Format (.dxf)
Mit grafischer Benutzeroberfläche für einfache Bedienung
"""

import sys
import re
from pathlib import Path
from typing import Dict
from threading import Thread
import ezdxf
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QFileDialog, QLabel, QProgressBar, QTextEdit,
    QMessageBox, QGroupBox, QLineEdit
)
from PyQt6.QtCore import Qt, pyqtSignal, QObject
from PyQt6.QtGui import QFont, QIcon, QColor, QTextCursor


class WorkerSignals(QObject):
    """Signale für Hintergrund-Konvertierung"""
    finished = pyqtSignal()
    error = pyqtSignal(str)
    progress = pyqtSignal(str)
    success = pyqtSignal(str)


class GerberParser:
    """Parser fuer Gerber RS-274X Dateien"""
    
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.apertures: Dict[int, dict] = {}
        self.current_aperture = None
        self.current_x = 0.0
        self.current_y = 0.0
        self.unit_scale = 1.0
        self.unit_name = "mm"
        self.format_spec = {'x_int': 3, 'x_dec': 4, 'y_int': 3, 'y_dec': 4}
        self.entities = []
        
    def parse_coordinate(self, coord_str: str, axis: str) -> float:
        """Koordinate gemaess Format-Spezifikation parsen"""
        if not coord_str:
            return self.current_x if axis == 'X' else self.current_y
        
        int_digits = self.format_spec[f'{axis.lower()}_int']
        dec_digits = self.format_spec[f'{axis.lower()}_dec']
        total_digits = int_digits + dec_digits
        
        sign = 1
        if coord_str.startswith('+') or coord_str.startswith('-'):
            sign = -1 if coord_str[0] == '-' else 1
            coord_str = coord_str[1:]
        
        coord_str = coord_str.zfill(total_digits)
        value = int(coord_str) / (10 ** dec_digits)
        return sign * value * self.unit_scale
    
    def parse_aperture_definition(self, line: str):
        """Aperture-Definitionen parsen"""
        match = re.match(r'%ADD(\d+)([A-Z]),([\d.X]+)\*%', line)
        if match:
            d_code = int(match.group(1))
            shape = match.group(2)
            params = match.group(3).split('X')
            
            aperture = {
                'shape': shape,
                'params': [float(p) * self.unit_scale for p in params]
            }
            self.apertures[d_code] = aperture
    
    def parse_format_spec(self, line: str):
        """Format-Spezifikation parsen"""
        match = re.match(r'%FSLAX(\d)(\d)Y(\d)(\d)\*%', line)
        if match:
            self.format_spec = {
                'x_int': int(match.group(1)),
                'x_dec': int(match.group(2)),
                'y_int': int(match.group(3)),
                'y_dec': int(match.group(4))
            }
    
    def parse_unit(self, line: str):
        """Einheit parsen und Skalierung setzen"""
        if '%MOMM*%' in line:
            self.unit_scale = 1.0
            self.unit_name = "mm"
        elif '%MOIN*%' in line:
            self.unit_scale = 25.4
            self.unit_name = "inch (-> mm)"
    
    def parse_operation(self, line: str):
        """Operationen parsen (D01, D02, D03)"""
        x_match = re.search(r'X([+-]?\d+)', line)
        y_match = re.search(r'Y([+-]?\d+)', line)
        
        new_x = self.parse_coordinate(x_match.group(1), 'X') if x_match else self.current_x
        new_y = self.parse_coordinate(y_match.group(1), 'Y') if y_match else self.current_y
        
        if 'D01*' in line:
            self.entities.append({
                'type': 'LINE',
                'start': (self.current_x, self.current_y),
                'end': (new_x, new_y),
                'aperture': self.current_aperture
            })
        elif 'D02*' in line:
            pass
        elif 'D03*' in line:
            self.entities.append({
                'type': 'FLASH',
                'position': (new_x, new_y),
                'aperture': self.current_aperture
            })
        
        self.current_x = new_x
        self.current_y = new_y
    
    def parse_aperture_select(self, line: str):
        """Aperture-Auswahl parsen"""
        match = re.match(r'D(\d+)\*', line)
        if match:
            d_code = int(match.group(1))
            if d_code >= 10:
                self.current_aperture = d_code
    
    def parse(self):
        """Gerber-Datei vollstaendig parsen"""
        with open(self.filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                
                if line.startswith('%FSLAX'):
                    self.parse_format_spec(line)
                elif line.startswith('%MO'):
                    self.parse_unit(line)
                elif line.startswith('%ADD'):
                    self.parse_aperture_definition(line)
                elif re.match(r'D\d+\*', line):
                    self.parse_aperture_select(line)
                elif re.search(r'[XY][+-]?\d+', line):
                    self.parse_operation(line)
        
        return self.entities


class DXFConverter:
    """Konverter von Gerber zu DXF"""
    
    def __init__(self, gerber_parser: GerberParser):
        self.parser = gerber_parser
        self.doc = ezdxf.new('R2010')
        self.msp = self.doc.modelspace()
        self.doc.header['$INSUNITS'] = 4
    
    def convert(self):
        """Konvertierung durchfuehren"""
        for entity in self.parser.entities:
            if entity['type'] == 'LINE':
                self.add_line(entity)
            elif entity['type'] == 'FLASH':
                self.add_flash(entity)
    
    def add_line(self, entity: dict):
        """Linie zum DXF hinzufuegen"""
        start = entity['start']
        end = entity['end']
        self.msp.add_line(start, end)
    
    def add_flash(self, entity: dict):
        """Flash (Pad) zum DXF hinzufuegen"""
        pos = entity['position']
        aperture_code = entity['aperture']
        
        if aperture_code and aperture_code in self.parser.apertures:
            aperture = self.parser.apertures[aperture_code]
            
            if aperture['shape'] == 'C':
                radius = aperture['params'][0] / 2.0
                self.msp.add_circle(pos, radius)
            elif aperture['shape'] == 'R':
                width = aperture['params'][0]
                height = aperture['params'][1] if len(aperture['params']) > 1 else width
                
                x, y = pos
                points = [
                    (x - width/2, y - height/2),
                    (x + width/2, y - height/2),
                    (x + width/2, y + height/2),
                    (x - width/2, y + height/2),
                    (x - width/2, y - height/2)
                ]
                self.msp.add_lwpolyline(points, close=True)
    
    def save(self, output_path: str):
        """DXF-Datei speichern"""
        self.doc.saveas(output_path)


class GerberConverterGUI(QMainWindow):
    """Hauptfenster der GUI-Anwendung"""
    
    def __init__(self):
        super().__init__()
        self.input_file = None
        self.output_file = None
        self.signals = WorkerSignals()
        self.signals.progress.connect(self.log_message)
        self.signals.error.connect(self.show_error)
        self.signals.success.connect(self.show_success)
        self.signals.finished.connect(self.on_conversion_finished)
        
        self.init_ui()
    
    def init_ui(self):
        """Benutzeroberfläche initialisieren"""
        self.setWindowTitle("Gerber to DXF Converter")
        self.setGeometry(100, 100, 700, 600)
        self.setStyleSheet(self.get_stylesheet())
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Titel
        title = QLabel("Gerber to DXF Converter")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # Input-Datei Bereich
        input_group = QGroupBox("Eingabe-Datei (GBR)")
        input_layout = QVBoxLayout()
        
        input_h_layout = QHBoxLayout()
        self.input_label = QLineEdit()
        self.input_label.setReadOnly(True)
        self.input_label.setPlaceholderText("Keine Datei ausgewählt...")
        input_h_layout.addWidget(QLabel("Datei:"), 0)
        input_h_layout.addWidget(self.input_label, 1)
        input_layout.addLayout(input_h_layout)
        
        btn_select_input = QPushButton("📂 GBR-Datei auswählen")
        btn_select_input.clicked.connect(self.select_input_file)
        btn_select_input.setMinimumHeight(40)
        input_layout.addWidget(btn_select_input)
        
        input_group.setLayout(input_layout)
        layout.addWidget(input_group)
        
        # Output-Datei Bereich
        output_group = QGroupBox("Ausgabe-Datei (DXF)")
        output_layout = QVBoxLayout()
        
        output_h_layout = QHBoxLayout()
        self.output_label = QLineEdit()
        self.output_label.setReadOnly(True)
        self.output_label.setPlaceholderText("Wird automatisch ermittelt...")
        output_h_layout.addWidget(QLabel("Datei:"), 0)
        output_h_layout.addWidget(self.output_label, 1)
        output_layout.addLayout(output_h_layout)
        
        output_group.setLayout(output_layout)
        layout.addWidget(output_group)
        
        # Fortschritt
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setRange(0, 0)
        layout.addWidget(self.progress_bar)
        
        # Log-Bereich
        log_label = QLabel("Protokoll:")
        layout.addWidget(log_label)
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(200)
        self.log_text.setStyleSheet("""
            QTextEdit {
                background-color: #f5f5f5;
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 5px;
                font-family: Courier;
                font-size: 10px;
            }
        """)
        layout.addWidget(self.log_text)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        btn_convert = QPushButton("🔄 Konvertieren")
        btn_convert.clicked.connect(self.convert)
        btn_convert.setMinimumWidth(150)
        btn_convert.setMinimumHeight(40)
        btn_convert.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """)
        button_layout.addWidget(btn_convert)
        
        btn_exit = QPushButton("❌ Beenden")
        btn_exit.clicked.connect(self.close)
        btn_exit.setMinimumWidth(150)
        btn_exit.setMinimumHeight(40)
        button_layout.addWidget(btn_exit)
        
        layout.addLayout(button_layout)
        
        central_widget.setLayout(layout)
    
    def get_stylesheet(self) -> str:
        """CSS-Styling für die Anwendung"""
        return """
            QMainWindow {
                background-color: #ffffff;
            }
            QGroupBox {
                border: 2px solid #ddd;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
                font-weight: bold;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px 0 3px;
            }
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                font-weight: bold;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #0b7dda;
            }
            QPushButton:pressed {
                background-color: #0a5fa0;
            }
            QLineEdit {
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 5px;
                background-color: #f9f9f9;
            }
            QLabel {
                color: #333;
            }
        """
    
    def select_input_file(self):
        """Eingabedatei auswählen"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "GBR-Datei auswählen",
            "",
            "Gerber Dateien (*.gbr);;Alle Dateien (*)"
        )
        
        if file_path:
            self.input_file = file_path
            self.input_label.setText(file_path)
            
            # Automatisch Output-Datei im gleichen Verzeichnis
            input_path = Path(file_path)
            output_path = input_path.parent / (input_path.stem + '.dxf')
            self.output_file = str(output_path)
            self.output_label.setText(str(output_path))
            
            self.log_message(f"✓ Eingabe-Datei: {input_path.name}")
            self.log_message(f"✓ Ausgabe-Datei: {output_path.name}")
    
    def convert(self):
        """Konvertierung starten"""
        if not self.input_file:
            self.show_error("Bitte wählen Sie zuerst eine GBR-Datei aus!")
            return
        
        if not Path(self.input_file).exists():
            self.show_error("Die Eingabedatei existiert nicht!")
            return
        
        # UI deaktivieren während Konvertierung
        self.progress_bar.setVisible(True)
        self.setEnabled(False)
        
        # Konvertierung in Thread ausführen
        thread = Thread(target=self.run_conversion, daemon=True)
        thread.start()
    
    def run_conversion(self):
        """Konvertierungsprozess (läuft in separatem Thread)"""
        try:
            input_path = Path(self.input_file)
            
            self.signals.progress.emit(f"📄 Lese Gerber-Datei: {input_path.name}")
            parser = GerberParser(self.input_file)
            entities = parser.parse()
            
            self.signals.progress.emit(f"✓ Gerber-Einheit: {parser.unit_name}")
            self.signals.progress.emit(f"✓ {len(entities)} Entities gefunden")
            self.signals.progress.emit(f"✓ {len(parser.apertures)} Apertures definiert")
            
            self.signals.progress.emit("🔄 Konvertiere zu DXF...")
            converter = DXFConverter(parser)
            converter.convert()
            converter.save(self.output_file)
            
            self.signals.success.emit(
                f"✅ Konvertierung erfolgreich!\n"
                f"Ausgabe: {Path(self.output_file).name}\n"
                f"Einheit: mm"
            )
            
        except Exception as e:
            self.signals.error.emit(f"❌ Fehler während Konvertierung:\n{str(e)}")
        
        finally:
            self.signals.finished.emit()
    
    def log_message(self, message: str):
        """Nachricht ins Log schreiben"""
        self.log_text.append(message)
        cursor = self.log_text.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        self.log_text.setTextCursor(cursor)
    
    def show_error(self, message: str):
        """Fehler-Meldung anzeigen"""
        self.log_message(message)
        QMessageBox.critical(self, "Fehler", message)
    
    def show_success(self, message: str):
        """Erfolgs-Meldung anzeigen"""
        self.log_message(message)
        QMessageBox.information(self, "Erfolg", message)
    
    def on_conversion_finished(self):
        """Nach Konvertierung: UI wieder aktivieren"""
        self.progress_bar.setVisible(False)
        self.setEnabled(True)


def main():
    """Hauptfunktion"""
    app = QApplication(sys.argv)
    
    # Anwendungs-Icon und Info setzen
    app.setApplicationName("Gerber to DXF Converter")
    app.setApplicationVersion("1.0")
    
    window = GerberConverterGUI()
    window.show()
    
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
