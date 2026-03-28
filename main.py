# student_manager.py
import sys
import os
import csv
from traceback import format_exc
from datetime import datetime
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QComboBox, QTableView,
    QHeaderView, QAbstractItemView, QMessageBox, QHBoxLayout, QVBoxLayout,
    QSizePolicy, QDialog, QFormLayout, QLineEdit, QSpinBox, QDoubleSpinBox,
    QDialogButtonBox, QFileDialog, QGroupBox, QRadioButton, QButtonGroup, QCheckBox
)
from PyQt6.QtCore import Qt, QSortFilterProxyModel
from PyQt6.QtGui import QIcon
from PyQt6.QtSql import (
    QSqlDatabase, QSqlQuery, QSqlRelation, QSqlRelationalTableModel,
    QSqlRelationalDelegate
)


class AddEditStudentDialog(QDialog):
    """Диалог для добавления/редактирования студента"""
    
    def __init__(self, parent=None, student_id=None):
        super().__init__(parent)
        self.student_id = student_id
        self.setWindowTitle("Добавить студента" if student_id is None else "Редактировать студента")
        self.setMinimumWidth(400)
        self.setupUI()
        
        if student_id:
            self.loadStudentData()
    
    def setupUI(self):
        layout = QFormLayout()
        
        # Поля ввода
        self.first_name_edit = QLineEdit()
        self.last_name_edit = QLineEdit()
        self.course_spin = QSpinBox()
        self.course_spin.setRange(1, 6)
        self.course_spin.setSuffix(" курс")
        
        # Выбор курсов (множественный выбор через чекбоксы)
        self.courses_group = QGroupBox("Выбранные курсы")
        courses_layout = QVBoxLayout()
        self.course_checkboxes = {}
        courses = ["Математика", "Физика", "Программирование", "Базы данных", "Сети"]
        for course in courses:
            cb = QCheckBox(course)
            self.course_checkboxes[course] = cb
            courses_layout.addWidget(cb)
        self.courses_group.setLayout(courses_layout)
        
        layout.addRow("Имя:", self.first_name_edit)
        layout.addRow("Фамилия:", self.last_name_edit)
        layout.addRow("Курс:", self.course_spin)
        layout.addRow(self.courses_group)
        
        # Кнопки
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)
        
        self.setLayout(layout)
    
    def loadStudentData(self):
        """Загрузка данных студента для редактирования"""
        query = QSqlQuery()
        query.prepare("SELECT first_name, last_name, course FROM students WHERE id = ?")
        query.addBindValue(self.student_id)
        
        if query.exec() and query.next():
            self.first_name_edit.setText(query.value(0))
            self.last_name_edit.setText(query.value(1))
            self.course_spin.setValue(query.value(2))
            
            # Загружаем курсы студента
            query2 = QSqlQuery()
            query2.prepare("SELECT course_name FROM student_courses WHERE student_id = ?")
            query2.addBindValue(self.student_id)
            
            if query2.exec():
                selected_courses = []
                while query2.next():
                    selected_courses.append(query2.value(0))
                
                for course, checkbox in self.course_checkboxes.items():
                    checkbox.setChecked(course in selected_courses)
    
    def getStudentData(self):
        """Получение данных из формы"""
        first_name = self.first_name_edit.text().strip()
        last_name = self.last_name_edit.text().strip()
        
        # Проверка на корректность
        if not first_name:
            QMessageBox.warning(self, "Ошибка", "Имя не может быть пустым!")
            return None
        if not last_name:
            QMessageBox.warning(self, "Ошибка", "Фамилия не может быть пустой!")
            return None
        
        selected_courses = [
            course for course, checkbox in self.course_checkboxes.items()
            if checkbox.isChecked()
        ]
        
        return {
            'first_name': first_name,
            'last_name': last_name,
            'course': self.course_spin.value(),
            'courses': selected_courses
        }


