from flask import Flask, request, jsonify
import productionFlaskStuff.getQueryInfo as queryStuff
app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "Hello, Flask!", "status": "success"})

@app.route('/query')
def getStuff():
    text = request.args.get("text", "Nebula Labs")
    return queryStuff.getQueryResults(text)
    #return jsonify({"message": text, "status": "success"})

if __name__ == '__main__':
    app.run(debug=True)


