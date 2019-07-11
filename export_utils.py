import os

repo_path = os.getcwd()[0:len(os.getcwd())]

def export_age_str_dict(age_str_dict):
    
    age_str_tables_path = repo_path + '/age_str_tables/'
    if not os.path.exists(age_str_tables_path):
        os.makedirs(age_str_tables_path)
    
    for key_country in age_str_dict:
        for feature_country in age_str_dict[key_country]:
            df_to_export = age_str_dict[key_country][feature_country]['age_structure_table']
            df_name = '{}_{}_str_table.csv'.format(key_country.lower(),feature_country.lower())
            df_to_export.to_csv(age_str_tables_path + df_name)