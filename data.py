import osmium
import geopandas as gpd
import sqlite3

class OSMHandler(osmium.SimpleHandler):
    def __init__(self):
        super(OSMHandler, self).__init__()
        self.restaurants = []

    def node(self, n):
        # Process nodes
        if 'amenity' in n.tags and n.tags['amenity'] == 'restaurant':
            self.restaurants.append({
                'name': n.tags.get('name', 'Unknown'),
                'cuisine': n.tags.get('cuisine', 'Unknown'),
                'geometry': 'POINT({} {})'.format(n.location.lon, n.location.lat)
            })

    def way(self, w):
        # Process ways
        pass

    def relation(self, r):
        # Process relations
        pass

# Specify the path to the OSM file
osm_file = 'new-york-latest.osm.pbf'

# Create an instance of the handler
handler = OSMHandler()

# Iterate over the OSM file and handle the data
handler.apply_file(osm_file)

# Convert restaurant data to a GeoDataFrame
gdf_restaurants = gpd.GeoDataFrame(handler.restaurants)

# Generate SQL statements
create_table_sql = '''
CREATE TABLE restaurants
    (name TEXT, cuisine TEXT, geometry TEXT);
'''

insert_data_sql = '''
INSERT INTO restaurants (name, cuisine, geometry)
VALUES
'''

for _, row in gdf_restaurants.iterrows():
    insert_data_sql += "('{}', '{}', '{}'),\n".format(row['name'], row['cuisine'], row['geometry'])

# Remove the trailing comma and newline character
insert_data_sql = insert_data_sql[:-2] + ';'

# Save the SQL statements to a .sql file
with open('restaurant_data.sql', 'w', encoding='utf-8') as file:
    file.write(create_table_sql + '\n')
    file.write(insert_data_sql)
