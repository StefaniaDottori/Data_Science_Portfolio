# -*- coding: utf-8 -*-
"""Preprocessing_ML_Telco.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1RRRr2UI2wMfFuw6Tlb158NBnC_nJ_k9H

# SUP ML 1 - PREPROCESSING

# Librerias
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import warnings
warnings.filterwarnings("ignore")

"""# Importar train data"""

from google.colab import drive
drive.mount('/content/drive')

df = pd.read_csv("/content/drive/MyDrive/DSC 0523– Entregable 2 - Borrero, Dottori, He/Modelo/EJERCICIO-ML-Sup/data/telecom_churn_TRAINTEST.csv")

var_dic = pd.read_csv ('/content/drive/MyDrive/DSC 0523– Entregable 2 - Borrero, Dottori, He/Modelo/EJERCICIO-ML-Sup/data/variable_dictionary.csv')

df.set_index('Customer_ID', inplace=True)

print('Se define {Customer_ID} como indice')

"""# EDA: Analisis Exploratorio"""

df.head()

df.info()

"""## Distribución del target"""

df['churn'].value_counts()

target = 'churn'
features = df.columns[df.columns!=target]

df.hist('churn')

proportion_churn = (df['churn'].value_counts()) / (len(df['churn'])) *100
proportion_churn

print(f'La distribucion de clientes que abandonan o permanecen en el servicio es proporcional')
print(f'{proportion_churn}')

df['churn']

X = df[features]

y = df[target]

sns.distplot(y)
plt.title('Distribucion del target: '+target)
plt.show()

# Se observa un churn en densidades equivalentes. Las distribucones en estandares y varianza se asemejan

"""## Analisis Univariable

* Distribucion de cada variable
"""

for i in features:
 if df[i].dtype.kind=="i" or df[i].dtype.kind=="f":
  sns.distplot(X[i])
  plt.title('Distribucion '+ i)
  plt.show()

    #declaramos for loop para graficar variables numericas.

"""## Analisis Variable-Target

* Relacion target-variable: se revisaron las variables por diccionario para comprender cual seria mejor de relacionar con el target. Hemos propuesto 5 graficos para ver el comportamiento del target en relacion a:
1. Mean overage minutes of use (ovrmou) / churn
2. Mean number of monthly minutes of use (mou) / churn
3. Number of models issued (models) / churn
4. Estimated income (income) / churn
"""

var_dic

var_dic.iloc[4,:]

#localizamos nombre de la variable con su posicionamiento de index columna y fila

f = sns.relplot(x='churn', y='ovrmou', data= df, color = 'orange')
f.fig.suptitle("Mean OVERAGE minutes of use/ target")
f.fig.subplots_adjust(top = 0.9)

#se observan valores similares de tiempo de uso excesivo (overage) del servicio en ambos grupos, por lo que no seria una variable
#que nos ayude a determinar si es una causa de abandono. El valor que se encuentra por encima de 4000 min, podria
#tratarse de un outlier

var_dic.iloc[1,:]

a = sns.catplot(x='churn', y='mou', kind='violin', split=True, bw=.50, color='pink', data= df)
a.fig.suptitle("Mean number of monthly minutes of use/ target")
a.fig.subplots_adjust(top = 0.9)

# al relacion el tiempo de uso promedio del servicio al mes, se observa un comportamiento simil en ambos
#grupos de clientes. La distribucion de densidades dada por el 'ancho' del violin, tambien se
#asemejan . Esta variable podria no tener impacto al momento de entender la razon de abandono.

var_dic.iloc[76, :]

a = sns.catplot(x='churn', y='models', kind='violin', split=True, bw=.50, color='green', data= df)
a.fig.suptitle("Number of models issued/ target")
a.fig.subplots_adjust(top = 0.9)

#el numero de modelos adquiridos durante la permanencia del cliente en ambos grupos es similar.
#esta variable, no nos aporta informacion valiosa para entender el motivo de abandono.

var_dic.iloc[86, :]

w = sns.displot(x='churn', y='income', color='orange', rug = True, kind = 'kde' , data= df)
w.fig.suptitle("Estimated income/ target")
w.fig.subplots_adjust(top = 0.9)

#podemos observar que el ingreso estimado de los clientes que abandonan o permanecen en el servicio
#es muy parecido, de modo que su capacidad economica tampoco es una variable que nos ayude a
#comprender el problema .

