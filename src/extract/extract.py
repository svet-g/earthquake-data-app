import os
from pathlib import Path
import sys
import geopandas
sys.path.append(str(Path(__file__).parent.parent.parent / "src"))
from utils.extract_utils import db_engine, get_table, recreate_geometry

cache_path = Path(__file__).parent.parent.parent / 'data' / 'cache' / 'earthquakes.parquet'

def extract():
    
    if os.path.isfile(cache_path):
        gdf = geopandas.read_parquet(cache_path)  
    else:
        engine = db_engine()
        table_name = 'earthquakes-svet-g'
        schema = 'de_2506_a'
        df = get_table(engine=engine, table_name=table_name, schema=schema)
        gdf = recreate_geometry(df)
        gdf.to_parquet(cache_path)
    return gdf

if __name__ == '__main__':
    extract()