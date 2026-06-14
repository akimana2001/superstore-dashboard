import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Superstore Analytics Dashboard",
    layout="wide",
    page_icon="📊"
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #f8f9fb; }
    .section-header {
        font-size: 1.4rem;
        font-weight: 700;
        color: #1a1a2e;
        border-left: 5px solid #4361ee;
        padding-left: 12px;
        margin: 30px 0 15px 0;
    }
    .ethics-block {
        background: #fff8e1;
        border-left: 5px solid #f59e0b;
        padding: 18px 22px;
        border-radius: 8px;
        margin-bottom: 14px;
    }
    .insight-block {
        background: #e8f5e9;
        border-left: 5px solid #22c55e;
        padding: 14px 20px;
        border-radius: 8px;
        margin-bottom: 10px;
    }
    .member-card {
        background: white;
        border-radius: 10px;
        padding: 14px 18px;
        margin-bottom: 8px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.07);
        border-left: 4px solid #4361ee;
    }
    .leader-card {
        background: #eff6ff;
        border-radius: 10px;
        padding: 14px 18px;
        margin-bottom: 8px;
        box-shadow: 0 2px 6px rgba(67,97,238,0.15);
        border-left: 4px solid #f59e0b;
    }
</style>
""", unsafe_allow_html=True)


# ── Data Loading ───────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_excel("super.xlsx")
    df["Order Date"] = pd.to_datetime(df["Order Date"])
    df["Year"] = df["Order Date"].dt.year
    df["Month"] = df["Order Date"].dt.to_period("M").astype(str)
    df["Quarter"] = "Q" + df["Order Date"].dt.quarter.astype(str) + " " + df["Year"].astype(str)
    df["Profit Margin %"] = (df["Profit"] / df["Sales"] * 100).round(2)
    return df

df = load_data()


# ══════════════════════════════════════════════════════════════════════════════
# HEADER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div style='background: linear-gradient(135deg,#1a1a2e,#4361ee);
            padding:32px 36px; border-radius:14px; margin-bottom:28px;'>
  <h1 style='color:white; margin:0; font-size:2.1rem;'>
    📊 Superstore Analytics Dashboard
  </h1>
  <p style='color:#c7d2fe; margin:8px 0 4px 0; font-size:1rem;'>
    Data Visualization for Decision Making &nbsp;·&nbsp; BSA83111
    &nbsp;·&nbsp; Faculty of Management &nbsp;·&nbsp; Level 8
  </p>
  <p style='color:#a5b4fc; margin:0; font-size:0.9rem;'>
    Instructor: Dr Patrick NIYISHAKA &nbsp;·&nbsp;
    Trimester 1, 2026 &nbsp;·&nbsp; Presentation: June 16, 2026
  </p>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# GROUP MEMBERS INTRODUCTION
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-header">👥 Group Members</div>', unsafe_allow_html=True)

st.markdown("""
<div class="leader-card">
  <strong>👑 Group Leader &nbsp;·&nbsp; &nbsp;—&nbsp; Dusengimana Olivier</strong><br>
  <span style='color:#4361ee;'>olivier.dusengimana24BA@keplercollege.ac.rw</span>
</div>
<div class="member-card">
  <strong>&nbsp;&nbsp; Christian Habineza</strong><br>
  <span style='color:#4361ee;'>christian.habineza24BA@keplercollege.ac.rw</span>
</div>
<div class="member-card">
  <strong> &nbsp;&nbsp; Gilbert Niyonkuru</strong><br>
  <span style='color:#4361ee;'>gilbert.niyonkuru24BA@keplercollege.ac.rw</span>
</div>
<div class="member-card">
  <strong>&nbsp;&nbsp; Ushadia Uwimbabazi</strong><br>
  <span style='color:#4361ee;'>shadia.uwimbabazi24BA@keplercollege.ac.rw</span>
</div>
<div class="member-card">
  <strong>&nbsp;&nbsp; Dative Akimana</strong><br>
  <span style='color:#4361ee;'>dative.akimana24BA@keplercollege.ac.rw</span>
