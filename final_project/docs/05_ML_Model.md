# Fase 5: Modelo Predictivo con Machine Learning

## Objetivos de la Fase
1. Construir un modelo de clasificación para predecir deserción
2. Comparar múltiples algoritmos de Machine Learning
3. Optimizar hiperparámetros del mejor modelo
4. Evaluar el modelo con métricas apropiadas
5. Interpretar y explicar las predicciones

## 1. Definición del Problema

### 1.1 Tipo de Problema
**Clasificación Binaria Supervisada**
- **Clase 1 (Positiva)**: Estudiante desertor
- **Clase 0 (Negativa)**: Estudiante activo/graduado

### 1.2 Variable Objetivo
```python
target = 'es_desertor'  # 1: Desertor, 0: No desertor
```

### 1.3 Métricas de Evaluación
Dado que la deserción puede ser una clase desbalanceada:
- **Accuracy**: Precisión global
- **Precision**: De los predichos como desertores, cuántos realmente lo son
- **Recall (Sensibilidad)**: De los desertores reales, cuántos detectamos
- **F1-Score**: Media armónica de Precision y Recall
- **ROC-AUC**: Área bajo la curva ROC
- **Matriz de Confusión**: Análisis de TP, FP, TN, FN

**Métrica Principal**: **F1-Score** (balance entre precision y recall)

## 2. Preparación de Datos para ML

### 2.1 Selección de Features
```python
# Features demográficas
demographic_features = [
    'edad', 'genero', 'estrato',
    'origen_geografico', 'departamento'
]

# Features académicas
academic_features = [
    'facultad', 'programa', 'nivel_academico',
    'modalidad', 'jornada', 'sede'
]

# Features temporales
temporal_features = [
    'periodo_año', 'semestre', 'periodo_num'
]

# Todas las features
X_features = demographic_features + academic_features + temporal_features
```

### 2.2 Feature Engineering

#### Variables Derivadas
```python
# Grupo etario
df['grupo_edad'] = pd.cut(df['edad'],
    bins=[0, 20, 25, 30, 100],
    labels=['16-20', '21-25', '26-30', '31+'])

# Grupo estrato
df['grupo_estrato'] = pd.cut(df['estrato'].astype(float),
    bins=[0, 2, 4, 6],
    labels=['Bajo', 'Medio', 'Alto'])

# Es primera matrícula
df['primer_semestre'] = (df['periodo_num'] == 1).astype(int)

# Modalidad es virtual
df['es_virtual'] = (df['modalidad'].isin(['VIRTUAL', 'DISTANCIA'])).astype(int)
```

#### Codificación de Variables
```python
# One-Hot Encoding para categóricas nominales
categorical_features = ['genero', 'modalidad', 'jornada']
df_encoded = pd.get_dummies(df, columns=categorical_features, drop_first=True)

# Label Encoding para categóricas ordinales
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
df['estrato_encoded'] = le.fit_transform(df['estrato'])

# Target Encoding para alta cardinalidad
from category_encoders import TargetEncoder
te = TargetEncoder()
df['programa_encoded'] = te.fit_transform(df['programa'], df['es_desertor'])
```

### 2.3 Manejo de Desbalanceo de Clases

#### Análisis de Desbalanceo
```python
class_distribution = df['es_desertor'].value_counts(normalize=True)
print(class_distribution)
# Ejemplo:
# 0 (No desertor):    0.75 (75%)
# 1 (Desertor):       0.25 (25%)
```

#### Técnicas de Balanceo
```python
from imblearn.over_sampling import SMOTE, ADASYN
from imblearn.under_sampling import RandomUnderSampler
from imblearn.combine import SMOTETomek

# Opción 1: SMOTE (Synthetic Minority Over-sampling)
smote = SMOTE(random_state=42)
X_resampled, y_resampled = smote.fit_resample(X_train, y_train)

# Opción 2: Class weights (en el modelo)
class_weight = {0: 1, 1: 3}  # Dar más peso a clase minoritaria
```

