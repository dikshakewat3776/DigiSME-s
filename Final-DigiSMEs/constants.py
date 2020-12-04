BASE_URL = 'https://sandbox-quickbooks.api.intuit.com'
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
        "price": "30"
    },
{
    "name": "carrot",
    "price": "30"
},
{
    "name": "carrot",
    "price": "30"
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
