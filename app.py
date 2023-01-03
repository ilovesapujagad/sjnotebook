import json
import os
import requests
import paramiko
from paramiko import SSHClient
from sys import stderr
from flask import Flask, request, jsonify,make_response

app = Flask(__name__)

api_key = os.environ.get("API_KEY", "")
if api_key == "":
    print("api key is required", file=stderr)

api_base_url = "https://api.stagingv3.microgen.id/query/api/v1/" + api_key

@app.route('/')
def hello_geek():
    return '<h1>Hello from Flask</h2>'

@app.post("/api/login")
def login():
    
    hostname = '10.10.65.3'
    port = 9995
    username = "centos"
    password = "qlwkejrh"
    userz = request.form.get('username')
    passz= request.form.get('password')
    usernamez= userz
    passwordz= passz
    
    command = "curl -i --data 'userName=%s&password=%s' -X POST http://10.10.65.3:9995/api/login" % (usernamez , passwordz)
    
    client = SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname, username=username, password=password)

#     command = "curl -i --data 'userName=admin&password=admin' -X POST http://10.207.26.22:9995/api/login"
    stdin, stdout, stderr = client.exec_command(command)
    # for line in stdout.readlines():
    #     print (line)
    z=stdout.read()
    # print(z)
    x = str(z)
    nu = x.find('Content-Type: application/json')
    g = int(nu)-162
    u = int(g)+47
    s = x[g:u]
    my_dict = {}
    my_dict['Set-Cookie']= s
    xs = make_response(my_dict)
    xs.headers["Set-Cookie"] = s
    client.close()
    return xs

@app.get("/api/list")
def cpu():
    source = str(request.args.get('JSESSIONID'))
    url = 'http://10.10.65.3:9995/api/notebook'
    cookies = {"JSESSIONID": source}
    r = requests.get(url, cookies=cookies)
    try:
        if r.status_code == 200:
            return r.json()
        else:
            return r.status_code(),401
    except Exception:
        return r.json(),401

@app.get("/api/notebook/<noteId>")
def cpus(noteId):
    sidnode = str(noteId)
    source = str(request.args.get('JSESSIONID'))
    url = 'http://10.10.65.3:9995/api/notebook/%s' % (sidnode)
    userz = request.form.get('username')
    cookies = {"JSESSIONID": source}
    r = requests.get(url, cookies=cookies)
    return r.json()

@app.post("/api/createnote")
def newnote():
    request_data = request.get_json()
    name = request_data['name']
    sudah = str(name)
    source = str(request.args.get('JSESSIONID'))
    url = 'http://10.10.65.3:9995/api/notebook'
    cookies = {"JSESSIONID": source}
    r = requests.post(url, cookies=cookies, json={"name": sudah})
    return r.json()

@app.route("/api/notebook/<id>", methods=["DELETE"])
def deletenote(id):
    sudah = str(id)
    source = str(request.args.get('JSESSIONID'))
    url = 'http://10.10.65.3:9995/api/notebook/%s' % (sudah)
    cookies = {"JSESSIONID": source}
    r = requests.delete(url, cookies=cookies)
    return r.json()

@app.post("/api/notebook/<noteid>/paragraph")
def newparagraph(noteid):
    request_data = request.get_json()
    title = request_data['title']
    text = request_data['text']
    snoteid = str(noteid)
    sudah = str(title)
    sudah2 = str(text)
    source = str(request.args.get('JSESSIONID'))
    url = 'http://10.10.65.3:9995/api/notebook/'+snoteid+'/paragraph'
    cookies = {"JSESSIONID": source}
    r = requests.post(url, cookies=cookies, json={"title": sudah,"text":sudah2 })
    return r.json()

@app.post("/api/notebook/run/<noteid>/<paragraphid>")
def runparagraph(noteid,paragraphid):
    snoteid = str(noteid)
    sparagraphId = str(paragraphid)
    source = str(request.args.get('JSESSIONID'))
    url = 'http://10.10.65.3:9995/api/notebook/run/'+snoteid+'/'+sparagraphId+''
    cookies = {"JSESSIONID": source}
    r = requests.post(url, cookies=cookies)
    return r.json()

@app.put("/api/notebook/<noteid>/rename")
def renameparagraph(noteid):
    request_data = request.get_json()
    name = request_data['name']
    sudah = str(name)
    snoteid = str(noteid)
    source = str(request.args.get('JSESSIONID'))
    url = 'http://10.10.65.3:9995/api/notebook'+snoteid+'/rename'
    cookies = {"JSESSIONID": source}
    r = requests.put(url, cookies=cookies, json={"name": sudah})
    return r.json()

@app.route("/api/notebook/<noteid>/paragraph/<paragraphid>", methods=["DELETE"])
def deleteparagraph(noteid,paragraphid):
    snoteid = str(noteid)
    sparagraphId = str(paragraphid)
    source = str(request.args.get('JSESSIONID'))
    url = 'http://10.10.65.3:9995/api/notebook/'+snoteid+'/paragraph/'+sparagraphId+''
    cookies = {"JSESSIONID": source}
    r = requests.delete(url, cookies=cookies)
    return r.json()

@app.post("/api/notebook/job/<noteid>")
def runallparagraph(noteid):
    snoteid = str(noteid)
    source = str(request.args.get('JSESSIONID'))
    url = 'http://10.10.65.3:9995/api/notebook/job/'+snoteid+''
    cookies = {"JSESSIONID": source}
    r = requests.post(url, cookies=cookies)
    return r.json()

@app.route("/api/notebook/<noteid>/paragraph/<paragraphid>", methods=["PUT"])
def updateparagraph(noteid,paragraphid):
    request_data = request.get_json()
    text = request_data['text']
    stext = str(text)
    snoteid = str(noteid)
    sparagraphId = str(paragraphid)
    source = str(request.args.get('JSESSIONID'))
    url = 'http://10.10.65.3:9995/api/notebook/'+snoteid+'/paragraph/'+sparagraphId+''
    cookies = {"JSESSIONID": source}
    r = requests.put(url, cookies=cookies, json={"text": stext})
    return r.json()

if __name__ == "__main__":
    app.run(debug=True)
