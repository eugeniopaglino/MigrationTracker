def get_age_groups(age_min, age_max):
    
    '''
    This function generates a dictionary with age groups as keys. The keys are tuples whose first element
    is the lower age limit and whose second element is the uppper age limit for each group. Each key has
    a unique feature 'name' that contains a string with the following structure: lower_limit - upper_limit.
    
    Each group contains five years and is constructed in such a way that the lower limit is a multiple of
    five exception made for the first and the last group.
    '''

    age_groups = {}
    
    for i in range(age_min, age_max+1):  

        if i == age_min:

            lower_limit = i
            
            if i % 5 == 0:
                upper_limit = i + 4
            else:
                for x in range(i,i+5):
                    if x % 5 == 0:
                        upper_limit = x-1

            age_groups[(lower_limit, upper_limit)] = {'name':'{}-{}'.format(lower_limit, upper_limit)}
            
        elif i == age_max:

            for x in range(age_max-4,age_max+1):
                if x % 5 == 0:
                    lower_limit = x

            age_groups[(lower_limit, )] = {'name':'{}+'.format(lower_limit)}
            
        else:

            if i % 5 == 0:

                lower_limit = i
                upper_limit = lower_limit + 4
                age_groups[(lower_limit, upper_limit)] = {'name':'{}-{}'.format(lower_limit, upper_limit)}

    return age_groups