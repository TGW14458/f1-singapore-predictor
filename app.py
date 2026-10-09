import json
from pathlib import Path

import pandas as pd
import streamlit as st

try:
    import fastf1
except ImportError:
    fastf1 = None

BASE_DIR = Path(__file__).parent
SPRINT_CSV = BASE_DIR / "sprint_predictions.csv"
RACE_CSV = BASE_DIR / "singapore_grand_prix_top5.csv"
MODEL_FILE = BASE_DIR / "f1_best_model.pkl"
FEATURE_FILE = BASE_DIR / "f1_model_features.json"

st.set_page_config(page_title="Singapore F1 Top 5 Predictor", page_icon="🏎️", layout="wide")
st.title("🏎️ Singapore F1 Top 5 Predictor")
st.caption("A student machine-learning project. Predictions are estimates, not guaranteed race outcomes.")

left, right = st.columns(2)

with left:
    st.subheader("Singapore Sprint — provisional Top 5")
    if SPRINT_CSV.exists():
        sprint = pd.read_csv(SPRINT_CSV)
        st.dataframe(sprint, use_container_width=True, hide_index=True)
    else:
        st.info("No Sprint prediction CSV found yet. Export it from your Colab notebook and add it to this project folder.")

with right:
    st.subheader("Singapore Grand Prix — provisional Top 5")
    if RACE_CSV.exists():
        race = pd.read_csv(RACE_CSV)
        st.dataframe(race, use_container_width=True, hide_index=True)
    else:
        st.info("No Grand Prix prediction CSV found yet. Export it from your Colab notebook and add it to this project folder.")

st.divider()
st.subheader("Refresh Sprint Qualifying results")
st.write("When FastF1 has published the session data, use this button to retrieve the actual Sprint Qualifying classification. This is separate from the model's predicted Top 5.")

if st.button("Refresh Sprint Qualifying data", type="primary"):
    if fastf1 is None:
        st.error("FastF1 is not installed. Install the packages listed in requirements.txt.")
    else:
        try:
            cache_dir = BASE_DIR / "fastf1_cache"
            cache_dir.mkdir(exist_ok=True)
            fastf1.Cache.enable_cache(str(cache_dir))
            with st.spinner("Checking FastF1 for Singapore Sprint Qualifying results…"):
                session = fastf1.get_session(2026, "Singapore", "SQ")
                session.load(telemetry=False, weather=False, messages=False)
                results = session.results.copy()
            if results.empty:
                st.warning("Sprint Qualifying results are not available from FastF1 yet.")
            else:
                cols = [c for c in ["Position", "Abbreviation", "FullName", "TeamName"] if c in results.columns]
                results = results[cols].copy()
                if "Position" in results.columns:
                    results["Position"] = pd.to_numeric(results["Position"], errors="coerce")
                    results = results.sort_values("Position")
                st.success("Sprint Qualifying classification loaded.")
                st.dataframe(results, use_container_width=True, hide_index=True)
        except Exception as exc:
            st.error("Could not retrieve Sprint Qualifying results. The session may not be available yet, or FastF1 may have encountered a data/network issue.")
            st.caption(str(exc))

with st.expander("Project files and model status"):
    st.write("Model file present:", MODEL_FILE.exists())
    st.write("Feature-list file present:", FEATURE_FILE.exists())
    st.write("This starter website displays the prediction CSVs exported by your notebook. It does not retrain the model or create a new prediction automatically yet.")

st.caption("Built with Python, Streamlit, pandas and FastF1.")
