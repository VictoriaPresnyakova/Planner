import json


def clear_rest_input_parameters(params):
    try:
        for k, v in params.items():
            if type(v) == dict:
                params[k] = str(json.dumps(v))
    except:
        return {}
    return params