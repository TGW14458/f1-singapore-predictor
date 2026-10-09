# Singapore F1 Top 5 Predictor

## Run on your laptop

1. Install Python 3.11 or a compatible recent Python version.
2. Open PowerShell in this folder.
3. Install packages:

   ```powershell
   python -m pip install -r requirements.txt
   ```

4. Start the website:

   ```powershell
   python -m streamlit run app.py
   ```

5. Open the local address Streamlit prints (usually `http://localhost:8501`).

## Add your Colab prediction files

Download `singapore_sprint_top5.csv` and `singapore_grand_prix_top5.csv` from the final export cell in Colab, then place both files beside `app.py`.

The `f1_best_model.pkl` and `f1_model_features.json` files are not required for this first display-only version. The website currently displays the exported predictions and can separately retrieve Sprint Qualifying classification when FastF1 has the data.

## Important project limitation

The notebook currently copies the same provisional ranking into both the Sprint and Grand Prix tables. These should not be presented as independent session-specific predictions until separate logic/models are implemented.
