import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title="Bike Sharing Dashboard",
    page_icon="🚲",
    layout="wide"
)

st.markdown("""
    <style>
    .main {
        background-color: #f0f8ff;
    }
    .stApp {
        background-image: linear-gradient(to right bottom, #f0f8ff, #e6f3ff, #dce9ff, #d2dfff, #c8d5ff);
    }
    div.css-1r6slb0.e1tzin5v2 {
        background-color: #ffffff;
        border: 2px solid #4e89ae;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 5px 5px 15px rgba(0,0,0,0.1);
    }
    div.css-12w0qpk.e1tzin5v2 {
        background-color: #ffffff;
        border: 2px solid #4e89ae;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 5px 5px 15px rgba(0,0,0,0.1);
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #ffffff;
        border-radius: 5px;
        padding: 10px 20px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    }
    .stTabs [aria-selected="true"] {
        background-color: #4e89ae;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <h1 style='text-align: center; color: #4e89ae; text-shadow: 2px 2px 4px rgba(0,0,0,0.1);'>
        🚲 BIKE SHARING STATISTICS
    </h1>
    <p style='text-align: center; color: #666; font-style: italic;'>
        
    </p>
    <hr style='width:50%; margin: auto; margin-bottom: 30px;'>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    day_df = pd.read_csv('data/day.csv')    # Ubah path
    hour_df = pd.read_csv('data/hour.csv')   # Ubah path
    
    # Convert dates
    day_df['dteday'] = pd.to_datetime(day_df['dteday'])
    hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])
    
    # Create mappings
    season_map = {1: 'Winter', 2: 'Spring', 3: 'Summer', 4: 'Fall'}
    weather_map = {1: 'Clear', 2: 'Mist', 3: 'Light Rain/Snow', 4: 'Heavy Rain/Snow'}
    weekday_map = {0: 'Sunday', 1: 'Monday', 2: 'Tuesday', 3: 'Wednesday', 
                   4: 'Thursday', 5: 'Friday', 6: 'Saturday'}
    
    # Apply mappings
    for df in [day_df, hour_df]:
        df['season'] = df['season'].map(season_map)
        df['weathersit'] = df['weathersit'].map(weather_map)
        df['weekday'] = df['weekday'].map(weekday_map)
    
    return day_df, hour_df


day_df, hour_df = load_data()

st.sidebar.header('Filters')
year = st.sidebar.selectbox('Select Year', day_df['dteday'].dt.year.unique())
season = st.sidebar.multiselect('Select Season', day_df['season'].unique())
weather = st.sidebar.multiselect('Select Weather', day_df['weathersit'].unique())

filtered_day_df = day_df.copy()
filtered_hour_df = hour_df.copy()

if year:
    filtered_day_df = filtered_day_df[filtered_day_df['dteday'].dt.year == year]
    filtered_hour_df = filtered_hour_df[filtered_hour_df['dteday'].dt.year == year]
if season:
    filtered_day_df = filtered_day_df[filtered_day_df['season'].isin(season)]
    filtered_hour_df = filtered_hour_df[filtered_hour_df['season'].isin(season)]
if weather:
    filtered_day_df = filtered_day_df[filtered_day_df['weathersit'].isin(weather)]
    filtered_hour_df = filtered_hour_df[filtered_hour_df['weathersit'].isin(weather)]

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f"""
        <div style='background-color: #4e89ae; padding: 20px; border-radius: 10px; text-align: center;'>
            <h3 style='color: white; margin: 0;'>Total Rentals</h3>
            <p style='color: white; font-size: 24px; margin: 0;'>{filtered_day_df['cnt'].sum():,}</p>
        </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown(f"""
        <div style='background-color: #43658b; padding: 20px; border-radius: 10px; text-align: center;'>
            <h3 style='color: white; margin: 0;'>Average Daily</h3>
            <p style='color: white; font-size: 24px; margin: 0;'>{filtered_day_df['cnt'].mean():,.0f}</p>
        </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown(f"""
        <div style='background-color: #4e89ae; padding: 20px; border-radius: 10px; text-align: center;'>
            <h3 style='color: white; margin: 0;'>Casual Users</h3>
            <p style='color: white; font-size: 24px; margin: 0;'>{(filtered_day_df['casual'].sum() / filtered_day_df['cnt'].sum() * 100):,.1f}%</p>
        </div>
    """, unsafe_allow_html=True)
with col4:
    st.markdown(f"""
        <div style='background-color: #43658b; padding: 20px; border-radius: 10px; text-align: center;'>
            <h3 style='color: white; margin: 0;'>Registered Users</h3>
            <p style='color: white; font-size: 24px; margin: 0;'>{(filtered_day_df['registered'].sum() / filtered_day_df['cnt'].sum() * 100):,.1f}%</p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ['Daily Trends', 'User Analysis', 'Weather Impact', 'Pattern Analysis', 'Hourly Analysis'])

with tab1:
    st.subheader('Daily Rental Trends')

    col1, col2 = st.columns([2, 2])
    with col1:
        start_date = st.date_input("Start Date", filtered_day_df['dteday'].min(), key='start_date')
    with col2:
        end_date = st.date_input("End Date", filtered_day_df['dteday'].max(), key='end_date')

    mask = (filtered_day_df['dteday'].dt.date >= start_date) & (filtered_day_df['dteday'].dt.date <= end_date)
    date_filtered_df = filtered_day_df.loc[mask]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=date_filtered_df['dteday'],
        y=date_filtered_df['cnt'],
        name='Total',
        line=dict(color='#0052cc', width=2),
        mode='lines'
    ))

    fig.add_trace(go.Scatter(
        x=date_filtered_df['dteday'],
        y=date_filtered_df['registered'],
        name='Registered',
        line=dict(color='#ff4d4d', width=2),
        mode='lines'
    ))

    fig.add_trace(go.Scatter(
        x=date_filtered_df['dteday'],
        y=date_filtered_df['casual'],
        name='Casual',
        line=dict(color='#00ccff', width=2),
        mode='lines'
    ))

    fig.update_layout(
        title={
            'text': 'Daily Rental Pattern',
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis_title='Date',
        yaxis_title='Number of Rentals',
        height=500,
        plot_bgcolor='white',
        paper_bgcolor='white',
        hovermode='x unified',
        xaxis=dict(
            showgrid=True,
            gridcolor='#E5E5E5',
            showline=True,
            linewidth=1,
            linecolor='#E5E5E5',

            rangeselector=dict(
                buttons=list([
                    dict(count=7, label="1W", step="day", stepmode="backward"),
                    dict(count=1, label="1M", step="month", stepmode="backward"),
                    dict(count=3, label="3M", step="month", stepmode="backward"),
                    dict(count=6, label="6M", step="month", stepmode="backward"),
                    dict(count=1, label="1Y", step="year", stepmode="backward"),
                    dict(step="all", label="All")
                ]),
                bgcolor="#E5E5E5",
                activecolor="#0052cc",
                x=0,
                y=1.1,
            )
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='#E5E5E5',
            showline=True,
            linewidth=1,
            linecolor='#E5E5E5',
            rangemode='tozero'
        ),
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='right',
            x=1
        ),
        margin=dict(l=60, r=30, t=100, b=60)
    )

    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader('User Type Analysis')

    # User distribution pie chart
    user_dist = pd.DataFrame({
        'Type': ['Casual', 'Registered'],
        'Count': [filtered_day_df['casual'].sum(), filtered_day_df['registered'].sum()]
    })
    fig = px.pie(user_dist, values='Count', names='Type',
                 title='Distribution of User Types')
    st.plotly_chart(fig, use_container_width=True)

    # Weekly pattern
    weekly_pattern = filtered_day_df.groupby('weekday')[['casual', 'registered']].mean().reset_index()
    fig = go.Figure()
    fig.add_trace(go.Bar(x=weekly_pattern['weekday'], y=weekly_pattern['casual'],
                         name='Casual'))
    fig.add_trace(go.Bar(x=weekly_pattern['weekday'], y=weekly_pattern['registered'],
                         name='Registered'))
    fig.update_layout(title='Average Daily Rentals by User Type',
                      barmode='group',
                      xaxis_title='Day of Week',
                      yaxis_title='Average Rentals')
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.subheader('Weather Impact Analysis')

    # Weather impact
    fig = px.box(filtered_day_df, x='weathersit', y='cnt',
                 title='Weather Impact on Rentals',
                 labels={'weathersit': 'Weather Condition', 'cnt': 'Number of Rentals'})
    st.plotly_chart(fig, use_container_width=True)

    # Temperature correlation
    fig = px.scatter(filtered_day_df, x='temp', y='cnt', color='season',
                     title='Temperature vs Rentals',
                     labels={'temp': 'Temperature (°C)', 'cnt': 'Number of Rentals'})
    st.plotly_chart(fig, use_container_width=True)

