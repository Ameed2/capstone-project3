"""
Olist Delivery Intelligence Dashboard
======================================
Streamlit app — Geographic Maps Section
Run:  streamlit run app.py
"""

import json
import math
import warnings
import urllib.request
import base64
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import folium
from folium.plugins import HeatMap
import streamlit as st
import streamlit.components.v1 as components

warnings.filterwarnings("ignore")

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Olist · Delivery Intelligence",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Brand colours (from Olist website) ────────────────────────────────────────
OLIST_BLUE   = "#0A4EE4"
OLIST_DARK   = "#0B1B4D"
OLIST_ACCENT = "#E84A2F"   # red-orange dot from logo
OLIST_TEAL   = "#8DD7D7"
OLIST_LIGHT  = "#F4F7FF"
OLIST_GREY   = "#6B7A99"

# ── Global CSS — Olist brand feel ──────────────────────────────────────────────
st.markdown(f"""
<style>
/* ── Google Font ── */
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

/* ── Root reset ── */
html, body, [class*="css"] {{
    font-family: 'Plus Jakarta Sans', sans-serif;
}}

/* ── Main background ── */
.stApp {{
    background: {OLIST_LIGHT};
}}

/* ── Sidebar ── */
[data-testid="stSidebar"] {{
    background: {OLIST_DARK} !important;
    border-right: 1px solid rgba(255,255,255,0.07);
}}
[data-testid="stSidebar"] * {{
    color: rgba(255,255,255,0.85) !important;
}}
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stMultiSelect label {{
    color: {OLIST_TEAL} !important;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}}
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {{
    color: rgba(255,255,255,0.55) !important;
    font-size: 0.8rem;
}}

/* ── Sidebar selectbox / multiselect ── */
[data-testid="stSidebar"] .stSelectbox > div > div,
[data-testid="stSidebar"] .stMultiSelect > div > div {{
    background: rgba(255,255,255,0.07) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    color: white !important;
    border-radius: 8px;
}}

/* ── Divider in sidebar ── */
[data-testid="stSidebar"] hr {{
    border-color: rgba(255,255,255,0.1);
}}

/* ── KPI metric cards ── */
.kpi-row {{
    display: flex;
    gap: 16px;
    margin-bottom: 28px;
    flex-wrap: wrap;
}}
.kpi-card {{
    flex: 1;
    min-width: 160px;
    background: white;
    border-radius: 14px;
    padding: 20px 24px;
    border: 1px solid rgba(10,78,228,0.1);
    box-shadow: 0 2px 12px rgba(10,78,228,0.06);
    transition: box-shadow 0.2s;
    position: relative;
    overflow: hidden;
}}
.kpi-card::before {{
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, {OLIST_BLUE}, {OLIST_TEAL});
}}
.kpi-card.alert::before {{
    background: linear-gradient(90deg, {OLIST_ACCENT}, #ff8c69);
}}
.kpi-label {{
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: {OLIST_GREY};
    margin-bottom: 6px;
}}
.kpi-value {{
    font-size: 2rem;
    font-weight: 800;
    color: {OLIST_DARK};
    line-height: 1;
    margin-bottom: 4px;
}}
.kpi-value.danger {{
    color: {OLIST_ACCENT};
}}
.kpi-sub {{
    font-size: 0.75rem;
    color: {OLIST_GREY};
}}

/* ── Section header ── */
.section-header {{
    display: flex;
    align-items: center;
    gap: 12px;
    margin: 32px 0 16px;
    padding-bottom: 12px;
    border-bottom: 2px solid rgba(10,78,228,0.1);
}}
.section-icon {{
    width: 36px;
    height: 36px;
    border-radius: 10px;
    background: linear-gradient(135deg, {OLIST_BLUE}, {OLIST_TEAL});
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1rem;
    flex-shrink: 0;
}}
.section-title {{
    font-size: 1.1rem;
    font-weight: 700;
    color: {OLIST_DARK};
    margin: 0;
}}
.section-desc {{
    font-size: 0.78rem;
    color: {OLIST_GREY};
    margin: 0;
}}

/* ── Map card wrapper ── */
.map-card {{
    background: white;
    border-radius: 16px;
    border: 1px solid rgba(10,78,228,0.08);
    box-shadow: 0 4px 24px rgba(10,78,228,0.06);
    overflow: hidden;
    margin-bottom: 20px;
}}
.map-card-header {{
    padding: 16px 20px;
    background: {OLIST_DARK};
    display: flex;
    align-items: center;
    gap: 10px;
}}
.map-badge {{
    background: {OLIST_BLUE};
    color: white;
    font-size: 0.65rem;
    font-weight: 700;
    padding: 3px 9px;
    border-radius: 20px;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}}
.map-card-title {{
    font-size: 0.9rem;
    font-weight: 600;
    color: white;
    margin: 0;
}}
.map-card-subtitle {{
    font-size: 0.72rem;
    color: rgba(255,255,255,0.5);
    margin: 0;
}}

/* ── Top header bar ── */
.top-header {{
    background: {OLIST_DARK};
    border-radius: 16px;
    padding: 24px 32px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 28px;
    border: 1px solid rgba(255,255,255,0.06);
    box-shadow: 0 8px 32px rgba(11,27,77,0.2);
    position: relative;
    overflow: hidden;
}}
.top-header::after {{
    content: '';
    position: absolute;
    top: -40px; right: -40px;
    width: 200px; height: 200px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(10,78,228,0.25) 0%, transparent 70%);
}}
.top-header-logo {{
    display: flex;
    align-items: center;
    gap: 14px;
}}
.logo-dot {{
    width: 42px; height: 42px;
    border-radius: 50%;
    background: white;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.1rem;
    font-weight: 900;
    color: {OLIST_BLUE};
    box-shadow: 0 0 0 4px rgba(10,78,228,0.3);
}}
.header-title {{
    font-size: 1.4rem;
    font-weight: 800;
    color: white;
    margin: 0;
}}
.header-sub {{
    font-size: 0.78rem;
    color: rgba(255,255,255,0.45);
    margin: 0;
    margin-top: 2px;
}}
.status-pill {{
    background: rgba(141,215,215,0.15);
    border: 1px solid rgba(141,215,215,0.3);
    border-radius: 20px;
    padding: 6px 14px;
    font-size: 0.75rem;
    color: {OLIST_TEAL};
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 6px;
}}
.dot-live {{
    width: 7px; height: 7px;
    border-radius: 50%;
    background: {OLIST_TEAL};
    animation: pulse 2s infinite;
}}
@keyframes pulse {{
    0%, 100% {{ opacity: 1; transform: scale(1); }}
    50%        {{ opacity: 0.5; transform: scale(1.3); }}
}}

/* ── Insight chips ── */
.insight-row {{
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    margin-top: 8px;
    margin-bottom: 20px;
}}
.chip {{
    background: white;
    border: 1px solid rgba(10,78,228,0.12);
    border-radius: 8px;
    padding: 8px 14px;
    font-size: 0.75rem;
    color: {OLIST_DARK};
    font-weight: 500;
    box-shadow: 0 1px 4px rgba(10,78,228,0.05);
}}
.chip b {{ color: {OLIST_BLUE}; }}
.chip.alert b {{ color: {OLIST_ACCENT}; }}

/* ── Hide streamlit chrome (keep header for sidebar toggle) ── */
#MainMenu, footer {{ visibility: hidden; }}
.block-container {{ padding-top: 1.5rem; padding-bottom: 2rem; }}

/* ── Plotly chart border ── */
.js-plotly-plot {{ border-radius: 0 0 14px 14px; }}
</style>
""", unsafe_allow_html=True)


