# Import the necessary libraries
import pandas as pd
import numpy as np
from PIL import Image
import torch
from torchvision import models
import torchvision.transforms as transforms
from sklearn.decomposition import PCA

def reduce_features(features):
    # Load the features from the CSV file into a Pandas DataFrame
    df = pd.read_csv("static/data/features_densenet_test.csv")

    # Load the dataset of images and obtain their features using the model
    image_features = []
    for i in range(len(df)):
        features = df.iloc[i, 1]
        features = np.array([float(x) for x in features[1:-1].split(",")])
        image_features.append(features)

    # Perform dimensionality reduction on the list of image features using PCA
    pca = PCA(n_components=128)
    reduced_features = pca.fit_transform(image_features)
    return reduced_features

# Define the query image and its features
def get_image_features(image):
    image = Image.open(image)

    # Convert the image to a PyTorch tensor
    image = transforms.ToTensor()(image)

    # resize the image to 224x224
    image = transforms.Resize((224, 224))(image)

    # Add a batch dimension to the image
    image = image.unsqueeze(0)

    # Set the device to use for PyTorch
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Load the pre-trained PyTorch model
    model = models.densenet121(pretrained=True)

    # Set the model to evaluation mode
    model.eval()

    # Move the model to the specified device
    model = model.to(device)

    # Move the image to the specified device
    image = image.to(device)

    # Obtain its features using the model
    query_features = model.features(image)

    # Convert the features to a NumPy array
    query_features = query_features.detach().cpu().numpy()
    
    return query_features[0]

def get_closest_images(query_image, df_image, reduced_features, nb_closest=50):
    query_features = get_image_features(query_image)
    # reshape to 2 dim
    query_features = query_features.reshape(1, -1)
    pca = PCA(n_components=128)
    query_features_reduced = pca.transform(query_features)

    # Compare the query features to the reduced features and return the most similar images
    similarity_scores = []
    for features in reduced_features:
        similarity = torch.nn.functional.cosine_similarity(torch.Tensor(query_features_reduced), torch.Tensor(features))
        similarity_scores.append(similarity)

    # Sort the similarity scores in descending order
    similarity_scores = np.array(similarity_scores)
    sorted_indices = np.argsort(similarity_scores)[::-1]

    # Get the top nb_closest most similar images
    most_similar_images = []
    for i in range(nb_closest):
        image_name = df_image.iloc[sorted_indices[i], 0]
        most_similar_images.append(image_name)

    return most_similar_images

def run(query_image):
    df_image = pd.read_csv("static/data/features_densenet_test.csv")
    reduced_features = reduce_features(df_image)
    closest_images = get_closest_images(query_image, df_image, reduced_features)
    return closest_images


if __name__ == "__main__":
    run()
