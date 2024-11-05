import pandas as pd
import numpy as np
import os

def load_data(filepath):
    """Load raw data from a CSV file."""
    return pd.read_csv(filepath)

def transform_data(raw_data):
    """Perform data transformation including renaming columns, changing data types, 
    mapping categorical values, and creating new columns."""
    # Copy the data to avoid modifying the original
    transformed_data = raw_data.copy()
    
    # Rename columns to lowercase and replace spaces with underscores
    transformed_data.columns = transformed_data.columns.str.lower().str.replace(' ', '_')
    
    # Convert 'fecha' to datetime format and rename it to 'date'
    transformed_data['date'] = pd.to_datetime(transformed_data['fecha'], format='%d/%m/%Y')
    transformed_data.drop('fecha', axis=1, inplace=True)
    
    # Add a 'day_id' column for unique day identifiers
    transformed_data['day_id'] = np.arange(1, len(transformed_data) + 1)
    
    # Map 'status' and 'productiveness' to numerical values
    status_map = {'In progress': 0, 'Complete': 1}
    transformed_data['status'] = transformed_data['status'].map(status_map)
    
    productiveness_map = {'⭐️': 1, '⭐️⭐️': 2, '⭐️⭐️⭐️': 3, '⭐️⭐️⭐️⭐️': 4, '⭐️⭐️⭐️⭐️⭐️': 5}
    transformed_data['productiveness'] = transformed_data['productiveness'].map(productiveness_map)
    
    # Fill missing values in 'important_achievements' with 'No'
    transformed_data['important_achievements'] = transformed_data['important_achievements'].fillna('No')
    
    # Create dummy variables for 'learning' column
    learning_dummies = transformed_data['learning'].str.get_dummies(sep=', ')
    final_transformed_data = pd.concat([transformed_data, learning_dummies], axis=1).drop(columns='learning')
    
    return final_transformed_data

def separate_tables(final_transformed_data):
    """Separate the final transformed data into a text table and a properties table."""
    text_table = final_transformed_data[['day_id', 'daily_overview']]
    properties_table = final_transformed_data.drop(columns=['daily_overview'])
    return text_table, properties_table

def save_tables(text_table, properties_table, output_dir):
    """Save the text and properties tables as CSV files."""
    os.makedirs(output_dir, exist_ok=True)
    text_table.to_csv(os.path.join(output_dir, 'text_table.csv'), index=False)
    properties_table.to_csv(os.path.join(output_dir, 'properties_table.csv'), index=False)
    print(f"Data saved to {output_dir}")

if __name__ == "__main__":
    # File paths
    input_filepath = 'D:/Estiven/Datos/Proyectos/100_days_of_data_project/data/raw/Daily Calendar - raw data.csv'
    output_dir = 'D:/Estiven/Datos/Proyectos/100_days_of_data_project/data/processed'

    # Raw data load
    raw_data = load_data(input_filepath)
    
    # Transformation of the data
    final_transformed_data = transform_data(raw_data)

    # Separate into text and properties tables
    text_table, properties_table = separate_tables(final_transformed_data)

    # Save the tables to CSV files
    save_tables(text_table, properties_table, output_dir)

    print("Data transformation complete.")
