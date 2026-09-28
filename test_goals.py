
from database.goals import get_customer_goals


customer_id = "CUST0001"

goals = get_customer_goals(customer_id)

print("Customer:", customer_id)
print("Number of goals:", len(goals))

for goal in goals:
    print(goal)