import matplotlib.pyplot as plt
from expression import Expression
import datetime

# Plots function and saves as an image file
def plot_and_save(ex, bottom=-50, top=50):  # Defaults range from -50 to 50 (100 values)
    # Create Expression instance
    equation = Expression(ex)

    # Generate a list of input values as a list
    x_axis_list = list(range(bottom, top))

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
    print(f"The figure has been saved to {file_name}")

