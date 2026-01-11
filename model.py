import torch
import torch.nn as nn
import math

class PositionalEncoding(nn.Module):
    """Sinusoidal positional encoding for time series"""
    def __init__(self, d_model, max_len=5000):
        super().__init__()
        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model))
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        pe = pe.unsqueeze(0)
        self.register_buffer('pe', pe)

    def forward(self, x):
        return x + self.pe[:, :x.size(1), :]

class MultiHeadAttentionWithViz(nn.Module):
    """Multi-head attention with visualization capabilities"""
    def __init__(self, d_model, num_heads, dropout=0.1):
        super().__init__()
        self.attention = nn.MultiheadAttention(d_model, num_heads, dropout=dropout, batch_first=True)
        self.attention_weights = None
    
    def forward(self, x):
        attn_output, attn_weights = self.attention(x, x, x, need_weights=True, average_attn_weights=True)
        self.attention_weights = attn_weights.detach()
        return attn_output

class AdvancedTimeSeriesTransformer(nn.Module):
    """Advanced Transformer with positional encoding and residual connections"""
    def __init__(self, input_dim, model_dim, num_heads, num_layers, dropout=0.1, use_positional_encoding=True):
        super().__init__()
        self.model_dim = model_dim
        self.use_positional_encoding = use_positional_encoding
        
        # Input projection
        self.input_proj = nn.Linear(input_dim, model_dim)
        self.input_norm = nn.LayerNorm(model_dim)
        
        # Positional encoding
        if use_positional_encoding:
            self.pos_encoder = PositionalEncoding(model_dim)
        
        # Transformer encoder layers with custom attention
        self.attention_layers = nn.ModuleList([
            MultiHeadAttentionWithViz(model_dim, num_heads, dropout) 
            for _ in range(num_layers)
        ])
        
        self.ffn_layers = nn.ModuleList([
            nn.Sequential(
                nn.Linear(model_dim, model_dim * 4),
                nn.GELU(),
                nn.Dropout(dropout),
                nn.Linear(model_dim * 4, model_dim),
                nn.Dropout(dropout)
            ) for _ in range(num_layers)
        ])
        
        self.norm_layers1 = nn.ModuleList([nn.LayerNorm(model_dim) for _ in range(num_layers)])
        self.norm_layers2 = nn.ModuleList([nn.LayerNorm(model_dim) for _ in range(num_layers)])
        
        # Output layers with residual connection
        self.global_pool = nn.AdaptiveAvgPool1d(1)
        self.fc_out = nn.Sequential(
            nn.Linear(model_dim, model_dim // 2),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(model_dim // 2, 1)
        )
        
        self.dropout = nn.Dropout(dropout)
        self._init_weights()
    
    def _init_weights(self):
        """Initialize weights using Xavier initialization"""
        for p in self.parameters():
            if p.dim() > 1:
                nn.init.xavier_uniform_(p)
    
    def forward(self, x, return_attention=False):
        # x: (batch, seq_len, input_dim)
        x = self.input_proj(x)
        x = self.input_norm(x)
        
        if self.use_positional_encoding:
            x = self.pos_encoder(x)
        
        x = self.dropout(x)
        
        # Store attention weights for visualization
        attention_weights = []
        
        # Pass through transformer layers
        for i, (attn_layer, ffn_layer, norm1, norm2) in enumerate(
            zip(self.attention_layers, self.ffn_layers, self.norm_layers1, self.norm_layers2)
        ):
            # Multi-head attention with residual
            residual = x
            x = attn_layer(x)
            x = norm1(x + residual)
            
            # FFN with residual
            residual = x
            x = ffn_layer(x)
            x = norm2(x + residual)
            
            if return_attention:
                attention_weights.append(attn_layer.attention_weights)
        
        # Global pooling over sequence dimension
        x = x.permute(0, 2, 1)  # (batch, model_dim, seq_len)
        x = self.global_pool(x).squeeze(-1)  # (batch, model_dim)
        
        # Final prediction
        out = self.fc_out(x)
        
        if return_attention:
            return out.squeeze(-1), attention_weights
        return out.squeeze(-1)
    
    def get_attention_weights(self):
        """Retrieve attention weights from all layers"""
        return [layer.attention_weights for layer in self.attention_layers if layer.attention_weights is not None]

# Keep backward compatibility
class TimeSeriesTransformer(AdvancedTimeSeriesTransformer):
    """Alias for backward compatibility"""
    pass
