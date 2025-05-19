from copy import deepcopy
from PyQt6.QtWidgets import QLabel, QComboBox, QPushButton, QVBoxLayout, QDialog,QMessageBox


class RelationWindow(QDialog):

    def __init__(self,parent):
        super().__init__(parent)
        self.parent = parent
        self.tables=self.parent.tables
        self.relations= self.parent.relations
        self.seen = set()


        self.setWindowTitle("Связи между таблицами")
        self.setGeometry(150, 150, 300, 200)

        layout = QVBoxLayout()


        self.label = QLabel("Выберите таблицы и поля для связи")

        self.table1_combo = QComboBox()

        self.table1_combo.addItems([k['name'] for k in self.tables ])




        self.table2_combo = QComboBox()
        self.table2_combo.addItems([k['name'] for k in self.tables])



        self.create_button = QPushButton("Создать связь")
        self.create_button.clicked.connect(self.create_relation)

        layout.addWidget(self.label)
        layout.addWidget(self.table1_combo)
        layout.addWidget(QLabel("Связать с :"))
        layout.addWidget(self.table2_combo)

        layout.addWidget(self.create_button)

        self.setLayout(layout)

    def detect_cycle(self, pair):


        buffer_relations = deepcopy(self.relations)
        if len(buffer_relations)>0:
            for items in deepcopy(list(buffer_relations.values())):
                for item in items:
                 if item not in buffer_relations.copy():
                    buffer_relations[item]=[]


        if pair[0] not in buffer_relations:
            buffer_relations[pair[0]] = []
        buffer_relations[pair[0]].append(pair[1])
        for elem in buffer_relations[pair[0]]:
            if elem not in buffer_relations:
             buffer_relations[elem]=[]








        visited = set()
        stack = set()

        def jump(node):
            if node in stack:
                return False

            if node in visited:
                return True

            stack.add(node)

            for neighbor in buffer_relations[node]:
                if not jump(neighbor):
                    return False

            stack.remove(node)

            visited.add(node)
            return True


        for nodes in buffer_relations:
            if nodes not in visited:
                if not jump(nodes):
                    return False
        return True



    def check_relation(self,table1,table2,pair_tuple):
        cycle = self.detect_cycle([table1, table2])
        if not cycle:
            QMessageBox.warning(self, "Ошибка", "Нельзя создавать циклические связи")
        else:
            self.seen.add(pair_tuple)
            if table1 in self.relations:
             self.relations[table1].append(table2)
            else:
                self.relations[table1]=[]
                self.relations[table1].append(table2)
            self.parent.relations_list_obj.add_relations([table1,table2])

            QMessageBox.information(self, "Готово", "Связь создана")



    def create_relation(self):
        table1 = self.table1_combo.currentText()

        table2 = self.table2_combo.currentText()
        pair_tuple = tuple(sorted((table1, table2)))
        if table1!=table2:
            if len(self.relations)>0:
                if pair_tuple in self.seen:
                    QMessageBox.warning(self, "Ошибка", "Связь между этими таблицами уже создана")
                    return
                else:
                    self.check_relation(table1,table2,pair_tuple)
            else:
                self.check_relation(table1,table2,pair_tuple)
        else:
            QMessageBox.warning(self, "Ошибка","Нельзя создавать связь с одной и той же таблицей")
            return




