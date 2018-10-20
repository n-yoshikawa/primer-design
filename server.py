from flask import Flask, request, render_template, jsonify

#import dna_design
import clustering

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/api", methods=['POST'])
def hello():
    sequence_list = []
    for amino in request.json["sequences"].splitlines():
        sequence_list.append(amino)
    n = int(request.json["number"])
    #result_base, generated_aminos = dna_design.optimize(sequence_list, n)
    result_base, generated_aminos = clustering.design(sequence_list, n)
    
    results = []
    for base, amino in zip(result_base, generated_aminos):
        results.append({"base": base,
                        "amino": amino})
    data = {
        "results": results,
        "sequences": sequence_list
    }
    return jsonify(data)

class Unbuffered(object):
   def __init__(self, stream):
       self.stream = stream
   def write(self, data):
       self.stream.write(data)
       self.stream.flush()
   def writelines(self, datas):
       self.stream.writelines(datas)
       self.stream.flush()
   def __getattr__(self, attr):
       return getattr(self.stream, attr)

import sys
sys.stdout = Unbuffered(sys.stdout)

if __name__ == '__main__':
    app.run(debug=True)
