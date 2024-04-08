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

def filter_complete_time_series(df):
    """
    Filters complete time series for each group of 'market', 'metric', 'product', and 'region'.

    Parameters:
        df (DataFrame): Input DataFrame.
        expected_length (int): Expected length of the time series.

    Returns:
        DataFrame: DataFrame with complete time series for each group.
    """
    # Convert 'date' column to datetime
    df['date'] = pd.to_datetime(df['date'])
    expected_length = df['date'].nunique()

    # Group by 'market', 'metric', 'product', and 'region'
    groups = df.groupby(['market', 'metric', 'product', 'region'])

    # Filter groups where the length of the time series is equal to the expected length
    complete_groups = [group for _, group in groups if len(group) == expected_length]

    # Concatenate the filtered groups into a new DataFrame
    complete_df = pd.concat(complete_groups)

    # Reset the index and drop the additional index column
    complete_df.reset_index(drop=True, inplace=True)

    return complete_df

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
    df['period'] = pd.cut(df['date'], 
                           bins=[pd.Timestamp.min, test_period_start, test_period_end, pd.Timestamp.max],
                           labels=['pre', 'test', 'post'],
                           right=False)
    
    return df