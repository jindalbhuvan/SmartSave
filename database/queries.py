import pandas as pd

from database.connection import get_connection


def get_all_transactions():
    connection = get_connection()

    query = """
    SELECT
        transaction_id,
        customer_id,
        transaction_date,
        transaction_type,
        category,
        description,
        amount
    FROM transactions
    """

    df = pd.read_sql(query, connection)

    connection.close()

    return df