import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load your dataset (adjust the path as needed)
file_path = 'Data/YouTube Scrapper - Visualization Tools - Hoja 1.csv'
df = pd.read_csv(file_path)

# Convert 'Published At' to datetime
df['Published At'] = pd.to_datetime(df['Published At'], errors='coerce')

# Extract year, month, day of week for time series visualization
df['Year'] = df['Published At'].dt.year
df['Month'] = df['Published At'].dt.month
df['DayOfWeek'] = df['Published At'].dt.day_name()

# Set seaborn style
sns.set(style="whitegrid")

# 1. Number of Videos by Search Topic
# plt.figure(figsize=(10, 5))
# topic_counts = df['Tópico de Búsqueda'].value_counts()
# sns.barplot(x=topic_counts.index, y=topic_counts.values)
# plt.title('Number of Videos by Search Topic')
# plt.xlabel('Search Topic')
# plt.ylabel('Number of Videos')
# plt.tight_layout()
# plt.show()

# # 2. Distribution of Video Duration (minutes) - Histogram and Boxplot
# fig, axes = plt.subplots(1, 2, figsize=(14, 5))
# sns.histplot(df['Duration (min)'], bins=30, kde=True, ax=axes[0])
# axes[0].set_title('Distribution of Video Duration (minutes)')
# axes[0].set_xlabel('Duration (min)')
# sns.boxplot(x=df['Duration (min)'], ax=axes[1])
# axes[1].set_title('Boxplot of Video Duration (minutes)')
# plt.tight_layout()
# plt.show()

# # 3. Contar los tipos de datos en el DataFrame
# data_types_count = df.dtypes.value_counts()

# # Crear gráfico de barras para tipos de datos
# plt.figure(figsize=(8, 5))
# data_types_count.plot(kind='bar')
# plt.title('Count of Data Types in Dataset')
# plt.xlabel('Data Type')
# plt.ylabel('Number of Columns')
# plt.xticks(rotation=0)
# plt.tight_layout()
# plt.show()

# 4. Number of Videos Published per Year
# plt.figure(figsize=(10, 5))
# year_counts = df['Year'].value_counts().sort_index()
# sns.barplot(x=year_counts.index.astype(str), y=year_counts.values)
# plt.title('Number of Videos Published per Year')
# plt.xlabel('Year')
# plt.ylabel('Number of Videos')
# plt.tight_layout()
# plt.show()

# # 5. Number of Videos Published per Month (all years combined)
# plt.figure(figsize=(10, 5))
# month_counts = df['Month'].value_counts().sort_index()
# sns.barplot(x=month_counts.index, y=month_counts.values)
# plt.title('Number of Videos Published per Month (All Years)')
# plt.xlabel('Month')
# plt.ylabel('Number of Videos')
# plt.tight_layout()
# plt.show()

# # 6. Calcular matriz de correlación solo con las columnas numéricas relevantes
# corr = df[['Views', 'Likes', 'Comments', 'Duration (min)']].corr()

# # Graficar heatmap
# plt.figure(figsize=(8, 6))
# sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f")
# plt.title('Correlation Heatmap of Numeric Variables')
# plt.tight_layout()
# plt.show()

# # 7. Calcular likes promedio por canal, y seleccionar los top 10 canales con más videos para claridad
# likes_per_channel = df.groupby('Channel Title')['Likes'].mean()
# video_counts = df['Channel Title'].value_counts()
# top_channels = video_counts[video_counts > 5].index  # Filtra canales con más de 5 videos para más relevancia

# likes_per_channel_filtered = likes_per_channel.loc[top_channels].sort_values(ascending=False).head(10)

# plt.figure(figsize=(12, 6))
# sns.barplot(x=likes_per_channel_filtered.values, y=likes_per_channel_filtered.index)
# plt.title('Top 10 Channels by Average Likes per Video (Channels with >5 Videos)')
# plt.xlabel('Average Likes')
# plt.ylabel('Channel Title')
# plt.tight_layout()
# plt.show()

# # 8. Contar cantidad de videos por día de la semana
# day_counts = df['DayOfWeek'].value_counts().reindex([
#     'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'
# ])

# plt.figure(figsize=(10, 5))
# sns.barplot(x=day_counts.index, y=day_counts.values)
# plt.title('Number of Videos Published by Day of the Week')
# plt.xlabel('Day of the Week')
# plt.ylabel('Number of Videos')
# plt.tight_layout()
# plt.show()

# # 9. Distribución de la duración de los videos por tema de búsqueda
# plt.figure(figsize=(12, 6))
# sns.boxplot(x='Tópico de Búsqueda', y='Duration (min)', data=df)
# plt.title('Duration Distribution by Search Topic')
# plt.xlabel('Search Topic')
# plt.ylabel('Duration (minutes)')
# plt.tight_layout()
# plt.show()


# # 10. Número total de vistas por canal (top 10)
# views_per_channel = df.groupby('Channel Title')['Views'].sum()
# top_channels_views = views_per_channel.sort_values(ascending=False).head(10)

# plt.figure(figsize=(12, 6))
# sns.barplot(x=top_channels_views.values, y=top_channels_views.index)
# plt.title('Top 10 Channels by Total Views')
# plt.xlabel('Total Views')
# plt.ylabel('Channel Title')
# plt.tight_layout()
# plt.show()

# # 11. Crear una columna que indique si el video tiene comentarios o no
# df['Has_Comments'] = df['Comments'] > 0

# # Contar videos con y sin comentarios
# comments_counts = df['Has_Comments'].value_counts()

# # Gráfico de barras
# plt.figure(figsize=(6, 5))
# comments_counts.plot(kind='bar')
# plt.title('Number of Videos With and Without Comments')
# plt.xlabel('Has Comments')
# plt.ylabel('Number of Videos')
# plt.xticks(ticks=[0,1], labels=['No', 'Yes'], rotation=0)
# plt.tight_layout()
# plt.show()

# Graph 4: Violin plot of video duration by year
plt.figure(figsize=(12, 6))
sns.violinplot(data=df, x='Year', y='Duration (min)', inner='box', palette='muted')
plt.title('Distribution of Video Duration by Year')
plt.xlabel('Year')
plt.ylabel('Duration (minutes)')
plt.tight_layout()
plt.show()

# Graph 5: Count plot of videos by channel title (top 8)
top_channels = df['Channel Title'].value_counts().nlargest(8).index
filtered_channel_df = df[df['Channel Title'].isin(top_channels)]

plt.figure(figsize=(12, 6))
sns.countplot(data=filtered_channel_df, y='Channel Title', order=top_channels, palette='Set3')
plt.title('Number of Videos by Top 8 Channels')
plt.xlabel('Number of Videos')
plt.ylabel('Channel Title')
plt.tight_layout()
plt.show()

# Graph 6: Scatter plot of Likes vs Views colored by Search Topic
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='Views', y='Likes', hue='Tópico de Búsqueda', alpha=0.7, s=100)
plt.title('Likes vs Views Colored by Search Topic')
plt.xlabel('Views')
plt.ylabel('Likes')
plt.legend(title='Search Topic', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()
