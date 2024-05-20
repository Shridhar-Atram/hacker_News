import pandas as pd

def load_data(file_path):
    """Load data from Excel file"""
    return pd.read_excel(file_path, skiprows=6).dropna()

def find_uncommon_cells(df1, df2, required_columns):
    """Find uncommon cells between two dataframes"""
    common = pd.merge(df1, df2, on=required_columns, suffixes=('_df1', '_df2'))
    df2_not_in_df1 = df2[~df2.set_index(required_columns).index.isin(df1.set_index(required_columns).index)]
    uncommon_cells = []

    for index, row in common.iterrows():
        for column in required_columns:
            cell_df1 = row[column + '_df1']
            cell_df2 = row[column + '_df2']
            if cell_df1 != cell_df2:
                uncommon_cells.append({
                    'Row': index + 2,
                    'Column': column,
                    'Value_df1': cell_df1,
                    'Value_df2': cell_df2
                })

    return df2_not_in_df1, uncommon_cells

def save_uncommon_cells(filename, df_uncommon_cells):
    """Save uncommon cells to Excel file"""
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        df_uncommon_cells.to_excel(writer, sheet_name='Uncommon_Cells')

        # Open the Excel workbook
        workbook = writer.book
        worksheet = writer.sheets['Uncommon_Cells']

        # Write uncommon cell coordinates
        for index, row in df_uncommon_cells.iterrows():
            cell_coord = worksheet.cell(row=row['Row'], column=1).coordinate
            value = f"Value mismatch: {row['Value_df1']} != {row['Value_df2']}"
            worksheet[cell_coord].value = value

        workbook.save(filename)

def main():
    # File paths
    file_path1 = "C:/Users/D117157/Test/Test/Archive/2024-03-14 Security Level Quality Check.xlsx"
    file_path2 = "C:/Users/D117157/Test/Test/Archive/2024-03-26 Security Level Quality Check.xlsx"

    # Load data
    df1 = load_data(file_path1)
    df2 = load_data(file_path2)

    # Define required columns
    required_columns = [
        'PGI-Merrill Lynch Sector Breakdown (PGI_BAMLSECT) - Level 1',
        'PGI-Merrill Lynch Sector Breakdown (PGI_BAMLSECT) - Level 2',
        'PGI-Merrill Lynch Sector Breakdown (PGI_BAMLSECT) - Level 3',
        'PGI-Merrill Lynch Sector Breakdown (PGI_BAMLSECT) - Level 4',
        'PGI - Risk Country Bloc Summary (PGI_RISKCNTRY) - Level 1',
        'PGI - Risk Country Bloc Summary (PGI_RISKCNTRY) - Level 2'
    ]

    # Find uncommon cells
    df2_not_in_df1, uncommon_cells = find_uncommon_cells(df1, df2, required_columns)

    # Save uncommon cells
    output_filename = "uncommon_cells.xlsx"
    df_uncommon_cells = pd.DataFrame(uncommon_cells)
    save_uncommon_cells(output_filename, df_uncommon_cells)

    print(f"Uncommon cell coordinates saved in {output_filename}")

if __name__ == "__main__":
    main()
