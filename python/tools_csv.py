import csv
import pprint
import random

def csv_write_header_if_empty(file: str, fieldnames: list):
    from tools import file_is_empty
    
    """_summary_

    Args:
        file (str): The file path
        fieldnames (list): The column names to write
    """
    if file_is_empty(file):
        with open(file, 'w', encoding='utf-8', newline='') as f:
            w = csv.DictWriter(f, fieldnames=fieldnames)
            w.writeheader()
            
            
# drop duplicates of column from csv (and write specified columns only)
def csv_drop_duplicates(from_file: str, to_file: str, column_to_drop_duplicates: str, to_file_fieldnames: list[str]):
    """_summary_
    Drops duplicate of row if element is a duplicate in the same columns and writes it to another file.
    
    Args:
        from_file (str): Original File
        to_file (str): New File
        column_to_drop_duplicates (str): If duplicate elements is present in the column, the element's whole row will be dropped
        to_file_fieldnames (list[str]): New file's fieldnames
    """
    seen = set()
    unique_rows = []

    with open(from_file, newline="", encoding="utf-8") as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            url = row[column_to_drop_duplicates]
            if url not in seen:
                seen.add(url)
                unique_rows.append({key: row[key] for key in to_file_fieldnames if key in row})

    with open(to_file, "w", newline="", encoding="utf-8") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=to_file_fieldnames)
        writer.writeheader()
        writer.writerows(unique_rows)
    print(f"Duplicates dropped: ({from_file} -> {to_file})")
    


def csv_append_status_column(csv_file: str, status_column_name="status", default_fill_text="pending"):
    """_summary_
    For when running a very time consuming program.
    Used with reset_status_column() and mark_status()
    Args:
        csv_file (str): File path of csv
        status_column_name (str): The new column name of the file
        default_fill_text (str): The default text for labelling pending tasks
    """
    with open(csv_file, newline='', encoding='utf-8') as f:
        reader = list(csv.reader(f))
        header = reader[0]

        if status_column_name in header:
            print(f"Column '{status_column_name}' already exists. No changes made.")
            return

        header.append(status_column_name)
        for row in reader[1:]:
            row.append(default_fill_text)

    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(reader)
    print(f"{csv_file}: Status column '{status_column_name}' added with default entry '{default_fill_text}'")
        

def csv_reset_status_column(csv_file: str, status_column_name="status", reset_to="pending"):
    """_summary_
    For when running a very time consuming program.
    Used with csv_append_status_column() and mark_status()
    
    Args:
        csv_file (str): File path of csv
        status_column_name (str): The name of the status column
        reset_to (str): The text to reset to in the status column

    Raises:
        ValueError: If status_column_name not in csv
    """
    with open(csv_file, newline='', encoding='utf-8') as f:
        reader = list(csv.reader(f))
        header = reader[0]

        if status_column_name not in header:
            raise ValueError(f"Column '{status_column_name}' does not exist in the CSV.")

        idx = header.index(status_column_name)
        for row in reader[1:]:
            if len(row) <= idx:
                row.extend([''] * (idx - len(row) + 1))
            row[idx] = reset_to

    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(reader)
        
    
def csv_mark_status(csv_file: str, target: str, target_column: str, status_column_name="status", mark_as="completed"):
    """_summary_
    For when running a very time consuming program.
    Used with csv_append_status_column() and reset_status_column()
    
    Args:
        csv_file (str): File path of csv
        target (str): The element to pinpoint
        target_column (str): The column to pinpoint
        status_column_name (str): The status column to change value
        mark_as (str): The value to mark as in the status column

    Raises:
        ValueError: 
        ValueError: 
    
    Example: 
        mark_status(
            CSV_FILE,
            amount,
            AMOUNT_OF_MONEY_COLUMN,
            STATUS_COLUMN,
            COMPLETED
        )
    """
    with open(csv_file, newline='', encoding='utf-8') as f:
        reader = list(csv.reader(f))
        header = reader[0]

        if target_column not in header:
            raise ValueError(f"Column '{target_column}' does not exist in the CSV.")
        if status_column_name not in header:
            raise ValueError(f"Column '{status_column_name}' does not exist in the CSV.")

        target_idx = header.index(target_column)
        status_idx = header.index(status_column_name)

        for row in reader[1:]:
            if len(row) <= max(target_idx, status_idx):
                row.extend([''] * (max(target_idx, status_idx) - len(row) + 1))
            if row[target_idx] == target:
                row[status_idx] = mark_as

    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(reader)
        
        
def csv_random_entry_check(file: str):
    """_summary_
    Prints out a random csv row in pprint format.
    
    Args:
        file (str): The file path
    """
    with open(file, 'r', encoding='utf-8') as f:
        d = list(csv.DictReader(f))
        pprint.pprint(d[random.randint(0, len(d))])


def csv_count_entries(file: str):
    """_summary_
    Prints out the number of entries in a csv file.

    Args:
        file (str): The file path
    """
    with open(file, 'r', encoding='utf-8') as f:
        print(f"{file}: {len(list(csv.DictReader(f)))} entries")
    
    
def csv_count_unique_columns(file: str, col: str) -> None:
    """_summary_
    Count the number of unique entries in a column of the csv file 
    Args:
        file (str): The file path
        col (str): The column name
    """
    s = set()
    with open(file, "r", encoding='utf-8') as f:
        r = csv.DictReader(f)
        for row in r:
            s.add(row[col])
        print(f"{file}: {len(s)} unique '{col}' entries")