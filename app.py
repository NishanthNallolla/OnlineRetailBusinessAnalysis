import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Online Retail Sales Dashboard",
    layout="wide"
)

@st.cache_data
def load_data():
    df = pd.read_excel("OnlineRetail.xlsx")
    df = df[(df['Quantity'] > 0) & (df['UnitPrice'] > 0)]
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    df['TotalPrice'] = df['Quantity'] * df['UnitPrice']
    return df

df = load_data()

st.sidebar.title("🔎 Filters")

country_filter = st.sidebar.multiselect(
    "Select Country",
    options=df['Country'].unique(),
    default=df['Country'].unique()
)

df = df[df['Country'].isin(country_filter)]

st.title("🛒 Online Retail Sales Analysis Dashboard")
st.caption("Interactive EDA | Business Insights | Streamlit + Plotly")

k1, k2, k3 = st.columns(3)

k1.metric("Total Revenue", f"${df['TotalPrice'].sum()/1e6:.2f} M")
k2.metric("Total Orders", f"{df['InvoiceNo'].nunique():,}")
k3.metric("Total Customers", f"{df['CustomerID'].nunique():,}")

st.divider()


top_products = (
    df.groupby('Description')['Quantity']
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig1 = px.bar(
    top_products,
    x='Quantity',
    y='Description',
    orientation='h',
    color='Quantity',
    color_continuous_scale='Viridis',
    title="Top 10 Best-Selling Products",
    template="plotly_dark"
)

st.plotly_chart(fig1, use_container_width=True)


top_countries = (
    df.groupby('Country')['TotalPrice']
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig2 = px.bar(
    top_countries,
    x='TotalPrice',
    y='Country',
    orientation='h',
    color='TotalPrice',
    color_continuous_scale='Magma',
    title="Top 10 Countries by Revenue",
    template="plotly_dark"
)

st.plotly_chart(fig2, use_container_width=True)

monthly_sales = (
    df.resample('M', on='InvoiceDate')['TotalPrice']
    .sum()
    .reset_index()
)

fig3 = px.line(
    monthly_sales,
    x='InvoiceDate',
    y='TotalPrice',
    markers=True,
    title="Monthly Revenue Trend",
    template="plotly_dark"
)

fig3.update_traces(line_width=3, line_color="#00c6ff")
st.plotly_chart(fig3, use_container_width=True)


top_customers = (
    df.groupby('CustomerID')['TotalPrice']
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig6 = px.bar(
    top_customers,
    x='TotalPrice',
    y=top_customers['CustomerID'].astype(str),
    orientation='h',
    color='TotalPrice',
    color_continuous_scale='Turbo',
    title="Top 10 Customers by Revenue",
    template="plotly_dark"
)

st.plotly_chart(fig6, use_container_width=True)

daily_sales = (
    df.resample('D', on='InvoiceDate')['TotalPrice']
    .sum()
    .reset_index()
)

fig7 = px.line(
    daily_sales,
    x='InvoiceDate',
    y='TotalPrice',
    title="Daily Sales Trend",
    template="plotly_dark"
)

fig7.update_traces(line_color="#2ecc71", line_width=2)
st.plotly_chart(fig7, use_container_width=True)

country_share = (
    df.groupby('Country')['TotalPrice']
    .sum()
    .sort_values(ascending=False)
    .head(5)
    .reset_index()
)

fig9 = px.pie(
    country_share,
    values='TotalPrice',
    names='Country',
    hole=0.45,
    title="Top 5 Countries – Revenue Share",
    color_discrete_sequence=px.colors.qualitative.Set2,
    template="plotly_dark"
)

st.plotly_chart(fig9, use_container_width=True)


