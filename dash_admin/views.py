from django.shortcuts import render
import matplotlib
matplotlib.use('Agg')  # Utiliser un backend non interactif
import matplotlib.pyplot as plt
import io
import base64
import pandas as pd

def averageCart(request):
    data = {
        'date': ['2023-01-01', '2023-01-02', '2023-01-08', '2023-01-15', '2023-01-23', '2023-01-30'],
        'total': [200, 150, 300, 250, 180, 320]
    }
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])  # Convertir la colonne 'date' en datetime
    df.set_index('date', inplace=True)  # Définir 'date' comme index

    # Générer le graphique quotidien et le convertir en URI
    daily_sales = df.resample('D').sum()
    daily_counts = df.resample('D').count()
    daily_average = daily_sales['total'] / daily_counts['total']

    fig, ax = plt.subplots()
    daily_average.plot(kind='line', marker='o', linestyle='-', color='blue', ax=ax)
    plt.title('Panier Moyen par Jour')
    plt.xlabel('Jour')
    plt.ylabel('Panier Moyen (€)')
    plt.grid(True)
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)  # Revenir au début du buffer
    daily_chart_uri = 'data:image/png;base64,' + base64.b64encode(buf.read()).decode('utf-8')

    # Générer le graphique mensuel et le convertir en URI
    monthly_sales = df.resample('M').sum()
    monthly_counts = df.resample('M').count()
    monthly_average = monthly_sales['total'] / monthly_counts['total']

    fig, ax = plt.subplots()
    monthly_average.plot(kind='line', marker='o', linestyle='-', color='green', ax=ax)
    plt.title('Évolution du Panier Moyen par Mois')
    plt.xlabel('Mois')
    plt.ylabel('Panier Moyen (€)')
    plt.grid(True)
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)  # Revenir au début du buffer
    monthly_chart_uri = 'data:image/png;base64,' + base64.b64encode(buf.read()).decode('utf-8')

    return render(request, 'dash_admin/charts.html', {
        'daily_chart_uri': daily_chart_uri,
        'monthly_chart_uri': monthly_chart_uri
    })
