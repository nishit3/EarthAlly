import base64
from io import BytesIO
from PIL import Image
import torch
import torch.nn as nn
from PIL import Image
import torchvision.transforms as transforms
from flask import request, jsonify, Flask
from flask_cors import CORS
from flask_ngrok import run_with_ngrok

app = Flask(__name__)
run_with_ngrok(app)
CORS(app, resources={r"/api/*": {"origins": "*"}})

def remove_bottom_20_pixels(b64_string):
    image_data = base64.b64decode(b64_string)
    image = Image.open(BytesIO(image_data)).convert('RGB')
    width, height = image.size
    new_height = height - 20
    cropped_image = image.crop((0, 0, width, new_height))
    return cropped_image
    

class CustomClassifier(nn.Module):
    def __init__(self, in_features, num_classes=2):
        super(CustomClassifier, self).__init__()
        self.fc1_1=nn.Linear(in_features=in_features, out_features=num_classes)

    def forward(self, x):
        x = self.fc1_1(x)
        return x 


class garbageClassifier(nn.Module):
    def __init__(self, in_features, num_classes=8):
        super(garbageClassifier, self).__init__()
        self.fc1_1=nn.Linear(in_features=448, out_features=num_classes)

    def forward(self, x):
        x = self.fc1_1(x)
        return x   


preprocess = transforms.Compose([
        transforms.Resize((128,128)),  
        transforms.ToTensor(),          
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])  
    ])
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


@app.route("/detectWildFire", methods=["POST"])
def detectWildFire():
    base64EncodedString = request.get_json()["b64EncodedImgString"]
    model = torch.load(r'wildfire_detector.pth')
    model.eval()
    image = remove_bottom_20_pixels(base64EncodedString)
    input_tensor = preprocess(image)
    input_batch = input_tensor.unsqueeze(0)
    model = model.to(device)
    input_batch = input_batch.to(device)
    model.eval()
    with torch.no_grad():
        output = model(input_batch)
    probabilities = torch.nn.functional.softmax(output[0], dim=0)
    _, predicted_class = torch.max(probabilities, 0)
    class_names = ['no_wildfire','wildfire']  
    predicted_label = class_names[predicted_class]
    return jsonify({"prediction": predicted_label}), 200


