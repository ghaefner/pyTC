import os
import re
import pandas as pd
from pytc.config import Columns

def skip_rows(df, n_rows):
    """
    Skip the first n_rows in the DataFrame.

    Parameters:
    - df: pandas DataFrame
        The DataFrame to skip rows from.
    - n_rows: int
        Number of rows to skip.

    Returns:
    - pandas DataFrame
        DataFrame with skipped rows.
    """
    return df.iloc[n_rows:, :].reset_index(drop=True)

def skip_incomplete_rows(df):
    """
    Skip rows with missing values at the beginning of the DataFrame.

    Parameters:
    - df: pandas DataFrame
        The DataFrame to skip incomplete rows from.

    Returns:
    - pandas DataFrame
        DataFrame with skipped incomplete rows.
    """
    n_row = first_complete_row(df)
    return skip_rows(df, n_row).infer_objects() if n_row else df

def first_complete_row(df):
    """
    Find the index of the first row without missing values.

    Parameters:
    - df: pandas DataFrame
        The DataFrame to find the first complete row from.

    Returns:
    - int or False
        Index of the first complete row or False if not found.
    """
    for i in range(len(df)):
        if not df.iloc[i].isnull().values.any():
            return i
    return False

def use_first_row_as_header(df):
    """
    Use the first row as column headers and drop it.

    Parameters:
    - df: pandas DataFrame
        The DataFrame to use the first row as header.

    Returns:
    - pandas DataFrame
        DataFrame with the first row as header and dropped.
    """
    return df.rename(columns=df.iloc[0]).drop(df.index[0]).reset_index(drop=True).infer_objects()

def list_files_by_pattern(path, pattern):
    """
    List files in a directory that match a pattern.

    Parameters:
    - path: str
        Path to the directory to search files in.
    - pattern: str
        Regular expression pattern to match filenames.

    Returns:
    - list of str
        List of filenames that match the pattern.
    """
    return [os.path.join(path, f) for f in os.listdir(path) if re.search(pattern, f)]

def drop_zero(df):
    """
    Drop rows where all values are zero.

    Parameters:
    - df: pandas DataFrame
        The DataFrame to drop zero rows from.

    Returns:
    - pandas DataFrame
        DataFrame with zero rows dropped.
    """
    return df.loc[~(df == 0).all(axis=1)]

def list_intersection(list1, list2):
    """
    Find the intersection of two lists.

    Parameters:
    - list1: list
        The first list.
    - list2: list
        The second list.

    Returns:
    - list
        List containing common elements from both lists.
    """
    return [value for value in list1 if value in list2]

def select_columns_if_exist(df, cols):
    """
    Select columns from a DataFrame if they exist.

    Parameters:
    - df: pandas DataFrame
        The DataFrame to select columns from.
    - cols: list of str
        List of column names to select.

    Returns:
    - pandas DataFrame
        DataFrame containing only the selected columns that exist in the original DataFrame.
    """
    return df.loc[:, df.columns.isin(cols)]

def purge_path(path, extension='.csv'):
    """
    Delete files with a specific extension from a directory.

    Parameters:
    - path: str
        Path to the directory to purge files from.
    - extension: str, optional (default='.csv')
        File extension to filter files for deletion.

    Returns:
    - None
    """
    for file in [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]:
        if file.endswith(extension):
            os.remove(os.path.join(path, file))

def apply_column_map(df:pd.DataFrame, column_map: dict) -> pd.DataFrame:
    df.rename(columns=column_map, inplace=True)
    df[Columns.METRIC] = "KEUR"
    return df

def convert_value_to_num(df):
    df[Columns.VALUE] = pd.to_numeric(df[Columns.VALUE], errors='coerce')
    return df

def filter_complete_timeseries(df, date_col='date'):
    """
    Filter groups in a DataFrame based on whether they have a complete time series.

    Args:
        df (pandas.DataFrame): Input DataFrame.
        date_col (str): Name of the column containing the date.

    Returns:
        pandas.DataFrame: Filtered DataFrame containing only groups with complete time series.
    """
    # Identify columns to use for grouping (all columns except 'date_col')
    group_cols = [col for col in df.columns if col != date_col]
    
    # Group DataFrame by all other columns
    grouped = df.groupby(group_cols)

    filtered_dfs = []
    
    # Iterate over each group
    for group_key, group_df in grouped:
        # Sort by date within each group
        group_df = group_df.sort_values(date_col)
        
        # Check if the date series is complete (i.e., no missing dates)
        date_series = group_df[date_col]
        min_date, max_date = date_series.min(), date_series.max()
        expected_dates = pd.date_range(start=min_date, end=max_date, freq='D')
        
        if date_series.reset_index(drop=True).equals(expected_dates):
            filtered_dfs.append(group_df)
    
    # Concatenate all filtered DataFrames
    if filtered_dfs:
        filtered_df = pd.concat(filtered_dfs)
    else:
        filtered_df = pd.DataFrame(columns=df.columns)  # Empty DataFrame if no complete groups
    
    return filtered_df

def add_period_column(df, TEST_PERIOD):
    """
    Add a 'period' column to the DataFrame based on specified TEST_PERIOD dates.

    Parameters:
    df (pandas.DataFrame): Input DataFrame with a 'date' column.
    TEST_PERIOD (list of datetime.date or datetime.datetime): List of dates defining the test period.

    Returns:
    pandas.DataFrame: DataFrame with an additional 'period' column.
    """
    # Convert TEST_PERIOD to datetime objects (in case they are not already)
    TEST_PERIOD = pd.to_datetime(TEST_PERIOD)

    # Determine min and max dates from TEST_PERIOD
    test_period_start = min(TEST_PERIOD)
    test_period_end = max(TEST_PERIOD)

    # Add 'period' column based on date conditions
    df['period'] = 'test'
    df.loc[df[Columns.DATE] < test_period_start, 'period'] = 'pre'
    df.loc[df[Columns.DATE] > test_period_end, 'period'] = 'post'
    
    return df
