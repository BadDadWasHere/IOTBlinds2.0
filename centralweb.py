import requests
from flask import Flask, render_template, request, redirect, send_from_directory

app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
#loads html

def index():
    if request.method == "GET":  #if the webconsole gets a Get command, "refresh the website"
        print("webconsole rendered")

        if len(logText) > 10:
            logText.pop(0)

        return render_template("index.html", ipaddress=ipaddrs,
                               log=logText)  #rendter the website
    else:  #POST
        form_dir = request.form.get("Direction")
        form_dev = request.form.get("Device")
        if (form_dir.lower() == "up" or form_dir.lower() == "down"
                or form_dir.lower() == "stop"):
            if form_dev == "All":
                sendCommand(form_dir)
                logText.append("Sent all " + form_dir.lower())
                print("sent direction to all ipaddress")
            elif form_dev in ipaddrs:
                logText.append("Sent " + form_dev.lower() + " " +
                               form_dir.lower())
                try:
                    requests.get("http://" + form_dev.lower() + "/" +
                                 form_dir.lower())
                except:
                    print("Couldn't Connect")
        else:
            print("invalid form_dir")
        return redirect("/")  #prints out what comes out after /(up, down stop)


@app.route('/myStyles.css')
def myStyleCSS():
    print("loading CSS")
    return send_from_directory("static", "myStyles.css")


ipaddrs = []
print("created ipaddrs list")
logText = []

print("logText string is created") 

def loadConfig(
    configfilename
):  #puts all ipaddrs in config.yaml into the list, contains file name
    import yaml  #import yaml library
    data_loaded = {}  #creates data load dictionary
    print("data loaded dictionary created")
    with open(configfilename, "r") as file:  #opens config file
        data_loaded = yaml.safe_load(
            file)  #load the entire file into data loaded
        print("data_loaded get yaml")
    global ipaddrs  #load ipaddrs into loadConfig
    ipaddrs = data_loaded.get(
        "ipaddrs"
    )  #extracted the the ipaddrs from data_loaded, stores it into ipaddrs
    print("ipaddrs get ipaddrs from data_loaded")


#sends requests.get to all the websites with the ipaddrs ip addresses
def sendCommand(cmdstring):
    cmdstring = cmdstring.lower(
    )  #no matter what the string is, it will always be lowercase

    if (cmdstring == "up" or cmdstring == "down" or cmdstring
            == "stop"):  #only runs if it cmdstring is up down stop||
        try:
            for i in ipaddrs:  #this will run through every ip address, change print to get
                requests.get("http://" + i + "/" +
                             cmdstring)  #sends get requests to each ip address
                print("send get command to " + i + " with " + cmdstring)
        except:  #if it doesnt connect, it will control the error and print Couldn't Connect
            print("Couldn't Connect")


#actually creates a playc where the script can run
if __name__ == "__main__":
    loadConfig("config.yaml")  #run loadConfig
    app.run(host='0.0.0.0', port=5000, debug=True)  #runs the python script
