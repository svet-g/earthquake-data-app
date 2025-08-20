import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
from src.extract.extract import extract

def interactive_earthquake_map():
    st.set_page_config(layout="wide", page_title="Interactive Earthquake Analysis")
    
    st.title('🌍 Interactive Earthquake Analysis')
    st.markdown("Filter and explore earthquake data with interactive controls")
    
    # Load earthquake data
    df = extract()
    
    # Create sidebar for filters
    st.sidebar.header('Filters')
    
    # Depth Group Filter
    if 'depth_group' in df.columns:
        depth_groups = st.sidebar.multiselect(
            'Depth Group',
            options=df['depth_group'].unique(),
            default=df['depth_group'].unique(),
            help="Select depth categories to display"
        )
    else:
        depth_groups = None
    
    # Magnitude Type Filter
    if 'magType' in df.columns:
        mag_types = st.sidebar.multiselect(
            'Magnitude Type',
            options=df['magType'].unique(),
            default=df['magType'].unique(),
            help="Filter by magnitude measurement type"
        )
    else:
        mag_types = None
    
    # Significance Filter
    if 'sig' in df.columns:
        sig_range = st.sidebar.slider(
            'Significance Range',
            min_value=int(df['sig'].min()),
            max_value=int(df['sig'].max()),
            value=(int(df['sig'].min()), int(df['sig'].max())),
            help="Filter by earthquake significance (higher = more significant)"
        )
    else:
        sig_range = None
    
    # Alert Level Filter
    if 'alert' in df.columns:
        alert_levels = df['alert'].dropna().unique()
        selected_alerts = st.sidebar.multiselect(
            'Alert Level',
            options=alert_levels,
            default=alert_levels,
            help="Filter by PAGER alert level"
        )
    else:
        selected_alerts = None
    
    # Time Filter
    if 'time' in df.columns:
        # Convert time column to datetime if it isn't already
        if not pd.api.types.is_datetime64_any_dtype(df['time']):
            df['time'] = pd.to_datetime(df['time'])
        
        time_range = st.sidebar.date_input(
            'Date Range',
            value=(df['time'].min().date(), df['time'].max().date()),
            min_value=df['time'].min().date(),
            max_value=df['time'].max().date(),
            help="Select date range for earthquakes"
        )
    else:
        time_range = None
    
    # Apply filters
    filtered_df = df.copy()
    
    if depth_groups:
        filtered_df = filtered_df[filtered_df['depth_group'].isin(depth_groups)]
    
    if mag_types:
        filtered_df = filtered_df[filtered_df['magType'].isin(mag_types)]
    
    if sig_range:
        filtered_df = filtered_df[
            (filtered_df['sig'] >= sig_range[0]) & 
            (filtered_df['sig'] <= sig_range[1])
        ]
    
    if selected_alerts:
        filtered_df = filtered_df[
            (filtered_df['alert'].isin(selected_alerts)) | 
            (filtered_df['alert'].isna())
        ]
    
    if time_range and len(time_range) == 2:
        start_date = pd.Timestamp(time_range[0], tz='UTC')
        end_date = pd.Timestamp(time_range[1], tz='UTC') + timedelta(days=1)
        filtered_df = filtered_df[
            (filtered_df['time'] >= start_date) & 
            (filtered_df['time'] < end_date)
        ]
    
    # Display filtered results info
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Earthquakes", len(filtered_df))
    with col2:
        if len(filtered_df) > 0:
            st.metric("Avg Magnitude", f"{filtered_df['mag'].mean():.1f}")
        else:
            st.metric("Avg Magnitude", "N/A")
    with col3:
        if len(filtered_df) > 0:
            st.metric("Max Significance", f"{filtered_df['sig'].max():,}")
        else:
            st.metric("Max Significance", "N/A")
    with col4:
        if len(filtered_df) > 0:
            high_alert = len(filtered_df[filtered_df['alert'].notna()])
            st.metric("With Alerts", high_alert)
        else:
            st.metric("With Alerts", "N/A")
    
    if len(filtered_df) == 0:
        st.warning("No earthquakes match the selected filters. Try adjusting your criteria.")
        return
    
    # Create tabs for different visualizations
    tab1, tab2, tab3 = st.tabs(["🗺️ Interactive Map", "📊 Time Series", "📈 Analysis"])
    
    with tab1:
        st.subheader("Interactive Earthquake Map")
        
        # Create size column for plotting (handle negative magnitudes)
        filtered_df = filtered_df.copy()
        filtered_df['size'] = filtered_df['mag'].apply(lambda x: max(abs(x) * 3 + 5, 3))
        
        # Create interactive plotly map
        fig = px.scatter_map(
            filtered_df,
            lat='latitude',
            lon='longitude',
            size='size',
            color='sig',
            hover_data={
                'mag': True,
                'depth': True,
                'sig': True,
                'alert': True,
                'magType': True,
                'depth_group': True,
                'place': True,
                'time': True,
                'latitude': ':.3f',
                'longitude': ':.3f'
            },
            color_continuous_scale='Viridis',
            size_max=20,
            height=600,
            title="Earthquakes colored by Significance, sized by Magnitude"
        )
        
        fig.update_layout(
            margin={"r":0,"t":50,"l":0,"b":0},
            coloraxis_colorbar=dict(
                title="Significance"
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("Earthquake Timeline")
        
        # Time series plot
        daily_counts = filtered_df.groupby(filtered_df['time'].dt.date).size().reset_index()
        daily_counts.columns = ['date', 'count']
        
        fig_timeline = px.line(
            daily_counts,
            x='date',
            y='count',
            title='Daily Earthquake Count',
            height=400
        )
        
        fig_timeline.update_layout(
            xaxis_title="Date",
            yaxis_title="Number of Earthquakes"
        )
        
        st.plotly_chart(fig_timeline, use_container_width=True)
    
    with tab3:
        st.subheader("Statistical Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Magnitude distribution by depth group
            if 'depth_group' in filtered_df.columns:
                fig_mag = px.box(
                    filtered_df,
                    x='depth_group',
                    y='mag',
                    title='Magnitude Distribution by Depth Group',
                    height=400
                )
                st.plotly_chart(fig_mag, use_container_width=True)
        
        with col2:
            # Significance vs Magnitude scatter
            fig_sig = px.scatter(
                filtered_df,
                x='mag',
                y='sig',
                color='depth_group' if 'depth_group' in filtered_df.columns else None,
                title='Significance vs Magnitude',
                height=400,
                hover_data=['place', 'time']
            )
            st.plotly_chart(fig_sig, use_container_width=True)
    
    # Display filtered data table
    with st.expander("📋 View Filtered Data"):
        st.dataframe(
            filtered_df[['time', 'place', 'mag', 'depth', 'sig', 'alert', 'magType', 'depth_group']].head(100),
            use_container_width=True
        )

# Call the function
if __name__ == '__main__':
    interactive_earthquake_map()