import pandas as pd

def count_disease_cases(csv_file):
    # Load CSV file
    df = pd.read_csv(csv_file)
    
    # Ensure column name is correct
    disease_col = 'diagnosis'
    if disease_col not in df.columns:
        raise ValueError(f"Column '{disease_col}' not found in CSV file.")
    
    # Count cases where diagnosis is 'CD'
    disease_count = df[disease_col].dropna().eq('CD').sum()
    
    print(f"Number of people who have the chroasdfasdf disease: {disease_count}")
    return disease_count

# Example usage
csv_file = "detailsDiseasedOrNot.csv"  # Replace with your actual CSV file path
count_disease_cases(csv_file)
