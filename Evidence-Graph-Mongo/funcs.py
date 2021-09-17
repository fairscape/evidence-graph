import requests, json, os

ORS_URL = os.environ.get("ORS_URL", "http://localhost:80/")

def remove_non_evidence(eg,eg_only = True,keep = []):
    '''
    Goes through json metadata removes keys unrelated to basic in or
    the evi ontology fixes minor formatting things
    '''
    for key in list(eg):
        if 'evi' not in key and 'eg' not in key and key != '@id' and \
                        key != 'author' and key != 'name' and key != '@type' \
                        and key not in keep:
            eg.pop(key, None)
            continue
        if 'evi:supports' == key:
            eg.pop(key, None)
            continue
        elif isinstance(eg[key],list):
            for dictionary in eg[key]:
                if isinstance(dictionary,dict):
                    dictionary = remove_non_evidence(dictionary)
        elif isinstance(eg[key],dict):
            eg[key] = remove_non_evidence(eg[key])
    return eg

def retrieve_metadata(ark,token):
    r = requests.get(
        ORS_URL + ark,
        headers={"Authorization": token}
        )
    return r.json()

def expand_evidence(id,token):
    temp_local_eg = EG(id,token)
    temp_local_eg.expand()
    return temp_local_eg.eg

def ark_exists(ark,token):
    '''
    Pings ors to see if ark is reconginzed
    '''

    r = requests.get(ORS_URL + ark,headers = {"Authorization": token})
    if r.status_code >= 400:
        raise Exception

def valid_ark(ark):
    pattern = re.compile("ark:\d+/[\d,\w,-]+")
    if pattern.match(ark):
        return True
    return False
