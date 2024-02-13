import matplotlib.pyplot as plt
from io import BytesIO
import base64


def generate_histogram1(request):
    request_json = request.get_json()
    if request_json and 'expenses' in request_json:
        data = request_json['expenses']
        amounts = [float(expense['amount']) for expense in data]

        plt.hist(amounts, bins=20, color='skyblue', edgecolor='black')
        plt.xlabel('Amount')
        plt.ylabel('Number of expenses')
        plt.title('expenses price histogram')
        plt.grid(True)

        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        plt.close()

        encoded_image = base64.b64encode(buffer.getvalue()).decode('utf-8')

        return {'image': encoded_image}
    else:
        return {'error': 'No data provided'}
