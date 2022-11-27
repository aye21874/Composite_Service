import logging.handlers
import requests
from flask import Flask, request, Response

from ColumbiaStudentResource import ColumbiaStudentResource

from datetime import datetime
import json

app = Flask(__name__)

# adding application keyword for gunicorn needs
application = app

# Create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

#I Solve my own problems ( No lecture tomorrow, prof in Europe )
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

@app.get("/api/health")
def get_health():
    t = str(datetime.now())
    msg = {
        "name": "F22-Starter-Microservice",
        "health": "Good",
        "at time": t
    }

    # DFF TODO Explain status codes, content type, ... ...
    result = Response(json.dumps(msg), status=200, content_type="application/json")

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
        # determine the MS where this http call should take us
        req = requests.get('https://cfan8n3rr9.execute-api.us-east-1.amazonaws.com/dev/' + MS_Name + '/' + path)
    elif request.method == "DELETE":
        # determine the MS where this http call should take us
        req = requests.delete('https://cfan8n3rr9.execute-api.us-east-1.amazonaws.com/dev/' + MS_Name + '/' + path)
    else:
        # determine the MS where this http call should take us
        req = requests.post('https://cfan8n3rr9.execute-api.us-east-1.amazonaws.com/dev/' + MS_Name + '/' + path)
    if req.status_code == 200:
        result = json.loads(req.content.decode('utf-8'))
        rsp = Response(json.dumps(result), status=200, content_type="application.json")
    else:
        rsp = Response(str(req.status_code), status=req.status_code, content_type="text/plain")
    return rsp
    # add http get calls to other MS


if __name__ == "__main__":
    app.run()


