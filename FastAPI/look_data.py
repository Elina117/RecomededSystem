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

#df = pd.read_sql('SELECT * FROM ildar_features_lesson_22', con=engine)

#df_post = pd.read_csv('post_data3.csv')
#df_user = pd.read_csv('user_data2.csv')

# # Записываем DataFrame в таблицу (с перезаписью, если она уже существует)
#df_user.to_sql('elina_galimova_user', con=engine, if_exists='replace', index=False)
#df_post.to_sql('elina_galimova_post', con=engine, if_exists='replace', index=False)
# # Считываем данные обратно в DataFrame
#df_user = pd.read_sql('SELECT * FROM elina_galimova_user', con=engine)
df_post = pd.read_sql('SELECT * FROM elina_galimova_post', con=engine)
# Печатаем считанные данные
print(df_post)

