# Required packages: huggingface_hub, git (if not installed already)

import os
import subprocess
from tqdm import tqdm
from huggingface_hub import HfApi, ModelFilter

# Check for required packages
required_packages = ["huggingface_hub", "git", "tqdm"]
missing_packages = []
for package in required_packages:
    try:
        __import__(package)
    except ImportError:
        missing_packages.append(package)

if missing_packages:
    print(f"The following packages are required but not installed: {', '.join(missing_packages)}\n")
    print("You can install them using conda with the following command:")
    print(f"conda install {' '.join(missing_packages)}\n")
    print("Or using pip with the following command:")
    print(f"pip install {' '.join(missing_packages)}\n")
    exit(1)

# Set destination directory
destination_dir = "SET YOUR DESTINATION DIRECTORY HERE"

# Set root Git URL
root_git_url = "https://huggingface.co/"

# Create destination directory if it doesn't exist
if not os.path.exists(destination_dir):
    os.makedirs(destination_dir)

# Set up Hugging Face API and filter for models
hf_api = HfApi()
models = hf_api.list_models(filter=ModelFilter(author="sd-concepts-library"))

# Sort models by likes
models_sorted = sorted(models, key=lambda m: m.likes, reverse=True)

# Download or update models
print("Downloading/updating models...")
for model in tqdm(models_sorted[:100]):
    model_dir_name = model.id.split("/")[-1]  # Get the model directory name from the model ID
    model_dir = os.path.join(destination_dir, model_dir_name)
    git_url = root_git_url + model.id

    if os.path.exists(model_dir):
        # Model already exists, check if it's up to date
        git_status_output = subprocess.check_output(["git", "status"], cwd=model_dir).decode()
        if "Your branch is up to date" in git_status_output:
            tqdm.write(f"✓ Up to date: {model.id}")
            continue

        # Model is not up to date, do a Git pull to update it
        subprocess.run(["git", "pull", "--recurse-submodules"], cwd=model_dir)
        tqdm.write(f"✓ Updated: {model.id}")
    else:
        # Model doesn't exist, do a Git clone to download it
        subprocess.run(["git", "clone", "--recurse-submodules", git_url], cwd=destination_dir)
        tqdm.write(f"✓ Downloaded: {model.id}")

print("Finished downloading/updating models.")
