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
      <p align="center">Повторный запуск программы. Существующие тригерры не пересоздаются. Если в БД есть хотябы одна запись, повторное заполнение БД не происходит</p>
   </p>
</figure>