</div>
""", unsafe_allow_html=True)

st.markdown("""
> **Project Goal:** Build an interactive data dashboard using the Sample Superstore
> dataset to support business decision-making through clear and honest visualizations.
> This dashboard covers sales performance, profitability trends, distribution analysis,
> ethical considerations, and actionable recommendations.
""")

st.markdown("---")


# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR FILTERS
# ══════════════════════════════════════════════════════════════════════════════
st.sidebar.markdown("## 🔍 Dashboard Filters")
st.sidebar.markdown("Adjust filters to explore the dataset interactively.")

regions    = st.sidebar.multiselect("🌍 Region",   sorted(df["Region"].unique()),   default=sorted(df["Region"].unique()))
categories = st.sidebar.multiselect("📦 Category", sorted(df["Category"].unique()), default=sorted(df["Category"].unique()))
years      = st.sidebar.multiselect("📅 Year",     sorted(df["Year"].unique()),     default=sorted(df["Year"].unique()))

profit_range = st.sidebar.slider(
    "💰 Profit Range ($)",
    float(df["Profit"].min()),
    float(df["Profit"].max()),
    (float(df["Profit"].min()), float(df["Profit"].max()))
)

filtered = df[
    df["Region"].isin(regions) &
    df["Category"].isin(categories) &
    df["Year"].isin(years) &
    df["Profit"].between(profit_range[0], profit_range[1])
]

st.sidebar.markdown("---")
st.sidebar.metric("📋 Filtered Records", f"{len(filtered):,}")
st.sidebar.metric("📦 Unique Products",  filtered["Product Name"].nunique())

if len(filtered) == 0:
    st.error("⚠️ No data matches the current filters. Please adjust your selections.")
    st.stop()


# ══════════════════════════════════════════════════════════════════════════════
# 1. KEY PERFORMANCE INDICATORS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-header">1. Key Performance Indicators (KPIs)</div>', unsafe_allow_html=True)

total_sales   = filtered["Sales"].sum()
total_profit  = filtered["Profit"].sum()
avg_sales     = filtered["Sales"].mean()
total_orders  = filtered["Order ID"].nunique()
profit_margin = (total_profit / total_sales * 100) if total_sales > 0 else 0
loss_count    = len(filtered[filtered["Profit"] < 0])
loss_pct      = loss_count / len(filtered) * 100

c1, c2, c3, c4, c5, c6 = st.columns(6)
c1.metric("Total Sales",     f"${total_sales:,.0f}M")
c2.metric("Total Profit",    f"${total_profit:,.0f}M")
c3.metric("Avg Order Value", f"${avg_sales:,.0f}")
c4.metric("Total Orders",    f"{total_orders:,}")
c5.metric("Profit Margin",   f"{profit_margin:.1f}%")
c6.metric("Loss Rate",       f"{loss_pct:.1f}%")


# ══════════════════════════════════════════════════════════════════════════════
# 2. TRENDS OVER TIME
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-header">2. Trends Over Time</div>', unsafe_allow_html=True)

col_t1, col_t2 = st.columns(2)

with col_t1:
    monthly = filtered.groupby("Month")[["Sales", "Profit"]].sum().reset_index()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=monthly["Month"], y=monthly["Sales"],
                             mode="lines+markers", name="Sales",
                             line=dict(color="#4361ee", width=2)))
    fig.add_trace(go.Scatter(x=monthly["Month"], y=monthly["Profit"],
                             mode="lines+markers", name="Profit",
                             line=dict(color="#22c55e", width=2, dash="dot")))
    fig.update_layout(title="📅 Monthly Sales & Profit Trend",
                      xaxis_tickangle=-45, height=380,
                      legend=dict(orientation="h", y=1.1))
    st.plotly_chart(fig, use_container_width=True)

with col_t2:
    yearly = filtered.groupby("Year")[["Sales", "Profit"]].sum().reset_index()
    fig = px.bar(yearly, x="Year", y=["Sales", "Profit"],
                 barmode="group", title="📆 Yearly Sales vs Profit",
                 color_discrete_map={"Sales": "#4361ee", "Profit": "#22c55e"},
                 height=380)
    st.plotly_chart(fig, use_container_width=True)

quarterly = filtered.groupby("Quarter")["Sales"].sum().reset_index()
fig = px.area(quarterly, x="Quarter", y="Sales",
              title="📊 Quarterly Sales Trend",
              color_discrete_sequence=["#4361ee"])
fig.update_layout(xaxis_tickangle=-30)
st.plotly_chart(fig, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# 3. COMPARISONS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-header">3. Comparisons</div>', unsafe_allow_html=True)

col_c1, col_c2 = st.columns(2)

with col_c1:
    region_data = filtered.groupby("Region")[["Sales", "Profit"]].sum().reset_index()
    fig = px.bar(region_data, x="Region", y=["Sales", "Profit"],
                 barmode="group", title="🌍 Sales & Profit by Region",
                 color_discrete_map={"Sales": "#4361ee", "Profit": "#22c55e"})
    st.plotly_chart(fig, use_container_width=True)

with col_c2:
    cat_data = filtered.groupby("Category")[["Sales", "Profit"]].sum().reset_index()
    fig = px.bar(cat_data, x="Category", y=["Sales", "Profit"],
                 barmode="group", title="📦 Sales & Profit by Category",
                 color_discrete_map={"Sales": "#4361ee", "Profit": "#22c55e"})
    st.plotly_chart(fig, use_container_width=True)

col_c3, col_c4 = st.columns(2)

with col_c3:
    sub_data = (filtered.groupby("Sub-Category")["Sales"]
                .sum().reset_index()
                .sort_values("Sales", ascending=True))
    fig = px.bar(sub_data, x="Sales", y="Sub-Category", orientation="h",
                 title="📂 Sales by Sub-Category",
                 color="Sales", color_continuous_scale="Blues")
    fig.update_layout(height=420)
    st.plotly_chart(fig, use_container_width=True)

with col_c4:
    ship_data = filtered.groupby("Ship Mode")["Sales"].sum().reset_index()
    fig = px.pie(ship_data, values="Sales", names="Ship Mode",
                 title="🚚 Sales Share by Shipping Mode",
                 color_discrete_sequence=px.colors.qualitative.Set2,
                 hole=0.4)
    st.plotly_chart(fig, use_container_width=True)

top_products = (filtered.groupby("Product Name")["Sales"]
                .sum().nlargest(10).reset_index())
fig = px.bar(top_products, x="Sales", y="Product Name", orientation="h",
             title="🏆 Top 10 Products by Sales",
             color="Sales", color_continuous_scale="Teal")
fig.update_layout(height=400)
st.plotly_chart(fig, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# 4. DISTRIBUTION OF DATA
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-header">4. Distribution of Data</div>', unsafe_allow_html=True)

col_d1, col_d2 = st.columns(2)

with col_d1:
    fig = px.histogram(filtered, x="Sales", nbins=50,
                       title="💵 Distribution of Sales Values",
                       color_discrete_sequence=["#4361ee"])
    fig.add_vline(x=filtered["Sales"].mean(), line_dash="dash",
                  line_color="red", annotation_text="Mean")
    st.plotly_chart(fig, use_container_width=True)

with col_d2:
    fig = px.box(filtered, x="Category", y="Profit", color="Category",
                 title="📊 Profit Distribution by Category",
                 color_discrete_sequence=px.colors.qualitative.Set2)
    st.plotly_chart(fig, use_container_width=True)

col_d3, col_d4 = st.columns(2)

with col_d3:
    sample = filtered.sample(min(1000, len(filtered)), random_state=42)
    fig = px.scatter(sample, x="Sales", y="Profit",
                     color="Category", size="Discount",
                     title="🔵 Sales vs Profit (Bubble size = Discount)",
                     opacity=0.6,
                     color_discrete_sequence=px.colors.qualitative.Set2)
    st.plotly_chart(fig, use_container_width=True)

with col_d4:
    fig = px.violin(filtered, y="Profit Margin %", x="Region",
                    color="Region", box=True,
                    title="🎻 Profit Margin Distribution by Region",
                    color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# 5. ALERTS AND HIGHLIGHTS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-header">5. Alerts & Highlights</div>', unsafe_allow_html=True)

loss_df    = filtered[filtered["Profit"] < 0]
high_disc  = filtered[filtered["Discount"] >= 0.4]
missing    = filtered.isnull().sum().sum()

al1, al2, al3 = st.columns(3)

with al1:
    color = "#ef4444" if loss_count > 100 else "#f59e0b"
    st.markdown(f"""
    <div style='background:{color}15; border:2px solid {color};
                border-radius:10px; padding:16px; text-align:center;'>
      <h2 style='color:{color}; margin:0;'>{loss_count:,}</h2>
      <p style='margin:4px 0 0 0; font-weight:600; color:{color};'>
        Loss-Making Transactions</p>
    </div>""", unsafe_allow_html=True)

with al2:
    color = "#f59e0b"
    st.markdown(f"""
    <div style='background:{color}15; border:2px solid {color};
                border-radius:10px; padding:16px; text-align:center;'>
      <h2 style='color:{color}; margin:0;'>{len(high_disc):,}</h2>
      <p style='margin:4px 0 0 0; font-weight:600; color:{color};'>
        Orders with Discount ≥ 40%</p>
    </div>""", unsafe_allow_html=True)

with al3:
    color = "#22c55e" if missing == 0 else "#ef4444"
    st.markdown(f"""
    <div style='background:{color}15; border:2px solid {color};
                border-radius:10px; padding:16px; text-align:center;'>
      <h2 style='color:{color}; margin:0;'>{missing}</h2>
      <p style='margin:4px 0 0 0; font-weight:600; color:{color};'>
        Missing Values Detected</p>
    </div>""", unsafe_allow_html=True)

st.markdown("")

# Discount vs Profit scatter with threshold lines
fig = px.scatter(filtered, x="Discount", y="Profit",
                 color="Category", trendline="ols",
                 title="⚠️ Discount vs Profit — Higher Discounts Often Cause Losses",
                 color_discrete_sequence=px.colors.qualitative.Set2)
fig.add_vline(x=0.4, line_dash="dash", line_color="red",
              annotation_text="40% Discount Threshold")
fig.add_hline(y=0, line_dash="dash", line_color="orange",
              annotation_text="Break-Even Line")
st.plotly_chart(fig, use_container_width=True)

# Top 10 loss-making products table  ← fixed: right= instead of max_val=
st.subheader("🔴 Top 10 Loss-Making Products")
top_losses = (
    loss_df[["Product Name", "Category", "Region", "Sales", "Profit", "Discount"]]
    .sort_values("Profit")
    .head(10)
    .reset_index(drop=True)
)
top_losses.index += 1

def highlight_loss(val):
    return "background-color: #fecaca" if val < 0 else ""

st.dataframe(
    top_losses.style
        .format({"Sales": "${:,.2f}", "Profit": "${:,.2f}", "Discount": "{:.0%}"})
        .applymap(highlight_loss, subset=["Profit"]),
    use_container_width=True
)

if loss_count > 0:
    st.warning(
        f"⚠️ **{loss_count:,} transactions** resulted in a loss, representing "
        f"**{loss_pct:.1f}%** of all filtered records. "
        f"Total loss amount: **${loss_df['Profit'].sum():,.2f}**"
    )


# ══════════════════════════════════════════════════════════════════════════════
# 6. FILTERS AND INTERACTIVITY
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-header">6. Filters & Interactivity</div>', unsafe_allow_html=True)

st.info("""
**How to use this dashboard:**
- 🌍 **Region filter** — isolate performance in East, West, Central, or South
- 📦 **Category filter** — compare Furniture, Office Supplies, or Technology
- 📅 **Year filter** — track how the business evolved year-over-year
- 💰 **Profit range slider** — focus on profitable deals or investigate losses
- 🔍 **Product search** — find any product instantly below
- All charts, KPIs, and tables update instantly based on your selections.
""")

search_term = st.text_input("🔍 Search for a specific product:",
                             placeholder="e.g. Staples, Chair, Phone")
if search_term:
    product_df = filtered[
        filtered["Product Name"].str.contains(search_term, case=False, na=False)
    ]
    if len(product_df) > 0:
        st.success(f"Found **{len(product_df)}** records matching '{search_term}'")
        agg = product_df.groupby("Product Name")[["Sales", "Profit"]].sum().reset_index()
        fig = px.bar(agg.head(15), x="Product Name", y=["Sales", "Profit"],
                     barmode="group", title=f"Results for: '{search_term}'",
                     color_discrete_map={"Sales": "#4361ee", "Profit": "#22c55e"})
        fig.update_layout(xaxis_tickangle=-30)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning(f"No products found matching '{search_term}'.")


# ══════════════════════════════════════════════════════════════════════════════
# 7. ETHICS, PRIVACY AND DATA INTEGRITY
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-header">7. Ethics, Privacy & Data Integrity</div>', unsafe_allow_html=True)

st.markdown("""
<div class="ethics-block">
<h4>🔒 Privacy & Data Protection</h4>
<p>The Superstore dataset contains <strong>personally identifiable information (PII)</strong>
including customer names, customer IDs, and geographic data down to city and postal-code level.
Under data protection principles such as <strong>GDPR</strong> and general privacy ethics:</p>
<ul>
  <li>Customer names and IDs are <strong>excluded from all visualizations</strong> in this
      dashboard to avoid unnecessary exposure.</li>
  <li>Data should only be accessed by authorized personnel with a legitimate business need
      (need-to-know principle).</li>
  <li>In a production environment this dataset should be <strong>anonymized or
      pseudonymized</strong> before sharing externally.</li>
  <li>Postal codes and city-level data can allow re-identification and must be handled
      with care.</li>