"""# Data Cleaning

* Eliminar filas sin target informado.
* Eliminar filas duplicadas (si tenemos ID, solo puede haber 1 registro por ID)
* Eliminar filas/columnas vacías y columnas irrelevantes
* Corregir data types incorrectos
* Categoricos: Corregir literales incorrectos (acentos, erratas, etc)
* Fechas y textos: convertir a variables numericas (hour, day, month, year...) o categoricas (weekday_name...)

# Imputación de nulos

* MODELOS DE ARBOLES: Imputar valor outlier.
* MODELOS LINEALES: imputar media, mediana o moda.
* Si vamos a practicar un Torneo de Modelos, preferible imputar valor outlier.
"""

df.shape

df.isnull().values.any()

df.info()

df.isnull().sum()

"""Comenzamos imputacion de nulos por orden de columna"""

var_dic.iloc[0,:]

df['rev'].isnull().sum()

df['rev'].max()

df['rev'].min()

#como se trata de dinero, revisamos valores por debajo de Cero ya que no tendrian sentido

df['rev'] = np.where(df['rev']<0, df['rev'] == 0, df['rev'])

df['rev'].min()

df['rev'].fillna(-999, inplace = True)

df['rev'].isnull().sum()

df.hist('rev', bins = 5)

var_dic.iloc[1,:]

df['mou'].isnull().sum()

df['mou'].max()

df['mou'].min()

df['mou'].fillna(-999, inplace = True)

df['mou'].isnull().sum()

#totmrc : 	Mean total monthly recurring charge

var_dic.iloc[2,:]

df['totmrc'].max()

df['totmrc'].min()

df['totmrc'] = np.where(df['totmrc']<0, df['totmrc'] == 0, df['totmrc'])

df['totmrc'].isnull().sum()

df['totmrc'].fillna(-999, inplace = True)

df['totmrc'].isnull().sum()

#columna 3 : da	- Mean number of directory assisted calls

var_dic.iloc[3, :]

df['da'].isnull().sum()

df['da'].max()

df['da'].min()

df['da'].fillna(-999, inplace = True)

df['da'].isnull().sum()

#columna 4 : 4	ovrmou	Mean overage minutes of use

var_dic.iloc[4, :]

df['ovrmou'].isnull().sum()

df['ovrmou'].max()

df['ovrmou'].min()

df['ovrmou'].fillna(-999, inplace = True)

df['ovrmou'].isnull().sum()

#columna 5 : ovrrev : Mean overage revenue

var_dic.iloc[5, :]

df['ovrrev'].max()

df['ovrrev'].min()

df['ovrrev'].isnull().sum()

df['ovrrev'].fillna(-999, inplace = True)

df['ovrrev'].isnull().sum()

#columna 6 : vceovr : Mean revenue of voice overage

var_dic.iloc[6, :]

df['vceovr'].isnull().sum()

df['vceovr'].max()

df['vceovr'].min()

df['vceovr'].fillna(-999, inplace = True)

df['vceovr'].isnull().sum()

#columna 7 : datovr : Mean revenue of data overage

var_dic.iloc[7, :]

df['datovr'].max()

df['datovr'].min()

df['datovr'].isnull().sum()

df['datovr'].fillna(-999, inplace = True)

df['datovr'].isnull().sum()

#columna 8 : roam : Mean number of roaming calls

var_dic.iloc[8,:]

df['roam'].max()

df['roam'].min()

df['roam'].isnull().sum()

df['roam'].fillna(-999, inplace = True)

df['roam'].isnull().sum()

#columna 9: change_mou : Percentage change in monthly minutes of use

var_dic.iloc[9, :]

df['change_mou'].max()

df['change_mou'].min()    #no son outliers: puede ser que sea una diferencia negativa de uso en minutos.

df['change_mou'].isnull().sum()

#df2 = df.copy()

df['change_mou'].fillna(-999, inplace = True)

df['change_mou'].isnull().sum()

#columna 10 : change_rev : Percentage change in monthly revenue vs previ

var_dic.iloc[10, :]

df['change_rev'].isnull().sum()

df['change_rev'].max()

df['change_rev'].min()

df['change_rev'].fillna(-999, inplace = True)

df['change_rev'].isnull().sum()



"""Aqui terminamos de imputar nulos de las primeras 11 columnas que presentaban NaNs.

Continuamos con las cols de 11-33 revisando outliers . No presentan valores nulos
"""

