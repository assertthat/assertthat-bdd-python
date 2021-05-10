import requests
from zipfile import ZipFile
from io import BytesIO
import datetime
import os
import json
import re

class JiraConnector:

    def download_features(project_id, access_key=None, secret_key=None, jira_server_url=None, output_folder='./features/', jql=None, mode='automated', tags=None,
                          proxy_uri=None, proxy_username=None, proxy_password=None):

        if access_key is None:
            if os.environ.get("ASSERTTHAT_ACCESS_KEY") is None:
                print("[ERROR] ASSERTTHAT_ACCESS_KEY is missing, should be provided as environment variable or parameter")
            else:
                access_key = os.environ.get("ASSERTTHAT_ACCESS_KEY")

        if secret_key is None:
            if os.environ.get("ASSERTTHAT_SECRET_KEY") is None:
                print("[ERROR] ASSERTTHAT_SECRET_KEY is missing, should be provided as environment variable or parameter")
            else:
                secret_key = os.environ.get("ASSERTTHAT_SECRET_KEY")

        if jira_server_url is None:
            path = 'https://bdd.assertthat.app/rest/api/1/project/' + project_id + '/features'
        else:
            path = jira_server_url+"/rest/assertthat/latest/project/" + project_id + "/client/features"
        headers = {}
        payload = {'mode': mode,
                   'jql': jql,
                   'tags': tags
                   }
        print('Fetching from: ' + path)

        if proxy_uri is None:
            proxies = None

        elif proxy_uri is not None:
            if proxy_username is None:
                proxy_http = "http://%s" % (proxy_uri)
                proxy_https = "https://%s" % (proxy_uri)
            elif proxy_username is not None:
                proxy_http = "http://%s:%s@%s" % (proxy_username, proxy_password, proxy_uri)
                proxy_https = "https://%s:%s@%s" % (proxy_username, proxy_password, proxy_uri)
            proxies = {'http': proxy_http,
                       'https': proxy_https
                       }

        try:
            response = requests.get(path, auth=(access_key, secret_key), headers=headers, params=payload,
                                    proxies=proxies)

            if response.status_code == 200:
                print('Fetched.')
                print('Preparing to extract...')
                zip = ZipFile(BytesIO(response.content))
                infolist = zip.infolist()
                zip.extractall(path=output_folder)
                print('[INFO] Downloaded ' + str(infolist.__len__()) + ' feature files into "' + output_folder + '"')

            response.raise_for_status()

        except requests.exceptions.HTTPError as errh:
            response_content = response.content
            print("[ERROR] Failed to download features %s" % (response_content))

        except requests.exceptions.RequestException as err:
            print("[ERROR] Failed to download features", err)

    def upload_report(project_id, access_key, secret_key, jira_server_url=None,
                      run_name='Test run ' + datetime.datetime.now().strftime("%d %b %Y %H:%M:%S"),
                      json_report_folder='./reports/', json_report_include_pattern='\.json$', type='cucumber',
                      proxy_uri=None, proxy_username=None, proxy_password=None):

        if jira_server_url is None:
            path = 'https://bdd.assertthat.app/rest/api/1/project/' + project_id + '/report'
        else:
            path = jira_server_url + "/rest/assertthat/latest/project/" + project_id + "/client/report"

        if proxy_uri is None:
            proxies = None

        elif proxy_uri is not None:
            if proxy_username is None:
                proxy_http = "http://%s" % proxy_uri
                proxy_https = "https://%s" % proxy_uri
            elif proxy_username is not None:
                proxy_http = "http://%s:%s@%s" % (proxy_username, proxy_password, proxy_uri)
                proxy_https = "https://%s:%s@%s" % (proxy_username, proxy_password, proxy_uri)
            proxies = {'http': proxy_http,
                       'https': proxy_https
                       }

        runId = '-1'
        for subdir, dirs, files in os.walk(json_report_folder):
            print("[INFO] Uploading json reports to AssertThat for %s " % files)
            for file in files:
                if re.search(r"%s" % json_report_include_pattern, file):
                    report_file = os.path.join(subdir, file)
                    upload_file = {'file': open(report_file, 'rb')}

                    headers = {}
                    payload = {'runName': run_name,
                               'type': type,
                               'runId': runId
                               }

                    try:
                        response = requests.post(path, auth=(access_key, secret_key), headers=headers, params=payload,
                                                 files=upload_file, proxies=proxies)
                        response_content = json.loads(response.content)

                        if response.status_code == 200:
                            runId = response_content['runId']
                            print("[INFO] Uploaded report file %s to AssertThat" % file)

                        response.raise_for_status()

                    except requests.exceptions.HTTPError as errh:
                        print("[ERROR] %s while uploading %s" % (response_content['message'], file))

                    except requests.exceptions.RequestException as err:
                        print("[ERROR] Failed to send request", err)
