# Initial setup in venv
    cd /d D:\...\dir_project
    python -m venv venv
    venv\Scripts\activate
    pip3 install -r requirements.txt


# Run
    D:\...\dir_project\venv\Scripts\python.exe D:\...\dir_project\main.py

# or
    cd /d D:\...\dir_project
    venv\Scripts\python.exe main.py

<figure>
   <p align="center">
      <img src="https://github.com/dr-number/Lab6__PyQT_Introduction_Databases/blob/main/for_read_me/task1.jpg">
      <img src="https://github.com/dr-number/Lab6__PyQT_Introduction_Databases/blob/main/for_read_me/task2.jpg">
      <p align="center">Вариант №2</p>
   </p>
</figure>

# Основная работа программы
<figure>
   <p align="center">
      <img src="https://github.com/dr-number/Lab6__PyQT_Introduction_Databases/blob/main/for_read_me/1_init_triggers_and_db.jpg">
      <p align="center">Первый запуск программы. Сознание структуры БД, создание тригерров. Заполнение БД</p>
   </p>
</figure>

<figure>
   <p align="center">
      <img src="https://github.com/dr-number/Lab6__PyQT_Introduction_Databases/blob/main/for_read_me/2_init_triggers_and_db_repeat_start.jpg">
      <p align="center">Повторный запуск программы. Существующие тригерры не пересоздаются. Если в БД есть хотябы одна запись, повторное заполнение БД не происходит. Соответственно повторный запуск программы проходит быстрее</p>
   </p>
</figure>

# Добавление данных
<figure>
   <p align="center">
      <img src="https://github.com/dr-number/Lab6__PyQT_Introduction_Databases/blob/main/for_read_me/7_add.jpg">
   </p>
   <p align="center">
      <img src="https://github.com/dr-number/Lab6__PyQT_Introduction_Databases/blob/main/for_read_me/7_add-2.jpg">
      <p align="center">Добавление нового курса</p>
   </p>
</figure>

<figure>
   <p align="center">
      <img src="https://github.com/dr-number/Lab6__PyQT_Introduction_Databases/blob/main/for_read_me/7_add-3.jpg">
   </p>
   <p align="center">
      <img src="https://github.com/dr-number/Lab6__PyQT_Introduction_Databases/blob/main/for_read_me/7_add-4.jpg">
      <p align="center">Добавление нового студента (в том числе на новый курс)</p>
   </p>
</figure>

# Редактирование данных
<figure>
   <p align="center">
      <img src="https://github.com/dr-number/Lab6__PyQT_Introduction_Databases/blob/main/for_read_me/4_edit_data_1.jpg">
      <p align="center">Редактирование данных. Исправление оценки</p>
   </p>
</figure>

<figure>
   <p align="center">
      <img src="https://github.com/dr-number/Lab6__PyQT_Introduction_Databases/blob/main/for_read_me/4_edit_data_1-2.jpg">
      <p align="center">Редактирование данных. Исправление оценки. (результат)</p>
   </p>
</figure>

# Удаление данных
<figure>
   <p align="center">
      <img src="https://github.com/dr-number/Lab6__PyQT_Introduction_Databases/blob/main/for_read_me/5_delete_record_1.jpg">
      <p align="center">Удаление данных. Подтверждение намерения удаления</p>
   </p>
</figure>

<figure>
   <p align="center">
      <img src="https://github.com/dr-number/Lab6__PyQT_Introduction_Databases/blob/main/for_read_me/5_delete_record_2.jpg">
      <p align="center">Данные успешно удалены</p>
   </p>
</figure>

# При удалении студета. Его данные удаляются и из связанных таблиц
<figure>
   <p align="center">
      <img src="https://github.com/dr-number/Lab6__PyQT_Introduction_Databases/blob/main/for_read_me/6_link_cours_delete.jpg">
      <p align="center">До удаления</p>
   </p>
</figure>
<figure>
   <p align="center">
      <img src="https://github.com/dr-number/Lab6__PyQT_Introduction_Databases/blob/main/for_read_me/6_link_cours_delete-2.jpg">
      <p align="center">Подтверждение удаления</p>
   </p>
</figure>
<figure>
   <p align="center">
      <img src="https://github.com/dr-number/Lab6__PyQT_Introduction_Databases/blob/main/for_read_me/6_link_cours_delete-3.jpg">
      <p align="center">Данные из связанной таблицы успешно удалены</p>
   </p>
</figure>

# Сортировка
<figure>
   <p align="center">
      <img src="https://github.com/dr-number/Lab6__PyQT_Introduction_Databases/blob/main/for_read_me/3_sort_students_1.jpg">
      <p align="center">Сортировка студентов по имени, по убыванию</p>
   </p>
</figure>
<figure>
   <p align="center">
      <img src="https://github.com/dr-number/Lab6__PyQT_Introduction_Databases/blob/main/for_read_me/3_sort_students_2.jpg">
      <p align="center">Сортировка студентов по фамилии, по возрастанию</p>
   </p>
</figure>
<figure>
   <p align="center">
      <img src="https://github.com/dr-number/Lab6__PyQT_Introduction_Databases/blob/main/for_read_me/3_sort_exams_1.jpg">
      <p align="center">Сортировка экзаменов по оценке, по убыванию</p>
   </p>
</figure>
<figure>
   <p align="center">
      <img src="https://github.com/dr-number/Lab6__PyQT_Introduction_Databases/blob/main/for_read_me/3_sort_courses_1.jpg">
      <p align="center">Сортировка курсов по названию, по убыванию</p>
   </p>
</figure>