from flask import Flask, render_template, send_from_directory
import os
import subprocess

# Check for required packages
required_packages = ['flask']
for package in required_packages:
    try:
        __import__(package)
    except ImportError:
        subprocess.check_call(['pip', 'install', package])

app = Flask(__name__)
embeddings_dir = "CHANGE THIS HERE TO WHERE YOUR EMBEDDINGS DIR IS"
@app.route('/')
def index():
    models = os.listdir(embeddings_dir)
    models_info = []
    for model in models:
        model_dir = os.path.join(embeddings_dir, model)
        try:
            with open(os.path.join(model_dir, "token_identifier.txt"), "r") as f:
                token = f.readline().strip()
        except FileNotFoundError:
            token = f"N/A"
        try:
            with open(os.path.join(model_dir, "type_of_concept.txt"), "r") as f:
                concept_type = f.readline().strip()
        except FileNotFoundError:
            concept_type = f"N/A"
        images_dir = os.path.join(model_dir, "concept_images")
        if os.path.exists(images_dir):
            image_files = [f for f in os.listdir(images_dir) if f.endswith((".jpg", ".jpeg", ".png"))]
            image_previews = [os.path.join(model, "concept_images", image_file) for image_file in image_files]
            if image_previews:
                image_preview = image_previews[0]
            else:
                image_preview = None
        else:
            image_files = [f for f in os.listdir(model_dir) if f.endswith((".jpg", ".jpeg", ".png"))]
            if image_files:
                image_previews = [os.path.join(model, image_file) for image_file in image_files]
                image_preview = os.path.join(model, image_files[0])
            else:
                image_previews = []
                image_preview = None
        models_info.append({"name": model, "token": token, "type": concept_type, "previews": image_previews, "preview": image_preview})
    return render_template("index.html", models=models_info)

@app.route('/images/<path:path>')
def send_image(path):
    return send_from_directory(embeddings_dir, path.replace("\\", "/"))

if __name__ == '__main__':
    app.run(host='0.0.0.0')
