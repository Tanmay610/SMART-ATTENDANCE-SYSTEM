import json 
import h5py
import warnings
import tensorflow as tf #provides the deep learning framework
from tensorflow.keras.layers import Layer
from tensorflow.keras import Model
from tensorflow.keras.saving import register_keras_serializable

warnings.filterwarnings("ignore")

@register_keras_serializable(package="Custom", name="ScaleSum")
class ScaleSum(Layer):
    def __init__(self, scale=1.0, **kwargs):
        super(ScaleSum, self).__init__(**kwargs)
        self.scale = scale

    def call(self, inputs):
        return inputs[0] + inputs[1] * self.scale

    def get_config(self):
        cfg = super(ScaleSum, self).get_config()
        cfg.update({"scale": self.scale})
        return cfg

class emb:
    _model = None

    def __init__(self):
        if emb._model is None:
            weights_path = "PreTrained_model/facenet_keras.h5"
            with h5py.File(weights_path, "r") as f:
                cfg = json.loads(f.attrs["model_config"])

            for l in cfg["config"]["layers"]:
                if l["class_name"] == "Lambda" and "ScaleSum" in l["name"]:
                    scale_val = l["config"].get("arguments", {}).get("scale", 1.0)
                    l["class_name"] = "ScaleSum"
                    l["module"] = "Custom"
                    l["config"] = {
                        "name": l["name"],
                        "trainable": l["config"].get("trainable", True),
                        "dtype": "float32",
                        "scale": scale_val,
                    }

            emb._model = Model.from_config(cfg["config"], custom_objects={"ScaleSum": ScaleSum})
            emb._model.load_weights(weights_path)
        self.model = emb._model

    def calculate(self, img):
        return self.model.predict(img, verbose=0)[0]
