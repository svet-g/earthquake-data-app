from utils.extract_utils import db_engine, get_table, recreate_geometry

def extract():
    engine = db_engine()
    table_name = 'earthquakes-svet-g'
    schema = 'de_2506_a'
    df = get_table(engine=engine, table_name=table_name, schema=schema)
    gdf = recreate_geometry(df)
    return gdf

if __name__ == '__main__':
    print(extract())