import pandas as pd
import time
from tqdm import tqdm, tnrange, tqdm_notebook

from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.reachestimate import ReachEstimate
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.targetingsearch import TargetingSearch

from dem_utils import get_age_groups

def get_age_structure_table_mig(access_token, user_id, destinations, origins, age_min=13, age_max=65, delay=0):
    
    '''
    This function creates a table for each destination-origin pair with the sex-age structure of
    the corresponding population. Age groups contain five years each and are constructed so that
    the lower age limit is always a multiple of five with the exception of the first and the last
    group. The output of the function is a dictionary with destinations as the keys, origins as the
    primary features, and an age-sex structure table for every pair.
    '''
    
    FacebookAdsApi.init(access_token=access_token)
    
    age_groups = get_age_groups(age_min,age_max)
    genders = {1:{'name' : 'male'}, 2:{'name' : 'female'}}
    
    age_groups_names = [list(age_groups.values())[x]['name'] for x in range(len(age_groups))]
    genders_names = [list(genders.values())[x]['name'] for x in range(len(genders))]
    
    dest_dict = get_destinations(access_token)
    origin_dict =  get_origins(access_token)
    
    check_countries(destinations,dest_dict)
    check_countries(origins,origin_dict)
    
    age_str_dict= {}
    age_str_table = pd.DataFrame(0, index=age_groups_names, columns=genders_names)
    
    try:
    
        for destination in destinations:
            for origin in origins:
                for gender in genders:
                    for age_group in age_groups:

                        if len(age_group) == 1:

                            fields = []
                            params = {
                                      'targeting_spec': {'geo_locations':{'countries':[dest_dict[destination]['code']]},
                                                         'genders': [gender],
                                                         'age_min': age_group[0],
                                                         'behaviors':[{'id': origin_dict[origin]['id'],
                                                                         'name': origin_dict[origin]['name']}],
                                                        },
                                     }

                        else:

                            fields = []
                            params = {
                                      'targeting_spec': {'geo_locations':{'countries':[dest_dict[destination]['code']]},
                                                         'genders': [gender],
                                                         'age_min': age_group[0],
                                                         'age_max': age_group[1],
                                                         'behaviors':[{'id': origin_dict[origin]['id'],
                                                                         'name': origin_dict[origin]['name']}],
                                                        },
                                     }

                        age_str_table.loc[age_groups[age_group]['name'],
                                    genders[gender]['name']] = AdAccount(user_id).get_reach_estimate(fields=fields,
                                                                          params=params)[0]['users']

                        time.sleep(delay)

                age_str_dict[destination] = {origin : {'age_structure_table' : age_str_table[:]}}
                age_str_table = pd.DataFrame(0, index=age_groups_names, columns=genders_names)
                
    except Exception as error:
        print(error)    
      
    finally:
        return age_str_dict

def get_age_structure_table_countries(access_token, user_id, destinations, age_min=13, age_max=65, delay=0):
    
    '''
    This function creates a table for each destination  with the sex-age structure of
    the corresponding population. Age groups contain five years each and are constructed so that
    the lower age limit is always a multiple of five with the exception of the first and the last
    group. The output of the function is a dictionary with destinations as the keys and an age-sex
    structure table for each one of them.
    '''
    
    FacebookAdsApi.init(access_token=access_token)
    
    age_groups = get_age_groups(age_min,age_max)
    genders = {1:{'name' : 'male'}, 2:{'name' : 'female'}}
    
    age_groups_names = [list(age_groups.values())[x]['name'] for x in range(len(age_groups))]
    genders_names = [list(genders.values())[x]['name'] for x in range(len(genders))]
    
    dest_dict = get_destinations(access_token)
    check_countries(destinations,dest_dict)
    
    age_str_dict = {}
    age_str_table = pd.DataFrame(0, index=age_groups_names, columns=genders_names)
    
    try:
    
        for destination in destinations:
            for gender in genders:
                for age_group in age_groups:

                    if len(age_group) == 1:

                        fields = []
                        params = {
                                  'targeting_spec': {'geo_locations':{'countries':[dest_dict[destination]['code']]},
                                                     'genders': [gender],
                                                     'age_min': age_group[0],
                                                     },
                                  }

                    else:

                        fields = []
                        params = {
                                  'targeting_spec': {'geo_locations':{'countries':[dest_dict[destination]['code']]},
                                                     'genders': [gender],
                                                     'age_min': age_group[0],
                                                     'age_max': age_group[1],
                                                     },
                                  }

                    age_str_table.loc[age_groups[age_group]['name'],
                                      genders[gender]['name']] = AdAccount(user_id).get_reach_estimate(fields=fields,
                                                                          params=params)[0]['users']

                    time.sleep(delay)

            age_str_dict[destination] = {'age_structure_table' : age_str_table[:]}
            age_str_table = pd.DataFrame(0, index=age_groups_names, columns=genders_names)
            
    except Exception as error:
        print(error)    
      
    finally:
        return age_str_dict
        
def get_all_age_structure_tables(access_token, user_id, destinations, origins, age_min=13, age_max=65, delay=0):
    
    age_str_dict = {}
    
    age_str_dict_mig = get_age_structure_table_mig(access_token, 
                                                   user_id, 
                                                   destinations, 
                                                   origins, 
                                                   age_min, 
                                                   age_max, 
                                                   delay)
    
    age_str_dict_countries = get_age_structure_table_countries(access_token, 
                                                               user_id, 
                                                               destinations, 
                                                               age_min, 
                                                               age_max, 
                                                               delay)
    
    for country in age_str_dict_countries:
        
        age_str_dict_mig[country][country] = age_str_dict_countries[country]
    
    return age_str_dict_mig