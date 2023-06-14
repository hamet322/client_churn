churn client prediction and price sensitivity

### Paso 1: Clonar el Proyecto desde su propio Github

```
git clone https://github.com/hamet322/client_churn
```

### Paso 2: Instalar los pre-requisitos

```
cd client_churn/
pip install -r requirements.txt
```

### Paso 3: Ejecutar las pruebas en el entorno

```
cd src

python data_model/make_dataset.py

python features/train_model.py

python models/eval_model.py

python models/predict_model.py
```