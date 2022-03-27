import matplotlib.pyplot as plt


def plotBarChart(title, x_label, y_label, x_data, y_data):
    plt.bar(x_data, y_data)
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.show()


title = "Comparison between batch picking vs non batch-picking"
x_label = "Batch Picking vs Non Batch Picking"
y_label = "Time"

x_data = ["Batch Picking", "Non Batch Picking"]
y_data = [1.3, 3]

plotBarChart(title, x_label, y_label, x_data, y_data)
