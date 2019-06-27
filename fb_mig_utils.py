def gen_mig_table(destinations, origins, access_token, user_id, age_min = 18, age_max = 65):
    
    '''
    This function call the Facebook Ads Api and returns a table whose index is a list of receiving
    countries passed through the destinations variable and whose columns are the sending countries
    passed through the origins list. Notice that the number returned refer to the stock of 
    migrants from a given sending country to a given receving country (as estimated by Facebook) and
    are updated to the moment when the function is called. In order for the function to work the
    Facebook Ads Api needs to be set.
    
    Arguments:
        
        - destinations and origins: this are lists of countries like [Country 1, Country 2, etc.] where 
                                     all elements of the lists are strings and represent country names;
        - access_token: your facebook user access token, find out more at 
                         https://developers.facebook.com/docs/marketing-api/access;
        - user_id: your facebook user id;
        - age_min and age_max: the minimum and maximum age users should have to be included in your
                               estimates.
                   
    '''

    import pandas as pd

    from facebook_business.adobjects.adaccount import AdAccount
    from facebook_business.adobjects.reachestimate import ReachEstimate
    from facebook_business.api import FacebookAdsApi
    
    from fb_mig_utils import get_destinations, get_origins, check_countries

    FacebookAdsApi.init(access_token=access_token)

    mig_table = pd.DataFrame(0, index=destinations, columns=origins)
    
    dest_dict = get_destinations()
    origin_dict =  get_origins()
    
    check_countries(destinations,dest_dict)
    check_countries(origins,origin_dict)
    
    for destination in destinations:
        for origin in origins:
        
            fields = []
            params = {
                'targeting_spec': {'geo_locations':{'countries':[dest_dict[destination]['code']]},
                                   'age_min':age_min,
                                   'age_max':age_max, 
                                   'behaviors':[{'id': origin_dict[origin]['id'],
                                                 'name': origin_dict[origin]['name']}],
                                  },
                     }
            
            mig_table.loc[destination,origin] = float(AdAccount(user_id).get_reach_estimate(fields=fields,
										      params=params)[0]['users'])           
        fields = []
        params = {
            'targeting_spec': {'geo_locations':{'countries':[dest_dict[destination]['code']]},
                               'age_min':age_min,
                               'age_max':age_max,
                              },
                 }
            
        mig_table.loc[destination,'Total Population'] = AdAccount(user_id).get_reach_estimate(fields=fields,
										 	      params=params)[0]['users']        
    return mig_table

def get_destinations():
    
    '''
    Gets an updated dictionaty of available destinations names and corresponding codes
    from facebook api.
    '''
    
    from facebook_business.adobjects.targetingsearch import TargetingSearch
    
    params = {
    'type': 'adgeolocation',
    'location_types': ['country'],
    'limit': 1000,
    }

    resp = TargetingSearch.search(params=params)
    
    country_dict = {}
    
    for i in range(len(resp)):
            
            country_name = resp[i]['name']
            country_code = resp[i]['country_code']
            
            country_dict[country_name] = {'code': country_code}
    
    return country_dict

def get_origins():
    
    '''
    Gets an updated dictionaty of available origins names and corresponding codes
    from facebook api.
    '''
    
    from facebook_business.adobjects.targetingsearch import TargetingSearch
    
    params = {
    'type': 'adTargetingCategory',
    'class': 'behaviors',
    'limit': 1000,
    }

    resp = TargetingSearch.search(params=params)

    country_dict = {}

    for i in range(len(resp)):

        if resp[i]['path'][0]=='Expats' and resp[i]['name'].find('Lived in')==0:

            char_name_starts = resp[i]['name'].find('- ')+2
            char_name_ends = len(resp[i]['name'])-1
            country = resp[i]['name'][char_name_starts:char_name_ends]
            country_id = resp[i]['id']
            country_name = resp[i]['name']

            country_dict[country] =  {'id': country_id, 'name': country_name}
            
    return country_dict

def check_countries(countries, countries_dict):
    
    '''
    Check that the destinations and origins passed belong to the respective dictionaries
    and report an error if they don't.
    '''
    
    error_message =  ('The country you specified ({}) is not available, \n' +
                      'maybe you mispelled it. You can check the full list \n' +
                      'of destinations available by calling the get_destinations() \n' + 
                      'or the get_origins functions. use the syntax: \n\n' +
		      '    for elem in sorted(get_destinations().items()): \n' +
    		      '		print(elem[0]) \n\n' +
		      'to have an ordered list of countries.') 
    
    for country in countries:
        
        assert (country in countries_dict), error_message.format(country)
        