import json
import yaml
import copy

def converter(swagger: str, outfile: str, filters: list) -> dict:
    '''
    def converter(swagger: str, outfile: str, filters: list) -> dict:

    Function to convert a yaml file to a json file, allowing certain
    elements of the yaml file to be filtered.

    General file output will appear as follows:
    output = {
            'openapi': '...',
            'info': { ... },
            'tags': [ ... ],
            'servers': [ ... ],
            'paths': {
                'path_including_filter_1': { ... },
                'path_including_filter_2': { ... },
            },
            'components': {
                'schemas': {
                    'filter': { ... },
                },
                'responses': { ... },
        }

    If no filters are supplied, everything under paths and
    componenets>schemas will be included.
    '''

    file_content = {}
    output_data = {}
    
    out_file = outfile if outfile.endswith(".json") else outfile + ".json"
    
    try:
        with open(swagger, "r") as file:
            yaml_data = yaml.load(file, Loader=yaml.loader.SafeLoader)
    
    except Exception:
        with open(swagger + ".yaml", "r") as file:
            yaml_data = yaml.load(file, Loader=yaml.loader.SafeLoader)
        
    output = copy.deepcopy(yaml_data)
    
    if len(filters) > 0:
        
        alt_filters = [filt.lower().replace(" ", "") for filt in filters]

        for path in yaml_data['paths']:
            rem = True

            for alt_filt in alt_filters:
                if alt_filt in path:
                    rem = False
                    break

            if rem:
                output['paths'].pop(path)

        for schema in yaml_data['components']['schemas']:

            if schema not in filters:
                output['components']['schemas'].pop(schema)

        with open(out_file, "w") as file:
            json.dump(output, file)    
    
    return output

print(
    converter(
        'config1.yaml',
        'config1out.json',
        ['Auth', 'Notification']
        )
)