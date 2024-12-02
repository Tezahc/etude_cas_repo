from flask import Flask, render_template,request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    return render_template('index.html')

# @app.route("/model",methods=['GET', 'POST'])
# def about():
#     return render_template('model.html')

@app.route('/model', methods=['GET', 'POST'])
def submit():
    # Récupérer les données du formulaire
    img = request.form.get('img')
    prompt = request.form.get('Prompt')
    
    # Traiter les données
    return render_template('model.html', prompt=prompt)

if __name__ == "__main__":
    app.run(debug=True)