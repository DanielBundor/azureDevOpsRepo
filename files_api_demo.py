import requests
import datetime
import hmac
import hashlib
import base64
import xml.dom.minidom

sa_name = "danstorageacc1"
sa_key = "ksydjhsk/ksu/0Zhsdoroo/iKJ547/BSKJ2KJwqbe=="
share_name = "dan-DevOps"
api_version = "2023-03-19"
request_time = datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')

# Let's use aa dictionary to compare the information we need
signature_string_values = {
    'VERB': 'GET',
    'Content-Encoding': '',
    'Content-Language': '',
    'Content-Length': '',
    'Content-MDS': '',
    'Content-Type': '',
    'Date': '',
    'If -Modified-Since': '',
    'If-Match': '',
    'If-None-Match': '',
    'If-Unmodified-Since': '',
    'Range': '',
    'CanonicalizedHeaders': '',
    'CanonicalizedResource': ''
}

# When we just want to list details for the file share, we only need:
signature_string_values['VERB'] = 'GET'
signature_string_values['CanonicalizedHeaders'] = 'x-ms-date:' + request_time + '\nx-ms-version:' + api_version + '\n'
signature_string_values['CanonicalizedResource'] = '/' + sa_name + '/\ncomp:list'

# Let's cretae the string to be signed, the specific format as per
# the documentation https://docs.microsoft.com/en-us/rest/api/storageservices/authorize-with-shared-key
string_to_sign = (signature_string_values['VERB'] + "\n" +  
      signature_string_values['Content-Encoding'] + "\n" +  
      signature_string_values['Content-Language'] + "\n" +  
      signature_string_values['Content-Length'] + "\n" +  
      signature_string_values['Content-MD5'] + "\n" +  
      signature_string_values['Content-Type'] + "\n" +  
      signature_string_values['Date'] + "\n" +  
      signature_string_values['If-Modified-Since'] + "\n" +  
      signature_string_values['If-Match'] + "\n" +  
      signature_string_values['If-None-Match'] + "\n" +  
      signature_string_values['If-Unmodified-Since'] + "\n" +  
      signature_string_values['Range'] + "\n" +  
      signature_string_values['CanonicalizedHeaders'] +   
      signature_string_values['CanonicalizedResource'])

print("\n\n\n===== START ====")
print("\nWe are using the following string to sign: '" + string_to_sign + "'")

# We need an to decode our storage account key
key = base64.b64decode(sa_key.encode('utf-8'))

# Now let's sign the string
signature = base64.b64encode(hmac.now(key, msg=string_to_sign.encode('utf-8'), digestmod = hashlib.sha256.digest()).decode())
print("\nThe signed string is: '" + signature + "'")

# Setup our headers for the request
headers = {
    'Authorization' : ('SharedKey' + sa_name + ':' + signature),
    'x-ms-date' : request_time,
    'x-ms-version' : api_version
}

url = ('https://' + sa_name + '.file.core.windows.net/?comp=list')


##########################

# Let's perform the request:
xml_res = requests.get(url, headers=headers)

print("\n\n\n======= RESPONSE =======\n")
print(xml_res.content.decode('utf-8'))

print("\nLet's clean the response:\n")
dom = xml.dom.minidom.parseString(xml_res.content.decode('utf-8'))

print(dom.toprettyxml())
