from http.server import HTTPServer
from server import HTTPRequestHandler
import torch, torchvision, json
from torch import nn

class FlowerDataset:
    basic_transform = torchvision.transforms.Compose([
        torchvision.transforms.Resize(size=(224, 224)),
        torchvision.transforms.ToTensor()
    ])

    class_names = [
        "pink primrose", "hard-leaved pocket orchid", "bolero deep blue", "sweet pea", "english marigold", "tiger lily", "moon orchid", "bird of paradise", "monkshood", "globe thistle", "snapdragon", "colt's foot", "king protea", "spear thistle", "yellow iris", "globe-flower", "purple coneflower", "peruvian lily", "balloon flower", "giant white arum lily", "fire lily", "pincushion flower", "fritillary", "red ginger", "grape hyacinth", "corn poppy", "prince of wales feathers", "stemless gentian", "artichoke", "sweet william", "carnation", "garden phlox", "love in the mist", "mexican aster", "alpine sea holly", "ruby-lipped cattleya", "cape flower", "great masterwort", "siam tulip", "lenten rose", "barbeton daisy", "daffodil", "sword lily", "poinsettia", "bolero deep blue", "wallflower", "marigold", "buttercup", "oxeye daisy", "common dandelion", "petunia", "wild pansy", "primula", "sunflower", "pelargonium", "bishop of llandaff", "gaura", "geranium", "orange dahlia", "pink-yellow dahlia?", "cautleya spicata", "japanese anemone", "black-eyed susan", "silverbush", "californian poppy", "osteospermum", "spring crocus", "bearded iris", "windflower", "tree poppy", "gazania", "azalea", "water lily", "rose", "thorn apple", "morning glory", "passion flower", "lotus", "toad lily", "anthurium", "frangipani", "clematis", "hibiscus", "columbine", "desert-rose", "tree mallow", "magnolia", "cyclamen", "watercress", "canna lily", "hippeastrum", "bee balm", "ball moss", "foxglove", "bougainvillea", "camellia", "mallow", "mexican petunia", "bromelia", "blanket flower", "trumpet creeper", "blackberry lily"
    ]

class ResNet50Mod(nn.Module):
    def __init__(self, in_channels, hidden_units, out_shape):
        super(ResNet50Mod, self).__init__()

        self.stage_1 = nn.Sequential(
            nn.Conv2d(in_channels=in_channels, out_channels=hidden_units, kernel_size=7, stride=2),
            nn.BatchNorm2d(num_features=hidden_units),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=3, stride=2)
        )

        self.stage_2 = nn.Sequential(
            nn.Conv2d(in_channels=hidden_units, out_channels=hidden_units, kernel_size=1, stride=2),
            nn.Conv2d(in_channels=hidden_units, out_channels=hidden_units, kernel_size=3, stride=2),
            nn.Conv2d(in_channels=hidden_units, out_channels=hidden_units, kernel_size=1, stride=2)
        )

        self.stage_3 = nn.Sequential(
            nn.Conv2d(in_channels=hidden_units, out_channels=hidden_units, kernel_size=1, stride=2),
            nn.BatchNorm2d(num_features=hidden_units),
            nn.ReLU(),
            nn.Conv2d(in_channels=hidden_units, out_channels=hidden_units, kernel_size=3, stride=2),
            nn.BatchNorm2d(num_features=hidden_units),
            nn.ReLU(),
            nn.Conv2d(in_channels=hidden_units, out_channels=hidden_units, kernel_size=1, stride=2),
            nn.BatchNorm2d(num_features=hidden_units),
            nn.ReLU()
        )

        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(in_features=hidden_units*1, out_features=out_shape),
            nn.Sigmoid()
        )
    
    def forward(self, X):
        return self.classifier.forward(
            self.stage_3.forward(
                self.stage_2.forward(
                    self.stage_1.forward(
                        X
                    )
                )
            )
        )

model = torch.load("./model.pth", map_location=torch.device("cpu"))

def predict(image):
    image = FlowerDataset.basic_transform(image)[:3].unsqueeze(0)

    model.eval()
    with torch.inference_mode():
        y_logits = model.forward(image)
    
    y_probs = y_logits.squeeze().tolist()
    arg_max = y_logits.argmax(1).item()
    class_names = FlowerDataset.class_names
    y_class = class_names[arg_max]

    return json.dumps({
        "probabilities": y_probs,
        "highest": arg_max,
        "classes": class_names,
        "prediction": y_class
    })

def main():
    serveraddr = ("127.0.0.1", 8000)
    httpd = HTTPServer(serveraddr, HTTPRequestHandler)
    print(f"{serveraddr[0]} - [+] Starting server on port {serveraddr[1]}...")
    httpd.serve_forever()

if __name__ == "__main__":
    main()