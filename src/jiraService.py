import requests
import json

def createIssue(summary, desc):
    url = 'https://vivatia.atlassian.net/rest/api/2/issue/'
    obj = {
    "fields": {
       "project":{"key": "SOL"},
       "summary": summary,
       "description": desc,
       "issuetype": {"name": "Soporte"}
       }
    }
    
    body = json.dumps(obj)
    print(body)
    response = requests.post(url, data=body, auth=('federico.rivarola@vivatia.com','m6Rau4YvxtAu2qYBeEak63F5'))
    print(response.text)

createIssue('Test 22082020', 'Esto es un test')