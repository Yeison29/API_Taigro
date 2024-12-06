import torch
import torchvision.models as models
import torch.nn as nn
from PIL import Image
import torchvision.transforms as transforms
import matplotlib.pyplot as plt

# Definir el dispositivo
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Usando dispositivo: {device}")

devices = ['Alternaria', 'Mildiu', 'Sana', 'Tizon', 'Virus_Enrrollamiento_Hoja_ Amarilla', 'Virus_Mosaico']

# Definir la arquitectura del modelo
model = models.efficientnet_b7(pretrained=False)
num_ftrs = model.classifier[1].in_features
model.classifier[1] = nn.Linear(num_ftrs, 11)  # Cambia '11' por el número de clases
model = model.to(device)

# Cargar los pesos
PATH = r"C:\Users\YDASC\Documents\TAIGRO\acc0.991496772871632.pt"  # Reemplaza con tu archivo
model.load_state_dict(torch.load(PATH, map_location=device))
model.eval()
print(f"Pesos cargados desde {PATH} y modelo en modo evaluación.")

# Definir las transformaciones
transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(256),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225]),
])

# Cargar y preprocesar la imagen
imagen_path = r"C:\Users\YDASC\Downloads\s.png"  # Reemplaza con tu imagen
imagen = Image.open(imagen_path).convert('RGB')
imagen_t = transform(imagen).unsqueeze(0).to(device)

# Realizar la inferencia
with torch.no_grad():
    outputs = model(imagen_t)
    probabilidades = torch.nn.functional.softmax(outputs[0], dim=0)

# Convertir las probabilidades a CPU y numpy
probabilidades = probabilidades.cpu().numpy()

for index, pro in enumerate(probabilidades):
    print(f"{devices[index]}: {pro * 100:.2f}%")
