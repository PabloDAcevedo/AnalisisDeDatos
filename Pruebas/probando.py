
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


df = pd.read_csv('w_mean_todos.csv')

# print(df.head())


# Limpiar archivos
df_limpio = df.dropna()

# Aseguramos la columnas de fecha con el formato correcto
df_limpio['fecha'] = pd.to_datetime(df_limpio['fecha'])


'''# Agregar columna con año - mes y filtra por año
df_limpio['año-mes'] = df_limpio['fecha'].dt.year

# Agrupar por año y calcular el sueldo media
sueldo_promedio_año = df_limpio.groupby('año-mes')['w_mean'].mean()

# Se configura grafico con seaborn y matprolib
sueldo_promedio_año.plot(kind='bar', figsize=(10,6))
plt.title('Sueldo Promedio por Año')
plt.xlabel('Año')
plt.ylabel('Sueldo Promedio')
plt.tight_layout()
plt.show()'''



'''# Agregar columna con año - mes y filtra por mes
df_limpio['año-mes'] = df_limpio['fecha'].dt.month

# Agrupar por mes y calcular el sueldo media
sueldo_promedio_mes = df_limpio.groupby('año-mes')['w_mean'].mean()

# Se configura grafico con seaborn y matprolib
sueldo_promedio_mes.plot(kind='bar', figsize=(8,5))
plt.title('Sueldo Promedio por Mes')
plt.xlabel('Mes')
plt.ylabel('Sueldo Promedio')
plt.tight_layout()
plt.show()'''
