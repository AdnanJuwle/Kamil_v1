from datasets import load_dataset
import pandas as pd

# Load the dataset
dataset = load_dataset('iris')

# Convert the dataset into a Pandas DataFrame
df = pd.DataFrame(dataset)

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(df.drop('target', axis=1), df['target'])

# Train a random forest classifier on the training set
clf = RandomForestClassifier()
clf.fit(X_train, y_train)

# Make predictions on the testing set
y_pred = clf.predict(X_test)

# Print the accuracy score of the model
print('Accuracy:', clf.score(X_test, y_test))