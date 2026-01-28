import sys
import requests
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QFileDialog,
    QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, 
    QTableWidgetItem, QFrame, QHeaderView
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

API_URL = "http://127.0.0.1:8000/api/upload/"

# --- MODERN STYLESHEET ---
QSS = """
QWidget {
    background-color: #f8f9fa;
    font-family: 'Segoe UI', Arial, sans-serif;
    color: #333;
}
QFrame#Card {
    background-color: white;
    border-radius: 8px;
    border: 1px solid #dee2e6;
}
QLabel#Header {
    font-size: 18px;
    font-weight: bold;
    color: #2c3e50;
    margin-bottom: 10px;
}
QLabel#StatValue {
    font-size: 14px;
    color: #555;
    padding: 5px;
}
QPushButton {
    background-color: #007bff;
    color: white;
    border-radius: 5px;
    padding: 8px 16px;
    font-weight: bold;
    font-size: 13px;
}
QPushButton:hover {
    background-color: #0056b3;
}
QTableWidget {
    border: none;
    background-color: white;
    gridline-color: #e9ecef;
}
QHeaderView::section {
    background-color: #e9ecef;
    padding: 4px;
    border: 1px solid #dee2e6;
    font-weight: bold;
}
"""

class ChartCanvas(FigureCanvasQTAgg):
    def __init__(self):
        # Match the background color of the UI
        fig = Figure(figsize=(5, 4), facecolor='#ffffff')
        self.ax = fig.add_subplot(111)
        self.ax.set_facecolor('#ffffff')
        super().__init__(fig)
        fig.tight_layout()

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chemical Equipment Visualizer")
        self.resize(1000, 750)
        self.setStyleSheet(QSS)

        # Main Layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(15)

        # --- HEADER SECTION ---
        header_layout = QHBoxLayout()
        title_label = QLabel("Equipment Dashboard")
        title_label.setObjectName("Header")
        
        self.upload_btn = QPushButton("↑ Upload CSV Data")
        self.upload_btn.setCursor(Qt.PointingHandCursor)
        self.upload_btn.clicked.connect(self.upload_csv)
        
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(self.upload_btn)
        self.main_layout.addLayout(header_layout)

        # --- SUMMARY CARDS ---
        self.summary_card = QFrame()
        self.summary_card.setObjectName("Card")
        summary_layout = QHBoxLayout(self.summary_card)
        
        self.summary_label = QLabel("Please upload a file to see analytics summary.")
        self.summary_label.setObjectName("StatValue")
        self.summary_label.setAlignment(Qt.AlignCenter)
        summary_layout.addWidget(self.summary_label)
        
        self.main_layout.addWidget(self.summary_card)

        # --- DATA VISUALIZATION SECTION (Middle) ---
        viz_layout = QHBoxLayout()
        
        # Chart Container
        self.chart_frame = QFrame()
        self.chart_frame.setObjectName("Card")
        chart_vbox = QVBoxLayout(self.chart_frame)
        self.chart = ChartCanvas()
        chart_vbox.addWidget(self.chart)
        
        viz_layout.addWidget(self.chart_frame, stretch=2)
        self.main_layout.addLayout(viz_layout)

        # --- TABLE SECTION (Bottom) ---
        table_frame = QFrame()
        table_frame.setObjectName("Card")
        table_vbox = QVBoxLayout(table_frame)
        
        self.table = QTableWidget()
        self.table.setAlternatingRowColors(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table_vbox.addWidget(self.table)
        
        self.main_layout.addWidget(table_frame, stretch=1)

    def upload_csv(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open CSV", "", "CSV Files (*.csv)")
        if not path:
            return

        try:
            files = {"file": open(path, "rb")}
            res = requests.post(API_URL, files=files)
            res.raise_for_status()
            data = res.json()

            self.show_summary(data["summary"])
            self.show_table(data["data"])
            self.show_chart(data["summary"]["type_distribution"])
        except Exception as e:
            self.summary_label.setText(f"Error: Could not connect to API or process file.\n{str(e)}")

    def show_summary(self, summary):
        text = (
            f"<b>Total Equipment:</b> {summary['total_equipment']}  |  "
            f"<b>Avg Flowrate:</b> {summary['average_flowrate']} m³/h  |  "
            f"<b>Avg Pressure:</b> {summary['average_pressure']} bar  |  "
            f"<b>Avg Temp:</b> {summary['average_temperature']} °C"
        )
        self.summary_label.setText(text)

    def show_table(self, rows):
        if not rows: return
        
        self.table.setRowCount(len(rows))
        self.table.setColumnCount(len(rows[0]))
        self.table.setHorizontalHeaderLabels(rows[0].keys())

        for i, row in enumerate(rows):
            for j, val in enumerate(row.values()):
                item = QTableWidgetItem(str(val))
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(i, j, item)

    def show_chart(self, dist):
        self.chart.ax.clear()
        colors = ['#007bff', '#6610f2', '#6f42c1', '#e83e8c', '#fd7e14']
        
        bars = self.chart.ax.bar(dist.keys(), dist.values(), color=colors[:len(dist)])
        self.chart.ax.set_title("Equipment Type Distribution", fontsize=12, pad=15, fontweight='bold')
        
        # Remove spines for a cleaner look
        self.chart.ax.spines['top'].set_visible(False)
        self.chart.ax.spines['right'].set_visible(False)
        
        self.chart.draw()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Set a global font
    app.setFont(QFont("Segoe UI", 10))
    window = App()
    window.show()
    sys.exit(app.exec_())