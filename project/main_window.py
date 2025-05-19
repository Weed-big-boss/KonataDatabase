from utils import get_file_path
from main_window_relations_module import MainWindowRelations
from utils import topological_sort
from generator_schema import relations_generator,schema_generator
from generator_schema import generator
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QComboBox,
    QPushButton, QVBoxLayout, QMessageBox, QListWidget, QHBoxLayout,
    QCheckBox, QFileDialog, QListWidgetItem, QTreeWidget,
)
from main_window_tables_module import MainWindowTables
class ColumnEditor(QWidget):
    def __init__(self,attributes_n_types,attribute_list):
        super().__init__()
        self.setWindowTitle("KonataBase")
        self.setGeometry(100, 100, 700, 700)
        self.setWindowIcon(QIcon(get_file_path('konata.ico')))
        self.tables_list_obj=MainWindowTables(self)
        self.relations_list_obj=MainWindowRelations(self)
        self.att_n_types = attributes_n_types
        self.tables = []
        self.relations= {}
        self.convertor={"str":"TEXT","int":"INTEGER",'None':"JSON","bytes":"BLOB","bool":"BOOLEAN","datetime":"DATETIME","list":"JSON","tuple":"JSON",
                        "NoneType":"JSON","Decimal":"NUMERIC","Zoneinfo":"VARCHAR(255)","dict":"JSON","set":"JSON","GENERATOR":"JSON",'timedelta':"JSON",
                        "time":"TEXT","date":"TEXT",'float':"FLOAT"}
        self.data=attribute_list
        self.tree_data={}
        main_layout = QVBoxLayout()

        table_layout= QHBoxLayout()

        self.label_name = QLabel("Название таблицы:")
        self.table_name_input = QLineEdit()

        self.create_table_button = QPushButton("Сформировать таблицу")
        self.create_table_button.clicked.connect(self.tables_list_obj.create_table)
        self.create_table_button.setFixedSize(160,24)

        self.delete_table_button = QPushButton("Удалить объект")
        self.delete_table_button.clicked.connect(self.delete_object)
        self.delete_table_button.setFixedSize(160,24)

        table_layout.addWidget(self.table_name_input)
        table_layout.addWidget(self.create_table_button)
        table_layout.addWidget(self.delete_table_button)


        col_layout = QHBoxLayout()

        self.col_name_input = QLineEdit()
        self.col_name_input.setPlaceholderText("Имя столбца")
        self.col_name_input.textChanged.connect(self.update_dropdown)
        self.col_name_input.setFixedSize(346,23)

        self.dropdown = QListWidget()
        self.dropdown.hide()
        self.dropdown.setWindowFlags(Qt.WindowType.ToolTip)
        self.dropdown.itemClicked.connect(self.select_item)

        self.col_type_combo = QComboBox()
        self.col_type_combo.addItems(["TEXT", "INTEGER", "FLOAT", "BOOLEAN", "DATE", "JSON", "BLOB", "DATETIME", "NUMERIC", "VARCHAR(255)"])
        self.col_type_combo.setFixedSize(110,23)

        self.not_null_check = QCheckBox("NOT NULL")

        self.add_column_button = QPushButton("Добавить столбец")
        self.add_column_button.clicked.connect(self.tables_list_obj.add_column)
        self.add_column_button.setFixedSize(120,25)

        col_layout.addWidget(self.col_name_input)
        col_layout.addWidget(self.col_type_combo)
        col_layout.addWidget(self.add_column_button)
        col_layout.addWidget(self.not_null_check)



        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["Таблицы", "", ""])

        self.relations_list= QTreeWidget()
        self.relations_list.setHeaderLabels(["Связи",""])




        self.relations_button= QPushButton("Создать связи между таблицами")
        self.relations_button.clicked.connect(self.relations_list_obj.create_relations)
        self.save_button = QPushButton("Сохранить SQL")
        self.save_button.clicked.connect(self.save_sql)

        self.tree.focusInEvent = self.on_list1_selected
        self.relations_list.focusInEvent = self.on_list2_selected

        main_layout.addWidget(self.label_name)
        main_layout.addLayout(table_layout)

        main_layout.addLayout(col_layout)
        main_layout.addWidget(QLabel("Добавленные столбцы:"))
        main_layout.addWidget(self.tree)
        main_layout.addWidget(self.relations_list)

        main_layout.addWidget(self.relations_button)

        main_layout.addWidget(self.save_button)


        self.setLayout(main_layout)

    def on_list1_selected(self,event):
        QTimer.singleShot(0, lambda: self.relations_list.clearSelection())
        return super(QTreeWidget, self.tree).focusInEvent(event)

    def on_list2_selected(self,event):
        QTimer.singleShot(0, lambda: self.tree.clearSelection())
        return super(QTreeWidget, self.relations_list).focusInEvent(event)

    def delete_object(self):

        object = self.tree.selectedItems()
        object2 = self.relations_list.selectedItems()
        if (not object) and (not object2):
            return
        if object:
            for item in object:
                parent = item.parent()
                if parent:
                    parent.removeChild(item)
                    for tables in self.tables:
                        if tables['name'] == parent.text(0):
                            for column in tables['columns']:
                                if column['name'] == item.text(0):
                                    tables['columns'].remove(column)
                                    break

                else:
                    for elem in self.tables:
                        if elem['name'] == item.text(0):
                            self.tables.remove(elem)
                            break
                    index = self.tree.indexOfTopLevelItem(item)
                    if index >= 0:
                        self.tree.takeTopLevelItem(index)
        if object2:
            for item in object2:


                parent = item.parent()
                if parent:
                    parent.removeChild(item)
                    self.relations[parent.text(0)].remove(item.text(0))
                    break
                else:
                    self.relations.pop(item.text(0))
                    index = self.relations_list.indexOfTopLevelItem(item)
                    if index >= 0:
                        self.relations_list.takeTopLevelItem(index)








    def update_dropdown(self, text):
        self.dropdown.clear()

        if not text:
            self.dropdown.hide()
            return

        results = [item for item in self.data if text.lower() in item.lower()]
        if results:
            for r in results:
                QListWidgetItem(r, self.dropdown)


            pos = self.col_name_input.mapToGlobal(self.col_name_input.rect().bottomLeft())
            self.dropdown.move(pos)
            self.dropdown.resize(self.col_name_input.width(), 100)
            self.dropdown.show()
        else:
            self.dropdown.hide()

    def select_item(self, item):
        self.col_type_combo.setCurrentText(self.convertor[self.att_n_types[item.text()]])
        self.col_name_input.setText(item.text())
        self.col_name_input.setFocus()
        self.dropdown.hide()





    def save_sql(self):
        if not self.tables:
            QMessageBox.warning(self, "Ошибка", "Нет сформированных таблиц.")
            return

        file_path, _ = QFileDialog.getSaveFileName(self, "Сохранить SQL файл", "", "SQL Files (*.sql)")
        if not file_path:
            return

        with open(file_path, "w", encoding="utf-8") as f:
            users_dict = {}
            tables_order = topological_sort(self.relations, self.tables)[::-1]
            for table in self.tables:
                if table['name'] not in tables_order:
                    tables_order.append(table['name'])
            for table in tables_order:
                sql = schema_generator(next((item for item in self.tables if item.get('name') == table), None),
                                       self.relations)
                f.write(sql + "\n\n")
            for table in self.tables:
                insert, users = generator(table)
                users_dict[table['name']] = users
                f.write(insert)

            insert_relations = relations_generator(users_dict, self.relations)
            f.write(insert_relations)
            print("✅ Файл 'output.sql' готов!")

        QMessageBox.information(self, "Сохранено", f"SQL файл сохранён:\n{file_path}")

