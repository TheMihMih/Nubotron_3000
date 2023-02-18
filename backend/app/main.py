from fastapi import FastAPI, Request, WebSocket
from fastapi.templating import Jinja2Templates
from kafka import KafkaConsumer, TopicPartition
import json
import psycopg2
import asyncio
from pydantic import BaseModel, StrictStr
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from aiokafka.helpers import create_ssl_context
from .consumer import add_data_in_db
from .pull_history import pull_history


app = FastAPI()

topic = 'zsmk-9433-dev-01'
loop = asyncio.get_event_loop()

context = create_ssl_context(
    cafile="app/CA.crt"
)

consumer = AIOKafkaConsumer(
    topic,
    group_id='Nubotron_3000',
    bootstrap_servers='rc1a-b5e65f36lm3an1d5.mdb.yandexcloud.net:9091',
    security_protocol="SASL_SSL",
    sasl_mechanism="SCRAM-SHA-512",
    sasl_plain_username='9433_reader',
    sasl_plain_password='eUIpgWu0PWTJaTrjhjQD3.hoyhntiK',
    ssl_context=context,
)


async def consume():
    await consumer.start()
    try:
        async for msg in consumer:
            my_bytes_value = msg.value
            my_json = my_bytes_value.decode('utf8').replace("'", '"')
            data = json.loads(my_json)
            date_time = str(data['moment'].replace('T', " ").split(".")[0])
            s = json.dumps(data, indent=4, sort_keys=True)
            add_data_in_db(date_time, s)
    finally:
        await consumer.stop()


@app.on_event("startup")
async def startup_event():
    await pull_history(topic)
    loop.create_task(consume())


@app.on_event("shutdown")
async def shutdown_event():
    await consumer.stop()


"/api/get_all_data/2023-02-18T18:17:31.749Z&2023-02-18T18:17:31.749Z&1h"
@app.get("/api/get_all_data/{start}{end}{interval}")
def get_all_data(request: Request) -> dict[str, float]:
    """Тут отдаем исторические данные"""
    conn = psycopg2.connect(
        host='db',
        port=5432,
        database="postgres",
        user="postgres",
        password="postgres",
    )
    start_date = start.replace("T", " ")[:16]
    finish_date = end.replace("T", " ")[:16]
    step = int(interval) if interval.endswith("m") else int(interval) * 60
    cur.execute(f"SELECT id from consumer_data where d_create::text like {start_date}")
    satrt_id = cur.fetchall()[0][0]
    cur.execute(f"SELECT id from consumer_data where d_create::text like {finish_date}")
    max_id = cur.fetchall()[0][0]
    ids = [range(satrt_id, max_id+1, step)]
    cur.execute(f"SELECT data from consumer_data where id in {ids}")

    return {"request": 200}


@app.get("/api/get_current_data")
def get_current_data():
    """Тут получаем актуальный последний из кафки и отдаем на фронт"""
    conn = psycopg2.connect(
        host='db',
        port=5432,
        database="postgres",
        user="postgres",
        password="postgres",
    )
    cur = conn.cursor()
    cur.execute("SELECT id, json FROM consumer_data ORDER BY consumer_data.id DESC LIMIT 1")
    data = cur.fetchall()
    conn.close()
    cur.close()
    return {"data": data}
