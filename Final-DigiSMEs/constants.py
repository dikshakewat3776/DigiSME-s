BASE_URL = 'https://sandbox-quickbooks.api.intuit.com'
ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'mp4']
config = {
    "DEBUG": True,
    "CACHE_TYPE": "simple",
    "CACHE_DEFAULT_TIMEOUT": 300
}
# Customer creation Api
CREATECUST_REQUEST = """ {
        "PrimaryEmailAddr": {
            "Address": "{}"
        },
        "DisplayName": "{}",
        "Suffix": "{}",
        "Title": "{}",
        "FamilyName": "{}",
        "PrimaryPhone": {
            "FreeFormNumber": "{}"
        },
        "CompanyName": "{}",
        "BillAddr": {
            "City": "{}",
            "PostalCode": "{}",
            "Line1": "{}",
            "Country": "{}"
        },
        "GivenName": "{}"
    }"""


CREATECUST_API = BASE_URL + "/v3/company/{}/customer?minorversion=14"


#Mock Poduct Data
TECHNOTOUCH_PRODUCT = [
    {
    "CompanyName": "TechnoTouch",
"ProductPriceDetails": [
    {
        "name": "carrot",
        "price": "15"
    },
{
    "name": "cauliflower",
    "price": "32"
},
{
    "name": "cabagge",
    "price": "25"
},
{
    "name": "tomatoes",
    "price": "23"
},
{
    "name": "bitter gourd",
    "price": "23"
},
{
    "name": "bottle gournd",
    "price": "23"
},
{
    "name": "egg Plant",
    "price": "23"
},
{
    "name": "spinach",
    "price": "23"
},
{
    "name": "apple",
    "price": "230"
},
],
"Address": {
        "lat":22.5726,
        "long":88.3639
}
    },
{
    "CompanyName": "Raju Bhaji",
"ProductPriceDetails": [
    {
        "name": "carrot",
        "price": "35"
    },
{
    "name": "Tomatoes",
    "price": "92"
},
{
    "name": "raddish",
    "price": "64"
},
],
"Address": {
        "lat":22.5726,
        "long":88.3639
}
}
    ]


USER_lOCATION = (11.435,34.578)


# item Api

CREATEITEM_API = BASE_URL + "/v3/company/{}/item"


# payment Api

PAYMENT_API = BASE_URL + "/v3/company/{}/payment"