class AddEditCourseDialog(QDialog):
    """Диалог для добавления/редактирования курса"""
    
    def __init__(self, parent=None, course_id=None):
        super().__init__(parent)
        self.course_id = course_id
        self.setWindowTitle("Добавить курс" if course_id is None else "Редактировать курс")
        self.setupUI()
        
        if course_id:
            self.loadCourseData()
    
    def setupUI(self):
        layout = QFormLayout()
        
        self.name_edit = QLineEdit()
        self.teacher_edit = QLineEdit()
        
        layout.addRow("Название курса:", self.name_edit)
        layout.addRow("Преподаватель:", self.teacher_edit)
        
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)
        
        self.setLayout(layout)
    
    def loadCourseData(self):
        """Загрузка данных курса для редактирования"""
        query = QSqlQuery()
        query.prepare("SELECT name, teacher FROM courses WHERE id = ?")
        query.addBindValue(self.course_id)
        
        if query.exec() and query.next():
            self.name_edit.setText(query.value(0))
            self.teacher_edit.setText(query.value(1))
    
    def getCourseData(self):
        """Получение данных из формы"""
        name = self.name_edit.text().strip()
        teacher = self.teacher_edit.text().strip()
        
        if not name:
            QMessageBox.warning(self, "Ошибка", "Название курса не может быть пустым!")
            return None
        
        return {'name': name, 'teacher': teacher}


class AddEditExamDialog(QDialog):
    """Диалог для добавления/редактирования экзамена"""
    
    def __init__(self, parent=None, exam_id=None):
        super().__init__(parent)
        self.exam_id = exam_id
        self.setWindowTitle("Добавить оценку" if exam_id is None else "Редактировать оценку")
        self.setupUI()
        
        if exam_id:
            self.loadExamData()
    
    def setupUI(self):
        layout = QFormLayout()
        
        # Выбор студента
        self.student_combo = QComboBox()
        query = QSqlQuery("SELECT id, first_name, last_name FROM students ORDER BY last_name")
        while query.next():
            student_text = f"{query.value(1)} {query.value(2)}"
            self.student_combo.addItem(student_text, query.value(0))
        
        # Выбор курса
        self.course_combo = QComboBox()
        query = QSqlQuery("SELECT id, name FROM courses ORDER BY name")
        while query.next():
            self.course_combo.addItem(query.value(1), query.value(0))
        
        self.grade_spin = QDoubleSpinBox()
        self.grade_spin.setRange(2, 5)
        self.grade_spin.setSingleStep(0.1)
        
        layout.addRow("Студент:", self.student_combo)
        layout.addRow("Курс:", self.course_combo)
        layout.addRow("Оценка:", self.grade_spin)
        
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)
        
        self.setLayout(layout)
    
    def loadExamData(self):
        """Загрузка данных экзамена для редактирования"""
        query = QSqlQuery()
        query.prepare("SELECT student_id, course_id, grade FROM exams WHERE id = ?")
        query.addBindValue(self.exam_id)
        
        if query.exec() and query.next():
            student_id = query.value(0)
            course_id = query.value(1)
            self.grade_spin.setValue(query.value(2))
            
            # Устанавливаем выбранного студента
            index = self.student_combo.findData(student_id)
            if index >= 0:
                self.student_combo.setCurrentIndex(index)
            
            # Устанавливаем выбранный курс
            index = self.course_combo.findData(course_id)
            if index >= 0:
                self.course_combo.setCurrentIndex(index)
    
    def getExamData(self):
        """Получение данных из формы"""
        return {
            'student_id': self.student_combo.currentData(),
            'course_id': self.course_combo.currentData(),
            'grade': self.grade_spin.value()
        }


