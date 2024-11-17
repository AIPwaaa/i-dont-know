# i-dont-know

1. Разработать эмулятор для языка оболочки ОС. Необходимо сделать работу
эмулятора как можно более похожей на сеанс shell в UNIX-подобной ОС.
Эмулятор должен запускаться из реальной командной строки, а файл с
виртуальной файловой системой не нужно распаковывать у пользователя.
Эмулятор принимает образ виртуальной файловой системы в виде файла формата
tar. Эмулятор должен работать в режиме GUI.
Конфигурационный файл имеет формат json и содержит:
• Имя пользователя для показа в приглашении к вводу.
• Путь к архиву виртуальной файловой системы.
Необходимо поддержать в эмуляторе команды ls, cd и exit, а также
следующие команды: 1. cal. 2. find. 3. whoami.
Все функции эмулятора должны быть покрыты тестами, а для каждой из
поддерживаемых команд необходимо написать 3 теста.

3. Функция ls выводит на экран список папок и файлов в текущей директории, если нету параметра, а также выводит
список папок и файлов той директории, которую указали в виде параметра
Функция cd вместо вывода списка файлов директории меняет текущую директори на указанную или остаётся в той же, если параметра нету
Функция find выводит все папки и файлы, которые соответствуют параметру, с их абсолютным путём
Функция cal выводит текущий месяц
Функция whoami выводит имя пользователя
Функция exit завершает сеанс bash

4. ![Снимок экрана 2024-11-17 220302](https://github.com/user-attachments/assets/effa06d9-9fa6-48e0-8d16-a2b92fa13963)
![Снимок экрана 2024-11-17 220701](https://github.com/user-attachments/assets/11f40faa-0bc0-4073-b107-2eee9126fd1f)
![Снимок экрана 2024-11-17 220921](https://github.com/user-attachments/assets/96a6309c-bdd0-4c23-bd9a-9aa16d4398c6)
![Снимок экрана 2024-11-17 220949](https://github.com/user-attachments/assets/96515996-0d1b-4fa5-964d-438efc3dbc44)
![Снимок экрана 2024-11-17 221012](https://github.com/user-attachments/assets/1b2b25eb-1c2c-4551-8dce-ec8c7f8c87bb)

5. Все 12 тесто выполнены (по 3 на команды ls, cd и find и по 1 на cal, whoami и exit)
