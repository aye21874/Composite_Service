import logging.handlers
import requests
from flask import Flask, request, Response, url_for, session, redirect
from authlib.integrations.flask_client import OAuth
from flask_cors import CORS

from datetime import datetime
import json

app = Flask(__name__)
app.secret_key = 'agasdgasasd'
CORS(app)

original_url = '/'


@app.before_request
def before_request():
    # need to verify the token first
    token = request.args.get('token')
    req = requests.get(f'https://www.googleapis.com/oauth2/v3/tokeninfo?id_token={token}')
    if req.status_code != 200:
        rsp = Response("wrong token", status=401, content_type="text/plain")
        return rsp
        # return redirect(url_for('login'))
    # if 'email' not in dict(session).keys() and request.endpoint != 'login' and request.endpoint != 'authorize':
    #     global original_url
    #     original_url = request.base_url
    #     google = oauth.create_client('google')
    #     redirect_url = url_for('authorize', _external=True)
    #     return google.authorize_redirect(redirect_url)


# auth config
oauth = OAuth(app)
oauth.register(
    name='google',
    client_id='373950359301-b15ek6eo55mfgavseio8kgp2pcqtd6l9.apps.googleusercontent.com',
    client_secret='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',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    jwks_uri='https://www.googleapis.com/oauth2/v3/certs',
    client_kwargs={'scope': 'openid profile email'}
)


@app.route('/get_token')
def get_token():
    token = dict(session).get('token', None)
    return token


@app.route('/login')
def login():
    google = oauth.create_client('google')
    redirect_url = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_url)


@app.route('/authorize')
def authorize():
    google = oauth.create_client('google')
    try:
        token = google.authorize_access_token()
        session['token'] = token
    except Exception as e:
        print(e)
    return redirect(original_url)


@app.route('/logout')
def logout():
    for key in list(session.keys()):
        session.pop(key)
    return redirect(url_for('login'))


# adding application keyword for gunicorn needs
application = app

# Create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# app.config['MySQL_HOST'] = 'localhost'


# Handler 
LOG_FILE = '/tmp/sample-app.log'
handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=1048576, backupCount=5)
handler.setLevel(logging.INFO)

# Formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Add Formatter to Handler
handler.setFormatter(formatter)

# add Handler to Logger
logger.addHandler(handler)

welcome = """
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
  <!--
    Copyright 2012 Amazon.com, Inc. or its affiliates. All Rights Reserved.

    Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file except in compliance with the License. A copy of the License is located at

        http://aws.Amazon/apache2.0/

    or in the "license" file accompanying this file. This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
  -->
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
  <title>Welcome</title>
  <style>
  body {
    color: #ffffff;
    background-color: #E0E0E0;
    font-family: Arial, sans-serif;
    font-size:14px;
    -moz-transition-property: text-shadow;
    -moz-transition-duration: 4s;
    -webkit-transition-property: text-shadow;
    -webkit-transition-duration: 4s;
    text-shadow: none;
  }
  body.blurry {
    -moz-transition-property: text-shadow;
    -moz-transition-duration: 4s;
    -webkit-transition-property: text-shadow;
    -webkit-transition-duration: 4s;
    text-shadow: #fff 0px 0px 25px;
  }
  a {
    color: #0188cc;
  }
  .textColumn, .linksColumn {
    padding: 2em;
  }
  .textColumn {
    position: absolute;
    top: 0px;
    right: 50%;
    bottom: 0px;
    left: 0px;

    text-align: right;
    padding-top: 11em;
    background-color: #1BA86D;
    background-image: -moz-radial-gradient(left top, circle, #6AF9BD 0%, #00B386 60%);
    background-image: -webkit-gradient(radial, 0 0, 1, 0 0, 500, from(#6AF9BD), to(#00B386));
  }
  .textColumn p {
    width: 75%;
    float:right;
  }
  .linksColumn {
    position: absolute;
    top:0px;
    right: 0px;
    bottom: 0px;
    left: 50%;

    background-color: #E0E0E0;
  }

  h1 {
    font-size: 500%;
    font-weight: normal;
    margin-bottom: 0em;
  }
  h2 {
    font-size: 200%;
    font-weight: normal;
    margin-bottom: 0em;
  }
  ul {
    padding-left: 1em;
    margin: 0px;
  }
  li {
    margin: 1em 0em;
  }
  </style>
</head>
<body id="sample">
  <div class="textColumn">
    <h1>Congratulations</h1>
    <p>Your first AWS Elastic Beanstalk Python Application is now running on your own dedicated environment in the AWS Cloud</p>
    <p>This environment is launched with Elastic Beanstalk Python Platform</p>
    <p> My Man, Lets GOooo, We fucking did it!!! </p>
  </div>
  
  <div class="linksColumn"> 
    <h2>What's Next?</h2>
    <ul>
    <li><a href="http://docs.amazonwebservices.com/elasticbeanstalk/latest/dg/">AWS Elastic Beanstalk overview</a></li>
    <li><a href="http://docs.amazonwebservices.com/elasticbeanstalk/latest/dg/index.html?concepts.html">AWS Elastic Beanstalk concepts</a></li>
    <li><a href="http://docs.amazonwebservices.com/elasticbeanstalk/latest/dg/create_deploy_Python_django.html">Deploy a Django Application to AWS Elastic Beanstalk</a></li>
    <li><a href="http://docs.amazonwebservices.com/elasticbeanstalk/latest/dg/create_deploy_Python_flask.html">Deploy a Flask Application to AWS Elastic Beanstalk</a></li>
    <li><a href="http://docs.amazonwebservices.com/elasticbeanstalk/latest/dg/create_deploy_Python_custom_container.html">Customizing and Configuring a Python Container</a></li>
    <li><a href="http://docs.amazonwebservices.com/elasticbeanstalk/latest/dg/using-features.loggingS3.title.html">Working with Logs</a></li>

    </ul>
  </div>
</body>
</html>
"""


