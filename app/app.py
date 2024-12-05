import os
import requests
import base64
from flask import Flask, render_template, request, Response
from flask_sqlalchemy import SQLAlchemy


# gestion / init du modèle ollama
def init_ollama():
    params = {
        "model": "llava-llama3" # llava machin
    }
    url = "http://ollama:11434/api/pull"
    rep = requests.post(url, json=params)

def send_prompt(prompt):
    params = {
        "model": "llava-llama3",
        "prompt": "Père castor écris moi une histoire :"+prompt,
        "stream": False
    }
    url = "http://ollama:11434/api/generate"
    rep = requests.post(url, json=params)
    return rep.json().get("response")

init_ollama()

# Création de l'app flask
app = Flask(__name__)

# Gestion / init de la db
app.config.from_object('config.Config')
db = SQLAlchemy(app)

class Story(db.Model):
    __tablename__ = 'upload'
    id = db.Column(db.Integer, primary_key=True)
    #img_path = db.Column(db.Text)#, unique=True, nullable=False)
    filename = db.Column(db.String(50), nullable=False)
    mimetype = db.Column(db.String(50), nullable=False)
    prompt = db.Column(db.Text)
    story = db.Column(db.Text)

with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template('index.html')

@app.route("/about")
def about():
    return render_template('about.html')

# Fabrice
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/model', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        # Récupérer les données du formulaire
        img = request.files['img']
        # encoded_string = base64.b64encode(img.read())
        mimetype = img.mimetype
        prompt = request.form.get('Prompt')
        story = send_prompt(prompt)

        if not img or img.filename == '':
            return "Aucun fichier reçu ou fichier non valide", 400  # Vérifiez que le fichier est présent

        # enregistrer l'image "localement"
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], img.filename)
        img.save(image_path)

        input = Story(
            #img = '',#, encoded_string,
            filename = img.filename,
            mimetype = mimetype,
            prompt = prompt,
            story = story
        )

        db.session.add(input)
        db.session.commit()

        return render_template('model.html', image_url=image_path,  histoire=story)
    # Traiter les données
    return render_template('model.html')


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")

