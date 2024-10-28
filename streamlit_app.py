import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime

# Set page configuration
st.set_page_config(page_title="Car Sales Dashboard", page_icon=":car:", layout="wide")

# Load Data
@st.cache_data
def load_data():
    return pd.read_csv("Car Sales.csv", encoding="ISO-8859-1")

df = load_data()

# Convert Date column to datetime and filter by selected date range
df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')
# df = df[(df["Date"] >= pd.to_datetime(start_date)) & (df["Date"] <= pd.to_datetime(end_date))]


# Sidebar
st.sidebar.title("Sales Insight")
st.sidebar.markdown("## Menu")
menu = st.sidebar.radio("", ("Overview", "Details"))

# Sidebar Filters
st.sidebar.markdown("## Filters")
body_style = st.sidebar.selectbox("Body Style", options=["All", "SUV", "Hatchback", "Sedan", "Passenger", "Hardtop"])
dealer_name = st.sidebar.selectbox("Dealer Name", options=["All", "Buddy Storebeck's Diesel Service Inc", "C & M Motors Inc", "Capitol KIA"])  # Example names; replace with unique values from your dataset
transmission = st.sidebar.selectbox("Transmission", options=["All", "Auto", "Manual"])
engine = st.sidebar.selectbox("Engine", options=["All", "Double Overhead Camshaft", "Overhead Camshaft"])

# # Load Data
# # Replace with the path to your actual dataset
# @st.cache_data
# def load_data():
#     return pd.read_csv("D:\Data Analysis Projects\Car Sales Project\Car Sales.csv", encoding="ISO-8859-1")

# df = load_data()

# # Data Preprocessing
# df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')

# Filter Data Based on Sidebar Inputs
if body_style != "All":
    df = df[df["Body Style"] == body_style]
if dealer_name != "All":
    df = df[df["Dealer_Name"] == dealer_name]
if transmission != "All":
    df = df[df["Transmission"] == transmission]
if engine != "All":
    df = df[df["Engine"] == engine]

# # Title and Date Range Display
# st.markdown("<h1 style='text-align: center; color: green;'>🚗 CAR SALES DASHBOARD | OVERVIEW</h1>", unsafe_allow_html=True)

# Top Header with Date Filter
header_col1, header_col2 = st.columns([3, 1])

with header_col1:
    st.markdown("<h1 style='text-align: left; color: green;'>🚗 CAR SALES DASHBOARD | " + menu.upper() + "</h1>", unsafe_allow_html=True)

with header_col2:
    # Date Range Picker
    st.write("**Select Date Range**")
    start_date = st.date_input("Start Date", datetime(2022, 1, 1), key="start_date")
    end_date = st.date_input("End Date", datetime(2022, 12, 31), key="end_date")

# Filter Data by Date
df = df[(df["Date"] >= pd.to_datetime(start_date)) & (df["Date"] <= pd.to_datetime(end_date))]