class StudentManager(QWidget):
    """Главное окно приложения"""
    
    def __init__(self):
        super().__init__()
        self.current_table = "students"
        self.initializeUI()
    
    def initializeUI(self):
        """Настройка графического интерфейса приложения"""
        self.setMinimumSize(1200, 700)
        self.setWindowTitle("Система управления студентами")
        self.createConnection()
        self.createTables()
        self.createTriggers()
        self.fillSampleData()
        self.createModel()
        self.setUpMainWindow()
        self.show()
    
    def createConnection(self):
        """Установка соединения с базой данных"""
        self.database = QSqlDatabase.addDatabase("QSQLITE")
        self.database.setDatabaseName("students.db")
        
        if not self.database.open():
            print("Невозможно открыть файл базы данных.")
            sys.exit(1)
    
    def createTables(self):
        """Создание таблиц в базе данных"""
        query = QSqlQuery()
        
        # Таблица студентов
        query.exec("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                course INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Таблица курсов
        query.exec("""
            CREATE TABLE IF NOT EXISTS courses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                teacher TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Таблица экзаменов
        query.exec("""
            CREATE TABLE IF NOT EXISTS exams (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                course_id INTEGER NOT NULL,
                grade REAL NOT NULL CHECK (grade >= 2 AND grade <= 5),
                exam_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
                FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE
            )
        """)
        
        # Таблица связей студентов и курсов (для множественного выбора)
        query.exec("""
            CREATE TABLE IF NOT EXISTS student_courses (
                student_id INTEGER NOT NULL,
                course_name TEXT NOT NULL,
                FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
                PRIMARY KEY (student_id, course_name)
            )
        """)
    
    def createTriggers(self):
        """Создание триггеров"""
        query = QSqlQuery()
        
        # Триггер 1: Автоматическое обновление updated_at при изменении студента
        query.exec("""
            CREATE TRIGGER IF NOT EXISTS update_student_timestamp 
            AFTER UPDATE ON students
            FOR EACH ROW
            BEGIN
                UPDATE students SET updated_at = CURRENT_TIMESTAMP 
                WHERE id = OLD.id;
            END
        """)
        
        # Триггер 2: Проверка оценки перед вставкой/обновлением
        query.exec("""
            CREATE TRIGGER IF NOT EXISTS validate_exam_grade
            BEFORE INSERT ON exams
            FOR EACH ROW
            WHEN NEW.grade < 2 OR NEW.grade > 5
            BEGIN
                SELECT RAISE(ABORT, 'Оценка должна быть от 2 до 5');
            END
        """)
        
        # Триггер 3: Логирование удаления студентов
        query.exec("""
            CREATE TABLE IF NOT EXISTS deleted_students_log (
                id INTEGER,
                first_name TEXT,
                last_name TEXT,
                course INTEGER,
                deleted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        query.exec("""
            CREATE TRIGGER IF NOT EXISTS log_student_deletion
            AFTER DELETE ON students
            FOR EACH ROW
            BEGIN
                INSERT INTO deleted_students_log (id, first_name, last_name, course)
                VALUES (OLD.id, OLD.first_name, OLD.last_name, OLD.course);
            END
        """)
        
        print("Триггеры успешно созданы")
    
    def fillSampleData(self):
        """Заполнение базы данных случайными значениями"""
        # Проверяем, есть ли данные в таблице студентов
        query = QSqlQuery("SELECT COUNT(*) FROM students")
        if query.exec() and query.next() and query.value(0) > 0:
            return  # Данные уже есть
        
        # Добавляем курсы
        courses = [
            ("Математика", "Иванов И.И."),
            ("Физика", "Петров П.П."),
            ("Программирование", "Сидоров С.С."),
            ("Базы данных", "Кузнецов А.А."),
            ("Сети", "Смирнов В.В.")
        ]
        
        for name, teacher in courses:
            query = QSqlQuery()
            query.prepare("INSERT INTO courses (name, teacher) VALUES (?, ?)")
            query.addBindValue(name)
            query.addBindValue(teacher)
            query.exec()
        
        # Добавляем студентов
        students = [
            ("Иван", "Иванов", 1, ["Математика", "Физика"]),
            ("Петр", "Петров", 2, ["Программирование", "Базы данных"]),
            ("Мария", "Сидорова", 3, ["Математика", "Программирование", "Сети"]),
            ("Анна", "Кузнецова", 2, ["Физика", "Сети"]),
            ("Дмитрий", "Смирнов", 4, ["Базы данных", "Программирование"]),
            ("Елена", "Волкова", 1, ["Математика"]),
            ("Алексей", "Морозов", 3, ["Физика", "Базы данных", "Сети"]),
            ("Ольга", "Новикова", 2, ["Программирование", "Математика"])
        ]
        
        for first_name, last_name, course, student_courses in students:
            query = QSqlQuery()
            query.prepare("INSERT INTO students (first_name, last_name, course) VALUES (?, ?, ?)")
            query.addBindValue(first_name)
            query.addBindValue(last_name)
            query.addBindValue(course)
            query.exec()
            
            student_id = query.lastInsertId()
            
            # Добавляем курсы студента
            for course_name in student_courses:
                query2 = QSqlQuery()
                query2.prepare("INSERT INTO student_courses (student_id, course_name) VALUES (?, ?)")
                query2.addBindValue(student_id)
                query2.addBindValue(course_name)
                query2.exec()
        
        # Добавляем экзамены
        exams = [
            (1, 1, 5), (1, 2, 4), (2, 3, 5), (2, 4, 4),
            (3, 1, 4), (3, 3, 5), (3, 5, 4), (4, 2, 4),
            (4, 5, 5), (5, 3, 5), (5, 4, 5), (6, 1, 5),
            (7, 2, 4), (7, 4, 4), (7, 5, 4), (8, 1, 4),
            (8, 3, 5)
        ]
        
        for student_id, course_id, grade in exams:
            query = QSqlQuery()
            query.prepare("INSERT INTO exams (student_id, course_id, grade) VALUES (?, ?, ?)")
            query.addBindValue(student_id)
            query.addBindValue(course_id)
            query.addBindValue(grade)
            query.exec()
        
        print("База данных заполнена тестовыми данными")
    
    def createModel(self):
        """Настройка модели и заголовков"""
        self.model = QSqlRelationalTableModel()
        self.updateModel()
        
        # Прокси модель для сортировки
        self.proxy_model = QSortFilterProxyModel()
        self.proxy_model.setSourceModel(self.model)

    def show_table_students(self):
        self.model.setTable("students")
        self.model.setHeaderData(0, Qt.Orientation.Horizontal, "ID")
        self.model.setHeaderData(1, Qt.Orientation.Horizontal, "Имя")
        self.model.setHeaderData(2, Qt.Orientation.Horizontal, "Фамилия")
        self.model.setHeaderData(3, Qt.Orientation.Horizontal, "Курс")
        self.model.setHeaderData(4, Qt.Orientation.Horizontal, "Дата создания")
        self.model.setHeaderData(5, Qt.Orientation.Horizontal, "Дата обновления")

    def show_table_courses(self):
        self.model.setTable("courses")
        self.model.setHeaderData(0, Qt.Orientation.Horizontal, "ID")
        self.model.setHeaderData(1, Qt.Orientation.Horizontal, "Название")
        self.model.setHeaderData(2, Qt.Orientation.Horizontal, "Преподаватель")
    
    def show_table_exams(self):
        self.model.setTable("exams")
        self.model.setRelation(1, QSqlRelation("students", "id", "first_name"))
        self.model.setRelation(2, QSqlRelation("courses", "id", "name"))
        self.model.setHeaderData(0, Qt.Orientation.Horizontal, "ID")
        self.model.setHeaderData(1, Qt.Orientation.Horizontal, "Студент")
        self.model.setHeaderData(2, Qt.Orientation.Horizontal, "Курс")
        self.model.setHeaderData(3, Qt.Orientation.Horizontal, "Оценка")
        self.model.setHeaderData(4, Qt.Orientation.Horizontal, "Дата экзамена")
    
    def updateModel(self):
        """Обновление модели в зависимости от выбранной таблицы"""
        self.model = QSqlRelationalTableModel()

        try:
            getattr(self, f"show_table_{self.current_table}")()
            self.model.select()
        
            if hasattr(self, 'proxy_model'):
                self.proxy_model.setSourceModel(self.model)
                if hasattr(self, 'table_view'):
                    self.table_view.setModel(self.proxy_model)
        except Exception as e:
            print(f"Error updateModel: {e}\n{format_exc()}")
    
    def setUpMainWindow(self):
        """Создание и расположение виджетов в главном окне"""

        PATH_UI_IMG = "ui_images"

        def create_button(title: str, slot, icon: str = "", css: str = "padding: 8px;"):
            btn = QPushButton(title)
            btn.clicked.connect(slot)
            btn.setStyleSheet(css)
            if icon:
                btn.setIcon(QIcon(os.path.join(PATH_UI_IMG, icon)))
            return btn

        
        title = QLabel("Система управления студентами")
        title.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        title.setStyleSheet("font: bold 24px; color: #2c3e50; padding: 10px;")
        
        students_btn = create_button(title="Студенты", slot=lambda: self.switchTable("students"), css="padding: 8px; font-weight: bold;")
        courses_btn = create_button(title="Курсы", slot=lambda: self.switchTable("courses"), css="padding: 8px; font-weight: bold;")
        exams_btn = create_button(title="Экзамены", slot=lambda: self.switchTable("exams"), css="padding: 8px; font-weight: bold;")
        
        add_btn = create_button(title="Добавить", slot=self.addItem, icon="add.png")
        edit_btn = create_button(title="Редактировать", slot=self.editItem, icon="edit.png")
        delete_btn = create_button(title="Удалить", slot=self.deleteItem, icon="delete.png")
        
        export_btn = create_button(title="Экспорт в CSV", slot=self.exportToCSV, icon="export.png")
        import_btn = create_button(title="Импорт из CSV", slot=self.importFromCSV, icon="import.png")
     
        
        self.sort_combo = QComboBox()
        self.sort_combo.currentTextChanged.connect(self.setSortingOrder)
        
        tables_h_box = QHBoxLayout()
        tables_h_box.addWidget(students_btn)
        tables_h_box.addWidget(courses_btn)
        tables_h_box.addWidget(exams_btn)
        tables_h_box.addStretch()
        
        operations_h_box = QHBoxLayout()
        operations_h_box.addWidget(add_btn)
        operations_h_box.addWidget(edit_btn)
        operations_h_box.addWidget(delete_btn)
        operations_h_box.addStretch()
        operations_h_box.addWidget(export_btn)
        operations_h_box.addWidget(import_btn)
        operations_h_box.addStretch()
        operations_h_box.addWidget(QLabel("Сортировка:"))
        operations_h_box.addWidget(self.sort_combo)
        
        # Создание табличного представления
        self.table_view = QTableView()
        self.table_view.setModel(self.proxy_model)
        horizontal = self.table_view.horizontalHeader()
        horizontal.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        vertical = self.table_view.verticalHeader()
        vertical.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_view.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table_view.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        
        # Инстанцирование делегата
        delegate = QSqlRelationalDelegate()
        self.table_view.setItemDelegate(delegate)
        
        # Основной макет
        main_v_box = QVBoxLayout()
        main_v_box.addWidget(title, Qt.AlignmentFlag.AlignLeft)
        main_v_box.addLayout(tables_h_box)
        main_v_box.addLayout(operations_h_box)
        main_v_box.addWidget(self.table_view)
        self.setLayout(main_v_box)
        
        # Устанавливаем начальные опции сортировки
        self.updateSortOptions()
    
    def switchTable(self, table_name):
        """Переключение между таблицами"""
        self.current_table = table_name
        self.updateModel()
        self.updateSortOptions()
    
    def updateSortOptions(self):
        """Обновление опций сортировки для текущей таблицы"""
        self.sort_combo.clear()
        if self.current_table == "students":
            self.sort_combo.addItems(["Сортировать по ID", "Сортировать по имени", 
                                      "Сортировать по фамилии", "Сортировать по курсу"])
        elif self.current_table == "courses":
            self.sort_combo.addItems(["Сортировать по ID", "Сортировать по названию", 
                                      "Сортировать по преподавателю"])
        elif self.current_table == "exams":
            self.sort_combo.addItems(["Сортировать по ID", "Сортировать по оценке", 
                                      "Сортировать по дате"])
    
    def addItem(self):
        """Добавление новой записи"""
        if self.current_table == "students":
            dialog = AddEditStudentDialog(self)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                data = dialog.getStudentData()
                if data:
                    query = QSqlQuery()
                    query.prepare("""
                        INSERT INTO students (first_name, last_name, course)
                        VALUES (?, ?, ?)
                    """)
                    query.addBindValue(data['first_name'])
                    query.addBindValue(data['last_name'])
                    query.addBindValue(data['course'])
                    
                    if query.exec():
                        student_id = query.lastInsertId()
                        
                        # Добавляем курсы студента
                        for course_name in data['courses']:
                            query2 = QSqlQuery()
                            query2.prepare("INSERT INTO student_courses (student_id, course_name) VALUES (?, ?)")
                            query2.addBindValue(student_id)
                            query2.addBindValue(course_name)
                            query2.exec()
                        
                        self.model.select()
                        QMessageBox.information(self, "Успех", "Студент успешно добавлен!")
                    else:
                        QMessageBox.warning(self, "Ошибка", "Не удалось добавить студента!")
        
        elif self.current_table == "courses":
            dialog = AddEditCourseDialog(self)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                data = dialog.getCourseData()
                if data:
                    query = QSqlQuery()
                    query.prepare("INSERT INTO courses (name, teacher) VALUES (?, ?)")
                    query.addBindValue(data['name'])
                    query.addBindValue(data['teacher'])
                    
                    if query.exec():
                        self.model.select()
                        QMessageBox.information(self, "Успех", "Курс успешно добавлен!")
                    else:
                        QMessageBox.warning(self, "Ошибка", "Не удалось добавить курс!")
        
        elif self.current_table == "exams":
            dialog = AddEditExamDialog(self)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                data = dialog.getExamData()
                if data:
                    query = QSqlQuery()
                    query.prepare("INSERT INTO exams (student_id, course_id, grade) VALUES (?, ?, ?)")
                    query.addBindValue(data['student_id'])
                    query.addBindValue(data['course_id'])
                    query.addBindValue(data['grade'])
                    
                    if query.exec():
                        self.model.select()
                        QMessageBox.information(self, "Успех", "Оценка успешно добавлена!")
                    else:
                        QMessageBox.warning(self, "Ошибка", f"Не удалось добавить оценку: {query.lastError().text()}")
    
    def editItem(self):
        """Редактирование выбранной записи"""
        current_index = self.table_view.currentIndex()
        if not current_index.isValid():
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, выберите запись для редактирования!")
            return
        
        source_index = self.proxy_model.mapToSource(current_index)
        row = source_index.row()
        record = self.model.record(row)
        item_id = record.value(0)
        
        if self.current_table == "students":
            dialog = AddEditStudentDialog(self, item_id)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                data = dialog.getStudentData()
                if data:
                    query = QSqlQuery()
                    query.prepare("""
                        UPDATE students 
                        SET first_name = ?, last_name = ?, course = ?
                        WHERE id = ?
                    """)
                    query.addBindValue(data['first_name'])
                    query.addBindValue(data['last_name'])
                    query.addBindValue(data['course'])
                    query.addBindValue(item_id)
                    
                    if query.exec():
                        # Обновляем курсы студента
                        query2 = QSqlQuery()
                        query2.prepare("DELETE FROM student_courses WHERE student_id = ?")
                        query2.addBindValue(item_id)
                        query2.exec()
                        
                        for course_name in data['courses']:
                            query2 = QSqlQuery()
                            query2.prepare("INSERT INTO student_courses (student_id, course_name) VALUES (?, ?)")
                            query2.addBindValue(item_id)
                            query2.addBindValue(course_name)
                            query2.exec()
                        
                        self.model.select()
                        QMessageBox.information(self, "Успех", "Данные студента обновлены!")
        
        elif self.current_table == "courses":
            dialog = AddEditCourseDialog(self, item_id)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                data = dialog.getCourseData()
                if data:
                    query = QSqlQuery()
                    query.prepare("UPDATE courses SET name = ?, teacher = ? WHERE id = ?")
                    query.addBindValue(data['name'])
                    query.addBindValue(data['teacher'])
                    query.addBindValue(item_id)
                    
                    if query.exec():
                        self.model.select()
                        QMessageBox.information(self, "Успех", "Данные курса обновлены!")
        
        elif self.current_table == "exams":
            dialog = AddEditExamDialog(self, item_id)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                data = dialog.getExamData()
                if data:
                    query = QSqlQuery()
                    query.prepare("UPDATE exams SET student_id = ?, course_id = ?, grade = ? WHERE id = ?")
                    query.addBindValue(data['student_id'])
                    query.addBindValue(data['course_id'])
                    query.addBindValue(data['grade'])
                    query.addBindValue(item_id)
                    
                    if query.exec():
                        self.model.select()
                        QMessageBox.information(self, "Успех", "Данные экзамена обновлены!")
    
    def deleteItem(self):
        """Удаление выбранной записи с подтверждением"""
        current_index = self.table_view.currentIndex()
        if not current_index.isValid():
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, выберите запись для удаления!")
            return
        
        # Запрос подтверждения
        reply = QMessageBox.question(
            self, "Подтверждение удаления",
            "Вы уверены, что хотите удалить эту запись?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            source_index = self.proxy_model.mapToSource(current_index)
            row = source_index.row()
            self.model.removeRow(row)
            
            if self.model.submitAll():
                self.model.select()
                QMessageBox.information(self, "Успех", "Запись успешно удалена!")
            else:
                QMessageBox.warning(self, "Ошибка", "Не удалось удалить запись!")
    
    def setSortingOrder(self, text):
        """Сортировка строк в таблице"""
        sort_column = 0
        if text == "Сортировать по ID":
            sort_column = 0
        elif text == "Сортировать по имени" and self.current_table == "students":
            sort_column = 1
        elif text == "Сортировать по фамилии" and self.current_table == "students":
            sort_column = 2
        elif text == "Сортировать по курсу" and self.current_table == "students":
            sort_column = 3
        elif text == "Сортировать по названию" and self.current_table == "courses":
            sort_column = 1
        elif text == "Сортировать по преподавателю" and self.current_table == "courses":
            sort_column = 2
        elif text == "Сортировать по оценке" and self.current_table == "exams":
            sort_column = 3
        elif text == "Сортировать по дате" and self.current_table == "exams":
            sort_column = 4
        
        self.proxy_model.sort(sort_column, Qt.SortOrder.AscendingOrder)
    
    def exportToCSV(self):
        """Экспорт главной таблицы в CSV файл"""
        if self.current_table != "students":
            QMessageBox.warning(self, "Ошибка", "Экспорт доступен только для таблицы студентов!")
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Сохранить CSV файл", "",
            "CSV Files (*.csv);;All Files (*)"
        )
        
        if file_path:
            try:
                with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    
                    # Записываем заголовки
                    headers = ["ID", "Имя", "Фамилия", "Курс", "Дата создания", "Дата обновления"]
                    writer.writerow(headers)
                    
                    # Записываем данные
                    query = QSqlQuery("SELECT id, first_name, last_name, course, created_at, updated_at FROM students")
                    while query.next():
                        row = [
                            query.value(0),
                            query.value(1),
                            query.value(2),
                            query.value(3),
                            query.value(4),
                            query.value(5)
                        ]
                        writer.writerow(row)
                
                QMessageBox.information(self, "Успех", f"Данные успешно экспортированы в {file_path}")
            except Exception as e:
                QMessageBox.warning(self, "Ошибка", f"Ошибка при экспорте: {str(e)}")
    
    def importFromCSV(self):
        """Импорт данных из CSV файла"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Выберите CSV файл", "",
            "CSV Files (*.csv);;All Files (*)"
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as csvfile:
                    reader = csv.reader(csvfile)
                    headers = next(reader)  # Пропускаем заголовки
                    
                    count = 0
                    for row in reader:
                        if len(row) >= 4:
                            query = QSqlQuery()
                            query.prepare("""
                                INSERT INTO students (first_name, last_name, course)
                                VALUES (?, ?, ?)
                            """)
                            query.addBindValue(row[1])  # Имя
                            query.addBindValue(row[2])  # Фамилия
                            query.addBindValue(int(row[3]))  # Курс
                            
                            if query.exec():
                                count += 1
                    
                    self.model.select()
                    QMessageBox.information(self, "Успех", f"Импортировано {count} записей из файла {file_path}")
            except Exception as e:
                QMessageBox.warning(self, "Ошибка", f"Ошибка при импорте: {str(e)}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = StudentManager()
    sys.exit(app.exec())
