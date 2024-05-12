import os
import glob
import csv
import tkinter as tk
from tkinter import messagebox

def clean_data():
    output_rows = []
    download_path = r'C:\\Users\\franc\\Downloads'
    output_folder = r'C:\\Users\\franc\\Downloads'
    csv_files = glob.glob(os.path.join(download_path, 'arkham_txns*.csv'))

    for csv_file in csv_files:
        with open(csv_file, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            from_address_idx = header.index('fromAddress')  
            from_label_idx = header.index('fromLabel')
            to_address_idx = header.index('toAddress')
            to_label_idx = header.index('toLabel')
            chain_idx = header.index('chain')
            
            for row in reader:
                address = row[from_address_idx] 
                label = row[from_label_idx].split()[0] # Take the first word only
                if address != label:
                    output_rows.append([address, label, row[chain_idx], 'exchange'])
                
                address = row[to_address_idx]
                label = row[to_label_idx].split()[0] # Take the first word only
                if address != label:
                    output_rows.append([address, label, row[chain_idx], 'exchange'])
                    
    output_rows = set(map(tuple, output_rows))

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        
    output_csv = os.path.join(output_folder, 'consolidatedarkham.csv')
    with open(output_csv, 'w') as f:
        writer = csv.writer(f)  
        writer.writerow(['address', 'entity', 'chain', 'category']) 
        writer.writerows(output_rows)
        
    # Delete original csv files
    for csv_file in csv_files:
        os.remove(csv_file)

    # Added popup code
    root = tk.Tk()
    root.withdraw()

    row_count = len(output_rows) 

    messagebox.showinfo('Complete', 'Finished consolidating CSVs! {} rows written. Output file: {}'.format(row_count, output_csv))

    result = messagebox.askquestion('Open File', 'Open output CSV file?')

    if result == 'yes':
        import subprocess
        subprocess.call(["open", output_csv])

# Main execution
if __name__ == "__main__":
    clean_data()