def inject_sidebar_quick_toggle():
    """Add a quick floating button to reopen sidebar when collapsed."""
    components.html(
        """
        <script>
        const doc = window.parent.document;
        if (!doc) { return; }

        if (!doc.getElementById("quick-open-sidebar-btn")) {
          const btn = doc.createElement("button");
          btn.id = "quick-open-sidebar-btn";
          btn.innerText = "☰ Open Filters";
          Object.assign(btn.style, {
            position: "fixed",
            left: "12px",
            top: "72px",
            zIndex: "10000",
            background: "#0A4EE4",
            color: "white",
            border: "none",
            borderRadius: "10px",
            padding: "8px 12px",
            fontSize: "12px",
            fontWeight: "700",
            cursor: "pointer",
            boxShadow: "0 4px 12px rgba(10,78,228,0.35)",
            display: "none"
          });
          btn.onclick = () => {
            const openBtn =
              doc.querySelector('[data-testid="stSidebarCollapsedControl"] button') ||
              doc.querySelector('button[aria-label="Open sidebar"]') ||
              doc.querySelector('button[title="Open sidebar"]') ||
              doc.querySelector('[data-testid="stSidebarCollapsedControl"]');
            if (openBtn) { openBtn.click(); }
          };
          doc.body.appendChild(btn);
        }

        const quickBtn = doc.getElementById("quick-open-sidebar-btn");
        const sync = () => {
          const collapsedControl = doc.querySelector('[data-testid="stSidebarCollapsedControl"]');
          quickBtn.style.display = collapsedControl ? "inline-flex" : "none";
        };
        sync();
        setTimeout(sync, 400);
        setTimeout(sync, 1200);
        </script>
        """,
        height=0,
    )


inject_sidebar_quick_toggle()


# ══════════════════════════════════════════════════════════════════════════════
# DATA & GEO
# ══════════════════════════════════════════════════════════════════════════════

STATE_COORDS = {
    "AC": (-70.812, -9.977),  "AL": (-36.954, -9.571),
    "AP": (-51.066,  1.413),  "AM": (-64.649, -3.119),
    "BA": (-41.722,-12.970),  "CE": (-39.333, -5.498),
    "DF": (-47.929,-15.780),  "ES": (-40.338,-19.183),
    "GO": (-49.632,-15.827),  "MA": (-45.289, -5.420),
    "MT": (-56.097,-12.681),  "MS": (-54.529,-20.777),
    "MG": (-44.698,-18.512),  "PA": (-52.291, -3.415),
    "PB": (-36.834, -7.240),  "PR": (-51.615,-24.895),
    "PE": (-37.862, -8.814),  "PI": (-42.811, -8.077),
    "RJ": (-43.397,-22.908),  "RN": (-36.524, -5.811),
    "RS": (-51.218,-30.034),  "RO": (-63.319,-10.830),
    "RR": (-61.328,  1.990),  "SC": (-50.488,-27.248),
    "SP": (-48.549,-22.250),  "SE": (-37.441,-10.575),
    "TO": (-48.295,-10.175),
}

STATE_NAMES = {
    "AC":"Acre","AL":"Alagoas","AP":"Amapá","AM":"Amazonas","BA":"Bahia",
    "CE":"Ceará","DF":"Distrito Federal","ES":"Espírito Santo","GO":"Goiás",
    "MA":"Maranhão","MT":"Mato Grosso","MS":"Mato Grosso do Sul",
    "MG":"Minas Gerais","PA":"Pará","PB":"Paraíba","PR":"Paraná",
    "PE":"Pernambuco","PI":"Piauí","RJ":"Rio de Janeiro","RN":"Rio G. do Norte",
    "RS":"Rio G. do Sul","RO":"Rondônia","RR":"Roraima","SC":"Santa Catarina",
    "SP":"São Paulo","SE":"Sergipe","TO":"Tocantins",
}

GEOJSON_URL = (
    "https://raw.githubusercontent.com/codeforamerica/"
    "click_that_hood/master/public/data/brazil-states.geojson"
)

@st.cache_data(show_spinner=False)
def load_geojson():
    try:
        with urllib.request.urlopen(GEOJSON_URL, timeout=12) as r:
            return json.loads(r.read())
    except Exception:
        return None


@st.cache_data(show_spinner=False)
def get_logo_data_uri():
    base = Path(__file__).resolve().parent.parent
    candidates = [
        base / "assets" / "mangoli.jpeg",
        base / "assets" / "mangoli.jpg",
        base / "assets" / "mangoli.png",
    ]
    for logo_path in candidates:
        if logo_path.exists():
            suffix = logo_path.suffix.lower()
            mime = "image/png" if suffix == ".png" else "image/jpeg"
            encoded = base64.b64encode(logo_path.read_bytes()).decode("ascii")
            return f"data:{mime};base64,{encoded}"
    return None


@st.cache_data(show_spinner=False)
def load_data():
    base = Path(__file__).resolve().parent.parent
    path = base / "data" / "processed"
    date_cols = [
        "order_purchase_timestamp","order_approved_at",
        "order_delivered_carrier_date","order_delivered_customer_date",
        "order_estimated_delivery_date",
    ]
    try:
        df    = pd.read_csv(path / "olist_merged.csv",   parse_dates=date_cols)
        items = pd.read_csv(path / "items_enriched.csv")
        items_geo = items.merge(
            df[["order_id","is_late","customer_state","customer_city",
                "order_purchase_timestamp"]],
            on="order_id", how="inner"
        )
        return df, items_geo, None
    except FileNotFoundError as e:
        return None, None, str(e)

