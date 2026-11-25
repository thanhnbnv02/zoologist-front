from urllib.parse import urlencode

import requests
import streamlit as st

BASE_URL = "http://localhost:8000/predict"


def build_request_url() -> str:
    url_params = _ask_user()
    return f"{BASE_URL}?{urlencode(url_params)}"


def _ask_user() -> dict[str, str]:
    island = st.selectbox("Island", ["Biscoe", "Dream", "Torgersen"], index=0)
    bill_length = st.number_input("Bill Length (in mm)", value=1)
    bill_depth = st.number_input("Bill Depth (in mm)", value=1)
    flipper_length = st.number_input("Flipper Length (in mm)", value=1)
    body_mass = st.number_input("Body Mass (in g)", value=1)
    gender = st.selectbox("Gender", ["Male", "Female"], index=0)
    return {
        "island": island,
        "bill_length_mm": bill_length,
        "bill_depth_mm": bill_depth,
        "flipper_length_mm": flipper_length,
        "body_mass_g": body_mass,
        "sex": gender,
    }


def get_predictions(request_url) -> dict:
    response = requests.get(request_url)
    return response.json()


def main():
    st.title("Penguin Predictor")

    with st.form("penguin_form"):
        request_url = build_request_url()
        submitted = st.form_submit_button("Predict")

    if submitted:
        try:
            st.json(get_predictions(request_url))
        except requests.RequestException as e:
            st.error(f"Could not reach the prediction API: {e}")


main()
