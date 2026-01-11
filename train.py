import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
from model import AdvancedTimeSeriesTransformer
import json
from data_loader import load_and_preprocess_data
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os

class EarlyStopping:
    """Early stopping to stop training when validation loss doesn't improve"""
    def __init__(self, patience=10, min_delta=0, verbose=True):
        self.patience = patience
        self.min_delta = min_delta
        self.verbose = verbose
        self.counter = 0
        self.best_loss = None
        self.early_stop = False
        self.best_model = None
        
    def __call__(self, val_loss, model):
        if self.best_loss is None:
            self.best_loss = val_loss
            self.best_model = model.state_dict()
        elif val_loss > self.best_loss - self.min_delta:
            self.counter += 1
            if self.verbose:
                print(f'EarlyStopping counter: {self.counter}/{self.patience}')
            if self.counter >= self.patience:
                self.early_stop = True
        else:
            self.best_loss = val_loss
            self.best_model = model.state_dict()
            self.counter = 0
        return self.early_stop

def load_config():
    """Load configuration from config.json"""
    with open('config.json', 'r') as f:
        return json.load(f)

def train(config):
    """Advanced training function with learning rate scheduling and early stopping"""
    print("📊 Loading data...")
    X_train, X_test, y_train, y_test, scaler = load_and_preprocess_data(
        config['symbol'],
        config['start'],
        config['end'],
        config['SEQ_LEN']
    )
    
    # Convert to PyTorch tensors
    X_train = torch.FloatTensor(X_train)
    y_train = torch.FloatTensor(y_train)
    X_test = torch.FloatTensor(X_test)
    y_test_tensor = torch.FloatTensor(y_test)
    
    # Initialize model
    input_dim = X_train.shape[2]
    model = AdvancedTimeSeriesTransformer(
        input_dim=input_dim,
        model_dim=config['MODEL_DIM'],
        num_heads=config['NUM_HEADS'],
        num_layers=config['NUM_LAYERS'],
        dropout=config.get('dropout', 0.1),
        use_positional_encoding=config.get('use_positional_encoding', True)
    )
    
    criterion = nn.MSELoss()
    optimizer = optim.AdamW(model.parameters(), lr=config['LR'], weight_decay=1e-5)
    
    # Learning rate scheduler
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(
        optimizer, mode='min', factor=0.5, patience=5
    )
    
    # Early stopping
    early_stopping = EarlyStopping(patience=config.get('patience', 15), verbose=True)
    
    # Training history
    history = {
        'train_loss': [],
        'val_loss': [],
        'learning_rate': []
    }
    
    # Training loop
    print(f"🚀 Training for up to {config['EPOCHS']} epochs...")
    best_val_loss = float('inf')
    
    for epoch in range(config['EPOCHS']):
        # Training
        model.train()
        optimizer.zero_grad()
        predictions = model(X_train)
        loss = criterion(predictions, y_train)
        loss.backward()
        
        # Gradient clipping
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
        
        optimizer.step()
        
        # Validation
        model.eval()
        with torch.no_grad():
            val_pred = model(X_test)
            val_loss = criterion(val_pred, y_test_tensor)
        
        # Update scheduler
        scheduler.step(val_loss)
        
        # Record history
        history['train_loss'].append(loss.item())
        history['val_loss'].append(val_loss.item())
        history['learning_rate'].append(optimizer.param_groups[0]['lr'])
        
        if (epoch + 1) % 10 == 0 or epoch == 0:
            print(f"Epoch {epoch+1}/{config['EPOCHS']}, "
                  f"Train Loss: {loss.item():.6f}, "
                  f"Val Loss: {val_loss.item():.6f}, "
                  f"LR: {optimizer.param_groups[0]['lr']:.6f}")
        
        # Check for best model
        if val_loss < best_val_loss:
            best_val_loss = val_loss
            best_model_state = model.state_dict()
        
        # Early stopping check
        if early_stopping(val_loss, model):
            print(f"\n⚠️ Early stopping triggered at epoch {epoch+1}")
            model.load_state_dict(early_stopping.best_model)
            break
    
    # Load best model
    if early_stopping.best_model is not None:
        model.load_state_dict(early_stopping.best_model)
    
    # Evaluation
    print("\n📈 Evaluating model...")
    model.eval()
    with torch.no_grad():
        predictions = model(X_test).numpy().flatten()
    
    # Get the number of features from scaler
    n_features = scaler.n_features_in_
    
    # Find Close column index (should be at position 3 in original data)
    close_idx = 3  # Close column position in original OHLCV data
    
    # The scaler was fit on all features, but we only predicted Close price
    # We need to inverse transform only the Close price column
    # Create dummy array with all features, put predictions in Close column
    dummy = np.zeros((len(predictions), n_features))
    dummy[:, close_idx] = predictions  # Close is column 3 in scaled data
    predictions_rescaled = scaler.inverse_transform(dummy)[:, close_idx]
    
    dummy_actual = np.zeros((len(y_test), n_features))
    dummy_actual[:, close_idx] = y_test.flatten()
    y_test_rescaled = scaler.inverse_transform(dummy_actual)[:, close_idx]
    
    # Calculate metrics
    mse = mean_squared_error(y_test_rescaled, predictions_rescaled)
    mae = mean_absolute_error(y_test_rescaled, predictions_rescaled)
    r2 = r2_score(y_test_rescaled, predictions_rescaled)
    rmse = np.sqrt(mse)
    mape = np.mean(np.abs((y_test_rescaled - predictions_rescaled) / y_test_rescaled)) * 100
    
    print(f"\n✅ Results:")
    print(f"  MSE: {mse:.4f}")
    print(f"  RMSE: {rmse:.4f}")
    print(f"  MAE: {mae:.4f}")
    print(f"  MAPE: {mape:.2f}%")
    print(f"  R²: {r2:.4f}")
    
    # Create output directory
    os.makedirs('outputs', exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Save model with timestamp
    model_path = f"outputs/model_{config['symbol']}_{timestamp}.pt"
    torch.save({
        'model_state_dict': model.state_dict(),
        'config': config,
        'scaler': scaler,
        'metrics': {'mse': mse, 'mae': mae, 'r2': r2, 'rmse': rmse, 'mape': mape}
    }, model_path)
    print(f"\n💾 Model saved to {model_path}")
    
    # Advanced visualizations
    create_advanced_visualizations(
        y_test_rescaled, predictions_rescaled, history, 
        model, X_test, config, timestamp
    )
    
    # Log experiment
    experiment = {
        'timestamp': timestamp,
        'symbol': config['symbol'],
        'mse': float(mse),
        'rmse': float(rmse),
        'mae': float(mae),
        'mape': float(mape),
        'r2': float(r2),
        'epochs_trained': len(history['train_loss']),
        'config': config
    }
    
    try:
        with open('experiment_log.json', 'r') as f:
            logs = json.load(f)
    except:
        logs = []
    
    logs.append(experiment)
    with open('experiment_log.json', 'w') as f:
        json.dump(logs, f, indent=2)
    
    return model, predictions_rescaled, y_test_rescaled

def create_advanced_visualizations(y_true, y_pred, history, model, X_test, config, timestamp):
    """Create comprehensive visualization plots"""
    
    # 1. Prediction vs Actual with Error Bands
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    # Plot 1: Predictions vs Actual
    axes[0, 0].plot(y_true, label='Actual', alpha=0.7, linewidth=2)
    axes[0, 0].plot(y_pred, label='Predicted', alpha=0.7, linewidth=2)
    axes[0, 0].fill_between(range(len(y_true)), y_true, y_pred, alpha=0.2)
    axes[0, 0].set_title(f'{config["symbol"]} Price Prediction', fontsize=14, fontweight='bold')
    axes[0, 0].set_xlabel('Time Step')
    axes[0, 0].set_ylabel('Price ($)')
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)
    
    # Plot 2: Learning Curves
    axes[0, 1].plot(history['train_loss'], label='Train Loss', alpha=0.7)
    axes[0, 1].plot(history['val_loss'], label='Val Loss', alpha=0.7)
    axes[0, 1].set_title('Learning Curves', fontsize=14, fontweight='bold')
    axes[0, 1].set_xlabel('Epoch')
    axes[0, 1].set_ylabel('Loss (MSE)')
    axes[0, 1].legend()
    axes[0, 1].set_yscale('log')
    axes[0, 1].grid(True, alpha=0.3)
    
    # Plot 3: Residual Analysis
    residuals = y_true - y_pred
    axes[1, 0].scatter(y_pred, residuals, alpha=0.5)
    axes[1, 0].axhline(y=0, color='r', linestyle='--', linewidth=2)
    axes[1, 0].set_title('Residual Plot', fontsize=14, fontweight='bold')
    axes[1, 0].set_xlabel('Predicted Values')
    axes[1, 0].set_ylabel('Residuals')
    axes[1, 0].grid(True, alpha=0.3)
    
    # Plot 4: Error Distribution
    axes[1, 1].hist(residuals, bins=50, edgecolor='black', alpha=0.7)
    axes[1, 1].set_title('Error Distribution', fontsize=14, fontweight='bold')
    axes[1, 1].set_xlabel('Prediction Error')
    axes[1, 1].set_ylabel('Frequency')
    axes[1, 1].axvline(x=0, color='r', linestyle='--', linewidth=2)
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f'outputs/analysis_{config["symbol"]}_{timestamp}.png', dpi=300)
    print(f"📊 Advanced analysis saved to outputs/analysis_{config['symbol']}_{timestamp}.png")
    plt.close()
    
    # 2. Attention Visualization
    try:
        model.eval()
        with torch.no_grad():
            _, attention_weights = model(X_test[:5], return_attention=True)
        
        if attention_weights:
            fig, axes = plt.subplots(1, len(attention_weights), figsize=(5*len(attention_weights), 4))
            if len(attention_weights) == 1:
                axes = [axes]
            
            for idx, (ax, attn) in enumerate(zip(axes, attention_weights)):
                attn_map = attn[0].cpu().numpy()  # First sample
                sns.heatmap(attn_map, ax=ax, cmap='viridis', cbar=True)
                ax.set_title(f'Layer {idx+1} Attention')
                ax.set_xlabel('Key Position')
                ax.set_ylabel('Query Position')
            
            plt.tight_layout()
            plt.savefig(f'outputs/attention_{config["symbol"]}_{timestamp}.png', dpi=300)
            print(f"🔍 Attention maps saved to outputs/attention_{config['symbol']}_{timestamp}.png")
            plt.close()
    except Exception as e:
        print(f"⚠️ Could not generate attention visualization: {e}")
    
    # 3. Learning Rate Schedule
    plt.figure(figsize=(10, 5))
    plt.plot(history['learning_rate'])
    plt.title('Learning Rate Schedule', fontsize=14, fontweight='bold')
    plt.xlabel('Epoch')
    plt.ylabel('Learning Rate')
    plt.yscale('log')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f'outputs/lr_schedule_{config["symbol"]}_{timestamp}.png', dpi=300)
    print(f"📉 LR schedule saved to outputs/lr_schedule_{config['symbol']}_{timestamp}.png")
    plt.close()