
import torch
import torch.nn as nn
import torch.nn.functional as F
from . import util

class _ActivationFactory:
    def __init__(self, name):
        self.name = name.lower()

    def __call__(self, *args, **kwargs):
        if self.name == "relu":
            return nn.ReLU(*args, **kwargs)
        if self.name == "tanh":
            return nn.Tanh()
        if self.name == "sigmoid":
            return nn.Sigmoid()
        if self.name == "gelu":
            return nn.GELU()
        if self.name in ["linear", "identity"]:
            return nn.Identity()
        raise ValueError(f"Unsupported activation: {self.name}")

class Activation:
    @staticmethod
    def by_name(name):
        return _ActivationFactory(name)
