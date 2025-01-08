import pandas as pd

def merge_csv_files():
    # Read both CSV files
    try:
        raptors_df = pd.read_csv('event_ids.csv')
        maple_leafs_df = pd.read_csv('event_ids_maple.csv')
        
        # Combine the dataframes
        combined_df = pd.concat([raptors_df, maple_leafs_df], ignore_index=True)
        
        # Sort by DateTime
        combined_df['DateTime'] = pd.to_datetime(combined_df['DateTime'])
        combined_df = combined_df.sort_values('DateTime')
        
        # Save to a new CSV file
        combined_df.to_csv('combined_events.csv', index=False)
        print(f"Successfully merged CSV files. Total events: {len(combined_df)}")
        print(f"Events breakdown:")
        print(f"Raptors events: {len(raptors_df)}")
        print(f"Maple Leafs events: {len(maple_leafs_df)}")
        
    except FileNotFoundError as e:
        print(f"Error: One or more CSV files not found. {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    merge_csv_files()