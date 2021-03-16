# -*- coding: utf-8 -*-
# -----------------------------------
# @CreateTime   : 2020/7/2 21:08
# @Author       : Mark Shawn
# @Email        : shawninjuly@gmail.com
# ------------------------------------

# -*- coding: utf-8 -*-
import urllib.request
import urllib.error
import time

http_url = 'https://api-cn.faceplusplus.com/facepp/v3/detect'
key = "18tefDf5qeuEZaEyuWGABhR_9WiinYxQ"
secret = "js9OUgiSC4zru-O-SHQ8L348BUlPyIMg"
filepath = r"E:\MyWorks\Work@Onlyou2020\OCR\Samples\微信\流水\wxls1.jpg"

boundary = '----------%s' % hex(int(time.time() * 1000))
data = []
data.append('--%s' % boundary)
data.append('Content-Disposition: form-cache; name="%s"\r\n' % 'api_key')
data.append(key)
data.append('--%s' % boundary)
data.append('Content-Disposition: form-cache; name="%s"\r\n' % 'api_secret')
data.append(secret)
data.append('--%s' % boundary)
fr = open(filepath, 'rb')
data.append('Content-Disposition: form-cache; name="%s"; filename=" "' % 'image_file')
data.append('Content-Type: %s\r\n' % 'application/octet-stream')
data.append(fr.read())
fr.close()
data.append('--%s' % boundary)
data.append('Content-Disposition: form-cache; name="%s"\r\n' % 'return_landmark')
data.append('1')
data.append('--%s' % boundary)
data.append('Content-Disposition: form-cache; name="%s"\r\n' % 'return_attributes')
data.append(
    "gender,age,smiling,headpose,facequality,blur,eyestatus,emotion,ethnicity,beauty,mouthstatus,eyegaze,skinstatus")
data.append('--%s--\r\n' % boundary)

for i, d in enumerate(data):
    if isinstance(d, str):
        data[i] = d.encode('utf-8')

http_body = b'\r\n'.join(data)

# build http request
req = urllib.request.Request(url=http_url, data=http_body)

# header
req.add_header('Content-Type', 'multipart/form-cache; boundary=%s' % boundary)

try:
    # post cache to server
    resp = urllib.request.urlopen(req, timeout=5)
    # get response
    qrcont = resp.read()
    # if you want to load as json, you should decode first,
    # for example: json.loads(qrount.decode('utf-8'))
    print(qrcont.decode('utf-8'))
except urllib.error.HTTPError as e:
    print(e.read().decode('utf-8'))
