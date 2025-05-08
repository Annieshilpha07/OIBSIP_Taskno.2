import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import json
import plotly.graph_objects as go

st.set_page_config(page_title="Unemployment Analysis India", layout="wide")

# Load data
df1 = pd.read_csv('Unemployment in India.csv')
df2 = pd.read_csv('Unemployment_Rate_upto_11_2020.csv')
df1.dropna(inplace=True)
df2.dropna(inplace=True)

df1.columns = df1.columns.str.strip()
df2.columns = df2.columns.str.strip()

# Convert Date column
df1['Date'] = pd.to_datetime(df1['Date'], dayfirst=True, errors='coerce')
df1['Month_Year'] = df1['Date'].dt.strftime('%b-%Y')
df1['Year'] = df1['Date'].dt.year

# Main function
def main():
    st.title(":rainbow[Unemployment Analysis in India]")
    
    #st.set_page_config(page_title="Unemployment Analysis India", layout="wide")
    selected = option_menu(
        menu_title="Unemployment Analysis Dashboard",
        options=["Home", "EDA & Insights"],
        icons=["house", "bar-chart-line"],
        default_index=0,
        orientation="horizontal"
    )

    if selected == "Home":
        st.markdown("<h2 style='color:#ff6600;'>📊 Unemployment Analysis During COVID-19 in India</h2>", unsafe_allow_html=True)

        col1, col2 = st.columns([2, 2], gap="large")

        with col1:
            st.markdown("<h3 style='color:#e67300;'>Overview</h3>", unsafe_allow_html=True)
            st.markdown("""
                <ul style='font-size:17px;'>
                    <li>Analysis of monthly unemployment trends across Indian states</li>
                    <li>Focus on COVID-19's impact starting from April 2020</li>
                    <li>Interactive charts and maps for data visualization</li>
                </ul>
            """, unsafe_allow_html=True)

            st.markdown("<h3 style='color:#e67300;'>Skills Takeaway</h3>", unsafe_allow_html=True)
            st.markdown("<p style='font-size:17px;'>Data Cleaning, EDA, Time Series, Geospatial Mapping, Streamlit, Plotly</p>", unsafe_allow_html=True)

            st.markdown("<h3 style='color:#e67300;'>About the Dataset</h3>", unsafe_allow_html=True)
            st.markdown('<p style="font-size:17px;">This dataset tracks unemployment rates across India during COVID-19, with data on states, unemployment rate, employed percentage, and labor participation.</p>', unsafe_allow_html=True)

            st.markdown("<h3 style='color:#e67300;'>Dataset Columns</h3>", unsafe_allow_html=True)
            st.markdown("""
                <ul style='font-size:17px;'>
                    <li>🌍 <b>Region</b>: State or union territory</li>
                    <li>📅 <b>Date</b>: When the data was recorded</li>
                    <li>🔄 <b>Frequency</b>: Data frequency (Monthly)</li>
                    <li>📉 <b>Estimated Unemployment Rate (%)</b></li>
                    <li>👷 <b>Estimated Employed</b></li>
                    <li>📊 <b>Estimated Labour Participation Rate (%)</b></li>
                    <li>🏡 <b>Area</b>: Urban or Rural</li>
                </ul>
            """, unsafe_allow_html=True)

        with col2:
            st.image("https://www.studyiq.com/articles/wp-content/uploads/2023/09/07153648/Unemployment-in-India.jpg", use_container_width=True)
            st.write(" ")
            st.image("https://cirs.qatar.georgetown.edu/wp-content/uploads/sites/3/2020/08/news_129130_50103_1597129611-1-1024x576.jpg", use_container_width=True)
            st.write(" ")
            st.markdown("<h3 style='color:#e67300;'>Purpose</h3>", unsafe_allow_html=True)
            st.markdown('<p style="font-size:17px;">Understand the impact of COVID-19 on unemployment in India and explore trends over time.</p>', unsafe_allow_html=True)

    if selected == "EDA & Insights":
        st.title("🔍 Exploratory Data Analysis")

        topics = [
            "1. 📉 State-wise Unemployment Rate in India - Histogram",
            "2. 📊 Year-wise Unemployment Rate in India",
            "3. 🌍 Average Unemployment Rate Across Indian Zones",
            "4. 🗺️ Unemployment by State (Choropleth Map)",
            "5. 📅 Monthly Unemployment Rate by Area - Bar Chart",
            "6. 👷 Monthly Labour Participation Rate by Area (Faceted View)",
            "7. 🏠 Estimated Employed Over Time by Area (Area Chart)",
            "8. 🔝 Top 10 Regions by Unemployment Rate",
            "9. 🚀 Top 10 Regions with Highest Employment Growth Rate",
            "10. 💡 Pre-COVID and Post-COVID Unemployment Rates",
            "11. 📉 State with Most Variation in Unemployment"
        ]

        selected_topic = st.selectbox("Select an EDA Topic", topics)
        st.write(f"You selected: **{selected_topic}**")

        if selected_topic == topics[0]:
            df_avg = df1.groupby('Region').agg({
                'Estimated Unemployment Rate (%)': 'mean',
                'Estimated Employed': 'sum'
            }).reset_index()
            fig = px.bar(df_avg, x='Region', y='Estimated Unemployment Rate (%)', color='Region',
                            title='Average Unemployment Rate per State', template='plotly',
                            hover_data={'Estimated Unemployment Rate (%)': ':.2f', 'Estimated Employed': ':.0f'})
            fig.update_layout(xaxis={'categoryorder': 'total descending'})
            st.plotly_chart(fig)

        elif selected_topic == topics[1]:
            df_filtered = df1[df1['Year'].isin([2019, 2020])]
            yearly_avg = df_filtered.groupby('Year')['Estimated Unemployment Rate (%)'].mean().reset_index()
            fig = px.bar(yearly_avg, x='Year', y='Estimated Unemployment Rate (%)', text='Estimated Unemployment Rate (%)',
                            title='Year-wise Average Unemployment Rate (2019 & 2020)', color='Estimated Unemployment Rate (%)')
            fig.update_traces(textposition='outside')
            st.plotly_chart(fig)

        elif selected_topic == topics[2]:
            df2.rename(columns={'Region': 'State', 'Region.1': 'Zone'}, inplace=True)
            zone_data = df2[['State', 'Zone']].drop_duplicates().groupby('Zone').size().reset_index(name='State Count')
            fig = px.pie(zone_data, names='Zone', values='State Count', title='Distribution of States by Zone')
            st.plotly_chart(fig)

        elif selected_topic == topics[3]:
            df2.columns = df2.columns.str.strip()
            df2.rename(columns={'Region': 'State', 'Region.1': 'Zone'}, inplace=True)
            df_state_avg = df2.groupby('State')['Estimated Unemployment Rate (%)'].mean().reset_index()

            with open("india_states.geojson.txt", "r") as f:
                india_geojson = json.load(f)

            fig = go.Figure(go.Choropleth(
                geojson=india_geojson,
                featureidkey="properties.ST_NM",
                locations=df_state_avg['State'],
                z=df_state_avg['Estimated Unemployment Rate (%)'],
                colorscale="Viridis",
                colorbar_title="Unemployment Rate (%)",
                marker_line_color='black',
                marker_line_width=0.5,
                hovertext=df_state_avg['State'],
                hoverinfo="location+z"
            ))

            fig.update_geos(visible=False, fitbounds="locations")

            fig.update_layout(
                title_text="Average Unemployment Rate by State (India)",
                geo=dict(showframe=False, showcoastlines=False),
                height=800,
                width=1000
            )
            st.plotly_chart(fig)

        elif selected_topic == topics[4]:
            fig = px.bar(df1, x='Month_Year', y='Estimated Unemployment Rate (%)', color='Area', barmode='group',
                            title='Monthly Unemployment Rate by Area')
            fig.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig)

        elif selected_topic == topics[5]:
            fig = px.bar(df1, x='Month_Year', y='Estimated Labour Participation Rate (%)', color='Area',
                            title='Monthly Labour Participation Rate by Area')
            fig.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig)

        elif selected_topic == topics[6]:
            fig = px.area(df1, x='Month_Year', y='Estimated Employed', color='Area',
                            title='Estimated Employed Over Time by Area')
            fig.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig)

        elif selected_topic == topics[7]:
            top_unemployment = df1.groupby('Region')['Estimated Unemployment Rate (%)'].mean().nlargest(10).reset_index()
            fig = px.bar(top_unemployment, x='Region', y='Estimated Unemployment Rate (%)', color='Region',
                            title='Top 10 Regions by Unemployment Rate')
            st.plotly_chart(fig)

        elif selected_topic == topics[8]:
            top_employed = df1.groupby('Region')['Estimated Employed'].mean().nlargest(10).reset_index()
            top_employed['Percentage'] = (top_employed['Estimated Employed'] / top_employed['Estimated Employed'].sum()) * 100
            fig = px.bar(top_employed, x='Region', y='Estimated Employed', color='Region',
                            title='Top 10 Regions with Highest Employment Growth Rate')
            st.plotly_chart(fig)

        elif selected_topic == topics[9]:
            covid_start = pd.to_datetime('2020-04-01')
            df1['COVID_19_Flag'] = df1['Date'].apply(lambda x: 'Yes' if x >= covid_start else 'No')
            avg_data = df1.groupby('COVID_19_Flag')['Estimated Unemployment Rate (%)'].mean().reset_index()
            avg_data['Period'] = avg_data['COVID_19_Flag'].map({'Yes': 'Post-COVID', 'No': 'Pre-COVID'})
            fig = px.bar(avg_data, x='Period', y='Estimated Unemployment Rate (%)', color='Period',
                            title='Average Unemployment Rate: Pre vs Post COVID')
            st.plotly_chart(fig)

        elif selected_topic == topics[10]:
            fig, ax = plt.subplots(figsize=(12, 6))
            sns.lineplot(data=df1, x='Date', y='Estimated Unemployment Rate (%)', ci=None, color='blue', ax=ax)
            ax.axvline(pd.to_datetime('2020-04-01'), color='red', linestyle='--', label='COVID-19 Start')
            ax.set_title('Unemployment Rate Trends Over Time')
            ax.legend()
            st.pyplot(fig)

if __name__ == "__main__":
    main()
