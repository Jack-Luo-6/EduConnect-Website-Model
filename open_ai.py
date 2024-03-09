from flask import Blueprint,request,render_template
import http.client, json

bp=Blueprint('open_ai',__name__)

@bp.route('/open_ai',methods=('GET','POST'))
def index(prompt=''):
    if request.method == 'POST':
        prompt = request.form['prompt']

        endpoint_url = '/openai/deployments/Davinci003-2023/completions?api-version=2022-12-01'
        headers = {
            'Content-Type': 'application/json',
            'api-key': '1fcc3afaded54cda94735c94fa060f83'
        }
        body = {
            'prompt': prompt,
            'max_tokens': 3900
        }
        try:
            conn = http.client.HTTPSConnection('appetizer.openai.azure.com')
            conn.request('POST',endpoint_url,json.dumps(body),headers)
            response = conn.getresponse()
            data = response.read()
            jdata = json.loads(data)
            body = jdata['choices'][0]['text']
        except Exception as e:
            return e
        else:
            return render_template('open_ai/results.html',prompt=prompt,body=body)

    return render_template('open_ai/index.html', prompt=prompt)