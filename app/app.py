from flask import Flask, render_template, request, Response
from config import app, db, api

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/about")
def about():
    return render_template('about.html')

class Upload(db.Model):
    _tablename_ = 'upload'

    id = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.Text, unique=True, nullable=False)
    filename = db.Column(db.String(50), nullable=False)
    mimetype = db.Column(db.Text, nullable=False)

@app.route('/model', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        file = request.files['files']

        if not file:
            return ({"error: No image uploaded"}, 400)
    
    mimetype = file.mimetype
    upload = Upload(img=file.read(), filename=file.filename, mimetype=mimetype)
    db.session.add(upload)
    db.session.commit()

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