# @app.route("/", methods=["GET", "PUT", "POST", "DELETE"])
# def do_basic():
#
#     method = request.method
#     path = request.path
#
#     response_txt = welcome
#
#     rsp = Response(status=200, response=response_txt, content_type="text/html")
#     return rsp


@app.route("/api/health")
def get_health():
    # token is valid
    t = str(datetime.now())
    msg = {
        "name": "F22-Starter-Microservice",
        "health": "Good",
        "at time": t,
    }
    # DFF TODO Explain status codes, content type, ... ...
    result = Response(json.dumps(msg), status=200, content_type="text/plain")
    return result


# @app.route("/api/courses/<uni>", methods=["GET"])
# def get_courses_by_uni(uni):
#     #get all courses enrolled by a particular uni
#
#     result = ColumbiaStudentResource.get_by_key(uni)
#
#     if result:
#         rsp = Response(json.dumps(result), status=200, content_type="application.json")
#     else:
#         rsp = Response("NOT FOUND", status=404, content_type="text/plain")
#
#     return rsp

# https://cfan8n3rr9.execute-api.us-east-1.amazonaws.com/dev/students/ab1234/courses
# # https://cfan8n3rr9.execute-api.us-east-1.amazonaws.com/dev/courses/ab1234
# this server will have its own api
# assuming /dev/<MS_NAME>/whatever//
# /api/students/page/1
# /api/students/page@1
# replace ->
@app.route("/api/<MS_Name>/<path:path>", methods=["GET", "POST", "DELETE"])
def get_MS(MS_Name,path):
    if request.method == "GET":
        req = requests.get('https://cfan8n3rr9.execute-api.us-east-1.amazonaws.com/dev/' + MS_Name + '/' + path)
    elif request.method == "DELETE":
        req = requests.delete('https://cfan8n3rr9.execute-api.us-east-1.amazonaws.com/dev/' + MS_Name + '/' + path)
    elif request.method == "POST":
        data = request.get_json()
        req = requests.post('https://cfan8n3rr9.execute-api.us-east-1.amazonaws.com/dev/' + MS_Name + '/' + path, data=data)
    else:
        return Response("Method not allowed", status=405, content_type="text/plain")
    if req.status_code == 200:
        result = json.loads(req.content.decode('utf-8'))
        rsp = Response(json.dumps(result), status=200, content_type="application.json")
    else:
        rsp = Response(str(req.status_code), status=req.status_code, content_type="text/plain")
    return rsp
    # add http get calls to other MS


