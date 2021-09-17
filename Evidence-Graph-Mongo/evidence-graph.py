#© 2020 By The Rector And Visitors Of The University Of Virginia

#Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
import flask, logging, os, jwt
from flask import Flask, render_template, request, redirect,jsonify

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TESTING = os.environ.get("NO_AUTH",False)
HOST_URL = os.environ.get("HOST_URL","")

app = Flask(__name__)

app.url_map.converters['everything'] = EverythingConverter

@app.route('/')
def homepage():
    return 'working'

@app.route('/<everything:ark>')
@user_level_permission
def eg_builder(ark):

    token = request.headers.get("Authorization")

    NO_AUTH = os.environ.get("NO_AUTH",False)
    if NO_AUTH:
        token = jwt.encode({'name': 'Admin','role':'admin','sub':'admin-id','groups':['test'],'aud':'https://fairscape.org'}, 'test secret', algorithm='HS256')

    args = request.args
    include = []
    for k, v in args.items():
        if v == '1':
            include.append(k)

    if not valid_ark(ark):
        return flask.jsonify({"error":"Improperly formatted Identifier"}), 400

    #Check to make sure request is for known ark
    try:
        ark_exists(ark,token)
    except:
        logger.error('User gievn ark does not exist ' + str(ark))
        return jsonify({'error':'Given ark does not exist.'}),503


    
