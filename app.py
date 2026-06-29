import streamlit as st
import json
from urllib.parse import quote, urlencode

st.set_page_config(
    page_title="SEMrush Filter URL Builder",
    page_icon="🔍",
    layout="centered"
)

st.markdown("""
    <style>
        .main { max-width: 760px; margin: auto; }
        .stTextArea textarea { font-size: 13px; }
        .url-box {
            background: #f0f4ff;
            border: 1px solid #c7d2fe;
            border-radius: 8px;
            padding: 14px 16px;
            font-family: monospace;
            font-size: 12px;
            word-break: break-all;
            color: #1e1b4b;
        }
        .tag-chip {
            display: inline-block;
            background: #e0e7ff;
            color: #3730a3;
            border-radius: 20px;
            padding: 2px 10px;
            margin: 2px 3px;
            font-size: 12px;
        }
        .counter {
            font-size: 13px;
            color: #6b7280;
            margin-bottom: 6px;
        }
    </style>
""", unsafe_allow_html=True)

st.title("🔍 SEMrush Filter URL Builder")
st.caption("Génère l'URL SEMrush avec exclusions de mots-clés en un clic.")

st.divider()

# --- Inputs ---
col1, col2 = st.columns([2, 1])
with col1:
    site_url = st.text_input(
        "URL du site (subfolder ou domaine)",
        value="https://www.berluti.com/fr-fr/",
        placeholder="https://www.example.com/fr-fr/"
    )
with col2:
    db = st.selectbox("Base de données", ["fr", "us", "uk", "de", "es", "it", "jp", "com"], index=0)

search_type = st.radio(
    "Type de recherche",
    ["subfolder", "domain", "subdomain"],
    horizontal=True,
    index=0
)

sort_field = st.selectbox(
    "Trier par",
    ["volume", "pos", "traffic", "trafficCost", "kd"],
    index=0
)

st.markdown("**Mots-clés à exclure** — séparés par `|`")
keywords_raw = st.text_area(
    label="Mots-clés à exclure",
    value="berluti|berlutti|berliti|berl",
    height=120,
    label_visibility="collapsed"
)

# --- Process keywords ---
keywords = [k.strip() for k in keywords_raw.split("|") if k.strip()]

if keywords:
    st.markdown(f'<div class="counter">{len(keywords)} mot(s)-clé(s) à exclure :</div>', unsafe_allow_html=True)
    chips_html = "".join(f'<span class="tag-chip">{k}</span>' for k in keywords[:60])
    if len(keywords) > 60:
        chips_html += f'<span class="tag-chip">+{len(keywords)-60} autres</span>'
    st.markdown(chips_html, unsafe_allow_html=True)

st.divider()

# --- Build URL ---
def build_semrush_url(site_url, keywords, db, search_type, sort_field):
    base = "https://www.semrush.com/analytics/organic/positions/"

    if not keywords:
        params = {
            "sortField": sort_field,
            "db": db,
            "q": site_url,
            "searchType": search_type
        }
        return base + "?" + "&".join(f"{k}={quote(str(v), safe='')}" for k, v in params.items())

    advanced = {}
    for i, kw in enumerate(keywords):
        advanced[str(i)] = {
            "inc": False,
            "fld": "phr",
            "cri": "containing",
            "val": kw
        }

    filter_obj = {
        "search": "",
        "volume": "",
        "positions": "",
        "positionsType": "all",
        "serpFeatures": None,
        "intent": [],
        "kd": "",
        "advanced": advanced
    }

    filter_json = json.dumps(filter_obj, ensure_ascii=False, separators=(',', ':'))
    filter_encoded = quote(filter_json, safe='')

    q_encoded = quote(site_url, safe='')

    url = (
        f"{base}?sortField={sort_field}"
        f"&filter={filter_encoded}"
        f"&db={db}"
        f"&q={q_encoded}"
        f"&searchType={search_type}"
    )
    return url


if st.button("✨ Générer l'URL", type="primary", use_container_width=True):
    if not site_url:
        st.warning("Merci d'entrer une URL de site.")
    else:
        final_url = build_semrush_url(site_url, keywords, db, search_type, sort_field)

        st.success(f"URL générée avec **{len(keywords)}** exclusion(s)")

        st.markdown("**URL finale :**")
        st.markdown(f'<div class="url-box">{final_url}</div>', unsafe_allow_html=True)

        st.code(final_url, language=None)

        st.markdown(
            f'<a href="{final_url}" target="_blank">'
            f'<button style="background:#4f46e5;color:white;border:none;padding:8px 20px;border-radius:6px;cursor:pointer;font-size:14px;">Ouvrir dans SEMrush ↗</button>'
            f'</a>',
            unsafe_allow_html=True
        )

st.divider()
st.caption("Outil local — aucune donnée envoyée. Compatible SEMrush Organic Positions.")
