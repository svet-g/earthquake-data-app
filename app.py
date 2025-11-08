import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
from src.extract.extract import extract

def app():
    st.set_page_config(layout='wide', page_title='🌍 Earthquake Data Analysis - Last 30 Days')
    
    st.title('🌍 Earthquake Data Analysis - Last 30 Days')

    # Add refresh button in sidebar
    if st.sidebar.button('🔄 Refresh Data'):
        st.cache_data.clear()
        st.rerun()
    
    # load earthquake df
    df = extract()
    df = df.copy()
    df = df[df['mag'] > 0] # remove any earthquake with magnitude less than zero - put this into transform in the etl!
    df['date'] = df['time'].dt.date # make a date column
    df['time'] = df['time'].dt.time # make a time column
    
    # create sidebar for filters with 'filters' header
    st.sidebar.header('⚙️ Filters')
    
    # create a function for multiselect filters
    def create_multiselect_filter(column_name):
        if column_name in df.columns:
            return st.sidebar.multiselect(
                f'{column_name}',
                options=df[column_name].unique(),
                default=df[column_name].unique()
            )
        else:
            return None
    
    # create filters for depth, magType and alert
    depth_groups = create_multiselect_filter('depth_group')
    mag_types = create_multiselect_filter('magType')
    selected_alerts = create_multiselect_filter('alert')
    
    # significance filter
    if 'sig' in df.columns:
        sig_range = st.sidebar.slider(
            'Significance Range',
            min_value=int(df['sig'].min()),
            max_value=int(df['sig'].max()),
            value=(int(df['sig'].min()), int(df['sig'].max()))
        )
    else:
        sig_range = None
    
    # apply filters
    filtered_df = df.copy().reset_index()
    
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
            (filtered_df['alert'].isin(selected_alerts))
        ]
    
    # display filtered results info
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric('Total Earthquakes', len(filtered_df))
    with col2:
        if len(filtered_df) > 0:
            st.metric('Average Magnitude', f'{filtered_df['mag'].mean():.2f}')
        else:
            st.metric('Average Magnitude', 'N/A')
    with col3:
        if len(filtered_df) > 0:
            st.metric('Max Significance', f'{filtered_df['sig'].max():,}')
        else:
            st.metric('Max Significance', 'N/A')
    with col4:
        if len(filtered_df) > 0:
            alert = len(filtered_df[filtered_df['alert'].notna()])
            st.metric('With Alerts', alert)
        else:
            st.metric('With Alerts', 'N/A')
    
    if len(filtered_df) == 0:
        st.warning('No earthquakes match the selected filters. Try adjusting your criteria.')
        return
    
    # create tabs for different visualizations
    tab1, tab2, tab3 = st.tabs(['🗺️ Interactive Map', '⏳ Time Analysis', '📈 Significance vs Magnitude Analysis'])
    
    with tab1:
        st.subheader('Earthquakes Colored by significance, Sized by magnitude')
        
        # Create interactive plotly map
        fig_map = px.scatter_map(
            filtered_df,
            lat='latitude',
            lon='longitude',
            size='mag',
            color='sig',
            hover_data={
                'mag': True,
                'depth': True,
                'sig': True,
                'alert': True,
                'magType': True,
                'depth_group': True,
                'place': True,
                'date': True,
                'time': True,
                'latitude': ':.3f',
                'longitude': ':.3f'
            },
            color_continuous_scale='Oryel',
            size_max=15,
            height=900,
            opacity=0.7,
            map_style = 'carto-darkmatter',
            zoom=1
        )
        
        st.plotly_chart(fig_map)
        
    
    with tab2:
        st.subheader('Earthquakes Over Time')
        
        # earthquakes over time
        daily_count = filtered_df.groupby(filtered_df['date']).count()
        daily_count['date'] = daily_count.index
        daily_count['count'] = daily_count['id']
        
        fig_timeline = px.line(
            daily_count,
            x='date',
            y='count',
            height=700
        )
        
        fig_timeline.update_layout(
            xaxis_title='Date',
            yaxis_title='Number of Earthquakes'
        )
        
        fig_timeline.update_traces(line_color='#edd492', line_width=3)
        
        st.plotly_chart(fig_timeline)
    
    with tab3:
        st.subheader('Earthquake by Significance against Magnitude')

        # sig vs mag
        fig_sig = px.scatter(
            data_frame=filtered_df,
            x='mag',
            y='sig',
            color='depth_group',
            height=700,
            color_discrete_map={'shallow': '#edd492', 'intermediate': '#f78e5c', 'deep': '#f76b56', 'highest_depth': '#ee4d5a'},
            hover_data=['felt', 'cdi', 'alert'], # sig value is determined on a number of factors, including: magnitude, maximum MMI, felt reports, and estimated impact.
            opacity=0.7
        )
        st.plotly_chart(fig_sig)
    
    # show filtered_df
    with st.expander('📋 Data'):
        st.dataframe(filtered_df)

if __name__ == '__main__':
    app()
