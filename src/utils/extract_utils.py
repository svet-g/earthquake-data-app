import os
from dotenv import load_dotenv
from sqlalchemy import text, create_engine, Engine
import pandas as pd
import geopandas

def db_engine(db='SOURCE') -> Engine:
    '''
    creates a database engine
    
    params: db (str) -> type of db: 'TARGET' or 'SOURCE' to complete the enviroment variable name string, defaults to 'SOURCE'
    
    returns: a SQLAlchemy db engine
    
    '''
    load_dotenv()
    user = os.getenv(f'{db}_DB_USER')
    password = os.getenv(f'{db}_DB_PASSWORD')
    host = os.getenv(f'{db}_DB_HOST')
    port = os.getenv(f'{db}_DB_PORT')
    database = os.getenv(f'{db}_DB_NAME')
    
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{database}')
    
    return engine

def get_table(engine, table_name, schema) -> pd.DataFrame:
    with engine.begin() as conn:
        df = pd.read_sql_table(table_name, conn, index_col='id', schema=schema)
        return df
        

# def recreate_geometry(df) -> geopandas.GeoDataFrame:
#     geometry = geopandas.points_from_xy(df['longitude'], df['latitude'], df['depth'])
#     gdf = geopandas.GeoDataFrame(df, geometry=geometry)
#     return gdf