
import pandas as pd
import plotly.express as px

# 1. Read the file "PIB.xlsx"
excel_file_PIB = 'PIB.xlsx'
try:
    pib_df = pd.read_excel(excel_file_PIB)  # Changed variable name to pib_df
except FileNotFoundError:
    print(f"Error: File not found at {excel_file_PIB}.  Please check the path and try again.")
    exit()

# Show the first lines and info to check the data
print("PIB Data:")
print(pib_df.head())
print(pib_df.tail())  # Added to show the last rows
print(pib_df.info())

# 2. Read the file "ratings.xlsx"
excel_file_ratings = 'ratings.xlsx'
try:
    ratings_df = pd.read_excel(excel_file_ratings)  # Changed variable name to ratings_df
except FileNotFoundError:
    print(f"Error: File not found at {excel_file_ratings}.  Please check the path and try again.")
    exit()

# 2.1 Identify the relevant columns
ratings_selected = ratings_df[['Rating', 'Stable outlook']].copy()  # Changed variable name

# 2.2 Handle missing values
ratings_selected = ratings_selected.dropna(subset=['Rating', 'Stable outlook'])  # Changed variable name
ratings_selected = ratings_selected.reset_index(drop=True)  # Changed variable name

# 2.3 Standardize country names (limited example, to be completed)
ratings_selected['Stable outlook'] = ratings_selected['Stable outlook'].replace({  # Changed variable name
    'U.S.': 'United States',
    'U.K.': 'United Kingdom'
    # Add other replacements as needed to match the names in PIB.xlsx
}, regex=False)

# 3. Read the inflation data from the image.
#    Since we cannot directly read from an image, I'll create a DataFrame
#    based on the data provided in the image.  You'll need to adapt this
#    if your actual inflation data is in a different format (e.g., a CSV or Excel file).
inflation_data = {
    'Country Name': ['Zimbabwe', 'Venezuela', 'Liban', 'Soudan', 'Argentine', 'Turquie', 'Suriname',
                     'Sierra Leone', 'Iran', 'Ghana', 'Haiti', 'Egypte', 'Laos', 'Pakistan',
                     'Ethiopie', 'Malawi', 'Burundi', 'Nigeria', 'Sao Tome e Principe'],  # Corrected column name
    'Inflation_2023': [667.36, 337.45, 221.34, 171.47, 133.48, 53.86, 51.58,
                       47.64, 44.58, 38.11, 36.81, 33.88, 31.23, 30.77,
                       30.22, 28.79, 26.94, 24.66, 21.26]
}
inflation_df = pd.DataFrame(inflation_data)

# Show the first lines and info to verify the inflation data.
print("Inflation Data:")
print(inflation_df.head())
print(inflation_df.info())


# 4. Merge the datasets (DataFrame)
#    First merge ratings and PIB, then merge the result with inflation data.
merged_df = pd.merge(ratings_selected, pib_df, left_on='Stable outlook', right_on='Country Name', how='left')
df_merged = pd.merge(merged_df, inflation_df, on='Country Name', how='left')  # Changed variable name to df_merged


# Show the first lines and info to verify the merge
print("Merged Data:")
print(df_merged.head())
print(df_merged.info())

# Show the names of the columns in df_merged
print("Columns in df_merged:")
print(df_merged.columns)

# 5.  Convert GDP to billions and ensure it is numeric
df_merged['2023'] = pd.to_numeric(df_merged['2023'], errors='coerce')  # Convert to numeric; errors become NaN
df_merged['2023_billion'] = df_merged['2023'] / 1e9  # Divide by one billion
df_merged['2023_billion'] = df_merged['2023_billion'].round(2)  # Round to 2 decimal places

# Set the order of ratings (from best to worst)
rating_order = ['AAA', 'AA+', 'AA', 'AA-', 'A+', 'A', 'A-', 'BBB+', 'BBB', 'BBB-',
                'BB+', 'BB', 'BB-', 'B+', 'B', 'B-', 'CCC+', 'CCC', 'CCC-', 'CC', 'SD', 'D']

# Set a custom color scale (green to red)
colorscale = {
    'AAA': 'green', 'AA+': '#7CFC00', 'AA': '#ADFF2F', 'AA-': '#BFFF00', 'A+': '#CDFF70',
    'A': '#F0E68C', 'A-': '#FFD700', 'BBB+': '#FFA500', 'BBB': '#FF8C00', 'BBB-': '#FF7F50',
    'BB+': '#FF6347', 'BB': '#FF4500', 'BB-': '#FF0000', 'B+': '#DC143C', 'B': '#B22222',
    'B-': '#8B0000', 'CCC+': '#800000', 'CCC': '#8B0000', 'CCC-': '#8B0080', 'CC': '#DC143C', 'SD': '#4B0082', 'D': '#4B0082'
}

# Create the choropleth map
fig = px.choropleth(
    df_merged,
    locations='Stable outlook',
    locationmode="country names",
    color='Rating',
    color_discrete_map=colorscale,
    category_orders={'Rating': rating_order},
    title='Sovereign Ratings, GDP (2023), and Inflation (2023)',  # Added Inflation to title
    labels={'Rating': 'Rating', '2023_billion': 'GDP (2023, billions USD)',
            'Inflation_2023': 'Inflation Rate (2023)'},  # Added label for Inflation
    hover_data=['Stable outlook', 'Rating', '2023_billion', 'Inflation_2023']  # Added Inflation to hover data
)

fig.show()