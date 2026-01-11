import torch
import torch.nn as nn
import json
import numpy as np
from datetime import datetime
from model import AdvancedTimeSeriesTransformer
from data_loader import load_and_preprocess_data
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import ParameterGrid
import optuna
from optuna.visualization import plot_optimization_history, plot_param_importances

def load_config():
    """Load base configuration"""
    with open('config.json', 'r') as f:
        return json.load(f)

def train_with_params(params, X_train, y_train, X_test, y_test, epochs=50):
    """Train model with given parameters"""
    X_train_t = torch.FloatTensor(X_train)
    y_train_t = torch.FloatTensor(y_train)
    X_test_t = torch.FloatTensor(X_test)
    y_test_t = torch.FloatTensor(y_test)
    
    input_dim = X_train.shape[2]
    model = AdvancedTimeSeriesTransformer(
        input_dim=input_dim,
        model_dim=params['MODEL_DIM'],
        num_heads=params['NUM_HEADS'],
        num_layers=params['NUM_LAYERS'],
        dropout=params.get('dropout', 0.1),
        use_positional_encoding=params.get('use_positional_encoding', True)
    )
    
    criterion = nn.MSELoss()
    optimizer = torch.optim.AdamW(model.parameters(), lr=params['LR'], weight_decay=params.get('weight_decay', 1e-5))
    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', factor=0.5, patience=5, verbose=False)
    
    best_val_loss = float('inf')
    patience_counter = 0
    patience = 10
    
    for epoch in range(epochs):
        model.train()
        optimizer.zero_grad()
        predictions = model(X_train_t)
        loss = criterion(predictions, y_train_t)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
        optimizer.step()
        
        model.eval()
        with torch.no_grad():
            val_pred = model(X_test_t)
            val_loss = criterion(val_pred, y_test_t)
        
        scheduler.step(val_loss)
        
        if val_loss < best_val_loss:
            best_val_loss = val_loss
            patience_counter = 0
        else:
            patience_counter += 1
            if patience_counter >= patience:
                break
    
    return best_val_loss.item()

def bayesian_optimization(config):
    """Advanced hyperparameter search using Bayesian Optimization (Optuna)"""
    print("🔍 Starting Bayesian Hyperparameter Optimization with Optuna...")
    
    # Load data
    X_train, X_test, y_train, y_test, scaler = load_and_preprocess_data(
        config['symbol'],
        config['start'],
        config['end'],
        config['SEQ_LEN']
    )
    
    def objective(trial):
        """Optuna objective function"""
        params = {
            'MODEL_DIM': trial.suggest_categorical('MODEL_DIM', [32, 64, 128, 256]),
            'NUM_HEADS': trial.suggest_categorical('NUM_HEADS', [2, 4, 8]),
            'NUM_LAYERS': trial.suggest_int('NUM_LAYERS', 1, 4),
            'LR': trial.suggest_loguniform('LR', 1e-4, 1e-2),
            'dropout': trial.suggest_float('dropout', 0.1, 0.5),
            'weight_decay': trial.suggest_loguniform('weight_decay', 1e-6, 1e-3),
            'use_positional_encoding': trial.suggest_categorical('use_positional_encoding', [True, False])
        }
        
        # Ensure NUM_HEADS divides MODEL_DIM
        while params['MODEL_DIM'] % params['NUM_HEADS'] != 0:
            params['NUM_HEADS'] = trial.suggest_categorical('NUM_HEADS', [2, 4, 8])
        
        val_loss = train_with_params(params, X_train, y_train, X_test, y_test, epochs=50)
        return val_loss
    
    # Create and run study
    study = optuna.create_study(
        direction='minimize',
        sampler=optuna.samplers.TPESampler(seed=42),
        pruner=optuna.pruners.MedianPruner()
    )
    
    study.optimize(objective, n_trials=30, show_progress_bar=True)
    
    # Results
    print(f"\n✨ Best trial: {study.best_trial.number}")
    print(f"✨ Best validation loss: {study.best_trial.value:.6f}")
    print(f"\n🏆 Best hyperparameters:")
    for key, value in study.best_trial.params.items():
        print(f"  {key}: {value}")
    
    # Save results
    results = {
        'timestamp': datetime.now().strftime('%Y%m%d_%H%M%S'),
        'method': 'Bayesian_Optimization_Optuna',
        'symbol': config['symbol'],
        'n_trials': 30,
        'best_val_loss': study.best_trial.value,
        'best_params': study.best_trial.params,
        'all_trials': [
            {
                'number': trial.number,
                'value': trial.value,
                'params': trial.params
            } for trial in study.trials
        ]
    }
    
    with open('hyperparameter_search_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n💾 Results saved to hyperparameter_search_results.json")
    
    # Visualizations
    try:
        import matplotlib.pyplot as plt
        
        fig1 = plot_optimization_history(study)
        fig1.write_image('outputs/optimization_history.png')
        
        fig2 = plot_param_importances(study)
        fig2.write_image('outputs/param_importances.png')
        
        print("📊 Optimization visualizations saved to outputs/")
    except Exception as e:
        print(f"⚠️ Could not create visualizations: {e}")
    
    return study.best_trial.params

def grid_search(config):
    """Traditional grid search for comparison"""
    print("🔍 Starting Grid Search...")
    
    param_grid = {
        'MODEL_DIM': [64, 128],
        'NUM_HEADS': [4, 8],
        'NUM_LAYERS': [2, 3],
        'LR': [1e-3, 5e-4],
        'dropout': [0.1, 0.2]
    }
    
    X_train, X_test, y_train, y_test, scaler = load_and_preprocess_data(
        config['symbol'],
        config['start'],
        config['end'],
        config['SEQ_LEN']
    )
    
    best_loss = float('inf')
    best_params = None
    results = []
    
    for params in ParameterGrid(param_grid):
        if params['MODEL_DIM'] % params['NUM_HEADS'] != 0:
            continue
        
        print(f"\nTrying params: {params}")
        val_loss = train_with_params(params, X_train, y_train, X_test, y_test, epochs=30)
        print(f"Validation Loss: {val_loss:.6f}")
        
        results.append({
            'params': params,
            'val_loss': val_loss
        })
        
        if val_loss < best_loss:
            best_loss = val_loss
            best_params = params
    
    print(f"\n🏆 Best params: {best_params}")
    print(f"🏆 Best validation loss: {best_loss:.6f}")
    
    # Save results
    output = {
        'timestamp': datetime.now().strftime('%Y%m%d_%H%M%S'),
        'method': 'Grid_Search',
        'symbol': config['symbol'],
        'best_val_loss': best_loss,
        'best_params': best_params,
        'all_results': results
    }
    
    with open('grid_search_results.json', 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"\n💾 Results saved to grid_search_results.json")
    return best_params

if __name__ == "__main__":
    config = load_config()
    
    print("Choose optimization method:")
    print("1. Bayesian Optimization (Recommended - more efficient)")
    print("2. Grid Search (Traditional - exhaustive)")
    
    choice = input("\nEnter choice (1 or 2, default=1): ").strip() or "1"
    
    if choice == "1":
        best_params = bayesian_optimization(config)
    else:
        best_params = grid_search(config)
    
    print("\n" + "="*60)
    print("Hyperparameter search complete!")
    print("Update config.json with the best parameters found above.")
    print("="*60)
