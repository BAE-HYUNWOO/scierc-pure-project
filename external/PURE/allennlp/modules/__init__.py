
import torch
import torch.nn as nn
import torch.nn.functional as F

class FeedForward(nn.Module):
    """
    Minimal replacement for allennlp.modules.FeedForward used by PURE.
    Supports:
    FeedForward(input_dim=..., num_layers=..., hidden_dims=..., activations=..., dropout=...)
    """
    def __init__(self, input_dim, num_layers, hidden_dims, activations, dropout=0.0):
        super().__init__()

        if isinstance(hidden_dims, int):
            hidden_dims = [hidden_dims] * num_layers
        if not isinstance(hidden_dims, (list, tuple)):
            raise ValueError("hidden_dims must be int/list/tuple")

        if callable(activations):
            activations = [activations] * num_layers
        elif not isinstance(activations, (list, tuple)):
            activations = [activations] * num_layers

        if isinstance(dropout, (int, float)):
            dropout = [float(dropout)] * num_layers

        layers = []
        prev_dim = input_dim

        for i in range(num_layers):
            out_dim = hidden_dims[i]
            layers.append(nn.Linear(prev_dim, out_dim))

            act = activations[i]
            if callable(act):
                layers.append(_FunctionalActivation(act))
            elif isinstance(act, nn.Module):
                layers.append(act)
            else:
                raise ValueError(f"Unsupported activation type: {type(act)}")

            if dropout[i] and dropout[i] > 0:
                layers.append(nn.Dropout(dropout[i]))

            prev_dim = out_dim

        self.seq = nn.Sequential(*layers)

    def forward(self, x):
        return self.seq(x)

class _FunctionalActivation(nn.Module):
    def __init__(self, func):
        super().__init__()
        self.func = func

    def forward(self, x):
        return self.func(x)