</ul>
</div>

<div class="ethics-block">
<h4>⚖️ Ethical Use of Data</h4>
<p>Data analysis carries ethical responsibilities. For this dashboard:</p>
<ul>
  <li><strong>No discrimination:</strong> Insights derived from regional or segment
      performance must not be used to disadvantage certain customer groups or regions
      unfairly.</li>
  <li><strong>Transparent communication:</strong> Visualizations present data honestly —
      axis scales start at zero, no cherry-picked date ranges, and loss data is shown
      alongside gains.</li>
  <li><strong>Avoid misleading visuals:</strong> All charts use consistent color coding
      and labeling so viewers can make accurate comparisons.</li>
  <li><strong>Consent:</strong> Customers whose data appears in this dataset should have
      consented to its use for analytics purposes at the point of data collection.</li>
</ul>
</div>

<div class="ethics-block">
<h4>🛡️ Data Integrity</h4>
<p>Reliable decisions depend on reliable data. The following checks were applied:</p>
<ul>
  <li><strong>Missing values:</strong> The dataset was checked for null entries. Any
      missing profit or sales values would distort KPIs significantly.</li>
  <li><strong>Duplicates:</strong> Order IDs were used to count unique orders correctly
      and avoid double-counting.</li>
  <li><strong>Data types:</strong> Order Date was converted to datetime format to enable
      accurate trend analysis.</li>
  <li><strong>Outlier awareness:</strong> Extreme discounts (≥ 40%) and large negative
      profits are flagged in the Alerts section rather than silently excluded.</li>
  <li><strong>No data manipulation:</strong> No records were removed to make the dashboard
      look better. All loss-making records are fully included.</li>
