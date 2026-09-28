from src.financial_health import (
    calculate_financial_health,
    generate_recommendations
)


health = calculate_financial_health(

    monthly_income=80000,

    monthly_expenses=50000,

    monthly_savings=30000,

    monthly_debt=10000,

    emergency_fund=180000,

    monthly_essential_expenses=30000,

    goal_progress=35
)


print("\nFINANCIAL HEALTH")
print("=" * 50)

for key, value in health.items():
    print(
        f"{key}: {value}"
    )


print("\nRECOMMENDATIONS")
print("=" * 50)

recommendations = generate_recommendations(
    health
)

for recommendation in recommendations:
    print("•", recommendation)