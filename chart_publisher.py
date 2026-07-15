from pptx.chart.data import CategoryChartData


def update_chart(shape, df):

    if not shape.has_chart:
        return

    chart = shape.chart

    chart_data = CategoryChartData()

    categories = []

    values = []

    first_column = df.columns[0]
    second_column = df.columns[1]

    for _, row in df.iterrows():

        categories.append(
            str(row[first_column])
        )

        values.append(
            float(row[second_column])
        )

    chart_data.categories = categories

    chart_data.add_series(
        second_column,
        values
    )

    chart.replace_data(
        chart_data
    )