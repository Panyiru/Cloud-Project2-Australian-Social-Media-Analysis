import couchdb
from data_handler import data_handler

output_data = []

if __name__ == '__main__':
    try:
        filename_income = 'average income/data1967150000828455613.json'
        property_name = 'median_tot_prsnl_inc_weekly'
        changed_property_name = 'average_income_per_person_per_week'
        data_handler.migrate_data_from_aurin_data_1(filename_income, property_name, changed_property_name,output_data )

        filename_children = 'children/data1812116153898532245.json'
        property_name1 = 'cf_no_children_p'
        property_name2 = 'total_p'
        changed_property_name = 'having_children_percentage'
        data_handler.migrate_data_from_aurin_data_2(filename_children, property_name1, property_name2, changed_property_name,output_data)

        filename_education = 'Higher Education/data4071342425412760320.json'
        property_name1 = 'uni_other_tert_instit_tot_p'
        property_name2 = 'tot_p'
        changed_property_name = 'higher_education_percentage'
        data_handler.migrate_data_from_aurin_data_3(filename_education, property_name1, property_name2, changed_property_name,output_data)

        filename_age = 'age/data6252086582398545451.json'
        property_name = 'med_age_psns_tot'
        changed_property_name = 'medium_age'
        data_handler.migrate_data_from_aurin_data_1(filename_age, property_name, changed_property_name,output_data)

        filename_volunteer = 'volunteer/data1217128629530106067.json'
        property_name = 'p_tot_volunteer'
        changed_property_name = 'volunteer_total_num'
        data_handler.migrate_data_from_aurin_data_1(filename_volunteer, property_name, changed_property_name,output_data)

        # Write into database
        couch_server = couchdb.Server('http://admin:team38@115.146.86.136:5984')
        db = couch_server['tweet']

        db['1234567890'] = {'rows': output_data}

    except Exception as e:
        print('Error: ' + str(e))


