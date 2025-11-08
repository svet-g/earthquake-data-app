import os
from pathlib import Path
import sys
import geopandas
import pandas as pd
import streamlit as st
sys.path.append(str(Path(__file__).parent.parent.parent / "src"))
from utils.extract_utils import db_engine, get_table

@st.cache_data(ttl=86400)
def extract():
    engine = db_engine()
    table_name = 'earthquakes-svet-g'
    schema = 'de_2506_a'
    df = get_table(engine=engine, table_name=table_name, schema=schema)
    # gdf = recreate_geometry(df)
    return df

if __name__ == '__main__':
    extract()
