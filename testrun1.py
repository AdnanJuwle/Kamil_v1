# Import necessary libraries
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import pandas as pd

# Load the dataset
df = pd.read_csv('student_marks.csv')

# Preprocess the data (if necessary)
# df = df[['feature1', 'feature2', ...]]

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(df.drop('marks', axis=1), df['marks'], test_size=0.2)

# Train a random forest regressor on the training data
model = RandomForestRegressor()
model.fit(X_train, y_train)

# Predict student's marks by taking user input
user_input = {'feature1': 5, 'feature2': 6} # Replace with actual features
predicted_marks = model.predict([user_input])[0]
print(f"Predicted marks for this student: {predicted_marks}")