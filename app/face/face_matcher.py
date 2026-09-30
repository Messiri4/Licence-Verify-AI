from facenet_pytorch import InceptionResnetV1
import torch


device = torch.device("cpu")

resnet = InceptionResnetV1(
    pretrained="vggface2"
).eval().to(device)


def create_embedding(face_tensor):
    if face_tensor is None:
        return None

    face_tensor = (
        face_tensor
        .unsqueeze(0)
        .to(device)
    )

    with torch.no_grad():
        embedding = resnet(
            face_tensor
        )

    return embedding


def compare_embeddings(
    embedding1,
    embedding2
):
    similarity = (
        torch.nn.functional
        .cosine_similarity(
            embedding1,
            embedding2
        )
    )

    return float(
        similarity.item()
    )