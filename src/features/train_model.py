import pandas as pd
import pickle
import os
from sklearn.ensemble import RandomForestClassifier

# Cargar la tabla transformada
def read_file_csv(filename):
    df = pd.read_csv(os.path.join('data/processed/', filename))
    X_train = df.drop(['churn','id'],axis=1)
    y_train = df['churn']
    print(filename, ' cargado correctamente')
    # Entrenamos el modelo con toda la muestra
    rf_model = RandomForestClassifier(n_estimators=100)
    rf_model.fit(X_train, y_train)
    print('Modelo entrenado')
    # Guardamos el modelo entrenado para usarlo en produccion
    package = 'models/best_model.pkl'
    pickle.dump(rf_model, open(package, 'wb'))
    print('Modelo exportado correctamente en la carpeta models')


# Entrenamiento completo
def main():
    read_file_csv('raw_t.csv')
    print('Finalizó el entrenamiento del Modelo')


if __name__ == "__main__":
    main()