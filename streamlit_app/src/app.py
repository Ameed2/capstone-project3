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

/* ── Hide streamlit chrome ── */
#MainMenu, footer, header {{ visibility: hidden; }}
.block-container {{ padding-top: 1.5rem; padding-bottom: 2rem; }}

/* ── Plotly chart border ── */
.js-plotly-plot {{ border-radius: 0 0 14px 14px; }}
</style>
""", unsafe_allow_html=True)


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
def load_data():
    PATH = "../data/processed/"
    date_cols = [
        "order_purchase_timestamp","order_approved_at",
        "order_delivered_carrier_date","order_delivered_customer_date",
        "order_estimated_delivery_date",
    ]
    try:
        df    = pd.read_csv(PATH + "olist_merged.csv",   parse_dates=date_cols)
        items = pd.read_csv(PATH + "items_enriched.csv")
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


# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════

with st.sidebar:
    # Logo area
    st.markdown(f"""
    <div style="padding:20px 0 8px; text-align:center;">
      <div style="display:inline-flex;align-items:center;gap:10px;">
        <div style="width:36px;height:36px;border-radius:50%;background:white;
             display:flex;align-items:center;justify-content:center;
             font-weight:900;color:{OLIST_BLUE};font-size:1rem;
             box-shadow:0 0 0 3px rgba(10,78,228,0.35);">o</div>
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

    st.markdown("**FILTERS**")

    # Load data to get filter options
    df_raw, items_geo_raw, load_err = load_data()

    if df_raw is not None:
        # Quarter filter
        df_raw["q"] = df_raw["order_purchase_timestamp"].dt.to_period("Q").astype(str)
        quarters = sorted(df_raw["q"].dropna().unique())
        selected_quarters = st.multiselect(
            "Time Period (Quarter)",
            options=quarters,
            default=quarters,
            help="Filter orders by purchase quarter",
        )

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
    df_f = df_f[df_f["q"].isin(selected_quarters)]
if selected_states:
    df_f = df_f[df_f["customer_state"].isin(selected_states)]

items_geo_f = items_geo_raw.copy()
if selected_quarters:
    items_geo_f["q"] = items_geo_f["order_purchase_timestamp"].dt.to_period("Q").astype(str)
    items_geo_f = items_geo_f[items_geo_f["q"].isin(selected_quarters)]
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
