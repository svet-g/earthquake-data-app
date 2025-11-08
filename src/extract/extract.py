import os
from pathlib import Path
import sys
import geopandas
import pandas as pd
sys.path.append(str(Path(__file__).parent.parent.parent / "src"))
from utils.extract_utils import db_engine, get_table

cache_path = Path(__file__).parent.parent.parent / 'data' / 'earthquakes.parquet'

def extract():
    
    if os.path.isfile(cache_path):
        df = pd.read_parquet(cache_path)  
    else:
        engine = db_engine()
        table_name = 'earthquakes-svet-g'
        schema = 'de_2506_a'
        df = get_table(engine=engine, table_name=table_name, schema=schema)
        # gdf = recreate_geometry(df)
        df.to_parquet(cache_path)
    return df

if __name__ == '__main__':
    extract()
