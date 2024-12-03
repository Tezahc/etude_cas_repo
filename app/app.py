from flask import Flask, render_template,request
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    return render_template('index.html')

@app.route('/model', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        # Récupérer les données du formulaire
        img = request.files.get('img')
        prompt = request.form.get('Prompt')
        if not img or img.filename == '':
            return "Aucun fichier reçu ou fichier non valide", 400  # Vérifiez que le fichier est présent


        image_path = os.path.join(app.config['UPLOAD_FOLDER'], img.filename)
        img.save(image_path)
        return render_template('model.html', image_url=image_path,  prompt=prompt)
    # Traiter les données
    return render_template('model.html')



if __name__ == "__main__":
    app.run(debug=True)