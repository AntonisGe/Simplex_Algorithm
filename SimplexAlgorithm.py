                             #Inputs
#=======================================================================
objective_function=input('Function to maximize (e.g. 3,4 means maximize 3x+4y): ')
print('')
print('For constrains: 1,0<21 means 1x + 0y =< 21')
print('Type "calc" to stop')
print('')

remember_this=0
number_of_variables=1
constrain='start'
constrain_help=[]
while constrain != 'calc':
    constrain=input('Constrain No{}: '.format(number_of_variables))
    if constrain != 'calc' and '=' not in constrain:
        constrain_help.append(constrain)
        number_of_variables += 1
    elif '=' in constrain:
        constrain_help.append(constrain.replace('=','<'))
        number_of_variables += 1
        constrain_help.append(constrain.replace('=','>'))
        remember_this += 1
        
number_of_variables = number_of_variables - 1 + remember_this

objective_function=[float(dummy) for dummy in objective_function.split(',')]
for i in range(number_of_variables):
    objective_function.append(0)

constrains=[[] for dummy in range(number_of_variables)]
for count,constrain in enumerate(constrain_help):
    if '<' in constrain:
        c=constrain.split('<')
        for dummy in c[0].split(','):
            constrains[count].append(float(dummy))
        for dummy in range(count):
            constrains[count].append(0)
        constrains[count].append(1)
        while len(constrains[count]) < len(objective_function):
            constrains[count].append(0)
        constrains[count].append(float(c[1]))
    elif '>' in constrain:
        c=constrain.split('>')
        for dummy in c[0].split(','):
            constrains[count].append(float(dummy))
        for dummy in range(count):
            constrains[count].append(0)
        constrains[count].append(-1)
        while len(constrains[count]) < len(objective_function):
            constrains[count].append(0)
        constrains[count].append(float(c[1]))

objective_function.append(0)
constrains.append(objective_function)

number_of_cols=len(constrains[0])
number_of_rows=len(constrains)

print('')

                             #Simplex Algorithm
#==============================================================================
for i in constrains:
    x=[round(j,2) for j in i]
    print(x)
print('==================')

#
#                                      The Algorithm 
#            ------------------------------------------------------------------
#            |   x1         x2         x3         s1       s2      s3   |  p  |
#            |----------------------------------------------------------|-----| 
#            |   2          3          1          1         0      0    |  20 |    <- 20/2=10   10<15 so this is the row_number_of_pivot.
#            |                                                          |     |    <- 15/1=15    
#            |   1          1          5          0         1      0    |  15 |
#            |                                                          |     | 
#            |   0          4          3          0         0      1    | 15  | 
#            |----------------------------------------------------------|-----|
#          Z |   14        10          0          0         0      0    |  0  |     <- Finds the biggest number in this row, which in this case is 14. The column that 14 is found is the Column_number_of_pivot.  
#             -----------------------------------------------------------------         Then it divides the p column entries with the corresponding entries in the Column_number_of_pivot.
#                __                                                                  The smallest number is the pivot which is used to 'reduce' the matrix.
#               /|\                                                        
#                | 
#       Column_number_of_pivot
#
#                             Algorithm stops when there are no negative numbers in the last row AND all variables are non-negative.



def negative_value_search():                        # In the algorithms all variables must be non-negative.
    found=0                                         # This function finds if there are negative variables in the tablaeu and returns True/False respectively. 
    for column in range(number_of_cols):            # I kept it out of the algorithm to make the algorithm simpler.
        count=0
        for row in range(number_of_rows):
            if constrains[row][column]<0.000001 and constrains[row][column]>-0.000001:
                count += 1
            else:
                row_index=row
        if count == number_of_rows-1:
            if constrains[row_index][-1]/constrains[row_index][column]<0:
                found += 1

    if found==0:
        return(False)
    else:
        return(True)
    

banned_list=[]                         # Sometimes the algorithms got stuck because in the column number of pivot all numbers where negative or 0.
                                       # So I put here the 'banned columns' when that happens and I will reset the banned_list every time the tablaeu changes.
                                       
negative_values_searcher=negative_value_search() # negative_values_searcher is T/F depending if negative variables exists.

while max(objective_function)>0 or negative_values_searcher:                         
    #finding pivot
    help_objective=[i for i in objective_function if i not in banned_list]   # we create a dummy list help_objective to put the coefficients of the objective function there but remove the banned columns.
    help_objective=[i for i in help_objective if i != 0]                      # We also remove 0 from the help_objective in case something like this happens:
                                                                 # objective function is : [-1, 0 , -1, -10, 0, 0] but negative variables exists, so the algorithm must continue.
                                                        # Later the algorithm will find the max value in objective function, but that will be 0 which will be a problem. 
    column_number_of_pivot=objective_function.index(max(help_objective))
    # find row number of pivot
    min_division=9999999                                                            
    for row in range(number_of_rows-1):                                                                                           
        if constrains[row][column_number_of_pivot]>0.000001:                                                                      
            d=constrains[row][-1]/constrains[row][column_number_of_pivot]                                                         
            if d<min_division:                                                                                                    
                row_number_of_pivot=row
                min_division=d
        
                
    #row reduction
    try:    # Here the algorithm checks if it can find a pivot. If it cannot, it means that the column examined should be on the banned list.
        
        pivot=constrains[row_number_of_pivot][column_number_of_pivot] #It will get stack here because row_number_of_pivot will be undefined.

        for row in range(number_of_rows):
            if row != row_number_of_pivot:
                factor=constrains[row][column_number_of_pivot]/pivot
                row_that_will_be_substracted=[factor*value for value in constrains[row_number_of_pivot]]
                new_row=[constrains[row][dummy]-row_that_will_be_substracted[dummy] for dummy in range(number_of_cols)]
                constrains[row]=new_row

        constrains[row_number_of_pivot]=[dummy/pivot for dummy in constrains[row_number_of_pivot]]
            
        objective_function=constrains[-1]
        banned_list=[]            # reset ban_list επειδή because tablaeu changed.
        for i in constrains:
            x=[round(j,2) for j in i]
            print(x)
        print('==================')
        negative_values_searcher=negative_value_search()  # finds if negative variables exist using the def written above.
            
    except:
        banned_list.append(column_number_of_pivot)


                             #Output
#=================================================================================
        
rows_already_used=[]   # We do not want the same row to be used twice. This will happen if the user puts linearly dependent rows. 
for column in range(number_of_cols-number_of_rows):
    count=0
    row_that_value_is_found=-1
    for row in range(number_of_rows):
        if constrains[row][column]<0.000001 and constrains[row][column]>-0.000001:# The reason I check for this condition -0.00001<x<0.00001 instead of x==0 is because there are rounding errors in python.
            count += 1
        else:
            row_that_value_is_found=row
    if count == number_of_rows-1 and row_that_value_is_found not in rows_already_used:
        print('x{} = {}'.format(column+1,constrains[row_that_value_is_found][-1]/constrains[row_that_value_is_found][column]))
        rows_already_used.append(row_that_value_is_found)
    else:
        print('x{} = 0'.format(column+1))