</ul>
</div>

<div class="ethics-block">
<h4>📉 Bias & Representativeness</h4>
<p>Potential sources of bias in this dataset and analysis:</p>
<ul>
  <li><strong>Sampling bias:</strong> This dataset covers only one company and may not
      represent all retail businesses or markets.</li>
  <li><strong>Temporal bias:</strong> If certain years have significantly more data than
      others, yearly comparisons may be misleading without normalization.</li>
  <li><strong>Survivorship bias:</strong> Only completed transactions are included;
      abandoned carts or rejected orders are not captured.</li>
  <li><strong>Geographic imbalance:</strong> If the West region has significantly more
      orders than others, regional averages should be interpreted with caution.</li>
</ul>
</div>
""", unsafe_allow_html=True)

st.subheader("📋 Live Data Quality Report")
dq1, dq2, dq3 = st.columns(3)
dq1.metric("Missing Values",     f"{missing}",              delta="0 is ideal",      delta_color="inverse")
dq2.metric("Duplicate Rows",     f"{filtered.duplicated().sum()}", delta="0 is ideal", delta_color="inverse")
dq3.metric("Loss Transaction %", f"{loss_pct:.1f}%",        delta="Lower is better", delta_color="inverse")


# ══════════════════════════════════════════════════════════════════════════════
# 8. SUMMARY AND INSIGHTS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-header">8. Summary & Insights</div>', unsafe_allow_html=True)

best_region   = filtered.groupby("Region")["Sales"].sum().idxmax()
best_category = filtered.groupby("Category")["Sales"].sum().idxmax()
best_sub      = filtered.groupby("Sub-Category")["Sales"].sum().idxmax()
worst_sub     = filtered.groupby("Sub-Category")["Profit"].sum().idxmin()
high_disc_loss = len(filtered[(filtered["Discount"] >= 0.4) & (filtered["Profit"] < 0)])

st.markdown("### 🔍 Key Findings")

findings = [
    f"💰 <strong>Total Sales</strong> across filtered data is <strong>${total_sales:,.2f}</strong> "
    f"with an overall profit margin of <strong>{profit_margin:.1f}%</strong>.",

    f"🏆 <strong>{best_region}</strong> is the highest-revenue region and "
    f"<strong>{best_category}</strong> is the best-performing product category.",

    f"📉 <strong>{worst_sub}</strong> sub-category generates the most losses — "
    f"likely driven by excessive discounting practices.",

    f"⚠️ <strong>{loss_count:,}</strong> transactions ({loss_pct:.1f}%) result in negative "
    f"profit, with <strong>{high_disc_loss:,}</strong> of those tied to discounts ≥ 40%.",

    f"📦 <strong>{best_sub}</strong> is the top-performing sub-category by total sales revenue.",
]

for finding in findings:
    st.markdown(f'<div class="insight-block">• {finding}</div>', unsafe_allow_html=True)

st.markdown("### 💡 Recommendations")
st.markdown("""
| # | Recommendation | Priority |
|---|---------------|----------|
| 1 | **Cap discounts at 20–30%** — discounts ≥ 40% strongly correlate with losses | 🔴 High |
| 2 | **Invest in Technology** — highest profit margin; increase marketing and stock | 🟠 Medium |
| 3 | **Review Furniture pricing** — lowest margin category; consider supplier renegotiation | 🟠 Medium |
| 4 | **Focus growth on West and East regions** — consistently highest revenue and profit | 🟡 Low |
| 5 | **Investigate Tables and Bookcases** sub-categories for discontinuation or repricing | 🔴 High |
| 6 | **Implement real-time profit alerts** when discount thresholds are exceeded at point of sale | 🟠 Medium |
""")


# ══════════════════════════════════════════════════════════════════════════════
# 9. DATASET METADATA
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-header">9. Dataset Metadata</div>', unsafe_allow_html=True)

st.markdown("""
| Field | Details |
|-------|---------|
| **Dataset Name** | Sample Superstore Dataset |
| **Dataset Type** | Tabular Dataset (structured, relational) |
| **Creator / Author** | Tableau Software |
| **Organization** | Tableau Software (now part of Salesforce) |
| **Contact** | support@tableau.com |
| **Date Created** | Public sample dataset; widely referenced since ~2014 |
| **Number of Records** | 9,994 rows |
| **Number of Variables** | 21 columns |
| **Repository / Link** | https://www.tableau.com/learn/articles/sample-data-sets |
| **License** | Public sample dataset for educational and analytical use |
| **Related Research** | Widely used in BI, data science education, and Kaggle competitions |
| **Coverage** | US retail orders from 2014 to 2017 |
""")

st.markdown("---")
st.markdown("""
<p style='text-align:center; color:#9ca3af; font-size:0.85rem;'>
  BSA83111 · Data Visualization for Decision Making ·
  Faculty of Management · Kepler College · 2026<br>
  Group: Dusengimana Olivier · Christian Habineza · Gilbert Niyonkuru ·
  Ushadia Uwimbabazi · Dative Akimana
</p>""", unsafe_allow_html=True)
