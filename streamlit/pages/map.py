import streamlit as st
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent / "src"))
from extract.extract import extract

def map():
    st.title('earthquake analysis')
    st.subheader('below is a map of earthquakes occuring in the last 30 days')
    gdf = extract()
    st.show(gdf.plot())
    
    
if __name__ == '__main__':
    map()