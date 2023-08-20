import torch
# import matplotlib.pyplot as plt
import numpy as np 
# import argparse
import pickle 
import os
from torchvision import transforms 
from rest_apis.build_vocab import Vocabulary
from rest_apis.model import EncoderCNN, DecoderRNN
from PIL import Image

from rest_apis import app






class CustomUnpickler(pickle.Unpickler):

    def find_class(self, module, name):
        try:
            return super().find_class(__name__, name)
            print("__name__", __name__)
        except AttributeError:
            print("module", module)
            return super().find_class(module, name)






# Device configuration
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

def load_image(image_path, transform=None):
    image = Image.open(image_path).convert('RGB')
    image = image.resize([224, 224], Image.LANCZOS)
    
    if transform is not None:
        image = transform(image).unsqueeze(0)
    
    return image

def getImageCaption( imagePath ):

    pathToInstance = app.instance_path.replace("/instance", "")
    print("This is the path now", pathToInstance)

    pathToEncoder = pathToInstance + "/" + app.config["ENCODER_PATH"]
    pathToDecoder = pathToInstance + "/" + app.config["DECODER_PATH"]
    pathToVocab = pathToInstance + "/" + app.config["VOCAB_PATH"]

    EMBED_SIZE = app.config["EMBED_SIZE"]
    HIDDEN_SIZE = app.config["HIDDEN_SIZE"]
    NUM_LAYERS = app.config["NUM_LAYERS"]

    # Image preprocessing
    transform = transforms.Compose([
        transforms.ToTensor(), 
        transforms.Normalize((0.485, 0.456, 0.406), 
                             (0.229, 0.224, 0.225))])
    
    # Load vocabulary wrapper
    # with open(pathToVocab, 'rb') as f:
    #     vocab = pickle.load(f)

    vocab = CustomUnpickler(open(pathToVocab, 'rb')).load()
    # Build models

    encoder = EncoderCNN(EMBED_SIZE).eval()  # eval mode (batchnorm uses moving mean/variance)
    decoder = DecoderRNN(EMBED_SIZE, HIDDEN_SIZE, len(vocab), NUM_LAYERS)
    encoder = encoder.to(device)
    decoder = decoder.to(device)

    # Load the trained model parameters
    encoder.load_state_dict(torch.load(pathToEncoder))
    decoder.load_state_dict(torch.load(pathToDecoder))

    # Prepare an image
    image = load_image(imagePath, transform)
    image_tensor = image.to(device)
    
    # Generate an caption from the image
    feature = encoder(image_tensor)
    sampled_ids = decoder.sample(feature)
    sampled_ids = sampled_ids[0].cpu().numpy()          # (1, max_seq_length) -> (max_seq_length)
    
    # Convert word_ids to words
    sampled_caption = []
    for word_id in sampled_ids:
        word = vocab.idx2word[word_id]
        sampled_caption.append(word)
        if word == '<end>':
            break

    sampled_caption.pop(0)
    sampled_caption.pop()

    sentence = '+'.join(sampled_caption)
    
    # Print out the image and the generated caption
    print (sentence, type(sentence))
    # image = Image.open(args.image)
    # plt.imshow(np.asarray(image))
    return sentence


