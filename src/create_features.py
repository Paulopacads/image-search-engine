
# Import the necessary libraries
import os
import torch
import torchvision
import torchvision.transforms as transforms
from PIL import Image
from torch.utils.data import Dataset, DataLoader
import csv

# Define a dataset that loads the images from a folder
class FolderDataset(Dataset):
    def __init__(self, folder_path, transform=None):
        self.folder_path = folder_path
        self.transform = transform
        self.files = os.listdir(folder_path)
        
    def __len__(self):
        return len(self.files)
    
    def __getitem__(self, idx):
        img_path = os.path.join(self.folder_path, self.files[idx])
        image = Image.open(img_path)
        # Convert the image to a PyTorch tensor
        image = transforms.ToTensor()(image)
        # resize the image to 224x224
        image = transforms.Resize((224, 224))(image)
        if self.transform:
            image = self.transform(image)
        return image

def run():
    # Set the device to use for PyTorch
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Create a dataset that loads the images from the "images" folder
    image_dir = "static/data/jpg"
    image_list = os.listdir(image_dir)
    dataset = FolderDataset(image_dir)

    # Create a dataloader for the dataset
    dataloader = DataLoader(
        dataset, batch_size=1, shuffle=False, num_workers=10
    )


    # Load the pre-trained VGG19 model
    model = torchvision.models.densenet121(pretrained=True)

    # Set the model to evaluation
    model.eval()

    # Move the model to the specified device
    model = model.to(device)


    header = ['image_id', "features"]
    # create csv file
    f_features = open('static/data/features_densenet_test.csv', 'w')
    # initialize writer for csv
    writer_features = csv.writer(f_features)
    # write header
    writer_features.writerow(header)


    import tqdm
    # Extract features from the images in the dataset
    for i, inputs in enumerate(tqdm.tqdm(dataloader)):
        # Move the input images to the specified device
        inputs = inputs.to(device)

        # Extract the features from the intermediate layer of the VGG19 model
        features = model.features(inputs)

        # Convert the features to a NumPy array
        features = features.detach().cpu().numpy()
        # Reshape the features to a 1D array
        features = features.reshape(features.shape[0], -1)
        # to string
        features = features[0].tolist()
        
        # write to csv
        writer_features.writerow([image_list[i], features])


    # Close the file
    f_features.close()

if __name__ == "__main__":
    run()