#columna 11  : Mean number of dropped (failed) voice calls

var_dic.iloc[11, :]

df['drop_vce'].min() #no hay outliers

df['drop_vce'].max()

df['drop_vce'].isnull().sum()

#columna 12: drop_dat : Mean number of dropped (failed) data calls

var_dic.iloc[12, :]

df['drop_dat'].max()

df['drop_dat'].min()

#columna 13: blck_vce: Mean number of blocked (failed) voice calls

var_dic.iloc[13, :]

df['blck_vce'].max()

df['blck_vce'].min()

#columna 14 : blck_dat : Mean number of blocked (failed) data calls

var_dic.iloc[14,:]

df['blck_dat'].max()

df['blck_dat'].min()

#columa 15: unan_vce: Mean number of unanswered voice calls

var_dic.iloc[15,:]

df['unan_vce'].max()

df['unan_vce'].min()

#columna 16 : Mean number of unanswered data calls

var_dic.iloc[16, :]

df['unan_dat'].max()

df['unan_dat'].min()

#columa 17 : plcd_vce : Mean number of attempted voice calls placed

var_dic.iloc[17, :]

df['plcd_vce'].max()

df['plcd_vce'].min()

#columa 18 : plcd_dat : Mean number of attempted data calls placed

var_dic.iloc[18,:]

df['plcd_dat'].max()

df['plcd_dat'].min()

# columna 19 :

var_dic.iloc[19,:]

df['recv_vce'].max()

df['recv_vce'].min()

#reviso las restantes con histograma

cols_a_revisar = ['recv_sms', 'comp_vce', 'comp_dat',
                  'custcare', 'ccrndmou', 'cc_mou', 'inonemin', 'threeway',
                  'threeway', 'mou_cvce', 'mou_cdat', 'mou_rvce', 'owylis_vce',
                  'mouowylisv']

for i in cols_a_revisar:
  print(df.hist(i, bins = 5))

# hasta ahora las primeras 33 columnas : limpias

var_dic.iloc[35,:]

var_dic.iloc[36,:]

var_dic.iloc[37,:]

var_dic.iloc[38,:]

var_dic.iloc[39,:]

var_dic.iloc[40,:]

var_dic.iloc[41,:]

var_dic.iloc[42,:]

var_dic.iloc[43,:]

var_dic.iloc[44,:]

var_dic.iloc[45,:]

var_dic.iloc[46,:]

var_dic.iloc[47,:]

var_dic.iloc[48,:]

var_dic.iloc[49,:]

var_dic.iloc[50,:]

var_dic.iloc[51,:]

var_dic.iloc[52,:]

df['new_cell'].value_counts()

var_dic.iloc[53,:]

var_dic.iloc[54,:]

var_dic.iloc[55,:]

var_dic.iloc[56,:]

var_dic.iloc[57,:]

var_dic.iloc[58,:]

var_dic.iloc[59,:]

var_dic.iloc[60,:]

var_dic.iloc[61,:]

var_dic.iloc[62,:]

var_dic.iloc[63,:]

var_dic.iloc[64,:]

var_dic.iloc[65,:]

var_dic.iloc[66,:]

df.isnull().sum()



"""Desde la Columna 33 a la 67 estan todas completas.
Continuamos analisis de 67 a 99.
"""

# columna 67 : avg6mou : Average monthly minutes of use over the previ

var_dic.iloc[67,:]

#aca

df.hist('avg6mou')

df['avg6mou'].isnull().sum()

df['avg6mou'].fillna(-999, inplace=True)

df['avg6mou'].isnull().sum()

# columna 68 : avg6qty : Average monthly number of calls over the prev

var_dic.iloc[68,:]

df.hist('avg6qty')

df['avg6qty'].isnull().sum()

df['avg6qty'].fillna(-999, inplace=True)

df['avg6rev'].isnull().sum()

# columna 69: avg6rev : Average monthly revenue over the previous six

var_dic.iloc[69,:]

df.hist('avg6rev')

df['avg6rev'].isnull().sum()

df['avg6rev'].fillna(-999, inplace=True)

df['avg6rev'].isnull().sum()

#columna 70 : prizm_social_one : Social group letter only

df['prizm_social_one'].value_counts()

df['prizm_social_one'].isnull().sum()

df['prizm_social_one'].fillna('S', inplace=True)

df['prizm_social_one'].value_counts()

