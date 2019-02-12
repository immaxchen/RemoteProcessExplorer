from flask import Flask, request, send_from_directory
import pythoncom, win32ts, wmi, json, urllib, subprocess

app = Flask(__name__)

@app.route('/RemoteProcessExplorer')
def index():
    return send_from_directory('.', 'RemoteProcessExplorer.html')

@app.route('/RemoteProcessExplorer/user')
def list_user():
    pythoncom.CoInitialize()
    data = {}
    for session in win32ts.WTSEnumerateSessions(win32ts.WTS_CURRENT_SERVER_HANDLE):
        sid = session['SessionId']
        data[sid] = win32ts.WTSQuerySessionInformation(None, sid, win32ts.WTSUserName)
    return json.dumps(data)

@app.route('/RemoteProcessExplorer/list')
def list_process():
    pythoncom.CoInitialize()
    data = []
    for process in wmi.WMI().Win32_Process():
        data.append([process.Name, process.SessionId, process.ProcessId])
    return json.dumps(data)

@app.route('/RemoteProcessExplorer/kill/<pid>')
def kill_process(pid):
    pythoncom.CoInitialize()
    process = wmi.WMI().Win32_Process(ProcessId=int(pid))[0]
    process.Terminate()
    return "0"

@app.route('/RemoteProcessExplorer/open/<cmd>')
def open_process(cmd):
    pythoncom.CoInitialize()
    full_cmd = urllib.parse.unquote_plus(cmd)
    process = subprocess.Popen(full_cmd, creationflags=subprocess.CREATE_NEW_CONSOLE)
    return "0"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
