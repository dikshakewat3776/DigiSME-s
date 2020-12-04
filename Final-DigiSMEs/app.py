from flask import Flask, url_for,render_template, flash
from flask import request,Response
from flask import jsonify
from intuitlib.client import AuthClient
from intuitlib.enums import Scopes
from werkzeug.utils import redirect, secure_filename
from flask_caching import Cache
import json
from constants import *
from geopy.distance import geodesic
import os
import requests


config = {
    "DEBUG": True,
    "CACHE_TYPE": "simple",
    "CACHE_DEFAULT_TIMEOUT": 300
}

app = Flask(__name__)

app.config.from_mapping(config)
cache = Cache(app)
app.secret_key = "digiSMESkey"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
path = os.getcwd()
UPLOAD_FOLDER = os.path.join(path, 'uploads')
if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'mp4']

auth_client = AuthClient(
                client_id='ABxIxSlfNGyaR4AEMXyVwuHQxCa9QH0gKdwisMVj8zmMLIROJb',
                client_secret='QwzxqcRflJrvjofb96BUoAU0ITqbAxjuejTl5gV2',
                environment='sandbox',
                # redirect_uri='https://developer.intuit.com/v2/OAuth2Playground/RedirectUrl',
                redirect_uri='https://localhost:5000/callback',
            )

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def hello_world():
    return render_template("RetailerRegister.html")

