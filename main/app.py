from flask import Flask, render_template, request, jsonify
from home import HOME
from morph import MORPH
from threshold import THRESHOLD
from transform import TRANSFORM

app = Flask(__name__)

@app.route('/', methods=["POST", "GET"])
def main_app():
    return render_template('index.html')

@app.route("/home", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        req_data = request.get_json()  # Renamed variable to avoid conflicts
        securityKey = req_data.get("securityKey")
       
        
        body = req_data.get("body")
        subtype = body.get("subtype")
        
        data = body.get("data")
        param = body.get("param")
                                  
        if securityKey == "app_ender":
            
            if subtype == "histo":
                    
                result = HOME(data, param).histo()
                    
                return jsonify(result)
            
            if subtype == "canny":
                    
                result = HOME(data, param).canny()
                    
                return jsonify(result)
            
            if subtype == "pseudo":
                    
                result = HOME(data, param).pseudo_color_mapping()
                    
                return jsonify(result)
            
            
@app.route("/morph", methods=["POST", "GET"])
def morph():
    if request.method == "POST":
        req_data = request.get_json()
        securityKey = req_data.get("securityKey")
        
        body = req_data.get("body")
        subtype = body.get("subtype")
        
        data = body.get("data")
        param = body.get("param")
                                  
        if securityKey == "app_ender":
            
            if subtype == "dilation":
                result = MORPH(data, param).dilation()
                return jsonify(result)
            
            if subtype == "erosion":
                result = MORPH(data, param).erosion()
                return jsonify(result)
            
            if subtype == "opening":
                result = MORPH(data, param).opening()
                return jsonify(result)
            
            if subtype == "closing":
                result = MORPH(data, param).closing()
                return jsonify(result)
            
@app.route("/segment", methods=["POST", "GET"])
def segment():
    if request.method == "POST":
        req_data = request.get_json()
        securityKey = req_data.get("securityKey")
        
        body = req_data.get("body")
       
        data = body.get("data")
        param = body.get("param")
                                  
        if securityKey == "app_ender":
            
            result = THRESHOLD(data, param).seg()
            return jsonify(result)
            
        
@app.route("/transform", methods=["POST", "GET"])
def trans():
    if request.method == "POST":
        req_data = request.get_json()
        securityKey = req_data.get("securityKey")
        
        body = req_data.get("body")
        subtype = body.get("subtype")
        
        data = body.get("data")
        param = body.get("param")
                                  
        if securityKey == "app_ender":
            
            
            
            if subtype == "fourier":
                result = TRANSFORM(data, param).fourier()
                return jsonify(result)
            
        
           
            
                       
            
    

if __name__ == "__main__":
    app.run(port=8000)
