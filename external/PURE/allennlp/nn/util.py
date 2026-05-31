
import torch

def batched_index_select(target, indices, flattened_indices=None):
    """
    Minimal replacement for allennlp.nn.util.batched_index_select.
    """
    if flattened_indices is not None:
        flat_target = target.reshape(-1, target.size(-1))
        selected = flat_target.index_select(0, flattened_indices.reshape(-1))
        return selected.reshape(*indices.size(), target.size(-1))

    if indices.dim() == 1:
        indices = indices.unsqueeze(-1)

    batch_size = target.size(0)
    sequence_length = target.size(1)
    hidden_size = target.size(-1)

    flat_target = target.reshape(batch_size * sequence_length, hidden_size)

    offsets = torch.arange(
        batch_size,
        device=target.device
    ).view(batch_size, *([1] * (indices.dim() - 1))) * sequence_length

    flat_indices = (indices + offsets).reshape(-1)

    selected = flat_target.index_select(0, flat_indices)
    return selected.reshape(*indices.size(), hidden_size)
