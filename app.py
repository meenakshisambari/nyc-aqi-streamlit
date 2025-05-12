import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import random

# --------------------------
# ✅ Page Setup
# --------------------------
st.set_page_config(page_title="NYC AQI Dashboard", layout="wide")
st.title("🌫️ NYC Air Quality Index (AQI) Dashboard")

# --------------------------
# ✅ Load and Prepare Data
# --------------------------
aqi_df = pd.read_csv("AQI_Classification.csv")

# Optional: strip column names in case of trailing spaces
aqi_df.columns = aqi_df.columns.str.strip()

# Convert date and extract time components
aqi_df['Start_Date'] = pd.to_datetime(aqi_df['Start_Date'], errors='coerce')
aqi_df['Year'] = aqi_df['Start_Date'].dt.year
aqi_df['Month'] = aqi_df['Start_Date'].dt.month

# --------------------------
# ✅ Create Tabs
# --------------------------
tabs = st.tabs(["📊 Dashboard", "🌐 Live AQI Scraper", "🤖 AQI Chatbot"])

# --------------------------
# 📊 Dashboard Tab
# --------------------------
with tabs[0]:
    st.header("📊 AQI Dashboard")

    selected_year = st.sidebar.selectbox("Select Year", sorted(aqi_df['Year'].dropna().unique()))
    threshold = st.sidebar.number_input("Set AQI Alert Threshold", min_value=0, max_value=500, value=100)

    filtered_df = aqi_df[aqi_df['Year'] == selected_year]

    if (filtered_df['AQI_Value'] > threshold).any():
        st.warning(f"⚠️ Alert: AQI exceeded {threshold} in {selected_year}!")
    else:
        st.success(f"✅ No AQI values above {threshold} in {selected_year}.")

    st.subheader(f"📈 Monthly Average AQI - {selected_year}")
    monthly_avg = filtered_df.groupby('Month')['AQI_Value'].mean()

    fig, ax = plt.subplots()
    monthly_avg.plot(kind='line', marker='o', ax=ax)
    ax.set_xlabel("Month")
    ax.set_ylabel("Average AQI")
    ax.set_title("Monthly AQI Trend")
    st.pyplot(fig)

    st.subheader("📊 AQI Category Distribution")
    st.bar_chart(filtered_df['AQI_Category'].value_counts())

    if st.checkbox("Show raw AQI data"):
        st.dataframe(filtered_df)

# --------------------------
# 🌐 Live AQI Scraper (Simulated)
# --------------------------
with tabs[1]:
    st.header("🌐 Live AQI Lookup (Simulated)")
    cities = ["New York", "Brooklyn", "Bronx", "Queens", "Manhattan"]
    selected_city = st.selectbox("Choose a City", cities)

    live_aqi = random.randint(30, 180)
    st.metric(label=f"Current AQI in {selected_city}", value=live_aqi)

    if live_aqi > 100:
        st.error("⚠️ Unhealthy air quality detected!")
    elif live_aqi > 50:
        st.warning("😐 Moderate air quality")
    else:
        st.success("😊 Good air quality")

# --------------------------
# 🤖 AQI Chatbot Tab (Rule-based)
with tabs[2]:
    st.header("🤖 Ask the AQI Bot")
    question = st.text_input("Ask: What was the average AQI in [region]?")

    if 'Location' in aqi_df.columns:
        # 🔍 DEBUG LINE – Shows all available locations
        st.write("Available locations:", aqi_df['Location'].dropna().unique())

        matched_region = None

        for region in aqi_df['Location'].dropna().unique():
            if region.lower() in question.lower() or question.lower() in region.lower():
                matched_region = region
                break

        if matched_region:
            avg_aqi = aqi_df[aqi_df['Location'] == matched_region]['AQI_Value'].mean()
            st.success(f"The average AQI for **{matched_region}** is **{avg_aqi:.2f}**.")
        elif question:
            st.warning("Sorry, I couldn't find that region in the dataset. Try typing a known NYC location.")
    else:
        st.error("❌ Column 'Location' not found in the dataset. Please check your file.")