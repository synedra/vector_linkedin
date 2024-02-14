import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# Load the dataset
data = pd.read_csv('imdb_top_1000.csv')  # Assuming 'imdb_dataset.csv' is your dataset file
print("The shape of the dataset is: {} rows and {} columns".format(data.shape[0], data.shape[1]))
# Split the dataset into features (X) and target variable (y)
data.dropna(inplace=True)  # Drop rows with missing values
data.drop(columns=['Released_Year','Poster_Link', 'Certificate','Overview','Director', 'Runtime', 'Genre', 'Meta_score', 'Series_Title', 'Star1','Star2','Star3','Star4'], inplace=True)

data['IMDB_Rating'] = pd.to_numeric(data['IMDB_Rating'], errors='coerce')


# Replace the Gross string with the appropriate integer value
data['Gross'] = data['Gross'].str.replace(',', '')
data['Gross'] = data['Gross'].astype('float64')
data['Gross'] = data['Gross'].replace(np.nan, 0)
data['Gross'] = data['Gross'].astype(int)

X = data.drop(columns=['IMDB_Rating'])
y = data['IMDB_Rating']
# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the linear regression model
model = LinearRegression()

# Fit the model to the training data
model.fit(X_train, y_train)

# Make predictions on the test data
y_pred = model.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
print('Mean Squared Error:', mse)