@app.route("/detectDeforestation", methods=["POST"])
def detectDeforestation():
    base64EncodedString = request.get_json()["b64EncodedImgString"]
    model = torch.load(r'deforestation_detector.pth')
    model.eval()
    image = remove_bottom_20_pixels(base64EncodedString)
    input_tensor = preprocess(image)
    input_batch = input_tensor.unsqueeze(0)
    model = model.to(device)
    input_batch = input_batch.to(device)
    model.eval()
    with torch.no_grad():
        output = model(input_batch)
    probabilities = torch.nn.functional.softmax(output[0], dim=0)
    _, predicted_class = torch.max(probabilities, 0)
    class_names = ['tags_agriculture artisinal_mine bare_ground clear primary road',
    'tags_agriculture artisinal_mine bare_ground clear primary road water',
    'tags_agriculture artisinal_mine clear conventional_mine cultivation habitation primary road water',
    'tags_agriculture artisinal_mine clear cultivation habitation primary road water',
    'tags_agriculture artisinal_mine clear cultivation habitation primary water',
    'tags_agriculture artisinal_mine clear cultivation primary',
    'tags_agriculture artisinal_mine clear cultivation primary road water',
    'tags_agriculture artisinal_mine clear cultivation primary water',
    'tags_agriculture artisinal_mine clear habitation primary road water',
    'tags_agriculture artisinal_mine clear habitation road water',
    'tags_agriculture artisinal_mine clear primary',
    'tags_agriculture artisinal_mine clear primary road',
    'tags_agriculture artisinal_mine clear primary road water',
    'tags_agriculture artisinal_mine clear primary selective_logging water',
    'tags_agriculture artisinal_mine clear primary water',
    'tags_agriculture artisinal_mine clear road water',
    'tags_agriculture artisinal_mine partly_cloudy primary water',
    'tags_agriculture bare_ground blooming cultivation partly_cloudy primary selective_logging',
    'tags_agriculture bare_ground clear',
    'tags_agriculture bare_ground clear conventional_mine habitation primary road',
    'tags_agriculture bare_ground clear conventional_mine habitation primary road water',
    'tags_agriculture bare_ground clear conventional_mine habitation road',
    'tags_agriculture bare_ground clear cultivation habitation primary',
    'tags_agriculture bare_ground clear cultivation habitation primary road',
    'tags_agriculture bare_ground clear cultivation habitation primary road selective_logging',
    'tags_agriculture bare_ground clear cultivation habitation primary road water',
    'tags_agriculture bare_ground clear cultivation habitation primary water',
    'tags_agriculture bare_ground clear cultivation primary',
    'tags_agriculture bare_ground clear cultivation primary road',
    'tags_agriculture bare_ground clear cultivation primary road water',
    'tags_agriculture bare_ground clear cultivation primary selective_logging water',
    'tags_agriculture bare_ground clear cultivation primary slash_burn',
    'tags_agriculture bare_ground clear cultivation primary water',
    'tags_agriculture bare_ground clear cultivation road',
    'tags_agriculture bare_ground clear habitation',
    'tags_agriculture bare_ground clear habitation primary',
    'tags_agriculture bare_ground clear habitation primary road',
    'tags_agriculture bare_ground clear habitation primary road slash_burn',
    'tags_agriculture bare_ground clear habitation primary road water',
    'tags_agriculture bare_ground clear habitation primary water',
    'tags_agriculture bare_ground clear habitation road',
    'tags_agriculture bare_ground clear primary',
    'tags_agriculture bare_ground clear primary road',
    'tags_agriculture bare_ground clear primary road water',
    'tags_agriculture bare_ground clear primary water',
    'tags_agriculture bare_ground clear road',
    'tags_agriculture bare_ground clear water',
    'tags_agriculture bare_ground cultivation haze primary water',
    'tags_agriculture bare_ground habitation haze primary road',
    'tags_agriculture bare_ground habitation partly_cloudy primary',
    'tags_agriculture bare_ground habitation partly_cloudy primary road',
    'tags_agriculture bare_ground haze',
    'tags_agriculture bare_ground haze primary',
    'tags_agriculture bare_ground haze primary road',
    'tags_agriculture bare_ground haze primary water',
    'tags_agriculture bare_ground partly_cloudy primary',
    'tags_agriculture bare_ground partly_cloudy primary road',
    'tags_agriculture bare_ground partly_cloudy primary water',
    'tags_agriculture bare_ground partly_cloudy road',
    'tags_agriculture blooming blow_down clear cultivation primary',
    'tags_agriculture blooming clear cultivation habitation primary',
    'tags_agriculture blooming clear cultivation primary',
    'tags_agriculture blooming clear cultivation primary road',
    'tags_agriculture blooming clear cultivation primary selective_logging',
    'tags_agriculture blooming clear cultivation primary slash_burn',
    'tags_agriculture blooming clear cultivation primary water',
    'tags_agriculture blooming clear habitation primary road',
    'tags_agriculture blooming clear primary',
    'tags_agriculture blooming clear primary road',
    'tags_agriculture blooming clear primary road water',
    'tags_agriculture blooming cultivation haze primary',
    'tags_agriculture blooming cultivation partly_cloudy primary selective_logging',
    'tags_agriculture blow_down clear cultivation primary',
    'tags_agriculture blow_down clear habitation primary',
    'tags_agriculture blow_down clear primary',
    'tags_agriculture blow_down partly_cloudy primary',
    'tags_agriculture blow_down partly_cloudy primary blow_down',
    'tags_agriculture clear',
    'tags_agriculture clear conventional_mine cultivation habitation primary',
    'tags_agriculture clear conventional_mine cultivation habitation primary road',
    'tags_agriculture clear conventional_mine habitation primary road',
    'tags_agriculture clear conventional_mine habitation road',
    'tags_agriculture clear conventional_mine primary road',
    'tags_agriculture clear conventional_mine primary road water',
    'tags_agriculture clear conventional_mine primary water',
    'tags_agriculture clear cultivation',
    'tags_agriculture clear cultivation cultivation habitation primary',
    'tags_agriculture clear cultivation cultivation habitation primary road',
    'tags_agriculture clear cultivation cultivation habitation primary road slash_burn',
    'tags_agriculture clear cultivation cultivation habitation primary road slash_burn water',
    'tags_agriculture clear cultivation cultivation habitation primary road water',
    'tags_agriculture clear cultivation cultivation habitation primary water',
    'tags_agriculture clear cultivation cultivation habitation road water',
    'tags_agriculture clear cultivation cultivation primary',
    'tags_agriculture clear cultivation cultivation primary road',
    'tags_agriculture clear cultivation cultivation primary road water',
    'tags_agriculture clear cultivation cultivation primary slash_burn',
    'tags_agriculture clear cultivation cultivation primary water',
    'tags_agriculture clear cultivation cultivation road',
    'tags_agriculture clear cultivation habitation primary',
    'tags_agriculture clear cultivation habitation primary conventional_mine',
    'tags_agriculture clear cultivation habitation primary road',
    'tags_agriculture clear cultivation habitation primary road selective_logging',
    'tags_agriculture clear cultivation habitation primary road slash_burn',
    'tags_agriculture clear cultivation habitation primary road slash_burn water',
    'tags_agriculture clear cultivation habitation primary road water',
    'tags_agriculture clear cultivation habitation primary selective_logging',
    'tags_agriculture clear cultivation habitation primary slash_burn',
    'tags_agriculture clear cultivation habitation primary water',
    'tags_agriculture clear cultivation habitation road',
    'tags_agriculture clear cultivation primary',
    'tags_agriculture clear cultivation primary blooming',
    'tags_agriculture clear cultivation primary blow_down',
    'tags_agriculture clear cultivation primary road',
    'tags_agriculture clear cultivation primary road selective_logging',
    'tags_agriculture clear cultivation primary road selective_logging slash_burn water',
    'tags_agriculture clear cultivation primary road slash_burn',
    'tags_agriculture clear cultivation primary road water',
    'tags_agriculture clear cultivation primary selective_logging',
    'tags_agriculture clear cultivation primary selective_logging water',
    'tags_agriculture clear cultivation primary slash_burn',
    'tags_agriculture clear cultivation primary slash_burn water',
    'tags_agriculture clear cultivation primary water',
    'tags_agriculture clear cultivation road',
    'tags_agriculture clear cultivation road water',
    'tags_agriculture clear cultivation water',
    'tags_agriculture clear habitation',
    'tags_agriculture clear habitation primary',
    'tags_agriculture clear habitation primary road',
    'tags_agriculture clear habitation primary road blow_down',
    'tags_agriculture clear habitation primary road selective_logging',
    'tags_agriculture clear habitation primary road selective_logging water',
    'tags_agriculture clear habitation primary road slash_burn',
    'tags_agriculture clear habitation primary road water',
    'tags_agriculture clear habitation primary road water conventional_mine',
    'tags_agriculture clear habitation primary slash_burn',
    'tags_agriculture clear habitation primary slash_burn water',
    'tags_agriculture clear habitation primary water',
    'tags_agriculture clear habitation road',
    'tags_agriculture clear habitation road water',
    'tags_agriculture clear primary',
    'tags_agriculture clear primary blow_down',
    'tags_agriculture clear primary conventional_mine',
    'tags_agriculture clear primary road',
    'tags_agriculture clear primary road conventional_mine',
    'tags_agriculture clear primary road selective_logging',
    'tags_agriculture clear primary road slash_burn',
    'tags_agriculture clear primary road slash_burn water',
    'tags_agriculture clear primary road water',
    'tags_agriculture clear primary road water conventional_mine',
    'tags_agriculture clear primary selective_logging',
    'tags_agriculture clear primary slash_burn',
    'tags_agriculture clear primary slash_burn water',
    'tags_agriculture clear primary water',
    'tags_agriculture clear primary water conventional_mine',
    'tags_agriculture clear road',
    'tags_agriculture clear road water',
    'tags_agriculture clear water',
    'tags_agriculture conventional_mine habitation partly_cloudy primary road',
    'tags_agriculture conventional_mine partly_cloudy primary',
    'tags_agriculture cultivation cultivation habitation partly_cloudy primary road',
    'tags_agriculture cultivation cultivation habitation partly_cloudy primary road water',
    'tags_agriculture cultivation cultivation haze primary road',
    'tags_agriculture cultivation cultivation partly_cloudy primary',
    'tags_agriculture cultivation cultivation partly_cloudy primary road',
    'tags_agriculture cultivation cultivation partly_cloudy primary water',
    'tags_agriculture cultivation habitation haze primary',
    'tags_agriculture cultivation habitation haze primary road',
    'tags_agriculture cultivation habitation haze primary road water',
    'tags_agriculture cultivation habitation haze primary water',
    'tags_agriculture cultivation habitation partly_cloudy primary',
    'tags_agriculture cultivation habitation partly_cloudy primary road',
    'tags_agriculture cultivation habitation partly_cloudy primary road water',
    'tags_agriculture cultivation habitation partly_cloudy primary slash_burn',
    'tags_agriculture cultivation habitation partly_cloudy primary water',
    'tags_agriculture cultivation haze primary',
    'tags_agriculture cultivation haze primary road',
    'tags_agriculture cultivation haze primary road water',
    'tags_agriculture cultivation haze primary water',
    'tags_agriculture cultivation partly_cloudy',
    'tags_agriculture cultivation partly_cloudy primary',
    'tags_agriculture cultivation partly_cloudy primary road',
    'tags_agriculture cultivation partly_cloudy primary road selective_logging',
    'tags_agriculture cultivation partly_cloudy primary road water',
    'tags_agriculture cultivation partly_cloudy primary selective_logging',
    'tags_agriculture cultivation partly_cloudy primary slash_burn',
    'tags_agriculture cultivation partly_cloudy primary water',
    'tags_agriculture habitation haze primary',
    'tags_agriculture habitation haze primary road',
    'tags_agriculture habitation haze primary road water',
    'tags_agriculture habitation haze primary water',
    'tags_agriculture habitation haze road',
    'tags_agriculture habitation partly_cloudy primary',
    'tags_agriculture habitation partly_cloudy primary road',
    'tags_agriculture habitation partly_cloudy primary road water',
    'tags_agriculture habitation partly_cloudy primary road water conventional_mine',
    'tags_agriculture habitation partly_cloudy primary water',
    'tags_agriculture habitation partly_cloudy road',
    'tags_agriculture haze',
    'tags_agriculture haze primary',
    'tags_agriculture haze primary road',
    'tags_agriculture haze primary road selective_logging',
    'tags_agriculture haze primary road water',
    'tags_agriculture haze primary water',
    'tags_agriculture haze road',
    'tags_agriculture haze water',
    'tags_agriculture partly_cloudy',
    'tags_agriculture partly_cloudy primary',
    'tags_agriculture partly_cloudy primary blow_down',
    'tags_agriculture partly_cloudy primary road',
    'tags_agriculture partly_cloudy primary road conventional_mine',
    'tags_agriculture partly_cloudy primary road selective_logging',
    'tags_agriculture partly_cloudy primary road slash_burn',
    'tags_agriculture partly_cloudy primary road water',
    'tags_agriculture partly_cloudy primary selective_logging',
    'tags_agriculture partly_cloudy primary slash_burn',
    'tags_agriculture partly_cloudy primary water',
    'tags_agriculture partly_cloudy road',
    'tags_agriculture partly_cloudy road water',
    'tags_agriculture partly_cloudy water',
    'tags_artisinal_mine bare_ground clear cultivation primary water',
    'tags_artisinal_mine bare_ground clear habitation primary road water',
    'tags_artisinal_mine bare_ground clear habitation road',
    'tags_artisinal_mine bare_ground clear primary',
    'tags_artisinal_mine bare_ground clear primary road',
    'tags_artisinal_mine bare_ground clear primary road water',
    'tags_artisinal_mine bare_ground clear primary selective_logging water',
    'tags_artisinal_mine bare_ground clear primary water',
    'tags_artisinal_mine bare_ground clear road water',
    'tags_artisinal_mine bare_ground clear water',
    'tags_artisinal_mine bare_ground partly_cloudy primary road',
    'tags_artisinal_mine bare_ground partly_cloudy primary road water',
    'tags_artisinal_mine bare_ground partly_cloudy primary water',
    'tags_artisinal_mine clear conventional_mine habitation primary road water',
    'tags_artisinal_mine clear conventional_mine primary road water',
    'tags_artisinal_mine clear cultivation primary road water',
    'tags_artisinal_mine clear cultivation primary water',
    'tags_artisinal_mine clear habitation primary road',
    'tags_artisinal_mine clear habitation primary road water',
    'tags_artisinal_mine clear habitation primary water',
    'tags_artisinal_mine clear primary',
    'tags_artisinal_mine clear primary road',
    'tags_artisinal_mine clear primary road selective_logging water',
    'tags_artisinal_mine clear primary road water',
    'tags_artisinal_mine clear primary selective_logging',
    'tags_artisinal_mine clear primary selective_logging water',
    'tags_artisinal_mine clear primary water',
    'tags_artisinal_mine clear road water',
    'tags_artisinal_mine clear water',
    'tags_artisinal_mine habitation partly_cloudy primary road water',
    'tags_artisinal_mine haze primary',
    'tags_artisinal_mine haze primary water',
    'tags_artisinal_mine partly_cloudy primary',
    'tags_artisinal_mine partly_cloudy primary road',
    'tags_artisinal_mine partly_cloudy primary road water',
    'tags_artisinal_mine partly_cloudy primary water',
    'tags_artisinal_mine partly_cloudy water',
    'tags_bare_ground blooming clear cultivation primary',
    'tags_bare_ground blow_down clear primary',
    'tags_bare_ground blow_down clear primary slash_burn',
    'tags_bare_ground clear',
    'tags_bare_ground clear conventional_mine habitation primary road',
    'tags_bare_ground clear conventional_mine habitation primary road water',
    'tags_bare_ground clear conventional_mine primary road',
    'tags_bare_ground clear cultivation habitation primary',
    'tags_bare_ground clear cultivation habitation primary road',
    'tags_bare_ground clear cultivation habitation primary road water',
    'tags_bare_ground clear cultivation habitation primary water',
    'tags_bare_ground clear cultivation primary',
    'tags_bare_ground clear cultivation primary road',
    'tags_bare_ground clear cultivation primary road selective_logging',
    'tags_bare_ground clear cultivation primary road water',
    'tags_bare_ground clear cultivation primary water',
    'tags_bare_ground clear habitation',
    'tags_bare_ground clear habitation primary',
    'tags_bare_ground clear habitation primary road',
    'tags_bare_ground clear habitation primary road water',
    'tags_bare_ground clear habitation primary selective_logging',
    'tags_bare_ground clear habitation primary water',
    'tags_bare_ground clear habitation road',
    'tags_bare_ground clear habitation road water',
    'tags_bare_ground clear primary',
    'tags_bare_ground clear primary road',
    'tags_bare_ground clear primary road selective_logging',
    'tags_bare_ground clear primary road water',
    'tags_bare_ground clear primary selective_logging slash_burn water',
    'tags_bare_ground clear primary selective_logging water',
    'tags_bare_ground clear primary slash_burn',
    'tags_bare_ground clear primary slash_burn water',
    'tags_bare_ground clear primary water',
    'tags_bare_ground clear road',
    'tags_bare_ground clear road water',
    'tags_bare_ground clear water',
    'tags_bare_ground conventional_mine partly_cloudy primary road',
    'tags_bare_ground cultivation habitation partly_cloudy primary',
    'tags_bare_ground cultivation haze primary',
    'tags_bare_ground cultivation partly_cloudy primary',
    'tags_bare_ground cultivation partly_cloudy primary road',
    'tags_bare_ground cultivation partly_cloudy primary selective_logging',
    'tags_bare_ground habitation haze primary road',
    'tags_bare_ground habitation haze primary water',
    'tags_bare_ground habitation partly_cloudy primary',
    'tags_bare_ground habitation partly_cloudy primary road',
    'tags_bare_ground haze',
    'tags_bare_ground haze primary',
    'tags_bare_ground haze primary water',
    'tags_bare_ground partly_cloudy',
    'tags_bare_ground partly_cloudy primary',
    'tags_bare_ground partly_cloudy primary road',
    'tags_bare_ground partly_cloudy primary slash_burn',
    'tags_bare_ground partly_cloudy primary water',
    'tags_blooming clear cultivation habitation primary slash_burn',
    'tags_blooming clear cultivation primary',
    'tags_blooming clear primary',
    'tags_blooming clear primary road',
    'tags_blooming clear primary selective_logging',
    'tags_blooming clear primary water',
    'tags_blooming cultivation partly_cloudy primary water',
    'tags_blooming haze primary',
    'tags_blooming partly_cloudy primary',
    'tags_blooming partly_cloudy primary selective_logging',
    'tags_blow_down clear cultivation habitation primary',
    'tags_blow_down clear cultivation primary',
    'tags_blow_down clear primary',
    'tags_blow_down clear primary blow_down',
    'tags_blow_down clear primary road',
    'tags_blow_down clear primary selective_logging',
    'tags_blow_down clear primary slash_burn',
    'tags_blow_down clear primary water',
    'tags_blow_down partly_cloudy primary',
    'tags_blow_down partly_cloudy primary water',
    'tags_clear bare_ground',
    'tags_clear conventional_mine habitation primary',
    'tags_clear conventional_mine habitation primary road',
    'tags_clear conventional_mine habitation primary road water',
    'tags_clear conventional_mine habitation road',
    'tags_clear conventional_mine primary',
    'tags_clear conventional_mine primary road',
    'tags_clear conventional_mine primary road water',
    'tags_clear conventional_mine primary water',
    'tags_clear cultivation habitation primary',
    'tags_clear cultivation habitation primary road',
    'tags_clear cultivation habitation primary road slash_burn',
    'tags_clear cultivation habitation primary road water',
    'tags_clear cultivation habitation primary selective_logging',
    'tags_clear cultivation habitation primary slash_burn',
    'tags_clear cultivation habitation primary slash_burn water',
    'tags_clear cultivation habitation primary water',
    'tags_clear cultivation primary',
    'tags_clear cultivation primary road',
    'tags_clear cultivation primary road selective_logging',
    'tags_clear cultivation primary road slash_burn',
    'tags_clear cultivation primary road water',
    'tags_clear cultivation primary selective_logging',
    'tags_clear cultivation primary selective_logging water',
    'tags_clear cultivation primary slash_burn',
    'tags_clear cultivation primary slash_burn water',
    'tags_clear cultivation primary water',
    'tags_clear habitation primary',
    'tags_clear habitation primary blooming',
    'tags_clear habitation primary road',
    'tags_clear habitation primary road selective_logging',
    'tags_clear habitation primary road water',
    'tags_clear habitation primary selective_logging',
    'tags_clear habitation primary slash_burn',
    'tags_clear habitation primary water',
    'tags_clear habitation road',
    'tags_clear habitation road water',
    'tags_clear habitation water',
    'tags_clear primary',
    'tags_clear primary blooming',
    'tags_clear primary blow_down',
    'tags_clear primary road',
    'tags_clear primary road blooming',
    'tags_clear primary road selective_logging',
    'tags_clear primary road selective_logging water',
    'tags_clear primary road water',
    'tags_clear primary road water conventional_mine',
    'tags_clear primary selective_logging',
    'tags_clear primary selective_logging water',
    'tags_clear primary slash_burn',
    'tags_clear primary slash_burn water',
    'tags_clear primary water',
    'tags_clear road',
    'tags_clear road water',
    'tags_clear water',
    'tags_cloudy',
    'tags_conventional_mine habitation partly_cloudy primary road',
    'tags_conventional_mine habitation partly_cloudy primary road water',
    'tags_conventional_mine haze primary',
    'tags_conventional_mine haze primary road',
    'tags_conventional_mine partly_cloudy',
    'tags_conventional_mine partly_cloudy primary',
    'tags_conventional_mine partly_cloudy primary road',
    'tags_conventional_mine partly_cloudy primary road water',
    'tags_cultivation habitation haze primary',
    'tags_cultivation habitation haze primary road water',
    'tags_cultivation habitation haze primary water',
    'tags_cultivation habitation partly_cloudy primary',
    'tags_cultivation habitation partly_cloudy primary road',
    'tags_cultivation habitation partly_cloudy primary road water',
    'tags_cultivation habitation partly_cloudy primary slash_burn',
    'tags_cultivation haze primary',
    'tags_cultivation haze primary road',
    'tags_cultivation haze primary slash_burn',
    'tags_cultivation haze primary water',
    'tags_cultivation partly_cloudy primary',
    'tags_cultivation partly_cloudy primary road',
    'tags_cultivation partly_cloudy primary selective_logging',
    'tags_cultivation partly_cloudy primary slash_burn',
    'tags_cultivation partly_cloudy primary water',
    'tags_habitation haze primary',
    'tags_habitation haze primary road',
    'tags_habitation haze primary road water',
    'tags_habitation haze primary slash_burn',
    'tags_habitation haze primary water',
    'tags_habitation haze water',
    'tags_habitation partly_cloudy primary',
    'tags_habitation partly_cloudy primary road',
    'tags_habitation partly_cloudy primary road water',
    'tags_habitation partly_cloudy primary water',
    'tags_habitation partly_cloudy road',
    'tags_haze primary',
    'tags_haze primary blooming',
    'tags_haze primary road',
    'tags_haze primary road selective_logging',
    'tags_haze primary road selective_logging water',
    'tags_haze primary road water',
    'tags_haze primary selective_logging',
    'tags_haze primary water',
    'tags_haze road water',
    'tags_haze water',
    'tags_partly_cloudy',
    'tags_partly_cloudy primary',
    'tags_partly_cloudy primary agriculture water',
    'tags_partly_cloudy primary blooming',
    'tags_partly_cloudy primary blow_down',
    'tags_partly_cloudy primary road',
    'tags_partly_cloudy primary road selective_logging',
    'tags_partly_cloudy primary road selective_logging water',
    'tags_partly_cloudy primary road water',
    'tags_partly_cloudy primary road water conventional_mine',
    'tags_partly_cloudy primary selective_logging',
    'tags_partly_cloudy primary selective_logging water',
    'tags_partly_cloudy primary slash_burn',
    'tags_partly_cloudy primary water',
    'tags_partly_cloudy road water',
    'tags_partly_cloudy water',
    'tags_water']  
    habi = 0.0
    for i in class_names:
        if "habitation" in i:
            ind = class_names.index(i)
            habi = habi + float(probabilities[ind].item())
    return jsonify({"prediction": habi*100}), 200


@app.route("/detectGarbage", methods=["POST"])
def detectGarbage():
    base64EncodedString = request.get_json()["b64EncodedImgString"]
    model = torch.load(r'garbage_detector.pth')
    model.eval()
    image = remove_bottom_20_pixels(base64EncodedString)
    preprocess = transforms.Compose([
    transforms.Resize((224,224)),  
    transforms.ToTensor(),          
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]) 
    ])
    input_tensor = preprocess(image)
    input_batch = input_tensor.unsqueeze(0)
    model = model.to(device)
    input_batch = input_batch.to(device)
    model.eval()
    with torch.no_grad():
        output = model(input_batch)
    output = output.logits
    probabilities = torch.nn.functional.softmax(output, dim=1)
    print(probabilities)
    _, predicted_class_tensor = torch.max(probabilities, dim=1)
    predicted_class = predicted_class_tensor.item()
    class_names = ["Cardboard waste","Clean Road","Dirty Roads", "Glass waste", "Metal waste", "Paper waste", "Plastic waste", "Garbage"]
    predicted_label = class_names[predicted_class]
    return jsonify({"prediction": predicted_label}), 200
    

if __name__ == "__main__":
    app.run()
