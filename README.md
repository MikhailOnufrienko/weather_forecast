## Weather Forecast App
### Приложение для справки о погоде (тестовое задание).

Приложение написано на Flask. Для хранения данных о пользователях и введенных городах используется Redis.
В Redis в качестве ключа выступает  IP адрес пользователя, значение - список введенных городов (используется для подсказок при последующем вводе и для сбора статистики).

1. Склонируйте репозиторий.
2. Переименуйте файл .env.example в .env и пропишите значение для переменной OPENCAGE_GEODATA_API_KEY (его можно получить, зарегистрировавшись с системе по адресу https://opencagedata.com/users/sign_up).
2. Перейдите в директорию weatherapp и выполните команду:

```
   docker-compose up --build -d
```

3. Зайдите в приложение по адресу:

```
   http://127.0.0.1:5000/
```

4. Введите название города. Приложение отобразит прогноз в выбранном городе на ближайшие сутки. При последующем вводе того же самого города приложение покажет подсказку (при условии что изначально название вводилось на английском языке; если вводить на русском, приложение покажет прогноз погоды, но правильная работа подсказок и статистики по городам не гарантируется).

5. Кнопка "Показать введенные города" отображает статистику по городам, прогноз погоды в которых смотрел данный пользователь. Отображаются города в отформатированном виде, то есть на английском языке вместе с названием страны и административной единицей - так, как они присылаются в ответе сервисом OpencageData (поэтому для корректной работы статистики желательно изначально указывать города на английском).

6. Тесты находятся в директории tests/. Перейдите в контейнер web командой:

```
docker-compose exec web bash
```

Запустите тесты:

```
pytest /tests
```
