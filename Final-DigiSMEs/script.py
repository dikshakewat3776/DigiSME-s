import requests

url = "https://sandbox-quickbooks.api.intuit.com/v3/company/4620816365156031990/customer?minorversion=14"

payload = "{\n    \"BillAddr\": {\n        \"Line1\": \"123 Main Street\",\n        \"City\": \"Mountain View\",\n        \"Country\": \"USA\",\n        \"CountrySubDivisionCode\": \"CA\",\n        \"PostalCode\": \"94042\"\n    },\n    \"Notes\": \"Here are other details.\",\n    \"DisplayName\": \"Groceries123\",\n    \"PrimaryPhone\": {\n        \"FreeFormNumber\": \"(555) 555-5555\"\n    },\n    \"PrimaryEmailAddr\": {\n        \"Address\": \"jdrew@myemail.com\"\n    }\n}\n"
headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': 'Bearer eyJlbmMiOiJBMTI4Q0JDLUhTMjU2IiwiYWxnIjoiZGlyIn0..XAJOR2fSlUEEAWG8BbN2wQ.fCpdASrrCzfUPl0pgh_H-M1F6SKmQ3QHs5sh8lHI07cEjK1hmH5KkNSssS_7f3PeG0ijImSmar5-Wv4jbmGQGLDjZNA0WW24jHX9pyZAgjI5gNKR6ipaRExKYgOefR-n8g8bQghuRSgCQq7YFWOA53nAUq_7iW0-YKS8M1mrRlz6h8HGg-KqEir6ukBvBRt0qd7_aSpYnJzvJzQV2RqFGwopGMJKy8DZ_kV_av-tWyiJ_syGlVjanqz1pyhOHKJaD2y07cNA5ig93iy_aOMv8sM8gex5j0OQ_lamRGy5wta370VgXbXeE2eOsadcc4j1ZPe8X2POjOjTvAqZv4-qeoLRmuL61IRU15czE2AuCGa1aIo9my70S9ISBQhNvv9N_q8pC660DNn5lRYnQoIFt9be23MCx7kVGn_H7DHOzUHINwb40oSNquPR5GWKt80KDimZwsMbUBtCBZBpnnpHDQiFz94D1d85zd__mLlY0F0FzBVbGQQJYltBNN1625ZubODU462GuNaHJYpmb87uN4oJP0uxFgi4aX9JZbBxc3u3-59DY5PmS9PEmSrhZB4Of6ASHv20oe2WUjVq1mmw9sYr_5uS4Jb7OnwJilDqtMmwFuKLuDcrFVqsUj3T1AIx7KlnX43_hG5W4iTQ1UoGkx6SrYYgtFg_NJFROfZAopHgCFxSScCgVmr0VMGaUAlPLPRBgcJiZj86YBN_Ml5RTShccK2KN9IGXh5jtEbIz8Y.QJ9T-s3iiPZUdvWkSW4a1Q',

}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)