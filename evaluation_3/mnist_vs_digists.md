# MNIST.ipynb vs digits.ipynb - Comparison
## Spanish version

### MNIST.ipynb
- **Dataset**: Utiliza el dataset MNIST completo original con imágenes de **28x28 píxeles**. Los datos se cargan desde archivos locales (.idx3-ubyte).
- **Modelo**: Implementa una Red Neuronal Convolucional (CNN), que es un modelo de **aprendizaje profundo** diseñado específicamente para reconocimiento de imágenes.
- **Librerías**: Utiliza las librerías **TensorFlow y Keras** para construir, entrenar y evaluar la red neur
onal.
- **Proceso**: El notebook cubre un flujo de trabajo completo de aprendizaje profundo:
  1. Carga y preprocesamiento de datos (normalización, codificación one-hot)
  2. Construcción de una arquitectura CNN multicapa
  3. Entrenamiento del modelo a lo largo de múltiples épocas
  4. Evaluación del rendimiento y visualización de resultados (gráficos de precisión/pérdida)
  5. Guardado del modelo entrenado y uso para predecir en una imagen personalizada nueva

### digits.ipynb
- **Dataset**: Utiliza el dataset `digits` incluido en la librería scikit-learn. Esta es una versión mucho más pequeña y de menor resolución (**8x8 píxeles**) del dataset MNIST.
- **Modelo**: Utiliza una Máquina de Vectores de Soporte (SVM), que es un algoritmo clásico de **aprendizaje automático**, no un modelo de aprendizaje profundo.
- **Librerías**: Depende completamente de la librería **scikit-learn para la carga de datos, entrenamiento del modelo y evaluación**.
- **Proceso**: Este notebook demuestra un enfoque más tradicional de aprendizaje automático:
  1. Carga del dataset desde scikit-learn
  2. División de los datos en conjuntos de entrenamiento y prueba
  3. Entrenamiento del clasificador SVM
  4. Evaluación del modelo usando un reporte de clasificación y una matriz de confusión

### Resumen de Diferencias Clave

| Característica | MNIST.ipynb | digits.ipynb |
|----------------|-------------|--------------|
| Dataset | MNIST completo (imágenes 28x28) | Digits de scikit-learn (imágenes 8x8) |
| Tecnología | Aprendizaje Profundo (TensorFlow/Keras) | Aprendizaje Automático Clásico (Scikit-learn) |
| Modelo | Red Neuronal Convolucional (CNN) | Máquina de Vectores de Soporte (SVM) |
| Complejidad | Mayor complejidad, más intensivo computacionalmente | Más simple, más rápido de entrenar |
| Alcance | Proyecto integral de aprendizaje profundo | Ejemplo sencillo de clasificación |



## English Version
### MNIST.ipynb
- **Dataset**: Uses the original, full MNIST dataset with 28x28 pixel images. The data is loaded from local files (.idx3-ubyte).
- **Model**: Implements a Convolutional Neural Network (CNN), which is a deep learning model specifically designed for image recognition.
- **Libraries**: Uses the TensorFlow and Keras libraries to build, train, and evaluate the neural network.
- **Process**: The notebook covers a complete deep learning workflow:
  1. Loading and preprocessing the data (normalization, one-hot encoding)
  2. Building a multi-layer CNN architecture
  3. Training the model over multiple epochs
  4. Evaluating performance and visualizing results (accuracy/loss graphs)
  5. Saving the trained model and using it to predict on a new, custom image

### digits.ipynb

- **Dataset**: Uses the [`digits`](https://scikit-learn.org/stable/auto_examples/classification/plot_digits_classification.html) dataset included with the scikit-learn library. This is a much smaller and lower-resolution (8x8 pixels) version of the MNIST dataset.
- **Model**: Uses a Support Vector Machine (SVM), which is a classic machine learning algorithm, not a deep learning model.
- **Libraries**: Relies entirely on the scikit-learn library for data loading, model training, and evaluation.
- **Process**: This notebook demonstrates a more traditional machine learning approach:
  1. Loading the dataset from scikit-learn
  2. Splitting the data into training and testing sets
  3. Training the SVM classifier
  4. Evaluating the model using a classification report and a confusion matrix

### Summary of Key Differences

| Feature | MNIST.ipynb | digits.ipynb |
|---------|-------------|--------------|
| Dataset | Full MNIST (28x28 images) | Scikit-learn's digits (8x8 images) |
| Technology | Deep Learning (TensorFlow/Keras) | Classic Machine Learning (Scikit-learn) |
| Model | Convolutional Neural Network (CNN) | Support Vector Machine (SVM) |
| Complexity | Higher complexity, more computationally intensive | Simpler, faster to train |
| Scope | End-to-end deep learning project | A straightforward classification example |




## Concepts and Terms
### MNIST
1. Convolution layer: Detects patterns and characteristics in images, extracts features from images and groups them into larger features.
2. Max pooling layer: Reduces the dimensionality of the data and keeps the most important information.
3. Dense layer: 
Capas Convolucionales/Pooling: Son como tus ojos y corteza visual. Detectan que hay "bigotes", "pelaje rayado", "cola larga" y "un tamaño mediano".

Capa Densa: Es como tu cerebro razonando. Toda esa información visual llega a tu cerebro, que combina esos rasgos y concluye: "Todas estas características juntas me hacen pensar que es un 85% de probabilidad de que sea un gato atigrado, un 10% de que sea un zorro, y un 5% de otra cosa".