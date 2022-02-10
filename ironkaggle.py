import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error
import sys

if __name__ == "__main__":
    print(f"Arguments count: {len(sys.argv)}")
    for i, arg in enumerate(sys.argv):
        print(f"Argument {i:>6}: {arg}")

truth = pd.read_csv('validation_solutions.csv')
print(truth.head())

if (len(sys.argv[1])>0):
    filename = sys.argv[1]
else:
    print('Pleas provide a file name')
    exit

pred = pd.read_csv(filename)
print(pred.head())

#index column is always the first column
both = pd.merge(truth, pred, left_on=truth.columns[0], right_on=pred.columns[0])


#column names; True_index	Sales	Blabla	Something  (index columns is repeated)
#so sales columns to compare are the second and fourth column
if (pred.columns[0]=='True_index'):
    mse = mean_squared_error(both.iloc[:, 1], round(both.iloc[:, 2],0))
else:
    mse = mean_squared_error(both.iloc[:, 1], round(both.iloc[:, 3],0))


print(f'RMSE for {filename} is {np.sqrt(mse)}.')
