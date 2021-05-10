# assertthat-bdd 
Python plugin for interaction with [AssertThat BDD Jira plugin](https://marketplace.atlassian.com/1219033)

# Main features are:

Download feature files before test run
Filter features to download based on mode (automated/manual/both), or/and JQL
Upload cucumber json after the run to AsserTthat Jira plugin

# Installation
To add the library to your project:

```pip install assertthat-bdd```

Full plugin configuration below, optional properties can be omitted.  

project_id, access_key secret_key can be found from the  [asserthat configuration page](https://assertthat.atlassian.net/wiki/spaces/ABTM/pages/725385217/Configuration)

```
from assertthat_bdd.jira_integration import JiraConnector

JiraConnector.download_features(
    # Jira project id e.g. 10001
    project_id='PROJECT_ID',
    # Optional can be supplied as environment variable ASSERTTHAT_ACCESS_KEY
    access_key='ASSERTTHAT_ACCESS_KEY',
    # Optional can be supplied as environment variable ASSERTTHAT_SECRET_KEY
    secret_key='ASSERTTHAT_SECRET_KEY',
    # Optional - default ./features
    output_folder='./features',
    #Required for Jira Server only. Omit if using Jira Cloud version
    jira_server_url: 'https://mycompanyjira.com'
    # Optional - all features downloaded by default - should be a valid JQL
    # jql = 'project = XX AND key in ('XXX-1')',
    # Optional - default automated (can be one of: manual/automated/both)
    mode='both',
    #Optional - tag expression filter for scenarios. More on tag expressions https://cucumber.io/docs/cucumber/api/#tag-expressions
    tags: '(@smoke or @ui) and (not @slow)',
    # Optional - Detail the proxy with the specific scheme e.g.'10.10.10.10:1010'
    # proxy_uri='proxyip:port',
    proxy_uri= 'proxy_uri',
    # Optional - user name which will be used for proxy authentication.*/
    proxy_username='username',
    # Optional - password which will be used for proxy authentication.*/
    proxy_password='password'
)

JiraConnector.upload_report(
    # Jira project id e.g. 10001
    project_id='PROJECT_ID',
    # Optional can be supplied as environment variable ASSERTTHAT_ACCESS_KEY
    access_key='ASSERTTHAT_ACCESS_KEY',
    # Optional can be supplied as environment variable ASSERTTHAT_SECRET_KEY
    secret_key='ASSERTTHAT_SECRET_KEY',
    # The name of the run - default 'Test run dd MMM yyyy HH:mm:ss'
    run_name= 'Dry Tests Run',
    #Required for Jira Server only. Omit if using Jira Cloud version
    jira_server_url: 'https://mycompanyjira.com'
    # Json report folder - default ./reports
    json_report_folder='./reports',
    # Regex to search for cucumber reports - default "\.json$"
    json_report_include_pattern='\.json$',
    # Optional - default cucumber (can be one of: cucumber/karate)
    type='cucumber'',
    # Optional - Detail the proxy with the specific scheme e.g.'10.10.10.10:1010'
    # proxy_uri='proxyip:port',
    # Optional - user name which will be used for proxy authentication.*/
    proxy_username='username',
    # Optional - password which will be used for proxy authentication.*/
    proxy_password='password'
    )
```

# Usage
We recommend running cucumber tests on integration-test phase as

- download features is running on pre-integration-test phase
- report submission on post-integration-test

# Example project
Refer to example project - https://github.com/assertthat/assertthat-behave-example
