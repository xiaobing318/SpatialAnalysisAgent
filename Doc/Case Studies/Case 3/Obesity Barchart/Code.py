import geopandas as gpd
import seaborn as sns
import matplotlib.pyplot as plt
import os
def create_obesity_barchart():
    # Define file paths
    shp_path = 'D:/Case_Studies/Data/US_Counties/US_Counties.shp'
    output_dir = 'C:/Users/AKINBOYEWA TEMITOPE/AppData/Roaming/QGIS/QGIS3/profiles/default/python/plugins/SpatialAnalysisAgent-master/Default_workspace'
    # Load the shapefile into a GeoDataFrame
    counties_gdf = gpd.read_file(shp_path)
    # Convert fields to appropriate datatypes if needed
    counties_gdf['Obesity'] = counties_gdf['Obesity'].astype(float)
    # Aggregate obesity prevalence by state
    obesity_by_state = counties_gdf.groupby('State')['Obesity'].mean().reset_index()
    # Create a bar plot using seaborn
    plt.figure(figsize=(12, 8))
    bar_plot = sns.barplot(x='State', y='Obesity', data=obesity_by_state)
    bar_plot.set_title('Obesity Prevalence by State in the United States')
    bar_plot.set_xlabel('State')
    bar_plot.set_ylabel('Average Obesity Prevalence (%)')
    # Rotate x labels for better readability
    bar_plot.set_xticklabels(bar_plot.get_xticklabels(), rotation=45, horizontalalignment='right')
    # Ensure the output file path is unique
    filename_base = 'US_Obesity_Prev_Barchart'
    filename = filename_base + '.png'
    output_html = os.path.join(output_dir, filename)
    version = 1
    while os.path.exists(output_html):
        filename = f"{filename_base}_{version}.png"
        output_html = os.path.join(output_dir, filename)
        version += 1
    # Save the plot as an HTML file in the output directory
    plt.tight_layout()
    plt.savefig(output_html)
    plt.close()
    # Print the path to the saved output
    print(output_html)
# Execute the function
create_obesity_barchart()




