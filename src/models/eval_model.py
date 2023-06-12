# Código de Evaluación - Modelo de Riesgo de Fuga
############################################################################

import pandas as pd
from sklearn import metrics
from sklearn.ensemble import RandomForestClassifier
import pickle
import matplotlib.pyplot as plt
from sklearn.metrics import *
import os


# Cargar la tabla transformada
def eval_model(filename):
    df = pd.read_csv(os.path.join('data/processed/', filename))
    print(filename, ' cargado correctamente')
    # Leemos el modelo entrenado para usarlo
    package = 'models/best_model.pkl'
    model = pickle.load(open(package, 'rb'))
    print('Modelo importado correctamente')
    # Predecimos sobre el set de datos de validación 
    X_test = df.drop(['churn', "id"],axis=1)
    y_test = df[['churn']]
    y_pred_test=model.predict(X_test)
    # Generamos métricas de diagnóstico
    cm_test = confusion_matrix(y_test,y_pred_test)
    print("Matriz de confusion: ")
    print(cm_test)
    accuracy_test=accuracy_score(y_test,y_pred_test)
    print("Accuracy: ", accuracy_test)
    precision_test=precision_score(y_test,y_pred_test)
    print("Precision: ", precision_test)
    recall_test=recall_score(y_test,y_pred_test)
    print("Recall: ", recall_test)
    print("================================================================")
   
    fig, ax = plt.subplots(figsize=(7.5, 7.5))
    ax.matshow(cm_test, cmap=plt.cm.Blues, alpha=0.3)
    for i in range(cm_test.shape[0]):
        for j in range(cm_test.shape[1]):
            ax.text(x=j, y=i,s=cm_test[i, j], va='center', ha='center', size='xx-large')
    
    plt.xlabel('Predictions', fontsize=18)
    plt.ylabel('Actuals', fontsize=18)
    plt.title('Confusion Matrix', fontsize=18)
    plt.savefig('src/visualization/confusion_matrix.png', format='png')
    plt.show()
  
# Validación desde el inicio
def main():
    df = eval_model('raw_v.csv')
    print('Finalizó la validación del Modelo')


if __name__ == "__main__":
    main()