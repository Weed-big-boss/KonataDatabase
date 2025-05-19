from main_window import ColumnEditor
from utils import data_catcher
from PyQt6.QtWidgets import QApplication, QMessageBox
import traceback
import sys





def handle_exception(exc_type, exc_value, exc_traceback):
    """Глобальный обработчик исключений"""
    error_msg = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    print(error_msg)  # Печать в консоль
    QMessageBox.critical(None, "Ошибка", f"Произошла ошибка:\n\n{error_msg}")
    sys.exit(1)
if __name__ == "__main__":
        sys.excepthook = handle_exception
        app = QApplication(sys.argv)
        att_n_types,attribue_list =data_catcher()
        window = ColumnEditor(att_n_types, attribue_list)
        window.show()
        sys.exit(app.exec())