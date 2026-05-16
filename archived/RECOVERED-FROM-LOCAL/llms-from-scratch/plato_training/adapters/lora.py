"""LoRA implementation — low-rank adaptation layers."""

import math
import torch
import torch.nn as nn
from typing import Optional


class LoRALayer(nn.Module):
    """
    LoRA (Low-Rank Adaptation) layer.
    
    Wraps an existing linear layer and adds trainable low-rank matrices.
    The original weights are frozen; only A and B are trained.
    
    Forward: W*x + (alpha/rank) * B @ A @ x
    
    After training, can be merged: W' = W + (alpha/rank) * B @ A
    """
    
    def __init__(
        self,
        original_layer: nn.Linear,
        rank: int = 8,
        alpha: int = 16,
        dropout: float = 0.0,
    ):
        super().__init__()
        self.original = original_layer
        self.rank = rank
        self.alpha = alpha
        self.scaling = alpha / rank
        
        d_in = original_layer.in_features
        d_out = original_layer.out_features
        
        # Freeze original weights
        self.original.weight.requires_grad_(False)
        if self.original.bias is not None:
            self.original.bias.requires_grad_(False)
        
        # LoRA matrices: A (d_in x r), B (r x d_out)
        # A initialized with Kaiming, B initialized to zero
        # This means initial output = original output (zero LoRA contribution)
        self.lora_A = nn.Parameter(torch.empty(d_in, rank))
        self.lora_B = nn.Parameter(torch.zeros(rank, d_out))
        
        nn.init.kaiming_uniform_(self.lora_A, a=math.sqrt(5))
        
        self.dropout = nn.Dropout(dropout) if dropout > 0 else nn.Identity()
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        original_output = self.original(x)
        lora_output = self.dropout(x) @ self.lora_A @ self.lora_B
        return original_output + lora_output * self.scaling
    
    def merge(self) -> nn.Linear:
        """Merge LoRA weights into the original layer. No inference overhead."""
        merged = nn.Linear(
            self.original.in_features,
            self.original.out_features,
            bias=self.original.bias is not None,
        )
        merged.weight.data = self.original.weight.data + (
            self.lora_B.T @ self.lora_A.T
        ) * self.scaling
        if self.original.bias is not None:
            merged.bias.data = self.original.bias.data.clone()
        return merged
    
    def lora_parameters(self):
        """Return only the trainable LoRA parameters."""
        return [self.lora_A, self.lora_B]
    
    def num_trainable_params(self) -> int:
        return self.lora_A.numel() + self.lora_B.numel()


def inject_lora(
    model: nn.Module,
    rank: int = 8,
    alpha: int = 16,
    target_modules: Optional[list] = None,
    dropout: float = 0.0,
) -> nn.Module:
    """
    Inject LoRA layers into a model's linear layers.
    
    Args:
        model: The neural network to adapt
        rank: LoRA rank (8 for classification, 32 for generation)
        alpha: LoRA alpha (scaling factor)
        target_modules: Layer names to inject into (None = all Linear layers)
        dropout: Dropout rate for LoRA
    
    Returns:
        The model with LoRA layers injected (original weights frozen)
    """
    if target_modules is None:
        target_modules = ["W_query", "W_value", "W_key", "W_out"]
    
    total_params = 0
    injected_count = 0
    
    for name, module in model.named_modules():
        if isinstance(module, nn.Linear):
            # Check if this layer should be adapted
            should_inject = any(t in name for t in target_modules)
            
            if should_inject:
                # Replace the linear layer with a LoRA-wrapped version
                lora_layer = LoRALayer(
                    module, rank=rank, alpha=alpha, dropout=dropout
                )
                
                # Navigate to parent and replace
                parts = name.split(".")
                parent = model
                for part in parts[:-1]:
                    parent = getattr(parent, part)
                setattr(parent, parts[-1], lora_layer)
                
                total_params += lora_layer.num_trainable_params()
                injected_count += 1
    
    return model
