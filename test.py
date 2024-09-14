import pandas as pd

df = pd.DataFrame({'float': [1.0],
                    'int': [1],
                  'datetime': [pd.Timestamp('20180310')],
                    'string': ['foo']})
print(df.dtypes)