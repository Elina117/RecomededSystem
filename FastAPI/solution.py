import pandas as pd
from sqlalchemy import create_engine


engine = create_engine(
    "postgresql://robot-startml-ro:pheiph0hahj1Vaif@postgres.lab.karpov.courses:6432/startml"
)

# Проверяем соединение
try:
    with engine.connect() as conn:
        print("Connection successful!")
except Exception as e:
    print(f"Error connecting to database: {e}")

df = pd.read_sql('SELECT * FROM ildar_features_lesson_22', con=engine)


# Записываем DataFrame в таблицу (с перезаписью, если она уже существует)
df.to_sql('elina_galimova_fin_proj', con=engine, if_exists='replace', index=False)

# Считываем данные обратно в DataFrame
df = pd.read_sql('SELECT * FROM elina_galimova_fin_proj', con=engine)

# Печатаем считанные данные
print(df)