df['prizm_social_one'].isnull().sum()

# columna 71 : area

var_dic.iloc[71,:]

df['area'].isnull().sum()

df['area'].value_counts()

df['area'].fillna('NEW YORK CITY AREA', inplace=True)

df['area'].value_counts()

df['area'].isnull().sum()

city_areas = {
    'NEW YORK CITY AREA': 'Northeast',
    'DC/MARYLAND/VIRGINIA AREA': 'Mid-Atlantic',
    'MIDWEST AREA': 'Midwest',
    'ATLANTIC SOUTH AREA': 'Southeast',
    'CALIFORNIA NORTH AREA': 'West',
    'DALLAS AREA': 'Southwest',
    'NEW ENGLAND AREA': 'Northeast',
    'SOUTHWEST AREA': 'Southwest',
    'CHICAGO AREA': 'Midwest',
    'LOS ANGELES AREA': 'West',
    'GREAT LAKES AREA': 'Midwest',
    'OHIO AREA': 'Midwest',
    'NORTHWEST/ROCKY MOUNTAIN AREA': 'West',
    'NORTH FLORIDA AREA': 'Southeast',
    'CENTRAL/SOUTH TEXAS AREA': 'Southwest',
    'HOUSTON AREA': 'Southwest',
    'SOUTH FLORIDA AREA': 'Southeast',
    'TENNESSEE AREA': 'Southeast',
    'PHILADELPHIA AREA': 'Mid-Atlantic'
}

df['area'] = df['area'].map(city_areas)

df['area'].value_counts()

# columna 72 : Dualband : capacidad de conectarse a las dos frecuencias utilizadas por las redes WiFi domésticas: 2,4 y 5 GHz.

var_dic.iloc[72,:]

df['dualband'].value_counts()

df['dualband'].isnull().sum()

df['dualband'].fillna('Y', inplace=True)

df['dualband'].isnull().sum()

# columna 73 : refurb_new : Handset: refurbished or new

var_dic.iloc[73, :]

df['refurb_new'].value_counts()

df['refurb_new'].isnull().sum()

df['refurb_new'].fillna('N', inplace=True)

df['refurb_new'].isnull().sum()

# columna 74 : hnd_price : Current handset price

var_dic.iloc[74,:]

df['hnd_price'].isnull().sum()

df.hist('hnd_price')

df['hnd_price'].fillna(-999, inplace=True)

df['hnd_price'].isnull().sum()

#columna 75 : phones : Number of handsets issued

var_dic.iloc[75,:]

df['phones'].isnull().sum()

df['phones'].value_counts()

df['phones'].fillna(1.0, inplace=True)

# columna 76 : models : Number of models issued

var_dic.iloc[76,:]

df['models'].describe()

df.hist('models')

df['models'].isnull().sum()

df['models'].fillna(1.0, inplace=True)

df['models'].isnull().sum()

#columna 77 : hnd_webcap : Handset web capability

var_dic.iloc[77,:]

df['hnd_webcap'].value_counts()

df['hnd_webcap'].isnull().sum()

df['hnd_webcap'].fillna('WCMB', inplace=True)

df['hnd_webcap'].value_counts()

df['hnd_webcap'].isnull().sum()

#columna 78 : truck :  Truck indicator

var_dic.iloc[78, :]

df['truck'].value_counts()

df['truck'].isnull().sum()

df['truck'].fillna(0.0, inplace=True)

df['truck'].value_counts()

df['truck'].isnull().sum()

# columna 79 : rv :  RV indicator

var_dic.iloc[79, :]

df['rv'].value_counts()

df['rv'].isnull().sum()

df['rv'].fillna(0.0, inplace=True)

df['rv'].value_counts()

# columna 80 : ownrent : Home owner/renter status

var_dic.iloc[80,:]

df['ownrent'].value_counts()

df['ownrent'].isnull().sum() *100/len(df['ownrent'])

df['ownrent'].notna().sum() *100/len(df['ownrent'])

df['ownrent'].value_counts(normalize=True)

df['ownrent'].isnull().sum()

df['ownrent'].fillna('O', inplace=True)

df['ownrent'].isnull().sum()

# columna 81 : lor : Length of residence

var_dic.iloc[81,:]

df.hist('lor')

df['lor'].isnull().sum() *100/len(df['lor'])

df['lor'].fillna(-999, inplace=True)

