from src.customer_health import get_customer_health


CUSTOMER_ID = "CUST0001"


result = get_customer_health(
    CUSTOMER_ID
)


print("\nCUSTOMER FINANCIAL PROFILE")
print("=" * 60)

profile = result["profile"]

for key, value in profile.items():

    print(
        f"{key}: {value}"
    )


print("\nFINANCIAL HEALTH")
print("=" * 60)

health = result["health"]

for key, value in health.items():

    print(
        f"{key}: {value}"
    )


print("\nRECOMMENDATIONS")
print("=" * 60)

for recommendation in result["recommendations"]:

    print(
        "•",
        recommendation
    )