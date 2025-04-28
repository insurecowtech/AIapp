import os

# Define the directories and files
structure = {
    "data/raw": [],
    "data/processed": [],
    "models/animal_classifier": [],
    "notebooks": [],
    "src": ["__init__.py"],
    "src/data": ["video_processor.py", "frame_extractor.py"],
    "src/models": ["classifier.py", "voting.py"],
    "src/app": ["interface.py"],
    "tests": ["test_video_processor.py", "test_frame_extractor.py", "test_classifier.py"],
    "configs": ["config.yaml"],
}

# Create the directories and files
for folder, files in structure.items():
    os.makedirs(folder, exist_ok=True)
    for file in files:
        filepath = os.path.join(folder, file)
        with open(filepath, 'w') as f:
            f.write("")  # Create an empty file

# Create additional files in the root directory
root_files = ["README.md", "requirements.txt", ".gitignore"]
for file in root_files:
    with open(file, 'w') as f:
        f.write("")  # Create empty files

print("Complete directory structure with placeholder files created!")
