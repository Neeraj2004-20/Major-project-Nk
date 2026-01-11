"""
Ensemble model and model interpretability utilities
"""
import torch
import torch.nn as nn
import numpy as np
from typing import List, Dict, Tuple
from model import AdvancedTimeSeriesTransformer
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

class EnsemblePredictor:
    """Ensemble of multiple models for improved predictions"""
    
    def __init__(self, models: List[nn.Module], weights: List[float] = None):
        self.models = models
        self.weights = weights if weights else [1/len(models)] * len(models)
        self.weights = torch.tensor(self.weights, dtype=torch.float32)
        self.weights /= self.weights.sum()  # Normalize
        
    def predict(self, x):
        """Make ensemble prediction"""
        predictions = []
        for model in self.models:
            model.eval()
            with torch.no_grad():
                pred = model(x)
                predictions.append(pred)
        
        # Weighted average
        predictions = torch.stack(predictions)
        ensemble_pred = (predictions.T @ self.weights).squeeze()
        
        return ensemble_pred
    
    def predict_with_uncertainty(self, x):
        """Predict with uncertainty estimate (variance across models)"""
        predictions = []
        for model in self.models:
            model.eval()
            with torch.no_grad():
                pred = model(x)
                predictions.append(pred.cpu().numpy())
        
        predictions = np.array(predictions)
        mean_pred = np.mean(predictions, axis=0)
        std_pred = np.std(predictions, axis=0)
        
        return mean_pred, std_pred

class ModelInterpreter:
    """Utilities for model interpretability"""
    
    @staticmethod
    def feature_importance_permutation(model, X, y, feature_names=None):
        """Calculate feature importance using permutation method"""
        model.eval()
        X_tensor = torch.FloatTensor(X)
        y_tensor = torch.FloatTensor(y)
        
        # Baseline performance
        with torch.no_grad():
            baseline_pred = model(X_tensor)
            baseline_loss = nn.MSELoss()(baseline_pred, y_tensor).item()
        
        importances = []
        n_features = X.shape[2]
        
        for feature_idx in range(n_features):
            # Permute feature
            X_permuted = X.copy()
            np.random.shuffle(X_permuted[:, :, feature_idx])
            
            X_perm_tensor = torch.FloatTensor(X_permuted)
            with torch.no_grad():
                perm_pred = model(X_perm_tensor)
                perm_loss = nn.MSELoss()(perm_pred, y_tensor).item()
            
            # Importance = increase in loss
            importance = perm_loss - baseline_loss
            importances.append(importance)
        
        # Create results dict
        if feature_names:
            importance_dict = dict(zip(feature_names, importances))
        else:
            importance_dict = {f"Feature_{i}": imp for i, imp in enumerate(importances)}
        
        # Sort by importance
        importance_dict = dict(sorted(importance_dict.items(), key=lambda x: x[1], reverse=True))
        
        return importance_dict
    
    @staticmethod
    def visualize_feature_importance(importance_dict, save_path='outputs/feature_importance.png'):
        """Visualize feature importance"""
        features = list(importance_dict.keys())
        importances = list(importance_dict.values())
        
        plt.figure(figsize=(12, 8))
        colors = ['green' if x > 0 else 'red' for x in importances]
        plt.barh(features, importances, color=colors, alpha=0.7)
        plt.xlabel('Importance (Increase in Loss)', fontsize=12)
        plt.title('Feature Importance (Permutation Method)', fontsize=14, fontweight='bold')
        plt.axvline(x=0, color='black', linestyle='--', linewidth=1)
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"📊 Feature importance plot saved to {save_path}")
        plt.close()
    
    @staticmethod
    def analyze_attention_patterns(model, X, save_path='outputs/attention_analysis.png'):
        """Analyze attention patterns across the dataset"""
        model.eval()
        X_tensor = torch.FloatTensor(X)
        
        all_attention_weights = []
        
        with torch.no_grad():
            for i in range(min(len(X), 100)):  # Sample 100 examples
                _, attention_weights = model(X_tensor[i:i+1], return_attention=True)
                all_attention_weights.append(attention_weights)
        
        # Average attention across samples
        if all_attention_weights and all_attention_weights[0]:
            n_layers = len(all_attention_weights[0])
            
            fig, axes = plt.subplots(1, n_layers, figsize=(5*n_layers, 5))
            if n_layers == 1:
                axes = [axes]
            
            for layer_idx in range(n_layers):
                # Collect attention for this layer
                layer_attentions = []
                for sample_attn in all_attention_weights:
                    if sample_attn[layer_idx] is not None:
                        layer_attentions.append(sample_attn[layer_idx].cpu().numpy())
                
                if layer_attentions:
                    avg_attention = np.mean(layer_attentions, axis=0)
                    
                    sns.heatmap(avg_attention, ax=axes[layer_idx], cmap='viridis', 
                               cbar=True, square=True)
                    axes[layer_idx].set_title(f'Layer {layer_idx+1}\nAverage Attention')
                    axes[layer_idx].set_xlabel('Key Position')
                    axes[layer_idx].set_ylabel('Query Position')
            
            plt.tight_layout()
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"🔍 Attention analysis saved to {save_path}")
            plt.close()
    
    @staticmethod
    def generate_saliency_map(model, X_sample, save_path='outputs/saliency_map.png'):
        """Generate saliency map showing input importance"""
        model.eval()
        X_tensor = torch.FloatTensor(X_sample).unsqueeze(0)
        X_tensor.requires_grad = True
        
        # Forward pass
        output = model(X_tensor)
        
        # Backward pass
        output.backward()
        
        # Saliency is the absolute value of gradients
        saliency = torch.abs(X_tensor.grad).squeeze().cpu().numpy()
        
        plt.figure(figsize=(12, 6))
        plt.imshow(saliency.T, aspect='auto', cmap='hot', interpolation='nearest')
        plt.colorbar(label='Importance')
        plt.xlabel('Time Step')
        plt.ylabel('Feature')
        plt.title('Saliency Map: Input Feature Importance', fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"🗺️ Saliency map saved to {save_path}")
        plt.close()

def create_ensemble_from_checkpoints(checkpoint_paths: List[str], input_dim: int, config: Dict) -> EnsemblePredictor:
    """Create ensemble from multiple model checkpoints"""
    models = []
    
    for checkpoint_path in checkpoint_paths:
        model = AdvancedTimeSeriesTransformer(
            input_dim=input_dim,
            model_dim=config['MODEL_DIM'],
            num_heads=config['NUM_HEADS'],
            num_layers=config['NUM_LAYERS'],
            dropout=config.get('dropout', 0.1)
        )
        
        checkpoint = torch.load(checkpoint_path, map_location='cpu')
        model.load_state_dict(checkpoint['model_state_dict'])
        model.eval()
        models.append(model)
    
    return EnsemblePredictor(models)

if __name__ == "__main__":
    print("Ensemble and interpretability utilities loaded.")
    print("Use these classes to:")
    print("  - Create ensemble models for better predictions")
    print("  - Analyze feature importance")
    print("  - Visualize attention patterns")
    print("  - Generate saliency maps")
