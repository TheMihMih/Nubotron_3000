# Nubotron_3000
<h1>Проект для ХАКАТОН ЕВРАЗА 2.0</h1>

<h2>Цифровой двойник эксгаустеров агломашины</h2>

Цель проекта: разработка веб-приложения, с помощью которого машинист эксгаустера сможет мониторить состояние эксгаустеров и прогнозировать их возможную поломку.

Основа работы сервиса - поток реальных данных с датчиков агрегата

---

<h2>В ходе выполнения проекта выполнялись следующие задачи:</h2>

1. Разработка сервиса для приема и сохранения потока данных с эксгаустера и предоставления интерфейса доступа к этим данным.

2. Разработка веб-интерфейса для рабочего места машиниста эксгаустера. Интерфейс должен позволять как минимум:

    - Отображать текущее состояние всех эксгаустеров на одном экране

    - Визуализировать детальные данные по конкретному эксгаустеру

    - Визуализировать поток данных во времени для анализа трендов

3. Разработка алгоритма определения даты замены ротора эксгаустера и отображение результатов его работы в веб-интерфейсе.

---

<h2>Запуск</h2>

    docker-compose up -d --build

---

<h2>Стек</h2>

<img src="images/postgres.png"  width="30%" height="30%">

<img src="images/fastapi.png"  width="30%" height="30%">

<img src="images/catboost.png"  width="30%" height="30%">

<img src="images/reactjs.png"  width="30%" height="30%">
