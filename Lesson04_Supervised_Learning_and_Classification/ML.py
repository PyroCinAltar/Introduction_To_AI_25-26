# 7A — Decision Tree on Iris (no database needed)
# from sklearn.datasets import load_iris
# from sklearn.model_selection import train_test_split
# from sklearn.tree import DecisionTreeClassifier
# from sklearn.metrics import accuracy_score, classification_report

# # 1) Load built-in data
# iris = load_iris()
# X, y = iris.data, iris.target

# # 2) Split into train/test
# X_train, X_test, y_train, y_test = train_test_split(
#     X, y, test_size=0.3, random_state=42
# )

# # 3) Train a Decision Tree
# clf = DecisionTreeClassifier(random_state=42)
# clf.fit(X_train, y_train)

# # 4) Evaluate
# y_pred = clf.predict(X_test)
# print("Accuracy:", accuracy_score(y_test, y_pred))
# print("\nClassification Report:\n", classification_report(y_test, y_pred, target_names=iris.target_names))

# # 5) Try a single new prediction (sepal_len, sepal_wid, petal_len, petal_wid)
# new_sample = [[5.1, 3.5, 1.4, 0.2]]
# print("Predicted class for", new_sample, "->", iris.target_names[clf.predict(new_sample)[0]])