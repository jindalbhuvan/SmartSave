from database.queries import get_all_transactions


df = get_all_transactions()

print("\n===== MYSQL TRANSACTION TEST =====\n")

print("Total transactions:", len(df))

print("\nFirst 5 transactions:")
print(df.head())

print("\nColumns:")
print(df.columns.tolist())