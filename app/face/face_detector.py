from facenet_pytorch import MTCNN
from PIL import Image
import torch


device = torch.device("cpu")

mtcnn = MTCNN(
    image_size=160,
    margin=20,
    keep_all=False,
    device=device
)


def extract_face_from_image(image_path):
    image = Image.open(image_path).convert("RGB")

    face = mtcnn(image)

    if face is None:
        return None

    return face