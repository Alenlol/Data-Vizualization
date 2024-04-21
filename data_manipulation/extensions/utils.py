import matplotlib.pyplot as plt
import base64
from io import BytesIO
import pandas as pd


class Visualize():
    x: int

    def __init__(self):
        pass

    def get_graph(self):
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_png = buffer.getvalue()
        graph = base64.b64encode(image_png)
        graph = graph.decode('utf-8')
        buffer.close()
        return graph

    def get_plot(self, x, y):
        plt.switch_backend('AGG')
        plt.figure(figsize=(10, 5))
        plt.title('Title')
        plt.plot(x, y)
        plt.xlabel('xitem')
        plt.ylabel('yitem')
        plt.tight_layout()
        graph = self.get_graph()
        return graph