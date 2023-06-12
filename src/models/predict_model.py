# Código de predicciones de fuga
############################################################################

import pandas as pd
import pickle
import os


# Cargar la tabla transformada
def score_model(filename, scores):
    df = pd.read_csv(os.path.join('data/processed/', filename))
    print(filename, ' cargado correctamente')
    # Leemos el modelo entrenado para usarlo
    package = 'models/best_model.pkl'
    model = pickle.load(open(package, 'rb'))
    print('Modelo importado correctamente')
    # Predecimos sobre el set de datos   
    
    res = model.predict(df).reshape(-1,1)
    pred = pd.DataFrame(res, columns=['PREDICT'])
    pred.to_csv(os.path.join('data/external/', scores))
    print(scores, 'exportado correctamente en la carpeta external')


# Scoring desde el inicio
def main():
    df = score_model('raw_s.csv','prediction.csv')
    print('Finalizó predicción del Modelo')


if __name__ == "__main__":
    main()