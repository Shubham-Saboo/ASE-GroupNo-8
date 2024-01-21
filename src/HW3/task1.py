import pandas as pd
from prettytable import PrettyTable

def analyze_dataset(filepath):
    # Load the dataset
    df = pd.read_csv(filepath)

    # Assuming the class label is in the last column
    class_col = df.columns[-1]
    class_counts = df[class_col].value_counts()
    total_rows = len(df)

    # Create and populate ASCII table
    table = PrettyTable()
    table.field_names = ["Class", "Count", "Percentage"]

    for class_label, count in class_counts.items():
        percentage = (count / total_rows) * 100
        table.add_row([class_label, count, f"{percentage:.2f}%"])

    return table

# Analyze the datasets
diabetes_table = analyze_dataset("../../data/diabetes.csv")
soybean_table = analyze_dataset("../../data/soybean.csv")

diabetes_table, soybean_table
output_file = '../../hw/w3/table.txt'  # Update with your desired file path

with open(output_file, 'w') as file:
    file.write(str(diabetes_table))
    file.write("\n\n")  # Adding some space between the tables
    file.write(str(soybean_table))

print(f"Tables saved to {output_file}")



