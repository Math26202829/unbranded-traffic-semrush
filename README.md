# SEMrush Filter URL Builder

Streamlit app to generate SEMrush Organic Positions URLs with keyword exclusions.

## Usage

1. Enter the target site URL (e.g. `https://www.berluti.com/fr-fr/`)
2. Paste your exclusion keywords separated by `|`
3. Click **Générer l'URL** → copy or open directly in SEMrush

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy on Streamlit Community Cloud

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repo and set `app.py` as the entry point
4. Deploy — no secrets or env vars needed
