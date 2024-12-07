import os
import pickle


def get_model_path(path: str) -> str:
    # Проверяем, где выполняется код (в LMS или локально)
    if os.environ.get("IS_LMS") == "1":
        # Путь для LMS
        MODEL_PATH = '/workdir/user_input/model'
    else:
        # Путь для локального выполнения
        MODEL_PATH = path
    return MODEL_PATH


def load_models():
    # Получаем путь к модели
    model_path = get_model_path("/my/super/path")

    # Открываем файл с моделью для чтения
    with open(model_path, 'rb') as model_file:
        model = pickle.load(model_file)

    # Проверяем, что модель имеет необходимые методы
    if not hasattr(model, 'predict') or not hasattr(model, 'predict_proba'):
        raise AttributeError("Модель должна содержать методы 'predict' и 'predict_proba'.")

    return model