### 2.4 División de Datos
```python
from sklearn.model_selection import train_test_split

# División: 70% train, 15% validation, 15% test
X_train, X_temp, y_train, y_temp = train_test_split(
    X, y, test_size=0.30, random_state=42, stratify=y
)
X_val, X_test, y_val, y_test = train_test_split(
    X_temp, y_temp, test_size=0.50, random_state=42, stratify=y_temp
)

print(f"Train: {len(X_train)}, Val: {len(X_val)}, Test: {len(X_test)}")
```

### 2.5 Normalización y Escalado
```python
from sklearn.preprocessing import StandardScaler, MinMaxScaler

# Escalar features numéricas
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_val_scaled = scaler.transform(X_val)
X_test_scaled = scaler.transform(X_test)
```

## 3. Modelos a Evaluar

### 3.1 Baseline: Dummy Classifier
```python
from sklearn.dummy import DummyClassifier

# Baseline: Predecir siempre la clase mayoritaria
dummy_clf = DummyClassifier(strategy='most_frequent')
dummy_clf.fit(X_train, y_train)
baseline_score = dummy_clf.score(X_val, y_val)
```

### 3.2 Modelos Lineales

#### Regresión Logística
```python
from sklearn.linear_model import LogisticRegression

lr = LogisticRegression(
    max_iter=1000,
    class_weight='balanced',
    random_state=42
)
lr.fit(X_train_scaled, y_train)
```

### 3.3 Modelos Basados en Árboles

#### Decision Tree
```python
from sklearn.tree import DecisionTreeClassifier

dt = DecisionTreeClassifier(
    max_depth=10,
    min_samples_split=20,
    min_samples_leaf=10,
    class_weight='balanced',
    random_state=42
)
dt.fit(X_train, y_train)
```

#### Random Forest
```python
from sklearn.ensemble import RandomForestClassifier

rf = RandomForestClassifier(
    n_estimators=100,
    max_depth=15,
    min_samples_split=10,
    class_weight='balanced',
    random_state=42,
    n_jobs=-1
)
rf.fit(X_train, y_train)
```

#### Gradient Boosting (XGBoost)
```python
import xgboost as xgb

# Calcular scale_pos_weight para desbalanceo
scale_pos_weight = (y_train == 0).sum() / (y_train == 1).sum()

xgb_clf = xgb.XGBClassifier(
    n_estimators=100,
    max_depth=6,
    learning_rate=0.1,
    scale_pos_weight=scale_pos_weight,
    random_state=42,
    use_label_encoder=False,
    eval_metric='logloss'
)
xgb_clf.fit(X_train, y_train)
```

#### LightGBM
```python
import lightgbm as lgb

lgb_clf = lgb.LGBMClassifier(
    n_estimators=100,
    max_depth=10,
    learning_rate=0.05,
    class_weight='balanced',
    random_state=42
)
lgb_clf.fit(X_train, y_train)
```

### 3.4 Modelos de Ensamble

#### Voting Classifier
```python
from sklearn.ensemble import VotingClassifier

voting_clf = VotingClassifier(
    estimators=[
        ('lr', lr),
        ('rf', rf),
        ('xgb', xgb_clf)
    ],
    voting='soft'  # Usa probabilidades
)
voting_clf.fit(X_train, y_train)
```

#### Stacking Classifier
```python
from sklearn.ensemble import StackingClassifier

stacking_clf = StackingClassifier(
    estimators=[
        ('rf', rf),
        ('xgb', xgb_clf),
        ('lgb', lgb_clf)
    ],
    final_estimator=LogisticRegression(),
    cv=5
)
stacking_clf.fit(X_train, y_train)
```

## 4. Evaluación de Modelos

### 4.1 Función de Evaluación
```python
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, roc_auc_score, classification_report,
    confusion_matrix
)

def evaluate_model(model, X, y, model_name):
    # Predicciones
    y_pred = model.predict(X)
    y_pred_proba = model.predict_proba(X)[:, 1]

    # Métricas
    results = {
        'Model': model_name,
        'Accuracy': accuracy_score(y, y_pred),
        'Precision': precision_score(y, y_pred),
        'Recall': recall_score(y, y_pred),
        'F1-Score': f1_score(y, y_pred),
        'ROC-AUC': roc_auc_score(y, y_pred_proba)
    }

    return results
```

