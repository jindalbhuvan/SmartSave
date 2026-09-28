import mysql.connector
from database.connection import get_connection


# ---------------------------------------------------------
# CREATE A NEW GOAL
# ---------------------------------------------------------
def create_goal(
    customer_id,
    goal_name,
    goal_category,
    target_amount,
    current_amount,
    target_date
):
    connection = get_connection()
    cursor = connection.cursor()

    query = """
    INSERT INTO goals
    (
        customer_id,
        goal_name,
        goal_category,
        target_amount,
        current_amount,
        target_date
    )
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    values = (
        customer_id,
        goal_name,
        goal_category,
        target_amount,
        current_amount,
        target_date
    )

    cursor.execute(query, values)

    connection.commit()

    goal_id = cursor.lastrowid

    cursor.close()
    connection.close()

    return goal_id


# ---------------------------------------------------------
# GET ALL GOALS OF A CUSTOMER
# ---------------------------------------------------------
def get_customer_goals(customer_id):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
    SELECT
        goal_id,
        customer_id,
        goal_name,
        goal_category,
        target_amount,
        current_amount,
        target_date,
        status,
        created_at
    FROM goals
    WHERE customer_id = %s
    ORDER BY target_date
    """

    cursor.execute(query, (customer_id,))

    goals = cursor.fetchall()

    cursor.close()
    connection.close()

    return goals


# ---------------------------------------------------------
# ADD CONTRIBUTION TO A GOAL
# ---------------------------------------------------------
def add_contribution(
    goal_id,
    contribution_date,
    amount,
    source
):
    connection = get_connection()
    cursor = connection.cursor()

    # Insert contribution into contributions table
    insert_query = """
    INSERT INTO contributions
    (
        goal_id,
        contribution_date,
        amount,
        source
    )
    VALUES (%s, %s, %s, %s)
    """

    values = (
        goal_id,
        contribution_date,
        amount,
        source
    )

    cursor.execute(insert_query, values)

    # Update the current amount of the goal
    update_query = """
    UPDATE goals
    SET current_amount = current_amount + %s
    WHERE goal_id = %s
    """

    cursor.execute(
        update_query,
        (amount, goal_id)
    )

    connection.commit()

    contribution_id = cursor.lastrowid

    cursor.close()
    connection.close()

    return contribution_id


# ---------------------------------------------------------
# GET CONTRIBUTION HISTORY FOR A GOAL
# ---------------------------------------------------------
def get_goal_contributions(goal_id):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
    SELECT
        contribution_id,
        goal_id,
        contribution_date,
        amount,
        source
    FROM contributions
    WHERE goal_id = %s
    ORDER BY contribution_date
    """

    cursor.execute(query, (goal_id,))

    contributions = cursor.fetchall()

    cursor.close()
    connection.close()

    return contributions