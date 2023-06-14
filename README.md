churn prediction and price sensiivity
========================================================================================================================================
El proyecto consiste determinar la siguiente hipotesis:
PowerCo es una empresa que brinda servicios de energia y gas, y en los ultimo meses han tenido clientes que han estado dejando los servicios. Ellos creen que es debido a los precios, y necesitan determinar si la variacion de precios ha determinado la fuga de clientes, ademas necesitan saber si darle un 20% de descuento ayudaria en detener la fuga de clientes y necesitan determinar si este descuento afectaría negativamente a la empresa.

Para solucionar el problema, se hizo un EDA de los datos 'client_data.csv' y 'price_data.csv'; se unieron ambos archivos en un DF y se uso la variacion de precios picos y precios mas bajos en los meses iniciales y finales del años, determinando así que la sensibilidad del precio no afecta a la fuga de clientes.

Finalmente se realizó el Feature Engineering para modelar los datos y usar el modelo RandomForest para determinar la probabilidad de fuga de clientes. Se hizo la simulación de descuento a los clientes con probabilidad alta de gufa y se determinó que no hay perdidas para la empresa, al contratio se tendría ganancias. 

========================================================================================================================================

The project aims to determine the following hypothesis:

PowerCo is a company that provides energy and gas services, and in recent months, they have experienced customers leaving their services. They believe this is due to prices, and they need to determine if the price variation has been the determining factor behind customer churn. Additionally, they need to assess whether offering a 20% discount would help in preventing customer churn and determine if this discount would have any negative impact on the company.

To address this issue, an Exploratory Data Analysis (EDA) was conducted on the 'client_data.csv' and 'price_data.csv' datasets. Both files were merged into a single DataFrame, and the variation in peak and lowest prices during the initial and final months of the year was examined. The analysis determined that price sensitivity does not affect customer churn.

Finally, Feature Engineering was performed to model the data, and the RandomForest model was used to determine the probability of customer churn. A simulation was conducted, applying the discount to customers with a high probability of churn, and it was determined that there would be no losses for the company. On the contrary, there would be gains.

Project Organization
------------

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io


--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
