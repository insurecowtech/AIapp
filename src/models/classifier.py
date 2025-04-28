from speciesnet import SpeciesNet, DEFAULT_MODEL
from speciesnet.utils import prepare_instances_dict

model = SpeciesNet(model_name=DEFAULT_MODEL)

def predict_image(image_path):
    # Prepare the instances dictionary with the image path
    instances_dict = prepare_instances_dict(filepaths=[image_path])

    # Initialize the SpeciesNet model with the default model
    

    # Run prediction
    predictions = model.classify(filepaths=[image_path])

    # Extract the prediction for the image
    prediction = predictions['predictions'][0]
    classes = prediction['classifications']['classes']
    # scores = prediction['classifications']['scores']

    # Get the top prediction
    top_class = classes[0]
    # top_score = scores[0]

    # Extract the common name from the classification string
    common_name = top_class.split(';')[-1]

    return common_name  #, top_score

# image_path = '/Users/fahimafridi/Downloads/Insurecow App/data/processed/frame_740.jpg'
# label, confidence = classify_animal_image(image_path)
# print(f"Predicted Animal: {label} (Confidence: {confidence:.2%})")