### 4.2 Comparación de Modelos
```python
models = {
    'Logistic Regression': lr,
    'Decision Tree': dt,
    'Random Forest': rf,
    'XGBoost': xgb_clf,
    'LightGBM': lgb_clf,
    'Voting': voting_clf
}

results = []
for name, model in models.items():
    result = evaluate_model(model, X_val, y_val, name)
    results.append(result)

results_df = pd.DataFrame(results)
results_df = results_df.sort_values('F1-Score', ascending=False)
print(results_df)
```

### 4.3 Matriz de Confusión
```python
import matplotlib.pyplot as plt
import seaborn as sns

def plot_confusion_matrix(y_true, y_pred, title):
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.title(f'Confusion Matrix - {title}')
    plt.ylabel('Actual')
    plt.xlabel('Predicted')
    plt.show()
```

### 4.4 Curva ROC
```python
from sklearn.metrics import roc_curve, auc

def plot_roc_curve(models_dict, X, y):
    plt.figure(figsize=(10, 8))

    for name, model in models_dict.items():
        y_pred_proba = model.predict_proba(X)[:, 1]
        fpr, tpr, _ = roc_curve(y, y_pred_proba)
        roc_auc = auc(fpr, tpr)

        plt.plot(fpr, tpr, label=f'{name} (AUC = {roc_auc:.3f})')

    plt.plot([0, 1], [0, 1], 'k--', label='Random')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC Curves Comparison')
    plt.legend()
    plt.grid(True)
    plt.show()
```

## 5. Optimización de Hiperparámetros

### 5.1 Grid Search
```python
from sklearn.model_selection import GridSearchCV

param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [5, 10, 15, 20],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}

grid_search = GridSearchCV(
    RandomForestClassifier(random_state=42),
    param_grid,
    cv=5,
    scoring='f1',
    n_jobs=-1,
    verbose=1
)

grid_search.fit(X_train, y_train)
best_rf = grid_search.best_estimator_
print(f"Best params: {grid_search.best_params_}")
```

### 5.2 Random Search
```python
from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import randint, uniform

param_distributions = {
    'n_estimators': randint(50, 200),
    'max_depth': randint(5, 30),
    'learning_rate': uniform(0.01, 0.3),
    'subsample': uniform(0.6, 0.4)
}

random_search = RandomizedSearchCV(
    xgb.XGBClassifier(random_state=42),
    param_distributions,
    n_iter=50,
    cv=5,
    scoring='f1',
    random_state=42,
    n_jobs=-1
)

random_search.fit(X_train, y_train)
best_xgb = random_search.best_estimator_
```

### 5.3 Optuna (Bayesian Optimization)
```python
import optuna

def objective(trial):
    params = {
        'n_estimators': trial.suggest_int('n_estimators', 50, 300),
        'max_depth': trial.suggest_int('max_depth', 3, 20),
        'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.3),
        'subsample': trial.suggest_float('subsample', 0.6, 1.0)
    }

    model = xgb.XGBClassifier(**params, random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_val)

    return f1_score(y_val, y_pred)

study = optuna.create_study(direction='maximize')
study.optimize(objective, n_trials=100)

print(f"Best F1: {study.best_value}")
print(f"Best params: {study.best_params}")
```

## 6. Interpretabilidad del Modelo

### 6.1 Feature Importance
```python
# Para modelos basados en árboles
feature_importance = pd.DataFrame({
    'feature': X.columns,
    'importance': best_model.feature_importances_
}).sort_values('importance', ascending=False)

# Visualización
plt.figure(figsize=(10, 8))
plt.barh(feature_importance['feature'][:15],
         feature_importance['importance'][:15])
plt.xlabel('Importance')
plt.title('Top 15 Feature Importances')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()
```

### 6.2 SHAP Values
```python
import shap

# Crear explainer
explainer = shap.TreeExplainer(best_model)
shap_values = explainer.shap_values(X_test)

# Summary plot
shap.summary_plot(shap_values, X_test, plot_type="bar")

# Dependence plot para feature específica
shap.dependence_plot("estrato", shap_values, X_test)

# Force plot para una predicción individual
shap.force_plot(explainer.expected_value,
                shap_values[0],
                X_test.iloc[0])
```

