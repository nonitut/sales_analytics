import pandas as pd
import matplotlib.pyplot as plt  # pip install matplotlib
import seaborn as sns  # pip install seaborn

file_path = './Продажи.csv'
data = pd.read_csv(file_path)

# Предварительный анализ
print(data.head())
print(data.info())

# Очистка и преобразование данных
data['Выручка'] = data['Выручка'].str.replace(r'[^\d.]', '', regex=True).astype(float)
data['Прибыль'] = data['Прибыль'].str.replace(r'[^\d.]', '', regex=True).astype(float)

if 'Затраты' not in data.columns:
    data['Затраты'] = 0  # Добавление столбца, если он отсутствует

data['Прибыль'] = data['Выручка'] - data['Затраты']
data['Рентабельность'] = (data['Прибыль'] / data['Выручка']) * 100

if 'Количество заказов' not in data.columns:
    data['Количество заказов'] = data['Количество']  # Используйте реальное название

data['Средний чек'] = data['Выручка'] / data['Количество заказов']

# Создание фигуры и осей для нескольких графиков
fig, axes = plt.subplots(3, 2, figsize=(14, 12))  # 3 строки и 2 столбца

# Гистограмма распределения выручки и прибыли
sns.histplot(data['Выручка'], kde=True, color='blue', bins=30, label='Выручка', ax=axes[0, 0])
sns.histplot(data['Прибыль'], kde=True, color='green', bins=30, label='Прибыль', ax=axes[0, 0])
axes[0, 0].set_title('Распределение выручки и прибыли')
axes[0, 0].legend()

# Диаграмма размаха (boxplot) для выручки и прибыли
sns.boxplot(data=data[['Выручка', 'Прибыль']], palette='Set2', ax=axes[0, 1])
axes[0, 1].set_title('Диаграмма размаха для выручки и прибыли')

# Визуализация выручки по приоритетам
if 'Приоритет' in data.columns:
    sns.barplot(data=data, x='Приоритет', y='Выручка', palette='viridis', ax=axes[1, 0])
    axes[1, 0].set_title("Выручка по приоритетам")

# Визуализация выручки по регионам
if 'Регион' in data.columns:
    sns.barplot(data=data, x='Регион', y='Выручка', palette='muted', ax=axes[1, 1])
    axes[1, 1].set_title("Выручка по регионам")
    axes[1, 1].tick_params(axis='x', rotation=45)

# Тепловая карта корреляции между числовыми признаками
corr_matrix = data[['Выручка', 'Прибыль', 'Затраты', 'Количество', 'Количество заказов', 'Средний чек']].corr()
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5, ax=axes[2, 0])
axes[2, 0].set_title('Корреляция между числовыми признаками')

# Если есть дата, строим график
if 'Дата' in data.columns:
    data.groupby('Дата')[['Выручка', 'Прибыль']].sum().plot(ax=axes[2, 1])
    axes[2, 1].set_title("Динамика выручки и прибыли по дням")
else:
    axes[2, 1].text(0.5, 0.5, "Столбец 'Дата' отсутствует", horizontalalignment='center', verticalalignment='center')

# Автоматическая настройка расположения графиков
plt.tight_layout()
plt.show()
