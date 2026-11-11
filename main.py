import streamlit as st
from llm import get_token
from llm import ask
import httpx

NUMBER_OPTIONS = {
    "1": "1",
    "2": "2",
    "4": "4",
    "6": "6",
}

FORMAT_OPTIONS = {
    "Список продуктов" : "Список продуктов",
    "Список продуктов + шаги" : "Список продуктов + шаги",
}

st.set_page_config(
    page_title="Рекомендации по приготовлению блюд",
    layout="centered",
)

st.title("Рекомендации по приготовлению блюд")
st.caption(
    "Укажите название блюда, количество персон и тип ответа — "
    "сервис подскажет список покупок"
)

with st.form("recommend_form"):
    current_dish = st.text_input(
        "Что приготовить *",
        placeholder="Например: рагу из говядины",
    )
    usage_label = st.selectbox(
        "Количество гостей *",
        options=list(NUMBER_OPTIONS.keys()),
    )
    list_of_products = st.selectbox(
        "Формат *",
        options=list(FORMAT_OPTIONS.keys()),
    )

    submitted = st.form_submit_button("🔍 Получить рекомендацию", type="primary")

if submitted:
    with st.spinner("Анализируем ваше блюдо и количество гостей, ожидайте ответа..."):
        prompt = f"Как приготовить {current_dish} для {NUMBER_OPTIONS[usage_label]} гостей? В ответе используйте формат {FORMAT_OPTIONS[list_of_products]}"
        if current_dish == "" or len(current_dish) > 50:
            st.error("Проверьте корректность введённых данных.")
        else:
            try:
                #token = get_token(url, key)
                response = ask(prompt)
            except httpx.ConnectError:
                st.error("Не удалось подключиться к API. Убедитесь, что сервер запущен.")
            except httpx.TimeoutException:
                st.error("Превышено время ожидания ответа. Попробуйте позже.")

            if response.status_code == 400 or response.status_code == 401 or response.status_code == 403 or response.status_code == 404:
                st.error("Проверьте корректность введённых данных.")
            elif response.status_code == 500 or response.status_code == 501 or response.status_code == 502 or response.status_code == 503 or response.status_code == 504:
                st.error("Проверьте подключение к сети.")
            else:
                st.divider()
                st.header("Результат")
                st.info(response.json()["choices"][0]["message"]["content"])