# Zenodo data flow

A simple flow to upload data using the Zenodo api!

[Zenodo](https://zenodo.org/) offers free scientific data hosting. One can either go to the website and upload manually, or publish and retrieve data via the API. 
This tutorial quickly implements the API to publish dummy data.

The API allows to automatically publish, store or host your data online, as well opens up possibilities for dashboarding from Zenodo.
![alt text](readme_images/zenodo.PNG?raw=true?)


Zenodo also allows to create communities where one can accept/reject what data goes into the community collection:

![alt text](readme_images/communities.PNG?raw=true)

running `main.py` while making some minor adaptations will publish dummy data into your repository.
You will need to create a Zenodo account first, this can be easily done on their website.

Be aware that there are 2 "websites":

* the regular website
* a sandbox version

They do not share your account and you will need a separate login to access your repository.
The sandbox one can be used to test things. The data there will probably be deleted on a regular base, so don't rely on this for anything other than testing!


Depending on if you would like to work in the sandbox or not, you can select this at the beginning of the script:

```python
sandbox = 0

if sandbox:
    ACCESS_TOKEN = 'secret'
    base_api = 'https://sandbox.zenodo.org/'
else:
    ACCESS_TOKEN = 'secret'
    base_api = 'https://zenodo.org/'
```

In the `upload_and_publish` function all the work is done, let's go over it.

We first test our token created when we registered an account at the Zenodo website:
```python
def upload_and_publish(input):

    # test token
    r = requests.get('{}api/deposit/depositions'.format(base_api),
                                           params={'access_token': ACCESS_TOKEN})
    print(r.status_code)
    print(r.json())
```

To start the publishing of data, we first create an empty upload:
```python
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
```

Next, we create a bucket that will be used to hold the .txt file we want to upload.

Edit `path` to upload your own little dummy data file.
The `put` requests additionally takes a `param` parameter, which just requires one parameter in this case, 'access_token'.

```python
    # bucket
    bucket_url = r.json()["links"]["bucket"]
    deposition_id = r.json()["id"]

    # New API
    filename = "test-data-zenodo.txt"
    path = r"C:\repos\zenodo-flow\%s" % filename

    # The target URL is a combination of the bucket link with the desired filename
    # seperated by a slash.
    with open(path, "rb") as fp:
        r = requests.put(
            "%s/%s" % (bucket_url, filename),
            data=fp,
            params=params,
            )
    r.json()
```

You can additionally also add metadata to the `put` request:
You can specify this by having a key called `metadata` added to the data parameter.

```python
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
```

Finally, we post this all via the API:

```python
    r = requests.post('{}api/deposit/depositions/{}/actions/publish'.format(base_api,deposition_id),
                          params={'access_token': ACCESS_TOKEN})
    print(r.status_code)
    print(r.json())
```

You can now verify the data in your uploads in zenodo:

![alt text](readme_images/first_upload.PNG?raw=true)

Click on the upload to check all the info related to this upload:

* The publisher (Maarten Van Loo)
* the data file attached (test-data-zenodo.txt)
* The publication date (23/08/2022)
* The DOI: (10.5281/zenodo.7016539)
* License (CC zero v1.0 Universal)
* Version (Version 1)

![alt text](readme_images/overviewofupload.PNG?raw=true)

Finally, you can also download the data file and verify the successful upload!:

![alt text](readme_images/data_upload.PNG?raw=true)


