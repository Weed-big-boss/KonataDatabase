from relation_window import RelationWindow
from PyQt6.QtWidgets import QTreeWidgetItemIterator,QTreeWidgetItem
class MainWindowRelations:
    def __init__(self,parent):
        self.parent=parent

    def create_relations(self):
        self.relation_window = RelationWindow(self.parent)
        self.relation_window.exec()
    def add_relations(self,new_relation):

        parent = self.find_item_by_text(new_relation[0])
        if parent is None:
            QTreeWidgetItem(self.parent.relations_list,[new_relation[0]])
            parent = self.find_item_by_text(new_relation[0])
        QTreeWidgetItem(parent, [new_relation[1]])

    def find_item_by_text(self, text,level=0):
        iterator = QTreeWidgetItemIterator(self.parent.relations_list)
        while iterator.value():
            item = iterator.value()
            if item.text(0) == text and self.get_item_level(item) == level:
                return item
            iterator += 1
        return None
    @staticmethod
    def get_item_level(item):
        level = 0
        parent = item.parent()
        while parent:
            level += 1
            parent = parent.parent()
        return level