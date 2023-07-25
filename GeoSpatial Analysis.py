import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

# Define filepath
filepath = r

# Load Excel file using Pandas
f = pd.read_excel(filepath, sheet_name=None)

# Iterate through each worksheet
for name, df in f.items():
    

    df.columns = df.columns.str.strip()  # Strip whitespace from column names
    print(df.columns)  # Print column names to verify

    # Step 2: Create Point geometries from latitude and longitude
    geometry = [Point(xy) for xy in zip(df['Longitude'], df['Latitude'])]

    # Step 3: Convert DataFrame to GeoDataFrame
    gdf = gpd.GeoDataFrame(df, crs='EPSG:4326', geometry=geometry)
    
    # Step 4: Create rings of 5-mile radius around each point
    gdf['buffered_geometry'] = gdf.geometry.buffer(5 / 69)  # Assuming 1 degree is approximately 69 miles
    
    # Step 5: Count points within each ring
    gdf['points_within_ring'] = gdf.apply(
        lambda row: gdf[gdf.geometry.within(row['buffered_geometry'])].shape[0], axis=1)
    
    # Step 6: Sort and find the top 20 clusters
    top_20_clusters = gdf.sort_values(by='points_within_ring', ascending=False).head(10)
    
    # Step 7: Save the top 20 clusters as the first Excel file
    output_file_path_clusters = r
    top_20_clusters.to_excel(output_file_path_clusters, index=False)
    print("Top 20 clusters saved to Excel file:", output_file_path_clusters)
    
    # Step 8: Create a new GeoDataFrame with the center points of the rings
    center_points = gdf.copy()
    center_points.geometry = center_points['buffered_geometry'].centroid
    
    # Step 9: Save the center points as the second Excel file
    output_file_path_center_points = r
    center_points.to_excel(output_file_path_center_points, index=False)
    print("Center points of rings saved to Excel file:", output_file_path_center_points)
