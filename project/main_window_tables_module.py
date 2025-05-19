from PyQt6.QtWidgets import QMessageBox, QTreeWidgetItem, QTreeWidgetItemIterator
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

class MainWindowTables:
    def __init__(self,parent):
        self.parent = parent
    def add_column(self):
        name = self.parent.col_name_input.text().strip()
        col_type = self.parent.col_type_combo.currentText()
        not_null = self.parent.not_null_check.isChecked()
        select = self.parent.tree.selectedItems()

        if not select:
            return

        if not name:
            QMessageBox.warning(self.parent, "Ошибка", "Имя столбца не может быть пустым.")
            return

        column = {
            "name": name,
            "type": col_type,
            "not_null": not_null
        }




        for elem in self.parent.tables:
            if elem['name']==select[0].text(0):
                for columns in elem['columns']:
                    if columns['name']==column['name']:
                        QMessageBox.warning(self.parent, "Ошибка", "Такой столбец уже существует.")
                        return
                elem['columns'].append(column)
                parent = self.find_item_by_text(elem['name'])
                QTreeWidgetItem(parent, [column['name'], column['type'],str(column['not_null'])])
                break


        self.parent.col_name_input.clear()
        self.parent.not_null_check.setChecked(False)


    def find_item_by_text(self, text):
        iterator = QTreeWidgetItemIterator(self.parent.tree)
        while iterator.value():
            item = iterator.value()
            if item.text(0) == text:
                return item
            iterator += 1
        return None

    def create_table(self):
        name = self.parent.table_name_input.text().strip()
        if not name:
            QMessageBox.warning(self.parent, "Ошибка", "Введите имя таблицы.")
            return
        for table in self.parent.tables:
            if name in table['name']:
                QMessageBox.warning(self.parent, "Ошибка", "Такая таблица уже существует.")
                return

        table_data = {
            "name": name,
            "columns": []
        }

        self.parent.tree_data[name] = {}

        parent = QTreeWidgetItem(self.parent.tree, [name])

        child_header = QTreeWidgetItem(["Название", "Тип", "Not NULL Flag"])
        child_header.setBackground(0, QColor(240, 240, 240))
        child_header.setBackground(1, QColor(240, 240, 240))
        child_header.setBackground(2, QColor(240, 240, 240))
        child_header.setFlags(child_header.flags() & ~Qt.ItemFlag.ItemIsSelectable)

        parent.addChild(child_header)

        self.parent.tables.append(table_data)




        self.parent.table_name_input.clear()