### 6.3 LIME (Local Interpretable Model-agnostic Explanations)
```python
import lime
import lime.lime_tabular

explainer = lime.lime_tabular.LimeTabularExplainer(
    X_train.values,
    feature_names=X_train.columns,
    class_names=['No Desertor', 'Desertor'],
    mode='classification'
)

# Explicar una predicción
i = 0  # Índice del ejemplo
exp = explainer.explain_instance(X_test.values[i],
                                  best_model.predict_proba)
exp.show_in_notebook()
```

## 7. Evaluación Final en Test Set

```python
# Mejor modelo seleccionado
final_model = best_xgb  # o el modelo con mejor F1-Score

# Predicción en test set
y_test_pred = final_model.predict(X_test)
y_test_proba = final_model.predict_proba(X_test)[:, 1]

# Métricas finales
print("=" * 50)
print("EVALUACIÓN FINAL EN TEST SET")
print("=" * 50)
print(classification_report(y_test, y_test_pred))

# Matriz de confusión
plot_confusion_matrix(y_test, y_test_pred, 'Test Set')

# ROC-AUC
test_roc_auc = roc_auc_score(y_test, y_test_proba)
print(f"\nROC-AUC Score: {test_roc_auc:.4f}")
```

## 8. Persistencia del Modelo

```python
import joblib
import pickle

# Guardar modelo
joblib.dump(final_model, 'src/models/desercion_model.pkl')

# Guardar scaler
joblib.dump(scaler, 'src/models/scaler.pkl')

# Guardar encoder
joblib.dump(encoder, 'src/models/encoder.pkl')

# Cargar modelo
loaded_model = joblib.load('src/models/desercion_model.pkl')
```

## 9. Validación Cruzada

```python
from sklearn.model_selection import cross_val_score, StratifiedKFold

skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

cv_scores = cross_val_score(
    final_model,
    X_train,
    y_train,
    cv=skf,
    scoring='f1',
    n_jobs=-1
)

print(f"CV F1-Scores: {cv_scores}")
print(f"Mean F1-Score: {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")
```

## 10. Integración con Dashboard

```python
def predict_student_risk(student_features):
    """
    Predice el riesgo de deserción de un estudiante

    Args:
        student_features: dict con características del estudiante

    Returns:
        dict con predicción y probabilidad
    """
    # Cargar modelo
    model = joblib.load('src/models/desercion_model.pkl')
    scaler = joblib.load('src/models/scaler.pkl')

    # Preparar features
    X = prepare_features(student_features)
    X_scaled = scaler.transform(X)

    # Predecir
    prediction = model.predict(X_scaled)[0]
    probability = model.predict_proba(X_scaled)[0, 1]

    # Clasificar riesgo
    if probability > 0.7:
        risk_level = "Alto"
    elif probability > 0.4:
        risk_level = "Medio"
    else:
        risk_level = "Bajo"

    return {
        'prediction': int(prediction),
        'probability': float(probability),
        'risk_level': risk_level
    }
```

## 11. Código de Referencia

**Notebook**: `notebooks/05_ML_Model.ipynb`

**Scripts**:
- `src/models/train_model.py`: Entrenamiento del modelo
- `src/models/evaluate_model.py`: Evaluación de modelos
- `src/models/predict.py`: Predicciones
- `src/models/interpret.py`: Interpretabilidad

## 12. Conclusiones del Modelo

### Resultados Esperados
- **Accuracy**: > 80%
- **F1-Score**: > 0.75
- **ROC-AUC**: > 0.85
- **Recall**: > 70% (importante detectar desertores)

### Mejor Modelo
*(Se completará después de la ejecución)*

### Features Más Importantes
*(Se completará con SHAP/Feature Importance)*

## 13. Próximos Pasos

- ✓ Modelo entrenado y validado
- → Documentar conclusiones
- → Crear recomendaciones
- → Preparar presentación

---

**Responsable**: Aprendizaje Computacional - Prof. July Galeano
**Estado**: En Desarrollo
**Última actualización**: Noviembre 2025