# universal interface
@app.route("/composite/students/<uni>", methods=["GET", "PUT", "POST", "DELETE"])
def student_by_uni(uni):
    if request.method == "GET":
        result = {'student_info': None, 'student_courses': None, 'student_contact': {'addresses': None, 'phones': None, 'emails': None}}
        req1 = requests.get(f'https://cfan8n3rr9.execute-api.us-east-1.amazonaws.com/dev/students/{uni}')
        req2 = requests.get(f'https://cfan8n3rr9.execute-api.us-east-1.amazonaws.com/dev/courses/{uni}')
        req3 = requests.get(f'https://cfan8n3rr9.execute-api.us-east-1.amazonaws.com/dev/contacts/{uni}/addresses')
        req4 = requests.get(f'https://cfan8n3rr9.execute-api.us-east-1.amazonaws.com/dev/contacts/{uni}/phones')
        req5 = requests.get(f'https://cfan8n3rr9.execute-api.us-east-1.amazonaws.com/dev/contacts/{uni}/emails')
        if req1.status_code == 200:
            result['student_info'] = json.loads(req1.content.decode('utf-8'))
        if req2.status_code == 200:
            result['student_courses'] = json.loads(req2.content.decode('utf-8'))
        if req3.status_code == 200:
            result['student_contact']['addresses'] = json.loads(req3.content.decode('utf-8'))
        if req4.status_code == 200:
            result['student_contact']['phones'] = json.loads(req4.content.decode('utf-8'))
        if req1.status_code == 200:
            result['student_contact']['emails'] = json.loads(req5.content.decode('utf-8'))

    elif request.method == "DELETE":
        result = {'student_info': False, 'student_courses': False,
                  'student_contact': {'addresses': False, 'phones': False, 'emails': False}}
        req1 = requests.delete(f'https://cfan8n3rr9.execute-api.us-east-1.amazonaws.com/dev/students/{uni}')
        req2 = requests.delete(f'https://cfan8n3rr9.execute-api.us-east-1.amazonaws.com/dev/courses/{uni}')
        req3 = requests.delete(f'https://cfan8n3rr9.execute-api.us-east-1.amazonaws.com/dev/contacts/{uni}/addresses')
        req4 = requests.delete(f'https://cfan8n3rr9.execute-api.us-east-1.amazonaws.com/dev/contacts/{uni}/phones')
        req5 = requests.delete(f'https://cfan8n3rr9.execute-api.us-east-1.amazonaws.com/dev/contacts/{uni}/emails')
        if req1.status_code == 200:
            result['student_info'] = True
        if req2.status_code == 200:
            result['student_courses'] = True
        if req3.status_code == 200:
            result['student_contact']['addresses'] = True
        if req4.status_code == 200:
            result['student_contact']['phones'] = True
        if req5.status_code == 200:
            result['student_contact']['emails'] = True

    elif request.method == "PUT":
        result = {'student_info': False, 'student_courses': False,
                  'student_contact': {'addresses': False, 'phones': False, 'emails': False}}
        data = request.get_json()
        req1 = requests.put(f'https://cfan8n3rr9.execute-api.us-east-1.amazonaws.com/dev/students/{uni}', data=data['student_info'])
        req2 = requests.post(f'https://cfan8n3rr9.execute-api.us-east-1.amazonaws.com/dev/courses/{uni}', data=data['student_courses'])
        req3 = requests.post(f'https://cfan8n3rr9.execute-api.us-east-1.amazonaws.com/dev/contacts/{uni}/addresses', data=data['student_contact']['addresses'])
        req4 = requests.post(f'https://cfan8n3rr9.execute-api.us-east-1.amazonaws.com/dev/contacts/{uni}/phones', data=data['student_contact']['emails'])
        req5 = requests.post(f'https://cfan8n3rr9.execute-api.us-east-1.amazonaws.com/dev/contacts/{uni}/emails', data=data['student_contact']['phones'])
        if req1.status_code == 200:
            result['student_info'] = True
        if req2.status_code == 200:
            result['student_courses'] = True
        if req3.status_code == 200:
            result['student_contact']['addresses'] = True
        if req4.status_code == 200:
            result['student_contact']['phones'] = True
        if req5.status_code == 200:
            result['student_contact']['emails'] = True

    elif request.method == "POST":
        result = {'student_info': False, 'student_courses': False,
                  'student_contact': {'addresses': False, 'phones': False, 'emails': False}}
        data = request.get_json()
        req1 = requests.post(f'https://cfan8n3rr9.execute-api.us-east-1.amazonaws.com/dev/students', data=data['student_info'])
        req2 = requests.post(f'https://cfan8n3rr9.execute-api.us-east-1.amazonaws.com/dev/courses/{uni}', data=data['student_courses'])
        req3 = requests.post(f'https://cfan8n3rr9.execute-api.us-east-1.amazonaws.com/dev/contacts/{uni}/addresses', data=data['student_contact']['addresses'])
        req4 = requests.post(f'https://cfan8n3rr9.execute-api.us-east-1.amazonaws.com/dev/contacts/{uni}/phones', data=data['student_contact']['emails'])
        req5 = requests.post(f'https://cfan8n3rr9.execute-api.us-east-1.amazonaws.com/dev/contacts/{uni}/emails', data=data['student_contact']['phones'])
        if req1.status_code == 200:
            result['student_info'] = True
        if req2.status_code == 200:
            result['student_courses'] = True
        if req3.status_code == 200:
            result['student_contact']['addresses'] = True
        if req4.status_code == 200:
            result['student_contact']['phones'] = True
        if req5.status_code == 200:
            result['student_contact']['emails'] = True
    else:
        return Response("Method not allowed", status=405, content_type="text/plain")
    rsp = Response(json.dumps(result), status=200, content_type="application.json")
    return rsp


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5013)


