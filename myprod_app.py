import sys
import sqlite3
import random
import datetime
import os
import openpyxl
from PyQt5 import QtCore, QtWidgets, QtGui


DB_PATH = "myprod.db"


class MyProdApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MyProd 헬스케어 제품 관리")
        self.resize(800, 600)

        self.conn = sqlite3.connect(DB_PATH)
        self.create_table()
        self.ensure_sample_data(100)

        self.create_ui()
        self.load_data()

    def create_table(self):
        cur = self.conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS MyProd (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                price INTEGER,
                qty INTEGER
            )
            """
        )
        self.conn.commit()

    def ensure_sample_data(self, n):
        cur = self.conn.cursor()
        cur.execute("SELECT COUNT(*) FROM MyProd")
        (count,) = cur.fetchone()
        if count >= n:
            return

        # Insert up to n sample rows
        to_add = n - count
        for i in range(1, to_add + 1):
            idx = count + i
            name = f"Product {idx:03d}"
            price = random.randint(1000, 200000)
            qty = random.randint(1, 200)
            cur.execute("INSERT INTO MyProd (name, price, qty) VALUES (?, ?, ?)", (name, price, qty))
        self.conn.commit()

    def create_ui(self):
        layout = QtWidgets.QVBoxLayout(self)

        # Title
        title = QtWidgets.QLabel("MyProd - 헬스케어 제품 관리")
        title.setObjectName("titleLabel")
        title.setAlignment(QtCore.Qt.AlignCenter)
        title.setFont(QtGui.QFont("Segoe UI", 16, QtGui.QFont.Bold))
        layout.addWidget(title)

        form_layout = QtWidgets.QHBoxLayout()

        self.name_edit = QtWidgets.QLineEdit()
        self.name_edit.setPlaceholderText("제품명")
        self.price_edit = QtWidgets.QLineEdit()
        self.price_edit.setPlaceholderText("가격 (정수)")
        self.qty_edit = QtWidgets.QLineEdit()
        self.qty_edit.setPlaceholderText("수량 (정수)")

        form_layout.addWidget(QtWidgets.QLabel("Name:"))
        form_layout.addWidget(self.name_edit)
        form_layout.addWidget(QtWidgets.QLabel("Price:"))
        form_layout.addWidget(self.price_edit)
        form_layout.addWidget(QtWidgets.QLabel("Qty:"))
        form_layout.addWidget(self.qty_edit)

        layout.addLayout(form_layout)

        btn_layout = QtWidgets.QHBoxLayout()
        self.add_btn = QtWidgets.QPushButton("입력")
        self.add_btn.setObjectName("addBtn")
        self.update_btn = QtWidgets.QPushButton("수정")
        self.update_btn.setObjectName("updateBtn")
        self.delete_btn = QtWidgets.QPushButton("삭제")
        self.delete_btn.setObjectName("deleteBtn")
        self.export_btn = QtWidgets.QPushButton("엑셀 내보내기")
        self.export_btn.setObjectName("exportBtn")
        self.search_edit = QtWidgets.QLineEdit()
        self.search_edit.setPlaceholderText("검색어 (이름으로 검색)")
        self.search_btn = QtWidgets.QPushButton("검색")
        self.search_btn.setObjectName("searchBtn")
        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.update_btn)
        btn_layout.addWidget(self.delete_btn)
        btn_layout.addWidget(self.export_btn)
        btn_layout.addStretch()
        btn_layout.addWidget(self.search_edit)
        btn_layout.addWidget(self.search_btn)

        layout.addLayout(btn_layout)

        # Table
        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["id", "name", "price", "qty"])
        self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)

        layout.addWidget(self.table)

        # Styling (QSS)
        qss = """
        QWidget { background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #f7f9fc, stop:1 #e8f0f8); font-family: 'Segoe UI', Arial; }
        QLabel#titleLabel { color: #2c3e50; font-size: 18px; font-weight: 600; padding: 8px; }
        QLineEdit { padding: 6px; border: 1px solid #cfd8e3; border-radius: 6px; background: white; }
        QPushButton { background-color: #27ae60; color: white; border-radius: 6px; padding: 6px 12px; }
        QPushButton#updateBtn { background-color: #f39c12; }
        QPushButton#deleteBtn { background-color: #c0392b; }
        QPushButton#searchBtn { background-color: #2980b9; }
        QPushButton#exportBtn { background-color: #8e44ad; }
        QTableWidget { background: white; gridline-color: #ecf0f1; border: 1px solid #dfe6ee; }
        QHeaderView::section { background-color: #34495e; color: white; padding: 4px; }
        QTableWidget::item:selected { background-color: #3498db; color: white; }
        """
        self.setStyleSheet(qss)

        # connect signals
        self.add_btn.clicked.connect(self.add_product)
        self.update_btn.clicked.connect(self.update_product)
        self.delete_btn.clicked.connect(self.delete_product)
        self.export_btn.clicked.connect(self.export_to_excel)
        self.search_btn.clicked.connect(self.search_products)
        self.table.itemSelectionChanged.connect(self.on_table_select)

    def load_data(self, filter_text=None):
        cur = self.conn.cursor()
        if filter_text:
            like = f"%{filter_text}%"
            cur.execute("SELECT id, name, price, qty FROM MyProd WHERE name LIKE ? ORDER BY id", (like,))
        else:
            cur.execute("SELECT id, name, price, qty FROM MyProd ORDER BY id")
        rows = cur.fetchall()

        self.table.setRowCount(len(rows))
        for r, row in enumerate(rows):
            for c, val in enumerate(row):
                item = QtWidgets.QTableWidgetItem(str(val))
                if c == 0:
                    # id column, make it uneditable-looking
                    item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)
                self.table.setItem(r, c, item)

    def validate_inputs(self):
        name = self.name_edit.text().strip()
        if not name:
            QtWidgets.QMessageBox.warning(self, "입력 오류", "제품명을 입력하세요.")
            return None
        try:
            price = int(self.price_edit.text().strip())
            qty = int(self.qty_edit.text().strip())
        except Exception:
            QtWidgets.QMessageBox.warning(self, "입력 오류", "가격과 수량은 정수여야 합니다.")
            return None
        return name, price, qty

    def add_product(self):
        v = self.validate_inputs()
        if not v:
            return
        name, price, qty = v
        cur = self.conn.cursor()
        cur.execute("INSERT INTO MyProd (name, price, qty) VALUES (?, ?, ?)", (name, price, qty))
        self.conn.commit()
        self.load_data()
        self.clear_inputs()

    def update_product(self):
        sel = self.table.currentRow()
        if sel < 0:
            QtWidgets.QMessageBox.information(self, "선택 필요", "수정하려는 항목을 선택하세요.")
            return
        id_item = self.table.item(sel, 0)
        if id_item is None:
            return
        prod_id = int(id_item.text())
        v = self.validate_inputs()
        if not v:
            return
        name, price, qty = v
        cur = self.conn.cursor()
        cur.execute("UPDATE MyProd SET name=?, price=?, qty=? WHERE id=?", (name, price, qty, prod_id))
        self.conn.commit()
        self.load_data()
        self.clear_inputs()

    def delete_product(self):
        sel = self.table.currentRow()
        if sel < 0:
            QtWidgets.QMessageBox.information(self, "선택 필요", "삭제하려는 항목을 선택하세요.")
            return
        id_item = self.table.item(sel, 0)
        if id_item is None:
            return
        prod_id = int(id_item.text())
        reply = QtWidgets.QMessageBox.question(self, '삭제 확인', f'ID {prod_id} 항목을 삭제하시겠습니까?',
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            cur = self.conn.cursor()
            cur.execute("DELETE FROM MyProd WHERE id=?", (prod_id,))
            self.conn.commit()
            self.load_data()
            self.clear_inputs()

    def search_products(self):
        txt = self.search_edit.text().strip()
        self.load_data(filter_text=txt if txt else None)

    def export_to_excel(self):
        # Build default filename with timestamp
        ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        default_name = os.path.join(os.getcwd(), f"myprod_export_{ts}.xlsx")
        path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "엑셀로 저장", default_name, "Excel Files (*.xlsx)")
        if not path:
            return
        try:
            wb = openpyxl.Workbook()
            ws = wb.active
            # headers
            headers = [self.table.horizontalHeaderItem(i).text() for i in range(self.table.columnCount())]
            ws.append(headers)
            # rows
            for r in range(self.table.rowCount()):
                row_vals = []
                for c in range(self.table.columnCount()):
                    item = self.table.item(r, c)
                    row_vals.append(item.text() if item is not None else "")
                ws.append(row_vals)
            wb.save(path)
            QtWidgets.QMessageBox.information(self, "완료", f"엑셀 파일로 저장했습니다:\n{path}")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "오류", f"엑셀 저장 중 오류가 발생했습니다:\n{e}")

    def on_table_select(self):
        sel = self.table.currentRow()
        if sel < 0:
            return
        name_item = self.table.item(sel, 1)
        price_item = self.table.item(sel, 2)
        qty_item = self.table.item(sel, 3)
        if name_item:
            self.name_edit.setText(name_item.text())
        if price_item:
            self.price_edit.setText(price_item.text())
        if qty_item:
            self.qty_edit.setText(qty_item.text())

    def clear_inputs(self):
        self.name_edit.clear()
        self.price_edit.clear()
        self.qty_edit.clear()

    def closeEvent(self, event):
        try:
            self.conn.close()
        except Exception:
            pass
        event.accept()


def main():
    app = QtWidgets.QApplication(sys.argv)
    w = MyProdApp()
    w.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
