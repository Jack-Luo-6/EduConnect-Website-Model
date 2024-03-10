import http.client, json

def ai_call(prompt):
    endpoint_url = '/openai/deployments/Davinci003-2023/completions?api-version=2022-12-01'
    headers = {
        'Content-Type': 'application/json',
        'api-key': '1fcc3afaded54cda94735c94fa060f83'
    }
    body = {
        'prompt': prompt,
        'max_tokens': 200
    }
    try:
        conn = http.client.HTTPSConnection('appetizer.openai.azure.com')
        conn.request('POST',endpoint_url,json.dumps(body),headers)
        response = conn.getresponse()
        data = response.read()
        jdata = json.loads(data)
        print(jdata['choices'][0]['text'])
    except Exception as e:
        print(e)

ai_call('write a hate letter to Liu Jiayi')
