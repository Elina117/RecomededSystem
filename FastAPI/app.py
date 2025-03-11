import os
import pickle
import hashlib
from typing import List
from datetime import datetime

import pandas as pd
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel

# Установка соединения с базой данных
DATABASE_URL = (
    "postgresql://robot-startml-ro:pheiph0hahj1Vaif@postgres.lab.karpov.courses:6432/startml"
)
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

salt = 'my_salt'
threshold = 50

#Функция для определения групп для A/B тестирования
def get_exp_group(user_id: int) -> str:
    hash_value = int(hashlib.md5((str(user_id) + salt).encode()).hexdigest(), 16)
    return 'control' if (hash_value % 100) < threshold else 'test'

class PostGet(BaseModel):
    id: int
    text: str
    topic: str

    class Config:
        orm_model = True

class Response(BaseModel):
    exp_group: str
    recommendations: List[PostGet]

# Функция для получения пути к модели
def get_model_path(model_version: str) -> str:
    if (
        os.environ.get("IS_LMS") == "1"
    ):  # проверяем где выполняется код в лмс, или локально. Немного магии
        model_path = f"/workdir/user_input/model_{model_version}"
    else:
        model_path = "your/path/to/model"
    return model_path

# Загрузка модели
def load_models(model_name: str):
    model_path = get_model_path(model_name)
    with open(model_path, "rb") as model_file:
        model = pickle.load(model_file)

    if not hasattr(model, "predict") or not hasattr(model, "predict_proba"):
        raise AttributeError(
            "Модель должна содержать методы 'predict' и 'predict_proba'."
        )
    return model

# Загрузка всех признаков из базы данных
def batch_load_sql(query: str) -> pd.DataFrame:
    CHUNKSIZE = 200000
    conn = engine.connect().execution_options(stream_results=True)
    chunks = []
    for chunk_dataframe in pd.read_sql(query, conn, chunksize=CHUNKSIZE):
        chunks.append(chunk_dataframe)
    conn.close()
    return pd.concat(chunks, ignore_index=True)

def load_features() -> pd.DataFrame:
    query = "SELECT * FROM public.elina_galimova_user"
    return batch_load_sql(query)

# Создание объекта FastAPI
app = FastAPI()

# Загрузка модели и данных
model_test = load_models("test")
model_control = load_models("control")

user = load_features()
posts = pd.read_sql(
    """
    SELECT * FROM public.elina_galimova_post
    """,
    engine,
)

# Функция для получения базы данных
def get_db():
    with SessionLocal() as db:
        yield db


@app.get("/post/recommendations/", response_model=Response)
def recommended_posts(id: int, time: datetime, limit: int = 5) -> Response:
    # Загружаем данные о пользователе
    exp_group = get_exp_group(id)

    user_data = user[user['user_id'] == id]

    if user_data.empty:
        raise ValueError("Пользователь не найден")

    # Формируем данные для предсказания
    data_test = posts.join(user_data, how="cross")[
        ["city", "country", "text_y", "topic_y", "most_frequent_word_y",
         "gender","age", "exp_group", 'emb_0', 'emb_1', 'emb_2', 'emb_3', 'emb_4',
         "length_text", "max_tfidf",
         "has_numbers", "text_length_more1500", "cnt_actions", "os_iOS", "os_organic"]
    ]

    data_control = posts.join(user_data, how="cross")[
        ["city", "country", "text_y", "topic_y", "most_frequent_word_y",
         "gender","age", "exp_group", "length_text", "max_tfidf",
         "has_numbers", "text_length_more1500", "cnt_actions", "os_iOS", "os_organic"]
    ]

    if exp_group == 'control':
        # Предсказания вероятностей
        data_control["pred"] = model_control.predict_proba(data_control)[:, 1]

        # Сортируем по вероятностям и выбираем топ-N
        data_control["post_id"] = posts["post_id"]
        top_posts = data_control.sort_values(by="pred", ascending=False).head(limit)
        indexes = list(top_posts["post_id"])

        # Получаем посты из pandas DataFrame по отобранным индексам
        query = posts[posts['post_id'].isin(indexes)]

        # Выбираем только нужные столбцы (id, text, topic)
        recommendations = query[['post_id', 'text', 'topic']].rename(columns={'post_id': 'id'}).to_dict(orient='records')

    elif exp_group == 'test':
        # Предсказания вероятностей
        data_test["pred"] = model_test.predict_proba(data_test)[:, 1]

        # Сортируем по вероятностям и выбираем топ-N
        data_test["post_id"] = posts["post_id"]
        top_posts = data_test.sort_values(by="pred", ascending=False).head(limit)
        indexes = list(top_posts["post_id"])

        # Получаем посты из pandas DataFrame по отобранным индексам
        query = posts[posts['post_id'].isin(indexes)]

        # Выбираем только нужные столбцы (id, text, topic)
        recommendations = query[['post_id', 'text', 'topic']].rename(columns={'post_id': 'id'}).to_dict(orient='records')
    else:
        raise ValueError('Неизвестная группа эксперимента')

    return Response(exp_group=exp_group, recommendations=recommendations)
