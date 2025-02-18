import os
import pickle
from typing import List
from datetime import datetime

import pandas as pd
from fastapi import FastAPI, Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from schema import PostGet

# Установка соединения с базой данных
DATABASE_URL = (
    "postgresql://robot-startml-ro:pheiph0hahj1Vaif@postgres.lab.karpov.courses:6432/startml"
)
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



# Функция для получения пути к модели
def get_model_path(path: str) -> str:
    if os.environ.get("IS_LMS") == "1":
        return "/workdir/user_input/model"
    return path

# Загрузка модели
def load_models():
    model_path = get_model_path("/my/super/path")
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
model = load_models()
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

@app.get("/post/recommendations/", response_model=List[PostGet])
def recommended_posts(id: int, time: datetime, limit: int = 5) -> List[PostGet]:
    # Загружаем данные о пользователе

    user_data = user[user['user_id'] == id]

    # Формируем данные для предсказания
    data = posts.join(user_data, how="cross")[
        ["city", "country", "text_y", "topic_y", "most_frequent_word_y",
         "gender","age", "exp_group", 'emb_0', 'emb_1', 'emb_2', 'emb_3', 'emb_4',
         "length_text", "max_tfidf",
         "has_numbers", "text_length_more1500", "cnt_actions", "os_iOS", "os_organic"]
    ]

    # Предсказания вероятностей
    data["pred"] = model.predict_proba(data)[:, 1]

    # Сортируем по вероятностям и выбираем топ-N
    data["post_id"] = posts["post_id"]
    top_posts = data.sort_values(by="pred", ascending=False).head(limit)
    indexes = list(top_posts["post_id"])

    # Получаем посты из pandas DataFrame по отобранным индексам
    query = posts[posts['post_id'].isin(indexes)]

    # Выбираем только нужные столбцы (id, text, topic)
    result = query[['post_id', 'text', 'topic']].rename(columns={'post_id': 'id'}).to_dict(orient='records')

    return result
