import pandas as pd



print("\nQ1. Brand with the highest number of mobile models")
df = pd.read_excel("mobile_sales.xlsx")

brand_counts = df["Brands"].value_counts().head(10)
print("Top Mobile Brands by Number of Models:\n")
print(brand_counts)



print("\nQ2. Top 10 mobile models based on their selling price")
df = pd.read_excel("mobile_sales.xlsx")

model_prices = df.groupby("Mobile").agg(
    Listings=("Selling Price", "count"),
    Avg_Selling_Price=("Selling Price", "mean")
)
top_10 = model_prices.sort_values("Avg_Selling_Price", ascending=False).head(10)
print("Top 10 Mobile Models by Selling Price:\n")
print(top_10.round(2))



print("\nQ3. Average selling price of mobiles for each brand")
df = pd.read_excel("mobile_sales.xlsx")

avg_price = df.groupby("Brands")["Selling Price"].mean().sort_values(ascending=False)
print("Average Selling Price by Brand:\n")
print(avg_price.round(2))



print("\nQ4. Mobile brand offering the highest average discount")
df = pd.read_excel("mobile_sales.xlsx")
df["Discount_Pct"] = df["Discount"] / df["Original Price"] * 100

brand_discount = df.groupby("Brands").agg(
    Avg_Discount=("Discount", "mean"),
    Avg_Discount_Pct=("Discount_Pct", "mean")
).sort_values("Avg_Discount", ascending=False)
print("Brands with Highest Average Discount:\n")
print(brand_discount.head(10).round(2))



print("\nQ5. Brands with highest average customer rating and average selling price")
df = pd.read_excel("mobile_sales.xlsx")

brand_summary = df.groupby("Brands").agg(
    Avg_Rating=("Rating", "mean"),
    Avg_Selling_Price=("Selling Price", "mean"),
    Listings=("Mobile", "count")
).sort_values("Avg_Rating", ascending=False)
print("Brands by Average Rating and Selling Price:\n")
print(brand_summary.head(10).round(2))



print("\nQ6. How mobile storage capacity affects average selling price")
df = pd.read_excel("mobile_sales.xlsx")

storage_price = df.groupby("Storage").agg(
    Listings=("Mobile", "count"),
    Avg_Selling_Price=("Selling Price", "mean")
)
storage_price = storage_price[storage_price["Listings"] >= 10]
print("Storage Capacity vs Average Selling Price:\n")
print(storage_price.round(2))



print("\nQ7. Mobile models providing highest discount amount and percentage discounted")
df = pd.read_excel("mobile_sales.xlsx")
df["Discount_Pct"] = df["Discount"] / df["Original Price"] * 100
model_discount = df.groupby("Mobile").agg(
    Discount=("Discount", "mean"), Discount_Pct=("Discount_Pct", "mean"), Listings=("Mobile", "count")
)
top_10 = model_discount.sort_values("Discount", ascending=False).head(10)
print("Mobile Models with Highest Discount:")
for model, row in top_10.iterrows():
    print(model)
    print(f"  Discount: Rs. {row['Discount']:.0f} | Discount: {row['Discount_Pct']:.2f}% | Listings: {row['Listings']}")



print("\nQ8. Combination of Memory and Storage offering best balance of Price and Rating")
df = pd.read_excel("mobile_sales.xlsx")
df["Memory_GB"] = pd.to_numeric(df["Memory"].astype(str).str.extract(r"(\d+(?:\.\d+)?)")[0], errors="coerce")
groups = df.groupby(["Memory_GB", "Storage"]).agg(
    Listings=("Mobile", "count"), Avg_Price=("Selling Price", "mean"), Avg_Rating=("Rating", "mean")
).reset_index()
groups = groups[groups["Listings"] >= 5].copy()
groups["Rating_Score"] = (groups["Avg_Rating"] - groups["Avg_Rating"].min()) / (groups["Avg_Rating"].max() - groups["Avg_Rating"].min())
groups["Price_Score"] = 1 - (groups["Avg_Price"] - groups["Avg_Price"].min()) / (groups["Avg_Price"].max() - groups["Avg_Price"].min())
groups["Balance_Score"] = (groups["Rating_Score"] + groups["Price_Score"]) / 2 * 100
print("Best Memory and Storage Combinations:\n")
print(groups.sort_values("Balance_Score", ascending=False).head(10).round(2).to_string(index=False))



print("\nQ9. Top 10 mobile models providing best value for money")
df = pd.read_excel("mobile_sales.xlsx")
models = df.groupby("Mobile").agg(
    Listings=("Mobile", "count"), Avg_Price=("Selling Price", "mean"), Avg_Rating=("Rating", "mean")
).reset_index()
models = models[models["Listings"] >= 2]
models["Value_Score"] = models["Avg_Rating"] / (models["Avg_Price"] / 10000)
top_10 = models.sort_values("Value_Score", ascending=False).head(10)
print("Top 10 Mobile Models by Value for Money:")
for _, row in top_10.iterrows():
    print(row["Mobile"])
    print(f"  Listings: {row['Listings']} | Price: Rs. {row['Avg_Price']:.2f} | Rating: {row['Avg_Rating']:.1f} | Value: {row['Value_Score']:.2f}")



print("\nQ10. Factors determining whether a mobile is classified as a Good Product")
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

df = pd.read_excel("mobile_sales.xlsx")
df["Memory_GB"] = pd.to_numeric(df["Memory"].astype(str).str.extract(r"(\d+(?:\.\d+)?)")[0], errors="coerce")
features = ["Selling Price", "Original Price", "Discount", "Memory_GB", "Storage"]
data = df[features + ["Rating"]].dropna()
data["Good_Product"] = (df.loc[data.index, "Rating"] >= 4.2).astype(int)
X_train, X_test, y_train, y_test = train_test_split(data[features], data["Good_Product"], test_size=0.2, random_state=42, stratify=data["Good_Product"])
model = RandomForestClassifier(n_estimators=200, random_state=42, class_weight="balanced")
model.fit(X_train, y_train)
importance = pd.Series(model.feature_importances_, index=features).sort_values(ascending=False)
print("Feature Importance for Good Product:\n")
print(importance.round(3))
print("\nTest Accuracy:", round(accuracy_score(y_test, model.predict(X_test)), 3))
