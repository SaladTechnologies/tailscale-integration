import os
import uuid
import socket
from flask import Flask, request
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

count_hc = 0
count_prediction = 0
salad_machine_id = os.getenv("SALAD_MACHINE_ID", "LOCAL")

@app.route('/')
def main():
    client_ip = request.remote_addr
    host_ip = request.host.split(":")[0]  
    local_ip = socket.gethostbyname(socket.gethostname()) 
    temp = {"SOURCE_IP": client_ip, "HTTP HOST": host_ip, "LOCAL_IP": local_ip}
    print(temp)
    return temp

@app.route('/hc')
def health():
    global count_hc
    count_hc += 1
    temp = f'salad_machine_id:{salad_machine_id}, hc:{count_hc}, prediction:{count_prediction}'
    print(temp)
    return {"STATUS": temp}

@app.route('/prediction', methods=['GET', 'POST'])
def hello_world():
    global count_prediction
    count_prediction += 1

    if request.method == "GET":
        temp = f'salad_machine_id:{salad_machine_id}, hc:{count_hc}, prediction:{count_prediction}'
    else:
        job_id = request.form.get('job_id')
        temp = f'job_id:{job_id}, salad_machine_id:{salad_machine_id}, hc:{count_hc}, prediction:{count_prediction}'

    print(temp)
    return temp

if __name__ == '__main__':
    # app.run(host="0.0.0.0", port=8888)
    app.run(host="::", port=8888) # Dual Stack: IPv4/v6