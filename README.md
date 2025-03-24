## Plataforma de Predicción de Admisiones Universitarias Mediante Modelos de Aprendizaje Automático

### Tabla de Contenidos

*   [Nombre](#nombre)
*   [Descripción](#descripción)
*   [Arquitectura](#arquitectura)
*   [Proceso](#proceso)
*   [Funcionalidades](#funcionalidades)
*   [Estado del proyecto](#estado-del-proyecto)

### Nombre

Plataforma de Predicción de Admisiones Universitarias Mediante Modelos de Aprendizaje Automático

### Descripción

Aplicación que, basada en datos de diferentes fuentes (exámenes como el GRE, TOEFL; y CV, experiencia y cartas de recomendación), calcula la probabilidad de ser admitido en diferentes universidades alrededor del mundo. Además, proporciona consejos e identifica áreas de mejora para que el usuario sepa cómo aumentar sus posibilidades de admisión.

![image](https://github.com/user-attachments/assets/9595b559-3c2b-4e07-8923-b8e4ce122342)

![image](https://github.com/user-attachments/assets/7e48ebe2-21fb-4774-a9ea-6ff60a939a33)

### Arquitectura

#### Backend:

*   Se utiliza FastAPI para exponer el modelo de predicción.
*   El modelo se basa en Random Forest, entrenado con los datos.
*   No se almacena información de los usuarios.

#### Frontend:

*   La interfaz se ha desarrollado en Bootstrap, permitiendo una visualización responsive y amigable.

### Proceso

#### Fuente del Dataset

*   Se utilizó el dataset Graduate Admission 2 obtenido de Kaggle.
*   https://www.kaggle.com/datasets/mohansacharya/graduate-admissions

#### Preparación y Limpieza de Datos

*   Se importaron las librerías necesarias (pandas, numpy, matplotlib, seaborn, entre otras).
*   Se cargó el archivo Admission\_Predict\_Ver1.1.csv y se realizó una exploración inicial para comprender su estructura.
*   Se identificaron y trataron valores faltantes, se normalizaron y transformaron las variables.
*   Se generaron gráficos y se calcularon estadísticas descriptivas para validar la calidad y consistencia del dataset.

#### Manejo de Excepciones y Control de Errores

*   Se implementaron bloques try-except para capturar y gestionar errores durante la carga y el procesamiento de datos.
*   Se validaron las entradas de datos para asegurar que el modelo reciba información correcta y consistente.

#### Análisis Estadístico

*   Se calcularon valores descriptivos (media, mediana, desviación estándar, etc.) para cada variable.
*   Se generaron visualizaciones (histogramas, gráficos de dispersión, mapas de calor) para analizar la distribución de los datos y las relaciones entre variables.
*   Se aplicaron técnicas de detección y tratamiento de outliers, utilizando métodos como el modelo de mínima covarianza robusta y análisis con la distribución chi-cuadrado.

#### Entrenamiento del Modelo

* Se entrenó un modelo de Random Forest para predecir la probabilidad de admisión.

* Se dividieron los datos en conjuntos de entrenamiento y prueba para evaluar el rendimiento del modelo.

* Se calcularon métricas de rendimiento como el error cuadrático medio (MSE), error absoluto medio (MAE) y el coeficiente de determinación ($R^2$).

  $$
  \begin{aligned}
  MSE &= \frac{1}{n} \sum_{i=1}^{n} (Y_i - \hat{Y}_i)^2 \\
  MAE &= \frac{1}{n} \sum_{i=1}^{n} |Y_i - \hat{Y}_i| \\
  R^2 &= 1 - \frac{\sum_{i=1}^{n} (Y_i - \hat{Y}_i)^2}{\sum_{i=1}^{n} (Y_i - \bar{Y})^2}
  \end{aligned}
  $$

### Funcionalidades

#### Integración en una Página Web:

*   La plataforma se carga en una página web prototipo desarrollada con Bootstrap, lo que permite una visualización responsive y una interfaz sencilla para el usuario.
*   Si se desarrollan integraciones adicionales (por ejemplo, en canales como WhatsApp, Discord, Telegram, o mediante una interfaz gráfica más avanzada), se actualizará esta sección con los detalles correspondientes.

### Estado del Proyecto

#### Fase de Desarrollo:

*   Actualmente, la plataforma se encuentra en fase de desarrollo, en la que se están realizando pruebas y mejoras continuas.

