import os
from flask import Flask, render_template, request, Response
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_object('config.Config')
db = SQLAlchemy(app)
print(app.config)

class Story(db.Model):
    _tablename_ = 'upload'
    id = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.Text, unique=True, nullable=False)
    filename = db.Column(db.String(50), nullable=False)
    mimetype = db.Column(db.String(50), nullable=False)
    prompt = db.Column(db.Text)

app.config['UPLOAD_FOLDER'] = 'static/uploads/'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# @app.before_first_request()
def create_tables():
    db.create_all()

with app.app_context():
    create_tables()

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/about")
def about():
    return render_template('about.html')

# Fabrice
@app.route('/model', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        # Récupérer les données du formulaire
        img = request.files['img']
        mimetype = img.mimetype
        prompt = request.form.get('Prompt')

        if not img or img.filename == '':
            return "Aucun fichier reçu ou fichier non valide", 400  # Vérifiez que le fichier est présent

        # enregistrer l'image "localement"
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], img.filename)
        img.save(image_path)

        story = Story(
            img = '',
            filename = img.filename,
            mimetype = mimetype,
            prompt = prompt
        )

        db.session.add(story)
        db.session.commit()

        return render_template('model.html', image_url=image_path,  prompt=prompt)
    # Traiter les données
    return render_template('model.html')


if __name__ == "__main__":
    app.run(debug=True)

