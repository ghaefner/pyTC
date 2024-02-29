from src.reader import DataReader

dat = DataReader(data_source="unify")
dat.read_unify_excel()
print(dat.data)