with tab4:
    st.subheader('Pattern Analysis')

    # Correlation heatmap
    corr_cols = ['temp', 'atemp', 'hum', 'windspeed', 'casual', 'registered', 'cnt']
    corr = filtered_day_df[corr_cols].corr()
    fig = px.imshow(corr,
                    labels=dict(color="Correlation"),
                    title='Correlation Heatmap')
    st.plotly_chart(fig, use_container_width=True)

    # Working day vs holiday pattern
    work_holiday = filtered_day_df.groupby('workingday')[['casual', 'registered']].mean().reset_index()
    fig = go.Figure()
    fig.add_trace(go.Bar(x=['Working Day', 'Holiday'], y=work_holiday['casual'],
                         name='Casual'))
    fig.add_trace(go.Bar(x=['Working Day', 'Holiday'], y=work_holiday['registered'],
                         name='Registered'))
    fig.update_layout(title='Average Rentals: Working Days vs Holidays',
                      barmode='group',
                      xaxis_title='Day Type',
                      yaxis_title='Average Rentals')
    st.plotly_chart(fig, use_container_width=True)

with tab5:
    st.subheader('Hourly Rental Analysis')

    # Average rentals by hour
    hourly_avg = filtered_hour_df.groupby('hr')[['casual', 'registered', 'cnt']].mean().reset_index()

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=hourly_avg['hr'], y=hourly_avg['cnt'],
                             name='Total', mode='lines+markers'))
    fig.add_trace(go.Scatter(x=hourly_avg['hr'], y=hourly_avg['casual'],
                             name='Casual', mode='lines+markers'))
    fig.add_trace(go.Scatter(x=hourly_avg['hr'], y=hourly_avg['registered'],
                             name='Registered', mode='lines+markers'))
    fig.update_layout(title='Average Hourly Rental Pattern',
                      xaxis_title='Hour of Day',
                      yaxis_title='Average Number of Rentals',
                      xaxis=dict(tickmode='linear', tick0=0, dtick=1))
    st.plotly_chart(fig, use_container_width=True)

    # Heatmap of hourly rentals by day of week
    hourly_weekday = filtered_hour_df.pivot_table(values='cnt',
                                                  index='hr',
                                                  columns='weekday',
                                                  aggfunc='mean')
    fig = px.imshow(hourly_weekday,
                    labels=dict(x='Day of Week', y='Hour of Day', color='Average Rentals'),
                    title='Heatmap: Average Rentals by Hour and Day')
    st.plotly_chart(fig, use_container_width=True)

st.markdown('---')
st.markdown('Created by Wuri')
