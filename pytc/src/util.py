import os
import re
 
def skip_rows(df, n_rows):
    return df.iloc[n_rows:, :].reset_index(drop=True)
 
def skip_incomplete_rows(df):
    n_row = first_complete_row(df)
    return skip_rows(df, n_row).infer_objects() if n_row else df
 
def first_complete_row(df):
    for i in range(len(df)):
        if not df.iloc[i].isnull().values.any():
            return i
    return False
 
def use_first_row_as_header(df):
    return df.rename(columns=df.iloc[0]).drop(df.index[0]).reset_index(drop=True).infer_objects()
 
def list_files_by_pattern(path, pattern):
    return [os.path.join(path, f) for f in os.listdir(path) if re.search(pattern, f)]
 
def drop_zero(df):
    return df.loc[~(df == 0).all(axis=1)]
 
def list_intersection(list1, list2):
    return [value for value in list1 if value in list2]

def select_columns_if_exist(df, cols):
    return df.loc[:, df.columns.isin(cols)]
 
def purge_path(path, extension='.csv'):
    for file in [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]:
        if file.endswith(extension):
            os.remove(os.path.join(path, file))
 