# notify_service
Notification Service with fastream and rabbitmq. 

# Настройка языка
1) Извлечь строки из шаблонов → POT
    pybabel extract -F babel.cfg -o locale/messages.pot .
2) Инициализировать локали (один раз на язык)
    pybabel init -i locale/messages.pot -d locale -l en
    pybabel init -i locale/messages.pot -d locale -l ro
    pybabel init -i locale/messages.pot -d locale -l ru
3) Перевести строки в .po
   Открой messages.po и заполни msgstr "" для каждого msgid.

4) Скомпилировать .po → .mo (для рантайма)
   pybabel compile -d locale
   Получишь messages.mo рядом с .po.

5) Обновлять при изменении шаблонов
   Когда меняешь шаблоны, повторяй:
   pybabel extract -F babel.cfg -o locale/messages.pot .
   pybabel update -i locale/messages.pot -d locale
   pybabel compile -d locale