#columna 82 : dwlltype : Dwelling Unit type

var_dic.iloc[82,:]

df['dwlltype'].value_counts()

df['dwlltype'].isnull().sum()

df['dwlltype'].isnull().sum() * 100/len(df['dwlltype'])

df['dwlltype'].value_counts(normalize=True)

df_dwlltype_counts = df["dwlltype"].value_counts()

# Calcular la proporción de cada color en relación con el total de colores no nulos
total_non_null = df_dwlltype_counts.sum()
proportions = df_dwlltype_counts / total_non_null

# Calcular el número de nulos que se asignará a cada color
total_nulls = df["dwlltype"].isnull().sum()

# Manejar el caso cuando no hay valores nulos
if total_nulls == 0:
    print("No hay valores nulos en la columna 'color'.")
else:
    nulls_per_dwlltype = np.round(proportions * total_nulls).astype(int)

    # Distribuir los nulos proporcionalmente en los colores existentes
    null_indices = df[df["dwlltype"].isnull()].index
    dwlltype = nulls_per_dwlltype.index.to_list()
    weights = nulls_per_dwlltype.values / nulls_per_dwlltype.sum()
    replacement_dwlltype = np.random.choice(dwlltype, size=len(null_indices), p=weights)
    df.loc[null_indices, "dwlltype"] = replacement_dwlltype

df['dwlltype'].value_counts()

#columna 83 : marital : marital status

var_dic.iloc[83,:]

df['marital'].value_counts()

df['marital'].isnull().sum()

df['marital'].value_counts()

df['marital'].fillna('U', inplace=True)

df['marital'].isnull().sum()

#columna 84 : adults : Number of adults in household

var_dic.iloc[84,: ]

df['adults'].value_counts()

df['adults'].isnull().sum()

# Assuming you have already loaded the DataFrame "df" containing the "adults" column

# Calculate the counts of each category in the "adults" column
df_adults_counts = df["adults"].value_counts()

# Calculate the proportion of each category in relation to the total non-null categories
total_non_null = df_adults_counts.sum()
proportions = df_adults_counts / total_non_null

# Calculate the number of missing values that will be assigned to each category
total_nulls = df["adults"].isnull().sum()

# Handle the case when there are no missing values
if total_nulls == 0:
    print("No hay valores nulos en la columna 'adults'.")
else:
    nulls_per_adults = np.round(proportions * total_nulls).astype(int)

    # Distribute the missing values proportionally among the existing categories
    null_indices = df[df["adults"].isnull()].index
    adults = nulls_per_adults.index.to_list()
    weights = nulls_per_adults.values / nulls_per_adults.sum()
    replacement_adults = np.random.choice(adults, size=len(null_indices), p=weights)
    df.loc[null_indices, "adults"] = replacement_adults

df['adults'].isnull().sum()

df['adults'].value_counts()

# columna 85 : infobase : InfoBase match

var_dic.iloc[85,:]

df['infobase'].value_counts()

df['infobase'].isnull().sum()*100/len(df['infobase'])

df['infobase'].fillna('M', inplace=True)

df['infobase'].isnull().sum()

# columna 86 : income : Estimated income

var_dic.iloc[86,:]

df['income'].isnull().sum()

df.hist('income')

df['income'].describe()

df['income'].fillna(-999, inplace=True)

df['income'].isnull().sum()

#columna 87 : numbcars :  Known number of vehicles

var_dic.iloc[87,:]

df['numbcars'].value_counts()

df['numbcars'].fillna(-999.00, inplace=True)

df['numbcars'].isnull().sum()

#columna 88 : HHstatin : Premier household status indicator

var_dic.iloc[88, :]

df['HHstatin'].value_counts()

df['HHstatin'].isnull().sum() * 100/len(df['HHstatin'])

# Assuming you have already loaded the DataFrame "df" containing the "HHstatin" column

# Calculate the counts of each category in the "HHstatin" column
df_HHstatin_counts = df["HHstatin"].value_counts()

# Calculate the proportion of each category in relation to the total non-null categories
total_non_null = df_HHstatin_counts.sum()
proportions = df_HHstatin_counts / total_non_null

# Calculate the number of missing values that will be assigned to each category
total_nulls = df["HHstatin"].isnull().sum()

# Handle the case when there are no missing values
if total_nulls == 0:
    print("No hay valores nulos en la columna 'HHstatin'.")
