# Визуализация цен недвижимости
Файл parser.py отвечает за получение данных с сайта cian.ru.
Парсинг происходит по районам введенного города.

Список доступных городов:
1) St.Petersburg
2) Moscow
3) Ekaterinburg

Вводить название города при запуске parser.py нужно именно так, как указано в списке выше.

Данный скрипт строит две гистограммы, которые находятся в папке с названием города,
а также карту самого города в формате html. Открыв карту,
можно увидеть город с раскрашенными районами по цене за квадратный метр.

Запустив файл window.py, откроется оконное приложение для просмотра созданных гистограмм для каждого города.
