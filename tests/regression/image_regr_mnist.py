from keras.datasets import mnist
import numpy as np
# Adjust the import path according to your project structure
from differences_images_conv import _regression
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

# Load MNIST dataset
(X_train_mnist, y_train_mnist), (X_test_mnist, y_test_mnist) = mnist.load_data()


# Initialize the regressor with corrected parameters
regressor_mnist = _regression.LingerImageRegressor(n_neighbours_1=5)

# Convert y to float for regression
y_train_mnist = y_train_mnist.astype('float32')
y_test_mnist = y_test_mnist.astype('float32')

# Fit the regressor (Assuming fit method is adjusted correctly)

print(X_test_mnist.shape)
X_test_mnist = X_test_mnist.reshape(X_test_mnist.shape[0], -1)
X_train_mnist = X_train_mnist.reshape(X_train_mnist.shape[0], -1)
diff_X, diff_y = regressor_mnist.fit(X_train_mnist, y_train_mnist)
diff_X = np.array(diff_X)
diff_y = np.array(diff_y)
diff_X = diff_X.reshape(-1, 28, 28, 1)
# Define the CNN model for regression tasks
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
    MaxPooling2D((2, 2)),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    Conv2D(64, (3, 3), activation='relu'),
    Flatten(),
    Dense(64, activation='relu'),
    Dense(1, activation='linear')
])

# Compile the model
model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mae'])

# Assuming `differences_X` and `differences_y` are prepared correctly in `fit`
# Train the model
model.fit(diff_X, diff_y, epochs=1, batch_size=32, validation_split=0.2)

# Use the trained model to make predictions on test data
predictions = regressor_mnist.predict(X_test_mnist, model=model, dataset='mnist', input_shape=(28, 28, 1))

# Perform further evaluation for regression, such as calculating RMSE or plotting actual vs. predicted values.