else:
    nulls_per_category = np.round(proportions * total_nulls).astype(int)

    # Distribute the missing values proportionally among the existing categories
    null_indices = df[df["HHstatin"].isnull()].index
    categories = nulls_per_category.index.to_list()
    weights = nulls_per_category.values / nulls_per_category.sum()
    replacement_HHstatin = np.random.choice(categories, size=len(null_indices), p=weights)
    df.loc[null_indices, "HHstatin"] = replacement_HHstatin

df['HHstatin'].isnull().sum()

# columna 89 : dwllsize : Dwelling size

var_dic.iloc[89, :]

df['dwllsize'].value_counts()

df['dwllsize'].isnull().sum()

df['dwllsize'].isnull().sum() * 100/len(df['dwllsize'])

df['dwllsize'].value_counts(normalize=True)

df['dwllsize'].fillna('A', inplace=True)

# columna 90 : forgntvl : Foreign travel dummy variable

var_dic.iloc[90, :]

df['forgntvl'].isnull().sum()

df['forgntvl'].value_counts()

df['forgntvl'].fillna(0.0, inplace=True)

df['forgntvl'].value_counts()

# columna 91 : ethnic : Ethnicity roll-up code

var_dic.iloc[91, :]

df['ethnic'].value_counts()

df['ethnic'].isnull().sum()

df['ethnic'].fillna('N', inplace=True)

df['ethnic'].isnull().sum()

#columna 92 : kid0_2 : Child 0 - 2 years of age in household

var_dic.iloc[92,:]

df['kid0_2'].value_counts()

df['kid0_2'].isnull().sum()

df['kid0_2'].fillna('U', inplace=True)

df['kid0_2'].isnull().sum()

#columna : 93 : kid3_5 : Child 3 - 5 years of age in household

var_dic.iloc[93,:]

df['kid3_5'].value_counts()

df['kid3_5'].isnull().sum()

df['kid3_5'].fillna('U', inplace=True)

df['kid3_5'].isnull().sum()

# columna 94 :  kid6_10 : Child 6 - 10 years of age in household

var_dic.iloc[94, :]

df['kid6_10'].value_counts()

df['kid6_10'].isnull().sum()

df['kid6_10'].fillna('U', inplace=True)

df['kid6_10'].isnull().sum()

# columna 95 : kid11_15 : Child 11 - 15 years of age in household

var_dic.iloc[95, :]

df['kid11_15'].value_counts()

df['kid11_15'].isnull().sum()

df['kid11_15'].fillna('U', inplace=True)

df['kid11_15'].isnull().sum()

# columna 96 : kid16_17 : Child 16 - 17 years of age in household

var_dic.iloc[96, :]

df['kid16_17'].value_counts()

df['kid16_17'].isnull().sum()

df['kid16_17'].fillna('U', inplace=True)

df['kid16_17'].isnull().sum()

# columna 97 :  creditcd : Credit card indicator

var_dic.iloc[97, :]

df['creditcd'].value_counts()

df['creditcd'].isnull().sum()

df['creditcd'].fillna('Y', inplace=True)

sevan_ = df[df['eqpdays'] <=0].index

df.drop(sevan_, inplace = True)

df['eqpdays'].describe()

# columna 98 : eqpdays : Number of days (age) of current equipment

var_dic.iloc[98, :]

df.hist('eqpdays')

df['eqpdays'].isnull().sum()

df['eqpdays'].fillna(-999, inplace=True)

df['eqpdays'].isnull().sum()

# columna 99 : Customer_ID

var_dic.iloc[99,:]

"""Haasta aqui, todas las variables revisadas e imputadas."""

# Check duplicados - NO hay duplicados
len(df.index.unique())==len(df.index)

df.shape



# df_recuperacion = pd.read_pickle("/conte")

df.info()

df.shape

if df.isnull().sum().any() == False:

  print('El dataset no contiene nulos a imputar')

"""Hacemos correlacion para revisar si hay variables que explican lo mismo (alta correlacion) o bien, no aportan a la resolucion del problema"""

corr = df.corr(numeric_only=True)

corr.style.background_gradient(cmap='coolwarm')

del(df["infobase"])

"""# Encoding categóricos

* Si tienen sentido ordinal, es decir, se pueden ordenar, encodear con una escala numerica. Ejemplo: {"Bajo":1, "Medio":2, "Alto":3}.
* Si tienen unicamente 2 clases, indicador booleano
* One Hot Encoding en resto de categoricos
"""

