import requests
import json

sandbox = 0

if sandbox:
    ACCESS_TOKEN = 'secret'
    base_api = 'https://sandbox.zenodo.org/'
else:
    ACCESS_TOKEN = 'secret'
    base_api = 'https://zenodo.org/'

def upload_and_publish(input):

    # test token
    r = requests.get('{}api/deposit/depositions'.format(base_api),
                                           params={'access_token': ACCESS_TOKEN})
    print(r.status_code)
    print(r.json())

    # empty upload
    headers = {"Content-Type": "application/json"}
    params = {'access_token': ACCESS_TOKEN}
    r = requests.post('{}api/deposit/depositions'.format(base_api),
                          params=params,
                          json={},
                          # Headers are not necessary here since "requests" automatically
                          # adds "Content-Type: application/json", because we're using
                          # the "json=" keyword argument
                          # headers=headers,
                          headers=headers)
    print(r.status_code)
    print(r.json())

    # bucket
    bucket_url = r.json()["links"]["bucket"]
    deposition_id = r.json()["id"]

    # New API
    filename = "test-data-zenodo.txt"
    path = r"C:\Users\VLOOM\OneDrive - VITO\Projects\vloca\%s" % filename

    # The target URL is a combination of the bucket link with the desired filename
    # seperated by a slash.
    with open(path, "rb") as fp:
        r = requests.put(
            "%s/%s" % (bucket_url, filename),
            data=fp,
            params=params,
            )
    r.json()

    # add meta-data
    data = {
        'metadata': {
             'title': 'My first upload',
             'upload_type': 'dataset',
             'description': 'This is my first upload',
             'creators': [{'name': 'Van Loo, Maarten',
                           'affiliation': 'VITO'}]
        }
     }
    r = requests.put('{}api/deposit/depositions/{}'.format(base_api,deposition_id),
                     params={'access_token': ACCESS_TOKEN},
                     data=json.dumps(data),
                     headers=headers)
    print(r.status_code)
    print(r.json())


    r = requests.post('{}api/deposit/depositions/{}/actions/publish'.format(base_api,deposition_id),
                          params={'access_token': ACCESS_TOKEN})
    print(r.status_code)
    print(r.json())

def list_uploads_user(ACCESS_TOKEN):
    response = requests.get('{}api/deposit/depositions'.format(base_api),
                            params={'access_token': ACCESS_TOKEN})
    print(response.json())

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    upload_and_publish('PyCharm')
    list_uploads_user(ACCESS_TOKEN)