if menu == "Overview":
    # KPI Summary
    total_sales = df["Price ($)"].sum()
    avg_price = df["Price ($)"].mean()
    cars_sold = df["Car_id"].count()

    # Display KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("YTD Total Sales", f"${total_sales:,.1f}", "23.59%")
    col2.metric("YTD Avg Price", f"${avg_price:,.0f}", "-0.79%")
    col3.metric("YTD Cars Sold", f"{cars_sold}", "24.57%")
    col4.metric("MTD Cars Sold", f"{cars_sold // 12}", "1.92%")  # Example Month-to-Date calculation

    # Weekly Sales Trend (assuming data contains multiple dates for a weekly trend)
    st.subheader("YTD Sales Weekly Trend")
    df['Week'] = df['Date'].dt.isocalendar().week  # Extract week number
    weekly_sales = df.groupby("Week")["Price ($)"].sum().reset_index()
    fig = px.line(weekly_sales, x="Week", y="Price ($)", title="YTD Sales Weekly Trend")
    st.plotly_chart(fig, use_container_width=True)

    # Sales by Body Style
    st.subheader("YTD Total Sales by Body Style")
    body_style_sales = df.groupby("Body Style")["Price ($)"].sum().reset_index()
    fig = px.pie(body_style_sales, names="Body Style", values="Price ($)", title="Total Sales by Body Style")
    st.plotly_chart(fig, use_container_width=True)

    # Sales by Color
    st.subheader("YTD Total Sales by Color")
    color_sales = df.groupby("Color")["Price ($)"].sum().reset_index()
    fig = px.pie(color_sales, names="Color", values="Price ($)", title="Total Sales by Color")
    st.plotly_chart(fig, use_container_width=True)

    # Map of Cars Sold by Region
    st.subheader("YTD Cars Sold by Dealer Region")
    # Example: assuming dataset has Latitude and Longitude for each dealer region
    # If not available, consider an approximate plot or use specific coordinates for known regions
    # Replace `Latitude` and `Longitude` with actual values in dataset if available.
    # df['Latitude'] = [37.7749, 34.0522, 36.1699]  # Example values, replace with actual if available
    # df['Longitude'] = [-122.4194, -118.2437, -115.1398]

    # # Generate random coordinates for demonstration
    # unique_regions = df['Dealer_Region'].unique()
    # region_coords = {region: (np.random.uniform(25, 50), np.random.uniform(-125, -70)) for region in unique_regions}
    # df['Latitude'] = df['Dealer_Region'].map(lambda x: region_coords[x][0])
    # df['Longitude'] = df['Dealer_Region'].map(lambda x: region_coords[x][1])

    # Dictionary with approximate latitude and longitude for each dealer region
    region_coords = {
        "Middletown": (41.5623, -72.6506),
        "Aurora": (39.7294, -104.8319),
        "Greenville": (34.8526, -82.3940),
        "Scottsdale": (33.4949, -111.9217),
        "Pasco": (46.2305, -119.0922),
        "Austin": (30.2672, -97.7431),
        "Janesville": (42.6828, -89.0187),
        # Add more as needed
    }

    # Map the coordinates to each row based on the Dealer_Region
    df['Latitude'] = df['Dealer_Region'].map(lambda x: region_coords.get(x, np.nan)[0])
    df['Longitude'] = df['Dealer_Region'].map(lambda x: region_coords.get(x, np.nan)[1])


    fig = px.scatter_mapbox(df, lat="Latitude", lon="Longitude", size="Price ($)", hover_name="Dealer_Region", 
                            color_discrete_sequence=["fuchsia"], zoom=3, height=700)
    fig.update_layout(mapbox_style="carto-darkmatter")
    st.plotly_chart(fig, use_container_width=True)

    # Company-Wise Sales Trend
    st.subheader("Company-Wise Sales Trend")
    company_sales = df.groupby("Company").agg({"Price ($)": "sum", "Car_id": "count"}).reset_index()
    fig = go.Figure(data=[
        go.Bar(name='YTD Total Sales', x=company_sales["Company"], y=company_sales["Price ($)"], marker=dict(color='blue')),
        go.Bar(name='YTD Cars Sold', x=company_sales["Company"], y=company_sales["Car_id"], marker=dict(color='orange'))
    ])
    fig.update_layout(barmode='group', title="Company-Wise Sales Trend")
    st.plotly_chart(fig, use_container_width=True)

# Details Page
elif menu == "Details":
    # Display KPI Metrics
    total_sales = df["Price ($)"].sum()
    avg_price = df["Price ($)"].mean()
    cars_sold = df["Car_id"].count()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("YTD Total Sales", f"${total_sales:,.1f}", "23.59%")
    col2.metric("YTD Avg Price", f"${avg_price:,.0f}", "-0.79%")
    col3.metric("YTD Cars Sold", f"{cars_sold}", "24.57%")
    col4.metric("MTD Cars Sold", f"{cars_sold // 12}", "1.92%")

    # Display Data Table
    st.subheader("Detailed Car Sales Data")
    st.write("Below is the detailed data for each car sale:")
    df_display = df[["Car_id", "Date", "Customer Name", "Dealer_Name", "Company", "Color", "Model", "Price ($)"]]
    df_display["Total Sales"] = df_display["Price ($)"].apply(lambda x: f"${x:,.0f}")
    st.dataframe(df_display.style.format({"Price ($)": "${:,.0f}"}), height=400)

    # Display total sum at the bottom
    st.write(f"**Total Sales:** ${total_sales:,.0f}")
