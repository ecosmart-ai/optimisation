# Integer programming / product selection from  catalogue
# Author Elias Zgheib : elias.zgheib@outlook.com

from mip import Model, xsum, maximize, BINARY, INTEGER, minimize
import math
import numpy as np
import pandas as pd
import timeit

start = timeit.default_timer()

# Importing the dataset
Input = pd.read_excel('input.xlsx')






MinOrder = Input.iloc[0,3:].tolist()
Input1 = Input[Input['Filter']==1]


Target = Input1.iloc[0:,2].tolist()

inf=1e20
Cost = Input1.iloc[0:,3:]
MaximumCost = Cost.max().max()
Cost = Cost.fillna(inf)
n, m  = Cost.shape

Cost = Cost.values.tolist()



N,M = range(n) , range(m)
Big=1e8

#create the model
model = Model('BestOrder')



#Create variable  matrix
# x = {(i, j): model.add_var(obj=0, var_type=INTEGER, name="x[%d ,%d]" % (i, j)) for i in N for j in M}
x = [[model.add_var(var_type=INTEGER) for j in M] for i in N]
W= [model.add_var(var_type=BINARY, name="W[%d]" %i )   for i in  M ] 


#Create Objective function
model.objective =minimize( xsum(Cost[i][j] *  x[i][j] for i in N for j in M))  # change pd to numpy if needed

#Create constraintes

#order the targeted number of items
for i in N:
    model+= xsum(  x[i][j] for j in M ) == Target[i] 
    model += xsum( x[i][j] if(  Cost[i][j]==inf ) else 0 for j in M ) == 0

for j in M:
    model+=  xsum( Cost[i][j]  *   x[i][j] if (Cost[i][j] <= MaximumCost)   else 0  for i in N ) >= MinOrder[j] - (W[j]*Big) 
    model+=  xsum( Cost[i][j]  *   x[i][j] if (Cost[i][j] <= MaximumCost)   else 0 for i in N ) <=  (1 - W[j])*Big    

    
# Optimize
model.optimize()


#Print Result
 
Cost_Function=0

result=np.zeros((n,m))

for i in N:
    for j in M :
        result[i,j] =  x[i][j].x
        Cost_Function += result[i,j]*Cost[i][j]
        
np.savetxt("result1.csv", result, delimiter=",")
print('  Result: {} '.format(Cost_Function))
stop = timeit.default_timer()
print('Time: ', stop - start)  