df.head()

target= ["churn"]
def obtener_lista_variables(dataset):
    lista_numericas=[]
    lista_boolean=[]
    lista_categoricas=[]
    for i in dataset:
        if    (dataset[i].dtype.kind=="f" or dataset[i].dtype.kind=="i") and len(dataset[i].unique())!= 2  and i not in target:
              lista_numericas.append(i)
        elif  (dataset[i].dtype.kind=="f" or dataset[i].dtype.kind=="i" or dataset[i].dtype.kind=="b")  and len(dataset[i].unique())== 2  and i not in target:
              lista_boolean.append(i)
        elif  (dataset[i].dtype.kind=="O")  and i not in target:
              lista_categoricas.append(i)

    return lista_numericas, lista_boolean, lista_categoricas

l_num,l_bool,l_cat=obtener_lista_variables(df)

for i in l_bool:
  if i in df:
    df[i+"_bool"]=df[i].astype(int)

for column in l_bool:
    if column in df:
        df = df.drop(column, axis=1)

l_num_2,l_bool_2,l_cat_2 =obtener_lista_variables(df)

l_num_2

l_bool_2

l_cat_2

df = pd.get_dummies(data=df, columns=l_cat_2)

"""# Eliminar alta correlación

* Analizar variables (X) altamente correlacionadas
* Eliminar una variable de cada pareja altamente correlacionada (>95% o >99%...) en el dataset (df)
"""

target = 'churn'
features = df.columns[df.columns!=target]

X = df[features]

y = df[target]

df.shape

# Mismo analisis, pero desde una funcion que nos facilita la vida

def highly_correlated(df, threshold):
    col_corr = list() # Set of all the names of deleted columns
    colnames = list()
    rownames = list()
    corr_matrix = df.corr().abs()
    for i in range(len(corr_matrix.columns)):
        for j in range(i):
            if (corr_matrix.iloc[i, j] >= threshold) and (corr_matrix.columns[j] not in col_corr):
                colnames.append(corr_matrix.columns[i]) # getting the name of column
                rownames.append(corr_matrix.index[j])
                col_corr.append(corr_matrix.iloc[i, j])
    Z = pd.DataFrame({'F1':colnames,
                      'F2':rownames,
                      'corr_F1_F2':col_corr,
                      'corr_F1_target': [np.abs(np.corrcoef(df[i])) for i in colnames],
                      'corr_F2_target': [np.abs(np.corrcoef(df[i])) for i in rownames]
                      })
    Z['F_to_delete'] = rownames
    Z['F_to_delete'][Z['corr_F1_target'] < Z['corr_F2_target']] = Z['F1'][Z['corr_F1_target'] < Z['corr_F2_target']]

    return Z

highly_corr = highly_correlated(df,0.95)
highly_corr

drop_cols = list(highly_corr['F_to_delete'])

df.drop(columns=drop_cols, inplace=True)
print('Eliminadas columnas altamente correlacionadas:', drop_cols)

df.shape

target = 'churn'
features = df.columns[df.columns!=target]

X2 = df[features]

y2 = df[target]

"""# Eliminar baja varianza

* Eliminar variables (X) practicamente constantes con un threshold minimo (1% o menos)
"""

pip install scikit-learn

from sklearn.feature_selection import VarianceThreshold

X2.shape

X2.info()

vt = VarianceThreshold(threshold = 0.01)

vt.fit(X2)

cols_lowvar = X2.columns[vt.get_support()==False]

X2.drop(columns=cols_lowvar,inplace=True)
print(len(cols_lowvar),' low variance features were removed:\n', cols_lowvar.to_list())

X2.shape

df.shape

y2.shape

"""# Guardar clean data"""

pd.to_pickle(df,'/content/drive/MyDrive/DSC 0523– Entregable 2 - Borrero, Dottori, He/Modelo/EJERCICIO-ML-Sup/data/ df_limpio_completo_Preprocessing_Final_ML_PK')

"""* Guardar en data path y mostrar el resultado en un head()"""

df_recuperacion=pd.read_pickle('/content/drive/MyDrive/DSC 0523– Entregable 2 - Borrero, Dottori, He/Modelo/EJERCICIO-ML-Sup/data/ df_limpio_completo_Preprocessing_Final_ML_PK')

df.head(2)

df.shape

df['churn']