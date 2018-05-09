import json

class data_handler():

    @staticmethod
    # For average income, average age and total volunteer_num
    def migrate_data_from_aurin_data_1(filename, property_name, changed_property_name, output_data):
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
                if data['features']:
                    for row in data['features']:
                        if row['properties'] and row['properties']['sa2_main16']:
                            find_key = False
                            for line_data in output_data:
                                if line_data['key'] == row['properties']['sa2_main16']:
                                    if line_data['value']:
                                        line_data['value'][changed_property_name] = row['properties'][property_name]
                                        find_key = True
                            if not find_key:
                                output_data.append({'key': row['properties']['sa2_main16'],
                                                    'value': {changed_property_name: row['properties'][property_name]}})
        except Exception as e:
            print('Error: ' + str(e))

    # For having_children_percentage
    @staticmethod
    def migrate_data_from_aurin_data_2(filename, property_name1, property_name2, changed_property_name, output_data):
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
                if data['features']:
                    for row in data['features']:
                        if row['properties'] and row['properties']['sa2_main16']:
                            find_key = False
                            for line_data in output_data:
                                if line_data['key'] == row['properties']['sa2_main16']:
                                    if line_data['value'] and not row['properties'][property_name2] == 0:
                                        percentage = (1 - (row['properties'][property_name1]) / (
                                        row['properties'][property_name2])) * 100
                                        line_data['value'][changed_property_name] = '{0:.4f}%'.format(percentage)
                                        find_key = True
                                    elif line_data['value'] and row['properties'][property_name2] == 0:
                                        line_data['value'][changed_property_name] = None
                            if not find_key and not row['properties'][property_name2] == 0:
                                percentage = (1 - row['properties'][property_name1] / row['properties'][
                                    property_name2]) * 100
                                output_data.append({'key': row['properties']['sa2_main16'],
                                                    'value': {changed_property_name: '{0:.4f}%'.format(percentage)}})
                            elif not find_key and row['properties'][property_name2] == 0:
                                output_data.append({'key': row['properties']['sa2_main16'],
                                                    'value': {changed_property_name: None}})
        except Exception as e:
            print('Error: ' + str(e))

    # For higher_education_percentage
    @staticmethod
    def migrate_data_from_aurin_data_3(filename, property_name1, property_name2, changed_property_name, output_data):
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
                if data['features']:
                    for row in data['features']:
                        if row['properties'] and row['properties']['sa2_main16']:
                            find_key = False
                            for line_data in output_data:
                                if line_data['key'] == row['properties']['sa2_main16']:
                                    if line_data['value'] and not row['properties'][property_name2] == 0:
                                        percentage = (row['properties'][property_name1]) / (
                                        row['properties'][property_name2]) * 100
                                        line_data['value'][changed_property_name] = '{0:.4f}%'.format(percentage)
                                        find_key = True
                                    elif line_data['value'] and row['properties'][property_name2] == 0:
                                        line_data['value'][changed_property_name] = None
                            if not find_key and not row['properties'][property_name2] == 0:
                                percentage = (row['properties'][property_name1]) / (
                                row['properties'][property_name2]) * 100
                                output_data.append({'key': row['properties']['sa2_main16'],
                                                    'value': {changed_property_name: '{0:.4f}%'.format(percentage)}})
                            elif not find_key and row['properties'][property_name2] == 0:
                                output_data.append({'key': row['properties']['sa2_main16'],
                                                    'value': {changed_property_name: None}})
        except Exception as e:
            print('Error: ' + str(e))