@app.route('/getAuth', methods=['POST', 'GET'])
def get_auth():
    """
    Get Auth Code and realm Id using Auth URL at redirected URI
    :return:
    """
    try:
        # Prepare scopes
        scopes = [
            # Scopes.INTUIT_NAME,
            Scopes.ACCOUNTING,
            # Scopes.PAYMENT,
            # Scopes.PAYROLL,
            # Scopes.PAYROLL_TIMETRACKING,
            # Scopes.PAYROLL_BENEFITS,
            # Scopes.PAYROLL_TIMETRACKING,
            # Scopes.PAYSLIP_READ
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




# # Loading the lat-long data for Kolkata & Delhi
# kolkata = (22.5726, 88.3639)
# delhi = (28.7041, 77.1025)
#
# # Print the distance calculated in km
# print(geodesic(kolkata, delhi).km)

@app.route('/Searchproduct',methods=["POST","GET"])
def Searchproduct():
    if request.method == "POST":
        matched_product = []
        keyword = request.form["keyword"]
        for companyName in  TECHNOTOUCH_PRODUCT:
            productdetail = companyName.get("ProductPriceDetails")[0]
            address = companyName.get("Address")
            if companyName.get("companyName") == keyword:
                return render_template("")
            else:
                for product in productdetail:
                    if json.loads(product).get("name") == keyword:
                        dist = (geodesic(USER_lOCATION,(address.get("lat"),address.get("long"))).km)
                        companyName["dist"] = dist
                        matched_product.append(companyName)
        matched_product.sort()
        return jsonify(matched_product)







class apiRequirement:
    realmId = "4620816365156031990"
    accessToken = "eyJlbmMiOiJBMTI4Q0JDLUhTMjU2IiwiYWxnIjoiZGlyIn0..zEugCcMagR13DvYZyk_Irw.vRUJmLT6cjBuUWvjv4Tk6cuiQBHz0HjqSfl3kjvjnmoEKJw1371knmKr945Xzub6H-y4AQex6kqGLFhKeZVFM6auQLoOGQpsvbzbGi-bV9tOXm5tnAjvM4pLuYV8R2qvQUnSqEoBM_sfysJW_B6QZKSaJhhbp8V6KX84s8lOxY0f5NBqwNiKXMinxOu2mkdoDpAp0ZRUprM4lV_L1A51oQaaYgP3CAdGkdn2Y_fWG7cgasB1pUkOaIL04kxsyqifq1AsIqhy106wDuXvwZTB_pBzA2wmZLvuLr7mQC7p91EWlS8iuUs7yHTBIwOm2BfkToemGn09Pq1QbSe7oeLxQkXbpAdYj1YssNkmGa-wildJlt4abgVG_GJZ-h1oFP1pH9QvaPiqYktSpn8XdfciwvJyBUKbttkKMSPcTvdzLZ26GK_5keU4xvwm41MVn-ntjYlFlnKD_xOMP72JtPQpPGSmM6IC9c82Uy7YbNJmRoWw2xB80_pzbicvWzL35Z2TuRfyzoIEsGJOBc_JPep99hU1VMzOxvfqkhf0sdNr-eI-zTKwsfVPq2-PF_69JwA6cghW9UQPjRf9g__n2jFIKJKMfIuSdrpu7VwO5VmBQS8aq70sNTPB4muZmPYF0NlsVW7Wc3ZddAu3S7mW6__sPD9wE5vrW2LM3FICRMNAQ-44IDoWHnCtEdCXkZmKgEM835y505EcArwZOFJoImokAlq-g-mWqivQAs5bFYliA2U.2m_UQB2Op84QQrEjjCmmOA"
    auth_header = 'Bearer {0}'.format(accessToken)
    headers = {
        'Authorization': auth_header,
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }




class Retailer(apiRequirement):
    @app.route('/registerRetailer',methods=["POST","GET"])
    def registerRetailer():
        if request.method == "POST":
            try:
                payload = {
                "PrimaryEmailAddr": {
                    "Address":request.form["email"]
                },
                "DisplayName": request.form["displayName"],
                "Suffix": request.form["Suffix"],
                "Title": request.form["Title"],
                "FamilyName": request.form["displayName"],
                "PrimaryPhone": {
                    "FreeFormNumber": request.form["mobile"]
                },
                "CompanyName": request.form["companyName"],
                "BillAddr": {
                    "City": request.form["City"],
                    "PostalCode": request.form["Zip"],
                    "Line1": request.form["Address"],
                    "Country": request.form["Country"],
                },
                "GivenName": request.form["displayName"]
            }
                payload = json.dumps(payload)
                response_createCust = requests.post(url=CREATECUST_API.format(apiRequirement.realmId),headers=apiRequirement.headers,data=payload)
                response = json.loads(response_createCust.text)
                print(response)
                if response_createCust.status_code == 200:
                    return render_template('RetailerRegister.html',message ="Company is successfully Registered")
                else :
                    if response["Fault"].get("Error"):
                        Error_res = response["Fault"].get("Error")[0]
                        if Error_res.get("Message") == "Duplicate Name Exists Error":
                            return render_template('RetailerRegister.html',message="Display is already Taken")
                    return render_template('RetailerRegister.html',message="Check the Entered Detail and try again")
            except Exception as e:
                return jsonify(e)
        elif request.method == "GET":
            return render_template("RetailerRegister.html")

    @app.route('/LoginRetailer', methods=["POST","GET"])
    def LoginRetailer():
        if request.method == "POST":
            if request.form["email"] == "laxmiDiksha@technotouch.com" and request.form["password"] == "TechnoTouch":
                return render_template("RetailerDashboard.html")
            else:
                return render_template("RetailerRegister.html",message = "User and Password is not correct")
        if request.method == "GET":
            return render_template("Login.html")


    @app.route("/productListDisplay",methods=["GET"])
    def productListDisplay():
        if request.method == "GET":
            # return render_template("ProductListDashboard.html",CompanyName=TECHNOTOUCH_PRODUCT["CompanyName"],productDetail=TECHNOTOUCH_PRODUCT["ProductPriceDetails"])
            return render_template("ProductListDashboard.html",context =TECHNOTOUCH_PRODUCT)


@app.route('/uploadFile/<int:retailerId>', methods=['POST'])
def upload_file(retailerId):
    if request.method == 'POST':
        if 'files[]' not in request.files:
            flash('No file part')
            return redirect(request.url)

        files = request.files.getlist('files[]')
        print(files)

        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(str(retailerId) + '_' + file.filename)
                print(filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        flash('File(s) successfully uploaded')
        return redirect('/uploadFile/{}'.format(retailerId), retailerId)

if __name__ == '__main__':
    app.run(ssl_context='adhoc')