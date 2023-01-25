import json
import os
import requests
import paramiko
from paramiko import SSHClient
from sys import stderr
from flask import Flask, request, jsonify,make_response,Response
from websocket import create_connection
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
    username = "sapujagad"
    password = "kayangan"
    # userz = request.form.get('username')
    # passz= request.form.get('password')
    # usernamez= userz
    # passwordz= passz
    
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
    # xs = make_response(my_dict)
    # xs.headers["Set-Cookie"] = s
    client.close()
    return jsonify(my_dict)


@app.get("/api/list")
def listnotebookbyuser():
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
def infonotebook(noteId):
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
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    request_data = request.get_json()
    data = json.loads(request.data)
    snoteid = str(noteid)
    source = str(request.args.get('JSESSIONID'))
    url = 'http://10.10.65.3:9995/api/notebook/'+snoteid+'/paragraph'
    cookies = {"JSESSIONID": source}
    r = requests.post(url, cookies=cookies, json=data)
    return r.json()

@app.post("/api/notebook/run/<noteid>/<paragraphid>")
def runparagraph(noteid,paragraphid):
    snoteid = str(noteid)
    sparagraphId = str(paragraphid)
    source = str(request.args.get('JSESSIONID'))
    url = 'http://10.10.65.3:9995/api/notebook/run/'+snoteid+'/'+sparagraphId+''
    urlinfo = 'http://10.10.65.3:9995/api/notebook/'+snoteid+'/paragraph/'+sparagraphId+''
    cookies = {"JSESSIONID": source}
    r = requests.post(url, cookies=cookies)
    resinfo = requests.get(urlinfo, cookies=cookies)
    x = str(resinfo.json()['body']['text'])
    print(x[0:3])
    if x[0:3] == "%md":
        urls = 'http://10.10.65.3:9995/api/notebook/'+snoteid+'/paragraph/'+sparagraphId+'/config'
        z = requests.put(urls, cookies=cookies, json = {"editorHide": True})
        return r.json()
    else:
        return r.json()
    
def logins():
    url = "https://database-query.v3.microgen.id/api/v1/fb6db565-2e6c-41eb-bf0f-66f43b2b75ae/auth/login"
    email = "admin@sapujagad.id"
    password = "123123"
    form_data = {'email': email,'password': password}
    res = requests.post(url,json=form_data)
    return res.json()['token']

def getlogins(id):
    bearer_token = logins()
    url="https://database-query.v3.microgen.id/api/v1/fb6db565-2e6c-41eb-bf0f-66f43b2b75ae/ZeppelinUser/"+id+""
    res = requests.get(url,headers={"Authorization": "Bearer %s" %bearer_token})

    return res.json()

def loginticket(username,password):
    logins = {"userName":username,"password":password}
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    url = "http://10.10.65.3:9995/api/login"
    x = requests.post(url, data=logins, headers=headers)
    return x.json()["body"]["ticket"]


@app.put("/api/notebook/<noteid>/rename")
def renamenote(noteid):
    zzz = str(noteid)
    source = str(request.args.get('JSESSIONID'))
    request_data = request.get_json()
    sss = str(request_data['name'])
    idd = str(request_data['idzeppelin'])
    xx = getlogins(idd)
    ticket= loginticket(str(xx['username']),str(xx['password']))
    roles = str(xx['role'])
    username = str(xx['username'])
    try:
        ws = create_connection("ws://10.10.65.3:9995/ws")
        ws.send(json.dumps({ "op": "NOTE_RENAME", "data": { "id": zzz, "name": sss }, "principal": username, "ticket": ticket, "roles": f"[\"{roles}\"]" }))
        result =  ws.recv()
        print (result)
        ws.close()
        return jsonify({"msg": "Success rename notebook"}), 200
    except:
        return jsonify({"msg": "error rename notebook"}), 400
        return jsonify({"msg": "error rename notebook"}), 400

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

@app.get("/api/export/<noteid>")
def exportnote(noteid):
    source = str(request.args.get('JSESSIONID'))
    snoteid = str(noteid)
    url = 'http://10.10.65.3:9995/api/notebook/export/'+snoteid+''
    cookies = {"JSESSIONID": source}
    r = requests.post(url, cookies=cookies)
    x = r.json()
    allMovieData = json.loads(str(x["body"]).replace('\n', ''))
    my_dict = {}
    my_dict['Set-Cookie']= allMovieData
    return Response(json.dumps(allMovieData), 
        mimetype='application/json',
        headers={'Content-Disposition':'attachment;filename=zones.json'})

@app.post("/api/notebook/<noteid>/<paragraphid>/move/<index>")
def index(noteid,paragraphid,index):
    snoteid = str(noteid)
    sparagraphId = str(paragraphid)
    sindex = str(index)
    source = str(request.args.get('JSESSIONID'))
    cookies = {"JSESSIONID": source}
    urlindex = 'http://10.10.65.3:9995/api/notebook/'+snoteid+'/paragraph/'+sparagraphId+'/move/'+sindex+''
    index = requests.post(urlindex,cookies=cookies)
    return index.json()




if __name__ == "__main__":
    app.run(debug=True)
