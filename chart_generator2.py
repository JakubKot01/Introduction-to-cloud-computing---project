import matplotlib.pyplot as plt
import numpy as np
import base64
from io import BytesIO


def generate_cumulative_bar_chart(request):
    request_json = request.get_json()
    if request_json and 'expenses' in request_json:
        data = request_json['expenses']
        categories = set(expense['category'] for expense in data)
        category_totals = {category: 0 for category in categories}

        for expense in data:
            category_totals[expense['category']] += float(expense['amount'])

        sorted_categories = sorted(categories)
        category_labels = [category for category in sorted_categories]
        category_values = [category_totals[category] for category in sorted_categories]

        plt.bar(category_labels, category_values, color='skyblue')
        plt.xlabel('Category')
        plt.ylabel('Cumulative Expense')
        plt.title('Cumulative Expense by Category')
        plt.xticks(rotation=45, ha='right')
        plt.grid(True)

        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        plt.close()

        encoded_image = base64.b64encode(buffer.getvalue()).decode('utf-8')

        return {'image': encoded_image}
    else:
        return {'error': 'No data provided'}
