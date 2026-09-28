from database.connection import get_connection


def get_customer_financial_profile(customer_id):

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
    SELECT
        transaction_type,
        SUM(amount) AS total_amount
    FROM transactions
    WHERE customer_id = %s
    GROUP BY transaction_type
    """

    cursor.execute(query, (customer_id,))

    results = cursor.fetchall()

    cursor.close()
    connection.close()

    income = 0
    expenses = 0

    for row in results:

        transaction_type = row["transaction_type"]
        amount = float(row["total_amount"])

        if transaction_type.lower() == "income":
            income += amount

        elif transaction_type.lower() == "expense":
            expenses += amount

    savings = income - expenses

    return {
        "customer_id": customer_id,
        "income": income,
        "expenses": expenses,
        "savings": savings
    }