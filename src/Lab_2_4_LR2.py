import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats
import seaborn as sns


class LinearRegressor:
    """
    Extended Linear Regression model with support for categorical variables and gradient descent fitting.
    """

    def __init__(self):
        self.coefficients = None
        self.intercept = None

    """
    This next "fit" function is a general function that either calls the *fit_multiple* code that
    you wrote last week, or calls a new method, called *fit_gradient_descent*, not implemented (yet)
    """

    def fit(self, X, y, method="least_squares", learning_rate=0.01, iterations=1000):
        """
        Fit the model using either normal equation or gradient descent.

        Args:
            X (np.ndarray): Independent variable data (2D array).
            y (np.ndarray): Dependent variable data (1D array).
            method (str): method to train linear regression coefficients.
                          It may be "least_squares" or "gradient_descent".
            learning_rate (float): Learning rate for gradient descent.
            iterations (int): Number of iterations for gradient descent.

        Returns:
            None: Modifies the model's coefficients and intercept in-place.
        """
        if method not in ["least_squares", "gradient_descent"]:
            raise ValueError(
                f"Method {method} not available for training linear regression."
            )
        if np.ndim(X) == 1:
            X = X.reshape(-1, 1)

        X_with_bias = np.c_[np.ones(X.shape[0]),X] # Añadir una columna de unos, np.c_ lo usamos para concatenar para decir si queremos a la izq o a la derecha es cambiar el orden
        #                                  # X.shape[0], X lo concatena a la izq, X, X.shape[0] lo concatena a la derecha
        if method == "least_squares":
            self.fit_multiple(X_with_bias, y)
        elif method == "gradient_descent":
            self.fit_gradient_descent(X_with_bias, y, learning_rate, iterations)

    def fit_multiple(self, X, y):
        """
        Fit the model using multiple linear regression (more than one independent variable).

        This method applies the matrix approach to calculate the coefficients for
        multiple linear regression.

        Args:
            X (np.ndarray): Independent variable data (2D array), with bias.
            y (np.ndarray): Dependent variable data (1D array).

        Returns:
            None: Modifies the model's coefficients and intercept in-place.
        """

        w = np.linalg.inv(np.transpose(X) @ X) @ (np.transpose(X) @ y)
        self.intercept = w[0]
        self.coefficients = w[1:]

    def fit_gradient_descent(self, X, y, learning_rate=0.01, iterations=1000):
        """
        Fit the model using either normal equation or gradient descent.

        Args:
            X (np.ndarray): Independent variable data (2D array), with bias.
            y (np.ndarray): Dependent variable data (1D array).
            learning_rate (float): Learning rate for gradient descent.
            iterations (int): Number of iterations for gradient descent.

        Returns:
            None: Modifies the model's coefficients and intercept in-place.
        """
        
        # Initialize the parameters to very small values (close to 0)
        m = len(y)
        self.coefficients = (
            np.random.rand(X.shape[1] - 1) * 0.01
        )  # Small random numbers
        self.intercept = np.random.rand() * 0.01 # Pillamos los parametros a un pequeño valor

        # Implement gradient descent (TODO)
        for epoch in range(iterations):
            predictions = self.predict(X[:,1:])
            error = predictions - y

            # TODO: Write the gradient values and the updates for the paramenters
            gradient = (learning_rate/m) * np.dot(X.T,error)
            
            self.intercept -= gradient[0]
            self.coefficients -= gradient[1:]

            # TODO: Calculate and print the loss every 10 epochs
            if epoch % 1000 == 0:
                mse = np.sum(np.power(error,2))/m
                print(f"Epoch {epoch}: MSE = {mse}")

    def predict(self, X):
        """
        Predict the dependent variable values using the fitted model.

        Args:
            X (np.ndarray): Independent variable data (1D or 2D array).
            fit (bool): Flag to indicate if fit was done.

        Returns:
            np.ndarray: Predicted values of the dependent variable.

        Raises:
            ValueError: If the model is not yet fitted.
        """
        X = np.transpose(X)
        if self.coefficients is None or self.intercept is None:
            raise ValueError("Model is not yet fitted")

        if np.ndim(X) == 1:
            # Predict when X is only one variable
            predictions = X * self.coefficients + self.intercept
        else:
            # Predict when X is more than one variable
            predictions = np.dot(X,self.coefficients) + self.intercept

        return predictions


def evaluate_regression(y_true, y_pred):
    """
    Evaluates the performance of a regression model by calculating R^2, RMSE, and MAE.

    Args:
        y_true (np.ndarray): True values of the dependent variable.
        y_pred (np.ndarray): Predicted values by the regression model.

    Returns:
        dict: A dictionary containing the R^2, RMSE, and MAE values.
    """

    # R^2 Score
    RSS = np.sum(np.power(y_true-y_pred,2))
    TSS = np.sum(np.power(y_true-np.mean(y_true),2))
    # TODO: Calculate R^2
    # r_squared = np.power(np.cov(y_true,y_pred,ddof=0),2) / (np.var(y_true,ddof=0) * np.var(y_pred))
    r_squared = 1 - (RSS/TSS)
    # Root Mean Squared Error
    # TODO: Calculate RMSE
    rmse = np.sqrt((1/len(y_true)) * np.sum(np.power(y_true-y_pred,2)))

    # Mean Absolute Error
    # TODO: Calculate MAE
    mae = (1/len(y_true)) * np.sum(np.abs(y_true-y_pred))

    return {"R2": r_squared, "RMSE": rmse, "MAE": mae}


def one_hot_encode(X, categorical_indices, drop_first=False):
    """
    One-hot encode the categorical columns specified in categorical_indices. This function
    shall support string variables.

    Args:
        X (np.ndarray): 2D data array.
        categorical_indices (list of int): Indices of columns to be one-hot encoded.
        drop_first (bool): Whether to drop the first level of one-hot encoding to avoid multicollinearity.

    Returns:
        np.ndarray: Transformed array with one-hot encoded columns.
    """
    X_transformed = X.copy()
    for index in sorted(categorical_indices, reverse=True):
        # TODO: Extract the categorical column
        categorical_column = X_transformed[:,index]
        

        # TODO: Find the unique categories (works with strings)
        unique_values = np.unique(categorical_column)
        

        # TODO: Create a one-hot encoded matrix (np.array) for the current categorical column
        one_hot = np.array([
            [1 if categoria == val else 0 for val in unique_values] for categoria in categorical_column
        ])     # Con esta parte obtenemos el 1 0 0                     Y aquí es para pillar 
                #                             0 1 0                     cada categoría de las posibles
                #                             ....          
        
        
        # Optionally drop the first level of one-hot encoding
        if drop_first:
            one_hot = one_hot[:, 1:]
        # TODO: Delete the original categorical column from X_transformed and insert new one-hot encoded columns
        
        X_transformed = np.delete(X_transformed,index,axis=1)
        # print(one_hot.shape)
        # print(X_transformed.shape)
        X_transformed = np.insert(X_transformed,index,one_hot.T, axis=1)  
        # Trasponemos para que coincidan filas y columnas, ya q funciona como la multiplicación. Entonces tienen que coincidir
    return X_transformed