def _add_coords(df_in, state_col, lon_col="lon", lat_col="lat"):
    df_out = df_in.copy()
    df_out[[lon_col, lat_col]] = (
        df_out[state_col]
        .map(lambda s: STATE_COORDS.get(s, (None, None)))
        .apply(pd.Series)
    )
    return df_out.dropna(subset=[lon_col, lat_col])


# ══════════════════════════════════════════════════════════════════════════════
# MAP BUILDERS
# ══════════════════════════════════════════════════════════════════════════════

def make_map1_choropleth(df_f, brazil_geo):
    """MAP 1 — Late Rate Choropleth + Volume Bubbles"""
    ss = (
        df_f.groupby("customer_state")
        .agg(n_orders=("order_id","count"), late_rate=("is_late","mean"))
        .reset_index()
    )
    ss = _add_coords(ss, "customer_state")
    ss["late_pct"]   = (ss["late_rate"]*100).round(2)
    ss["state_name"] = ss["customer_state"].map(STATE_NAMES)

    choro = go.Choropleth(
        geojson      = brazil_geo,
        locations    = ss["customer_state"],
        z            = ss["late_pct"],
        featureidkey = "properties.sigla",
        colorscale   = [
            [0.00, "#1a9641"], [0.20, "#a6d96a"],
            [0.55, "#fdae61"], [1.00, "#d7191c"],
        ],
        zmin=0, zmax=20,
        colorbar=dict(
            title=dict(text="Late Rate (%)", font=dict(size=11, color="white")),
            tickfont=dict(color="white", size=10),
            len=0.55, y=0.38, x=1.01,
            bgcolor="rgba(11,27,77,0.6)",
            bordercolor="rgba(255,255,255,0.1)", borderwidth=1,
        ),
        hovertemplate=(
            "<b>%{location} — %{customdata[0]}</b><br>"
            "Late Rate: <b>%{z:.1f}%</b><br>"
            "Orders: %{customdata[1]:,}<extra></extra>"
        ),
        customdata=ss[["state_name","n_orders"]].values,
        name="Late Rate",
    )

    bubble = go.Scattergeo(
        lon=ss["lon"], lat=ss["lat"],
        hovertemplate=(
            "<b>%{customdata[0]}</b><br>"
            "Orders: <b>%{customdata[1]:,}</b><br>"
            "Late: <b>%{customdata[2]:.1f}%</b><extra></extra>"
        ),
        customdata=ss[["state_name","n_orders","late_pct"]].values,
        marker=dict(
            size       = np.sqrt(ss["n_orders"]) / 5.5,
            color      = ss["late_pct"],
            colorscale = "RdYlGn_r",
            cmin=0, cmax=20,
            opacity    = 0.78,
            line_color = "white",
            line_width = 1.5,
            showscale  = False,
        ),
        name="Volume",
    )

    fig = go.Figure(data=[choro, bubble])
    fig.update_layout(
        geo=dict(
            scope="south america",
            showland=True,  landcolor="#0B1B4D",
            showocean=True, oceancolor="#06112e",
            showcountries=True, countrycolor="rgba(255,255,255,0.12)",
            showlakes=False,
            fitbounds="locations",
            projection_type="mercator",
            bgcolor="#06112e",
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor ="rgba(0,0,0,0)",
        font=dict(family="Plus Jakarta Sans", color="white"),
        margin=dict(l=0, r=0, t=0, b=0),
        height=520,
        legend=dict(
            font=dict(color="white", size=10),
            bgcolor="rgba(11,27,77,0.6)",
            bordercolor="rgba(255,255,255,0.1)", borderwidth=1,
            x=0.01, y=0.99,
        ),
    )
    return fig


def make_map2_routes(items_geo_f, top_n=120):
    """MAP 2 — Shipping Route Arcs (dark theme)"""
    corridor = (
        items_geo_f.groupby(["seller_state","customer_state"])
        .agg(n_orders=("order_id","nunique"), late_rate=("is_late","mean"))
        .reset_index()
    )
    corridor = _add_coords(corridor, "seller_state", "s_lon","s_lat")
    corridor = _add_coords(corridor, "customer_state","c_lon","c_lat")
    corridor["late_pct"] = (corridor["late_rate"]*100).round(2)

    w_min, w_max = corridor["n_orders"].min(), corridor["n_orders"].max()
    corridor["lw"] = 0.8 + 10*(corridor["n_orders"]-w_min)/(w_max-w_min+1)

    def _color(p, vmax=25):
        t = max(0, min(1, p/vmax))
        r = int(232*t);  g = int(220*(1-t))
        return f"rgba({r},{g},80,0.7)"

    top = corridor.nlargest(top_n, "n_orders")

    traces = []
    for _, row in top.iterrows():
        traces.append(go.Scattergeo(
            lon=[row["s_lon"], row["c_lon"]],
            lat=[row["s_lat"], row["c_lat"]],
            mode="lines",
            line=dict(width=row["lw"], color=_color(row["late_pct"])),
            hovertext=(
                f"<b>{row['seller_state']} → {row['customer_state']}</b><br>"
                f"Orders: {row['n_orders']:,}  |  Late: {row['late_pct']:.1f}%"
            ),
            hoverinfo="text",
            showlegend=False,
        ))

    # Seller hub dots
    hubs = (
        items_geo_f.groupby("seller_state")
        .agg(n=("seller_id","nunique"), lr=("is_late","mean"))
        .reset_index()
    )
    hubs = _add_coords(hubs, "seller_state","s_lon","s_lat")

    traces.append(go.Scattergeo(
        lon=hubs["s_lon"], lat=hubs["s_lat"],
        mode="markers",
        marker=dict(size=9, color=OLIST_TEAL, symbol="square",
                    line_color="white", line_width=1),
        hovertext=hubs.apply(
            lambda r: f"<b>Seller hub: {r['seller_state']}</b><br>"
                      f"Sellers: {r['n']:,}  |  Late: {r['lr']*100:.1f}%", axis=1),
        hoverinfo="text",
        name="Seller Hub",
    ))

    # Invisible colorbar for legend
    traces.append(go.Scattergeo(
        lon=[None], lat=[None], mode="markers",
        marker=dict(
            colorscale=[[0,"#3abd60"],[0.5,"#f7dc6f"],[1,"#c0392b"]],
            cmin=0, cmax=25, color=[0],
            colorbar=dict(
                title=dict(text="Late Rate (%)", font=dict(size=11,color="white")),
                tickfont=dict(color="white", size=10),
                len=0.5, y=0.35, x=1.01,
                bgcolor="rgba(11,27,77,0.6)",
                bordercolor="rgba(255,255,255,0.1)", borderwidth=1,
            ),
            showscale=True, size=0,
        ),
        showlegend=False, hoverinfo="none",
    ))

    fig = go.Figure(data=traces)
    fig.update_layout(
        geo=dict(
            scope="south america",
            showland=True,  landcolor="#141428",
            showocean=True, oceancolor="#06080f",
            showcountries=True, countrycolor="rgba(141,215,215,0.2)",
            fitbounds="locations", projection_type="mercator",
            bgcolor="#06080f",
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Plus Jakarta Sans", color="white"),
        legend=dict(
            font=dict(color="white", size=10),
            bgcolor="rgba(11,27,77,0.7)",
            bordercolor="rgba(255,255,255,0.1)", borderwidth=1,
            x=0.01, y=0.99,
        ),
        margin=dict(l=0, r=0, t=0, b=0),
        height=520,
    )
    return fig


def make_map3_sellers(items_geo_f):
    """MAP 3 — Seller Risk Bubble Map"""
    ss = (
        items_geo_f.groupby(["seller_id","seller_state"])
        .agg(n_orders=("order_id","nunique"),
             late_rate=("is_late","mean"),
             n_late=("is_late","sum"))
        .reset_index()
    )
    ss = ss[ss["n_orders"] >= 10].copy()
    ss = _add_coords(ss, "seller_state","s_lon","s_lat")
    rng = np.random.default_rng(42)
    ss["s_lon"] += rng.uniform(-1.2, 1.2, len(ss))
    ss["s_lat"] += rng.uniform(-1.2, 1.2, len(ss))
    ss["late_pct"] = (ss["late_rate"]*100).round(2)
    ss["seller_short"] = ss["seller_id"].str[:10] + "…"

    fig = px.scatter_geo(
        ss, lat="s_lat", lon="s_lon",
        size="n_orders", color="late_pct",
        color_continuous_scale=[
            [0.0,"#1a9641"],[0.4,"#a6d96a"],
            [0.7,"#fdae61"],[1.0,"#d7191c"],
        ],
        range_color=[0, 35],
        size_max=40,
        hover_name="seller_short",
        hover_data={
            "seller_state": True,
            "n_orders":     True,
            "late_pct":     ":.1f",
            "n_late":       True,
            "s_lat": False, "s_lon": False,
        },
        labels={
            "late_pct":     "Late Rate (%)",
            "n_orders":     "Orders",
            "n_late":       "Late Orders",
            "seller_state": "State",
        },
        scope="south america",
    )
    fig.update_geos(
        showland=True,  landcolor="#0B1B4D",
        showocean=True, oceancolor="#06112e",
        showcountries=True, countrycolor="rgba(255,255,255,0.1)",
        fitbounds="locations", projection_type="mercator",
        bgcolor="#06112e",
    )
    fig.update_coloraxes(colorbar=dict(
        title=dict(text="Late Rate (%)", font=dict(size=11, color="white")),
        tickfont=dict(color="white", size=10),
        len=0.55, y=0.38, x=1.01,
        bgcolor="rgba(11,27,77,0.6)",
        bordercolor="rgba(255,255,255,0.1)", borderwidth=1,
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Plus Jakarta Sans", color="white"),
        margin=dict(l=0, r=0, t=0, b=0),
        height=520,
    )
    return fig


def make_map4_folium(df_f):
    """MAP 4 — Folium Heatmap (all vs late orders)"""
    merged = df_f.merge(
        pd.DataFrame([
            {"customer_state": k, "lat": v[1], "lon": v[0]}
            for k, v in STATE_COORDS.items()
        ]),
        on="customer_state", how="left",
    ).dropna(subset=["lat","lon"])

    m = folium.Map(
        location=[-14.235, -51.925], zoom_start=4,
        tiles="CartoDB dark_matter", prefer_canvas=True,
    )

    # All orders
    fg_all = folium.FeatureGroup(name="🔵  All Orders — Density", show=True)
    HeatMap(
        merged[["lat","lon"]].values.tolist(),
        radius=28, blur=22, max_zoom=8,
        gradient={"0.2":"#0A4EE4","0.6":"#8DD7D7","1.0":"#ffffff"},
        min_opacity=0.35,
    ).add_to(fg_all)
    fg_all.add_to(m)

    # Late only
    fg_late = folium.FeatureGroup(name="🔴  Late Orders — Density", show=False)
    late_pts = merged.loc[merged["is_late"]==1, ["lat","lon"]].values.tolist()
    if late_pts:
        HeatMap(
            late_pts,
            radius=28, blur=22, max_zoom=8,
            gradient={"0.2":"#E84A2F","0.6":"#ff6b35","1.0":"#ffffff"},
            min_opacity=0.45,
        ).add_to(fg_late)
    fg_late.add_to(m)

    # State markers
    fg_pins = folium.FeatureGroup(name="📊  State Stats", show=True)
    ss = (
        df_f.groupby("customer_state")
        .agg(n=("order_id","count"), lr=("is_late","mean"))
        .reset_index()
    )
    for _, row in ss.iterrows():
        coord = STATE_COORDS.get(row["customer_state"])
        if not coord:
            continue
        pct = row["lr"]*100
        col = "#d7191c" if pct>=15 else ("#fdae61" if pct>=10 else "#1a9641")
        folium.CircleMarker(
            location=[coord[1], coord[0]],
            radius=max(6, math.sqrt(row["n"])/28),
            color="white", weight=1.5,
            fill=True, fill_color=col, fill_opacity=0.82,
            tooltip=folium.Tooltip(
                f"<b style='font-family:sans-serif'>{row['customer_state']} — "
                f"{STATE_NAMES.get(row['customer_state'],'')} </b><br>"
                f"Orders: {row['n']:,}<br>"
                f"Late Rate: <b style='color:{col}'>{pct:.1f}%</b>",
            ),
        ).add_to(fg_pins)
    fg_pins.add_to(m)

    folium.LayerControl(collapsed=False, position="topright").add_to(m)

    # Watermark title
    title_html = f"""
    <div style="position:fixed;bottom:12px;left:12px;z-index:9999;
         background:rgba(11,27,77,0.88);color:white;
         padding:8px 14px;border-radius:10px;
         font-family:'Plus Jakarta Sans',sans-serif;font-size:12px;
         border:1px solid rgba(255,255,255,0.12);">
      <b>Olist</b> · Delivery Heatmap &nbsp;|&nbsp;
      Toggle layers using the control →
    </div>"""
    m.get_root().html.add_child(folium.Element(title_html))
    return m


def make_order_route_map(seller_state, customer_state, risk_pct):
    """Single-order route preview (state centroid to state centroid)."""
    s_coord = STATE_COORDS.get(seller_state)
    c_coord = STATE_COORDS.get(customer_state)
    if not s_coord or not c_coord:
        return None

    color = "#1a9641" if risk_pct < 10 else ("#fdae61" if risk_pct < 20 else "#d7191c")
    fig = go.Figure()
    fig.add_trace(go.Scattergeo(
        lon=[s_coord[0], c_coord[0]],
        lat=[s_coord[1], c_coord[1]],
        mode="lines+markers",
        line=dict(width=6, color=color),
        marker=dict(size=[10, 12], color=[OLIST_TEAL, OLIST_ACCENT]),
        hovertemplate="<extra></extra>",
        showlegend=False,
    ))
    fig.update_layout(
        title=f"Route Preview: {seller_state} → {customer_state}",
        geo=dict(
            scope="south america",
            showland=True, landcolor="#0B1B4D",
            showocean=True, oceancolor="#06112e",
            showcountries=True, countrycolor="rgba(255,255,255,0.12)",
            fitbounds="locations", projection_type="mercator",
            bgcolor="#06112e",
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        margin=dict(l=0, r=0, t=55, b=0),
        height=420,
    )
    return fig


def quarter_label(q_value):
    """Convert 'YYYYQn' to a human-friendly month range label."""
    month_map = {"Q1": "Jan-Mar", "Q2": "Apr-Jun", "Q3": "Jul-Sep", "Q4": "Oct-Dec"}
    q_str = str(q_value)
    if "Q" not in q_str:
        return q_str
    year = q_str[:4]
    q_part = q_str[-2:]
    return f"{month_map.get(q_part, q_part)} {year}"


def state_distance_km(state_a, state_b):
    """Haversine distance between state centroids (km)."""
    a = STATE_COORDS.get(state_a)
    b = STATE_COORDS.get(state_b)
    if not a or not b:
        return np.nan
    lon1, lat1 = a
    lon2, lat2 = b
    r = 6371.0
    p1, p2 = np.radians(lat1), np.radians(lat2)
    dphi = np.radians(lat2 - lat1)
    dlmb = np.radians(lon2 - lon1)
    h = np.sin(dphi / 2) ** 2 + np.cos(p1) * np.cos(p2) * np.sin(dlmb / 2) ** 2
    return float(2 * r * np.arctan2(np.sqrt(h), np.sqrt(1 - h)))


def distance_bin_from_km(distance_km):
    if pd.isna(distance_km):
        return "unknown"
    if distance_km <= 300:
        return "0-300km"
    if distance_km <= 700:
        return "300-700km"
    if distance_km <= 1200:
        return "700-1200km"
    if distance_km <= 3000:
        return "1200-3000km"
    return "3000km+"


def _mode_or_unknown(series):
    s = series.dropna().astype(str)
    if s.empty:
        return "unknown"
    m = s.mode()
    return str(m.iloc[0]) if not m.empty else str(s.iloc[0])


@st.cache_data(show_spinner=False)
def build_eta_profiles(df_raw, items_geo_raw):
    """Build hierarchical historical ETA profiles with category + distance."""
    category_col = (
        "product_category_name_english"
        if "product_category_name_english" in items_geo_raw.columns
        else ("product_category_name" if "product_category_name" in items_geo_raw.columns else None)
    )

    base = df_raw[
        ["order_id", "order_purchase_timestamp", "order_delivered_customer_date", "customer_state", "customer_city"]
    ].copy()
    base["lead_days"] = (
        base["order_delivered_customer_date"] - base["order_purchase_timestamp"]
    ).dt.days
    base = base[base["lead_days"].between(1, 120, inclusive="both")].copy()

    if category_col:
        order_items = (
            items_geo_raw[["order_id", "seller_state", category_col]]
            .groupby("order_id", as_index=False)
            .agg(
                seller_state=("seller_state", _mode_or_unknown),
                category=(category_col, _mode_or_unknown),
            )
        )
    else:
        order_items = (
            items_geo_raw[["order_id", "seller_state"]]
            .groupby("order_id", as_index=False)
            .agg(seller_state=("seller_state", _mode_or_unknown))
        )
        order_items["category"] = "unknown"

    base = base.merge(order_items, on="order_id", how="left")
    base["seller_state"] = base["seller_state"].fillna("unknown")
    base["category"] = base["category"].fillna("unknown")
    base["month"] = base["order_purchase_timestamp"].dt.month
    base["state_distance_km"] = [
        state_distance_km(s, c)
        for s, c in zip(base["seller_state"], base["customer_state"])
    ]
    base["distance_bin"] = base["state_distance_km"].apply(distance_bin_from_km)

    def _agg(cols, min_n):
        g = (
            base.groupby(cols, dropna=False)["lead_days"]
            .agg(
                n="count",
                p50="median",
                p75=lambda s: s.quantile(0.75),
                p90=lambda s: s.quantile(0.90),
            )
            .reset_index()
        )
        return {"cols": cols, "min_n": min_n, "table": g}

    profiles = [
        _agg(["seller_state", "customer_state", "category", "distance_bin", "month"], 25),
        _agg(["seller_state", "customer_state", "category", "distance_bin"], 30),
        _agg(["seller_state", "customer_state", "category"], 40),
        _agg(["seller_state", "customer_state", "distance_bin"], 50),
        _agg(["seller_state", "customer_state"], 80),
        _agg(["customer_state", "category"], 80),
        _agg(["customer_state"], 120),
    ]

    global_stats = {
        "p50": float(base["lead_days"].median()),
        "p75": float(base["lead_days"].quantile(0.75)),
        "p90": float(base["lead_days"].quantile(0.90)),
        "n": int(len(base)),
        "matched_on": "global",
    }
    return profiles, global_stats


def lookup_eta_stats(profiles, query):
    for p in profiles:
        cols = p["cols"]
        tbl = p["table"]
        mask = pd.Series(True, index=tbl.index)
        for c in cols:
            mask &= tbl[c].astype(str) == str(query.get(c, ""))
        sub = tbl[mask]
        if not sub.empty:
            row = sub.sort_values("n", ascending=False).iloc[0]
            if int(row["n"]) >= p["min_n"]:
                return {
                    "p50": float(row["p50"]),
                    "p75": float(row["p75"]),
                    "p90": float(row["p90"]),
                    "n": int(row["n"]),
                    "matched_on": ", ".join(cols),
                }
    return None


def render_order_risk_page(df_raw, items_geo_raw):
    st.markdown("## Logistics Order Risk Simulator")
    st.caption(
        "Simulate a new order and get late-risk plus a recommended customer delivery promise window."
    )

    if df_raw is None or items_geo_raw is None:
        st.error("Data unavailable for simulation. Please verify `data/processed/` files.")
        return

    states = sorted(df_raw["customer_state"].dropna().unique().tolist())
    qnum_series = df_raw["order_purchase_timestamp"].dt.quarter
    qnum_labels = {1: "Jan-Mar (Q1)", 2: "Apr-Jun (Q2)", 3: "Jul-Sep (Q3)", 4: "Oct-Dec (Q4)"}

    c1, c2, c3 = st.columns(3)
    seller_state = c1.selectbox("Origin (Seller State)", options=states, index=states.index("SP") if "SP" in states else 0)
    customer_state = c2.selectbox("Destination (Customer State)", options=states, index=states.index("RJ") if "RJ" in states else 0)
    planned_order_date = c3.date_input(
        "Planned Order Date",
        value=pd.Timestamp.today().date(),
        help="Use the expected order date from your operations planning.",
    )
    planned_order_ts = pd.Timestamp(planned_order_date)
    planned_qnum = int(((planned_order_ts.month - 1) // 3) + 1)
    planned_q_label = qnum_labels.get(planned_qnum, f"Q{planned_qnum}")
    st.caption(f"Seasonality bucket used for risk: **{planned_q_label}**")

    cities = (
        df_raw.loc[df_raw["customer_state"] == customer_state, "customer_city"]
        .dropna().astype(str).sort_values().unique().tolist()
    )
    if not cities:
        cities = ["unknown_city"]
    customer_city = st.selectbox("Destination City", options=cities)

    category_col = (
        "product_category_name_english"
        if "product_category_name_english" in items_geo_raw.columns
        else ("product_category_name" if "product_category_name" in items_geo_raw.columns else None)
    )
    category_options = (
        sorted(items_geo_raw[category_col].dropna().astype(str).unique().tolist())
        if category_col
        else []
    )
    selected_category = st.selectbox(
        "Item Category",
        options=category_options if category_options else ["unknown_category"],
        help="Category baseline contributes directly to the risk score.",
    )

    order_value = st.slider("Order Value (R$)", min_value=20, max_value=3000, value=280, step=20)
    n_items = st.slider("Item Count", min_value=1, max_value=12, value=2, step=1)

    # Historical baselines for risk
    global_rate = float(df_raw["is_late"].mean())
    q_lookup = df_raw.assign(q_num=qnum_series).groupby("q_num")["is_late"].mean()
    q_rate = float(q_lookup.get(planned_qnum, global_rate))

    state_lookup = df_raw.groupby("customer_state")["is_late"].mean()
    state_rate = float(state_lookup.get(customer_state, global_rate))

    city_lookup = df_raw.groupby(["customer_state", "customer_city"])["is_late"].mean()
    city_rate = float(city_lookup.get((customer_state, customer_city), state_rate))

    corridor_lookup = items_geo_raw.groupby(["seller_state", "customer_state"])["is_late"].mean()
    corridor_rate = float(corridor_lookup.get((seller_state, customer_state), global_rate))

    if category_col:
        cat_lookup = items_geo_raw.groupby(category_col)["is_late"].mean()
        category_rate = float(cat_lookup.get(selected_category, global_rate))
    else:
        category_rate = global_rate

    # Blend + small operational adjustments.
    # Category is included because product type changes handling/transit complexity.
    base_risk = (
        0.40 * corridor_rate
        + 0.25 * city_rate
        + 0.20 * state_rate
        + 0.15 * category_rate
    )
    season_multiplier = 0.9 + (q_rate / global_rate) * 0.1 if global_rate > 0 else 1.0
    order_multiplier = 1.0 + min((order_value / 3000) * 0.08 + (n_items / 12) * 0.08, 0.16)
    risk = float(np.clip(base_risk * season_multiplier * order_multiplier, 0, 1))
    risk_pct = risk * 100

    if risk_pct >= 20:
        tier = "High"
        advice = [
            "Prioritize fast carrier allocation and proactive ETA communication.",
            "Escalate to operations watchlist for same-day monitoring.",
            "Consider split shipment if multiple items are involved.",
        ]
    elif risk_pct >= 12:
        tier = "Medium"
        advice = [
            "Use standard carrier with tighter SLA monitoring.",
            "Send customer proactive tracking updates.",
            "Validate dispatch cut-off and warehouse capacity.",
        ]
    else:
        tier = "Low"
        advice = [
            "Proceed with normal fulfillment flow.",
            "Keep automated check-ins for SLA adherence.",
            "No manual escalation required unless status changes.",
        ]

    # Data-driven ETA from historical segment profiles (route + category + distance + month).
    profiles, global_eta = build_eta_profiles(df_raw, items_geo_raw)
    state_dist_km = state_distance_km(seller_state, customer_state)
    dist_bin = distance_bin_from_km(state_dist_km)
    query = {
        "seller_state": seller_state,
        "customer_state": customer_state,
        "customer_city": customer_city,
        "category": selected_category,
        "distance_bin": dist_bin,
        "month": planned_order_ts.month,
    }
    eta_stats = lookup_eta_stats(profiles, query) or global_eta
    p50_days, p75_days, p90_days = eta_stats["p50"], eta_stats["p75"], eta_stats["p90"]

    complexity_buffer = int(
        np.ceil(
            max(0, (n_items - 2) / 4) + max(0, (order_value - 500) / 1500)
        )
    )
    if tier == "High":
        rec_days = p90_days
    elif tier == "Medium":
        rec_days = p75_days
    else:
        rec_days = p50_days

    recommended_days = int(np.clip(np.ceil(rec_days + complexity_buffer), 2, 90))
    window_start_days = int(np.clip(np.floor(p50_days), 1, 90))
    window_end_days = int(np.clip(np.ceil(p90_days + complexity_buffer), 2, 95))

    eta_date = planned_order_ts + pd.Timedelta(days=recommended_days)
    eta_start = planned_order_ts + pd.Timedelta(days=window_start_days)
    eta_end = planned_order_ts + pd.Timedelta(days=window_end_days)

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Predicted Late Risk", f"{risk_pct:.1f}%")
    k2.metric("Risk Tier", tier)
    k3.metric("Historical Corridor Late %", f"{corridor_rate*100:.1f}%")
    k4.metric("Category Baseline Late %", f"{category_rate*100:.1f}%")

    e1, e2, e3 = st.columns(3)
    e1.metric("Suggested ETA", eta_date.strftime("%d %b %Y"))
    e2.metric("Promise Window Start", eta_start.strftime("%d %b %Y"))
    e3.metric("Promise Window End", eta_end.strftime("%d %b %Y"))
    st.caption(
        f"ETA based on {eta_stats['n']:,} historical orders matched on: `{eta_stats['matched_on']}` "
        f"(distance bucket: {dist_bin}, approx {state_dist_km:.0f} km)."
    )

    route_fig = make_order_route_map(seller_state, customer_state, risk_pct)
    if route_fig:
        st.plotly_chart(route_fig, use_container_width=True, config={"displaylogo": False})
    else:
        st.info("Route preview unavailable for this state pair.")

    st.markdown("### Why this risk?")
    why_df = pd.DataFrame({
        "Driver": [
            "Route corridor history",
            "Destination city history",
            "Destination state history",
            "Item category history",
            f"Seasonality ({planned_q_label})",
            "Order complexity/value adjustment",
            "Lead-time baseline blend (city/state/global)",
        ],
        "Value": [
            f"{corridor_rate*100:.2f}%",
            f"{city_rate*100:.2f}%",
            f"{state_rate*100:.2f}%",
            f"{category_rate*100:.2f}%",
            f"{q_rate*100:.2f}%",
            f"x{order_multiplier:.3f}",
            f"{p50_days:.1f}/{p75_days:.1f}/{p90_days:.1f} days",
        ],
        "Contribution": [
            "40%",
            "25%",
            "20%",
            "15%",
            "Adjustment",
            "Adjustment",
            "Historical quantiles",
        ],
    })
    st.table(why_df)

    st.markdown("### Recommended actions")
    for a in advice:
        st.markdown(f"- {a}")


# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════

logo_uri = get_logo_data_uri()
if logo_uri:
    sidebar_logo_inner = (
        f'<img src="{logo_uri}" alt="logo" '
        'style="width:30px;height:30px;border-radius:50%;object-fit:cover;display:block;" />'
    )
else:
    sidebar_logo_inner = "o"

with st.sidebar:
    # Logo area
    st.markdown(f"""
    <div style="padding:20px 0 8px; text-align:center;">
      <div style="display:inline-flex;align-items:center;gap:10px;">
        <div style="width:36px;height:36px;border-radius:50%;background:white;
             display:flex;align-items:center;justify-content:center;
             font-weight:900;color:{OLIST_BLUE};font-size:1rem;
             box-shadow:0 0 0 3px rgba(10,78,228,0.35);">{sidebar_logo_inner}</div>
        <span style="font-size:1.1rem;font-weight:800;color:white;
              font-family:'Plus Jakarta Sans',sans-serif;">olist</span>
      </div>
      <div style="font-size:0.68rem;color:rgba(255,255,255,0.35);
           margin-top:4px;letter-spacing:0.08em;text-transform:uppercase;">
        Delivery Intelligence
      </div>
    </div>
    <hr style="margin:12px 0 20px;border-color:rgba(255,255,255,0.08)"/>
    """, unsafe_allow_html=True)

    st.markdown("**VIEW**")
    page_mode = st.radio(
        "Select page",
        options=["Executive Maps", "Order Risk Simulator"],
        index=0,
        label_visibility="collapsed",
    )

    st.markdown("**FILTERS**")

    # Load data to get filter options
    df_raw, items_geo_raw, load_err = load_data()

    if df_raw is not None:
        # Quarter filter
        df_raw["q"] = df_raw["order_purchase_timestamp"].dt.to_period("Q").astype(str)
        quarters = sorted(df_raw["q"].dropna().unique())
        quarter_filter_labels = [quarter_label(q) for q in quarters]
        quarter_filter_map = dict(zip(quarter_filter_labels, quarters))
        selected_quarters = st.multiselect(
            "Time Period",
            options=quarter_filter_labels,
            default=quarter_filter_labels,
            help="Filter by month ranges (quarter-level seasonality).",
        )
        selected_quarter_values = [quarter_filter_map[q] for q in selected_quarters]

        # State filter
        all_states = sorted(df_raw["customer_state"].dropna().unique())
        selected_states = st.multiselect(
            "Customer State",
            options=all_states,
            default=all_states,
            help="Filter by customer delivery state",
        )

        # Route count
        top_n = st.slider(
            "MAP 2 — Route Corridors",
            min_value=30, max_value=200, value=100, step=10,
            help="Number of top shipping corridors to display",
        )

        st.markdown("<hr/>", unsafe_allow_html=True)

        # Map visibility toggles
        st.markdown("**MAP VISIBILITY**")
        show_m1 = st.checkbox("MAP 1 — Late Rate Choropleth", value=True)
        show_m2 = st.checkbox("MAP 2 — Shipping Routes",       value=True)
        show_m3 = st.checkbox("MAP 3 — Seller Risk Bubbles",   value=True)
        show_m4 = st.checkbox("MAP 4 — Customer Heatmap",      value=True)

        st.markdown("<hr/>", unsafe_allow_html=True)
        st.markdown(
            f"<p style='font-size:0.72rem;'>Brazilian E-Commerce Dataset<br>"
            f"Capstone Project · 2026</p>",
            unsafe_allow_html=True,
        )
    else:
        st.error("Data not found. Check `../data/processed/` path.")
        show_m1 = show_m2 = show_m3 = show_m4 = False


# ══════════════════════════════════════════════════════════════════════════════
# MAIN CONTENT
# ══════════════════════════════════════════════════════════════════════════════

if page_mode == "Order Risk Simulator":
    render_order_risk_page(df_raw, items_geo_raw)
    st.stop()

# ── Top header ─────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="top-header">
  <div class="top-header-logo">
    <div class="logo-dot">o</div>
    <div>
      <p class="header-title">Delivery Intelligence Dashboard</p>
      <p class="header-sub">Brazilian E-Commerce · Olist Dataset · Geographic Analysis</p>
    </div>
  </div>
  <div class="status-pill">
    <div class="dot-live"></div>
    Live Analysis
  </div>
</div>
""", unsafe_allow_html=True)

if df_raw is None:
    st.error(f"⚠️  Could not load data: `{load_err}`")
    st.info("Make sure `olist_merged.csv` and `items_enriched.csv` exist in `../data/processed/`")
    st.stop()

# ── Apply filters ───────────────────────────────────────────────────────────
df_f = df_raw.copy()
if selected_quarters:
    df_f = df_f[df_f["q"].isin(selected_quarter_values)]
if selected_states:
    df_f = df_f[df_f["customer_state"].isin(selected_states)]

items_geo_f = items_geo_raw.copy()
if selected_quarters:
    items_geo_f["q"] = items_geo_f["order_purchase_timestamp"].dt.to_period("Q").astype(str)
    items_geo_f = items_geo_f[items_geo_f["q"].isin(selected_quarter_values)]
if selected_states:
    items_geo_f = items_geo_f[items_geo_f["customer_state"].isin(selected_states)]

# ── KPI cards ───────────────────────────────────────────────────────────────
total_orders  = len(df_f)
late_rate_pct = df_f["is_late"].mean() * 100
n_late        = df_f["is_late"].sum()
n_states      = df_f["customer_state"].nunique()
worst_state   = (
    df_f.groupby("customer_state")["is_late"].mean()
    .idxmax() if total_orders > 0 else "—"
)
worst_pct     = (
    df_f.groupby("customer_state")["is_late"].mean().max() * 100
    if total_orders > 0 else 0
)

st.markdown(f"""
<div class="kpi-row">
  <div class="kpi-card">
    <div class="kpi-label">Total Orders</div>
    <div class="kpi-value">{total_orders:,}</div>
    <div class="kpi-sub">Filtered selection</div>
  </div>
  <div class="kpi-card alert">
    <div class="kpi-label">Late Rate</div>
    <div class="kpi-value danger">{late_rate_pct:.1f}%</div>
    <div class="kpi-sub">{n_late:,} late deliveries</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-label">On-Time Rate</div>
    <div class="kpi-value">{100-late_rate_pct:.1f}%</div>
    <div class="kpi-sub">{total_orders-n_late:,} on-time</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-label">States Covered</div>
    <div class="kpi-value">{n_states}</div>
    <div class="kpi-sub">Customer destinations</div>
  </div>
  <div class="kpi-card alert">
    <div class="kpi-label">Worst State</div>
    <div class="kpi-value danger">{worst_state}</div>
    <div class="kpi-sub">{worst_pct:.1f}% late rate</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Quick insight chips ─────────────────────────────────────────────────────
top3_late = (
    df_f.groupby("customer_state")["is_late"].mean()
    .nlargest(3).index.tolist()
)
top3_vol = (
    df_f.groupby("customer_state")["order_id"].count()
    .nlargest(3).index.tolist()
)
st.markdown(f"""
<div class="insight-row">
  <div class="chip alert">⚠️ Highest late-rate states: <b>{", ".join(top3_late)}</b></div>
  <div class="chip">📦 Highest order volume: <b>{", ".join(top3_vol)}</b></div>
  <div class="chip">🗓️ Quarters selected: <b>{len(selected_quarters) if selected_quarters else 0}</b></div>
  <div class="chip">🗺️ States selected: <b>{len(selected_states) if selected_states else 0}</b></div>
</div>
""", unsafe_allow_html=True)

# ── Load GeoJSON ─────────────────────────────────────────────────────────────
brazil_geo = load_geojson()
geo_ok = brazil_geo is not None

# ══════════════════════════════════════════════════════════════════════════════
# MAP 1 + MAP 2  (side by side on large screens, stacked on small)
# ══════════════════════════════════════════════════════════════════════════════

if show_m1 or show_m2:
    col1, col2 = st.columns(2, gap="medium")

if show_m1:
    with col1:
        st.markdown(f"""
        <div class="map-card">
          <div class="map-card-header">
            <span class="map-badge">MAP 1</span>
            <div>
              <p class="map-card-title">Late Rate by State — Choropleth</p>
              <p class="map-card-subtitle">
                Colour = late %, bubble size = order volume · hover for details
              </p>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)
        if geo_ok:
            with st.spinner("Rendering choropleth…"):
                fig1 = make_map1_choropleth(df_f, brazil_geo)
            st.plotly_chart(fig1, use_container_width=True, config={
                "displayModeBar": True,
                "modeBarButtonsToRemove": ["select2d","lasso2d"],
                "displaylogo": False,
            })
        else:
            st.warning("⚠️  GeoJSON unavailable (offline?). State boundaries cannot be drawn.")

if show_m2:
    with col2:
        st.markdown(f"""
        <div class="map-card">
          <div class="map-card-header">
            <span class="map-badge">MAP 2</span>
            <div>
              <p class="map-card-title">Shipping Route Analysis</p>
              <p class="map-card-subtitle">
                Arc thickness = volume · colour = late rate · ■ = seller hub
              </p>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)
        with st.spinner("Rendering shipping routes…"):
            fig2 = make_map2_routes(items_geo_f, top_n=top_n)
        st.plotly_chart(fig2, use_container_width=True, config={
            "displayModeBar": True,
            "modeBarButtonsToRemove": ["select2d","lasso2d"],
            "displaylogo": False,
        })

# ══════════════════════════════════════════════════════════════════════════════
# MAP 3 + MAP 4
# ══════════════════════════════════════════════════════════════════════════════

if show_m3 or show_m4:
    col3, col4 = st.columns(2, gap="medium")

if show_m3:
    with col3:
        st.markdown(f"""
        <div class="map-card">
          <div class="map-card-header">
            <span class="map-badge" style="background:{OLIST_ACCENT};">MAP 3</span>
            <div>
              <p class="map-card-title">Seller Risk Intelligence</p>
              <p class="map-card-subtitle">
                Bubble size = orders · colour = late rate · target red + large bubbles
              </p>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)
        with st.spinner("Rendering seller risk map…"):
            fig3 = make_map3_sellers(items_geo_f)
        st.plotly_chart(fig3, use_container_width=True, config={
            "displayModeBar": True,
            "modeBarButtonsToRemove": ["select2d","lasso2d"],
            "displaylogo": False,
        })

if show_m4:
    with col4:
        st.markdown(f"""
        <div class="map-card">
          <div class="map-card-header">
            <span class="map-badge" style="background:{OLIST_ACCENT};">MAP 4</span>
            <div>
              <p class="map-card-title">Customer Density Heatmap</p>
              <p class="map-card-subtitle">
                Toggle layers — 🔵 all orders vs 🔴 late orders density
              </p>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)
        with st.spinner("Rendering heatmap…"):
            m4 = make_map4_folium(df_f)
            m4_html = m4._repr_html_()
        components.html(m4_html, height=538, scrolling=False)

# ── Footer ───────────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="
  margin-top:48px;
  padding:18px 28px;
  background:{OLIST_DARK};
  border-radius:14px;
  display:flex;
  align-items:center;
  justify-content:space-between;
  border:1px solid rgba(255,255,255,0.05);
">
  <span style="font-family:'Plus Jakarta Sans',sans-serif;font-size:0.78rem;
        color:rgba(255,255,255,0.35);">
    © 2026 Olist Delivery Intelligence · Brazilian E-Commerce Dataset
  </span>
  <span style="font-family:'Plus Jakarta Sans',sans-serif;font-size:0.78rem;
        color:rgba(141,215,215,0.6);">
    Capstone Project — Predictive Delivery Analytics
  </span>
</div>
""", unsafe_allow_html=True)
