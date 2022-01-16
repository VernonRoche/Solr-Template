import requests


###
#   Sends a request to gerbeaud.com to convert a reference to a json/dictionary format.
###
def get_json_from_url(meta_reference):
    params = dict(
        m=meta_reference,
    )
    url = 'https://www.gerbeaud.com/s/json_export_content.php?m='+meta_reference
    resp = requests.get(url=url)
    print("!INCOMING JSON RESPONSE FROM SERVER!")
    print(resp.text)
    if resp.text == "\n":
        return None
    return resp.json()


###
#   To use with get_json_from_url. Returns the first number from which meta_reference starts and the last where it ends
#   For example if A5 is the starting point and A360 the end-> [5, 360]
###
def get_category_bound(category_letter):
    url = 'https://www.gerbeaud.com/s/json_get_bounds.php'
    params = dict(
        t=category_letter
    )
    resp = requests.get(url=url, params=params)
    resp_json = resp.json()
    return [int(resp_json['first'][1:]), int(resp_json['last'][1:])]
