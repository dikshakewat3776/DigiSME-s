from flask import Flask, url_for
from flask import request
from flask import jsonify
from intuitlib.client import AuthClient
from intuitlib.enums import Scopes
from werkzeug.utils import redirect
from flask_caching import Cache
import requests
# from resources.get_auth_code import

config = {
    "DEBUG": True,
    "CACHE_TYPE": "simple",
    "CACHE_DEFAULT_TIMEOUT": 300
}


app = Flask(__name__)


app.config.from_mapping(config)
cache = Cache(app)


auth_client = AuthClient(
                client_id='ABxIxSlfNGyaR4AEMXyVwuHQxCa9QH0gKdwisMVj8zmMLIROJb',
                client_secret='QwzxqcRflJrvjofb96BUoAU0ITqbAxjuejTl5gV2',
                environment='sandbox',
                # redirect_uri='https://developer.intuit.com/v2/OAuth2Playground/RedirectUrl',
                redirect_uri='https://localhost:5000/callback',
            )


@app.route('/')
def hello_world():
    print(request)
    return 'Hello, World!'


@app.route('/getAuth', methods=['POST', 'GET'])
def get_auth():
    """
    Get Auth Code and realm Id using Auth URL at redirected URI
    :return:
    """
    try:
        # Prepare scopes
        scopes = [
            Scopes.ACCOUNTING,
        ]
        # Get authorization URL
        auth_url = auth_client.get_authorization_url(scopes)
        print(auth_url)
        return redirect(auth_url)
    except Exception as e:
        print(e)


@app.route('/callback', methods=['POST', 'GET'])
@cache.cached(timeout=300)
def callback():
    authCode = request.args.get('code')
    realmId = request.args.get('realmId')
    if authCode and realmId:
        cache.set("authCode", authCode) and cache.set("realmId", realmId)
    authCode = cache.get('authCode')
    realmId = cache.get('realmId')
    print(authCode, realmId)
    res = {'authCode': authCode, 'realmId': realmId}
    return jsonify(res)


@app.route('/getToken', methods=['POST', 'GET'])
@cache.cached(timeout=3600)
def get_token():
    authCode = cache.get('authCode')
    realmId = cache.get('realmId')
    print(authCode)
    print(realmId)
    auth_client.get_bearer_token(authCode, realm_id=realmId)
    access_token = auth_client.access_token
    refresh_token = auth_client.refresh_token
    if access_token and refresh_token is not None:
        cache.set('access_token', access_token)
        cache.set('refresh_token', refresh_token)
    res = {'access_token': access_token, 'refresh_token': refresh_token}
    return jsonify(res)


@app.route('/getCompanyInfo', methods=['POST', 'GET'])
def getCompanyInfo():
    realmId = cache.get('realmId')
    accessToken = cache.get('access_token')
    if realmId and accessToken is not None:
        base_url = 'https://sandbox-quickbooks.api.intuit.com'
        url = '{0}/v3/company/{1}/companyinfo/{1}'.format(base_url, realmId)
        auth_header = 'Bearer {0}'.format(accessToken)
        headers = {
            'Authorization': auth_header,
            'Accept': 'application/json'
        }
        response = requests.get(url, headers=headers)
        print(response.text)
        return jsonify(response.text)


if __name__ == '__main__':
    app.run(ssl_context='adhoc')