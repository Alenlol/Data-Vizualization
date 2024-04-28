import matplotlib.pyplot as plt
import base64
from io import BytesIO
import pandas as pd
from django.conf import settings


class Visualize():
    data: pd

    def __init__(self, data):
        self.data = pd.read_csv(str(settings.BASE_DIR).replace('\\', '/')+'/static/data_collection/' + data)

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
        plt.plot(self.data[x], self.data[y])
        plt.xlabel('xitem')
        plt.ylabel('yitem')
        plt.tight_layout()
        graph = self.get_graph()
        return graph

    def set_data(self, file):
        self.data = pd.read_csv(file)

    def get_title_names(self):
        return self.data.columns

    def check_data(self, values):
        no_duplicate_value = set(values)

        if len(no_duplicate_value) == len(values):
            return True
        return False
