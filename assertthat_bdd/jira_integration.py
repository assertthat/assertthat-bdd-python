import requests
from zipfile import ZipFile
from io import BytesIO
import datetime
import os
import json
import re

class JiraConnector:

    def download_features(project_id, access_key=None, secret_key=None, token=None, jira_server_url=None, output_folder='./features/', jql=None, mode='automated', tags=None,
                          proxy_uri=None, proxy_username=None, proxy_password=None):

        # Use environment variable for token if not provided
        if token is None:
            token = os.environ.get("ASSERTTHAT_TOKEN")

        # Check for conflicting authentication methods
        if token and (access_key or secret_key):
            print("[ERROR] Both token and access_key/secret_key are provided. Please use only one authentication method.")
            return

        # If no token, try to get access_key and secret_key from environment or parameters
        if token is None:
            if access_key is None:
                access_key = os.environ.get("ASSERTTHAT_ACCESS_KEY")
                if access_key is None:
                    print("[ERROR] ASSERTTHAT_ACCESS_KEY is missing, should be provided as environment variable or parameter")
                    return

            if secret_key is None:
                secret_key = os.environ.get("ASSERTTHAT_SECRET_KEY")
                if secret_key is None:
                    print("[ERROR] ASSERTTHAT_SECRET_KEY is missing, should be provided as environment variable or parameter")
                    return

        # Set up the URL and headers
        if jira_server_url is None:
            path = f'https://bdd.assertthat.app/rest/api/1/project/{project_id}/features'
        else:
            path = f'{jira_server_url}/rest/assertthat/latest/project/{project_id}/client/features'

        headers = {'X-Atlassian-Token': 'no-check'}
        if token:
            headers['Authorization'] = f'Bearer {token}'

        payload = {
            'mode': mode,
            'jql': jql,
            'tags': tags
        }
        print('Fetching from: ' + path)

        # Configure proxies if provided
        if proxy_uri:
            if proxy_username:
                proxy_http = f"http://{proxy_username}:{proxy_password}@{proxy_uri}"
                proxy_https = f"https://{proxy_username}:{proxy_password}@{proxy_uri}"
            else:
                proxy_http = f"http://{proxy_uri}"
                proxy_https = f"https://{proxy_uri}"
            proxies = {'http': proxy_http, 'https': proxy_https}
        else:
            proxies = None

        # Make the request with appropriate authentication
        try:
            if token:
                response = requests.get(path, headers=headers, params=payload, proxies=proxies)
            else:
                response = requests.get(path, auth=(access_key, secret_key), headers=headers, params=payload, proxies=proxies)

            if response.status_code == 200:
                print('Fetched.')
                print('Preparing to extract...')
                zip_file = ZipFile(BytesIO(response.content))
                infolist = zip_file.infolist()
                zip_file.extractall(path=output_folder)
                print('[INFO] Downloaded ' + str(len(infolist)) + ' feature files into "' + output_folder + '"')
            else:
                print(f"[ERROR] Failed to download features: {response.status_code}")

            response.raise_for_status()

        except requests.exceptions.HTTPError as errh:
            print("[ERROR] Failed to download features:", errh)
        except requests.exceptions.RequestException as err:
            print("[ERROR] Failed to download features", err)

    def upload_report(project_id, access_key=None, secret_key=None, token=None, jira_server_url=None,
                      run_name='Test run ' + datetime.datetime.now().strftime("%d %b %Y %H:%M:%S"),
                      json_report_folder='./reports/', json_report_include_pattern=r'\.json$', type='cucumber',
                      proxy_uri=None, proxy_username=None, proxy_password=None):

        # Use environment variable for token if not provided
        if token is None:
            token = os.environ.get("ASSERTTHAT_TOKEN")

        # Check for conflicting authentication methods
        if token and (access_key or secret_key):
            print("[ERROR] Both token and access_key/secret_key are provided. Please use only one authentication method.")
            return

        # Set up the URL
        if jira_server_url is None:
            path = f'https://bdd.assertthat.app/rest/api/1/project/{project_id}/report'
        else:
            path = f'{jira_server_url}/rest/assertthat/latest/project/{project_id}/client/report'

        # Configure proxies if provided
        if proxy_uri:
            if proxy_username:
                proxy_http = f"http://{proxy_username}:{proxy_password}@{proxy_uri}"
                proxy_https = f"https://{proxy_username}:{proxy_password}@{proxy_uri}"
            else:
                proxy_http = f"http://{proxy_uri}"
                proxy_https = f"https://{proxy_uri}"
            proxies = {'http': proxy_http, 'https': proxy_https}
        else:
            proxies = None

        headers = {'X-Atlassian-Token': 'no-check'}
        if token:
            headers['Authorization'] = f'Bearer {token}'

        runId = '-1'
        for subdir, dirs, files in os.walk(json_report_folder):
            print(f"[INFO] Uploading JSON reports to AssertThat for files: {files}")
            for file in files:
                if re.search(json_report_include_pattern, file):
                    report_file = os.path.join(subdir, file)
                    upload_file = {'file': open(report_file, 'rb')}

                    payload = {
                        'runName': run_name,
                        'type': type,
                        'runId': runId
                    }

                    try:
                        if token:
                            response = requests.post(path, headers=headers, params=payload, files=upload_file, proxies=proxies)
                        else:
                            response = requests.post(path, auth=(access_key, secret_key), headers=headers, params=payload, files=upload_file, proxies=proxies)

                        response_content = json.loads(response.content)

                        if response.status_code == 200:
                            runId = response_content.get('runId', runId)  # Update runId if provided in response
                            print(f"[INFO] Uploaded report file {file} to AssertThat")

                        response.raise_for_status()

                    except requests.exceptions.HTTPError as errh:
                        print(f"[ERROR] {response_content.get('message', 'Unknown error')} while uploading {file}")

                    except requests.exceptions.RequestException as err:
                        print("[ERROR] Failed to send request", err)
