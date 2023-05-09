import matplotlib.pyplot as plt
import expression
import os
import datetime

def plot_and_save(ex):
    # Create Expression instance
    equation = expression.Expression(ex)

    # Generate a list of input values as a list
    x_axis_list = list(range(-50, 50))

    # Evaluate the expression for each value
    y_axis_list = equation.evaluate_list_of_values(x_axis_list)

    # Create the plot
    plt.plot(x_axis_list, y_axis_list)

    # Get the current date-time
    now = datetime.datetime.now()

    # Construct a unique file name
    current_date_time = f"{now.year}-{now.month}-{now.day}_{now.hour}-{now.minute}-{now.second}:{now.microsecond}"
    file_name = f"Figure_{current_date_time}.png"
    plt.savefig(file_name)

