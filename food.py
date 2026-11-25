import pandas as pd



print("\nQ1. Restaurant with the highest number of food items")
df = pd.read_csv("fastfood.csv")

item_counts = df["restaurant"].value_counts()
print("Restaurants with the Most Food Items:\n")
print(item_counts)



print("\nQ2. Top 10 food items with the highest number of calories")
df = pd.read_csv("fastfood.csv")

top_10 = df.nlargest(10, "calories")[["restaurant", "item", "calories"]]
print("Top 10 Highest-Calorie Food Items:\n")
print(top_10.to_string(index=False))



print("\nQ3. Average calorie count of food items for each restaurant")
df = pd.read_csv("fastfood.csv")

avg_calories = df.groupby("restaurant")["calories"].mean().sort_values(ascending=False)
print("Average Calories by Restaurant:\n")
print(avg_calories.round(2))



print("\nQ4. Restaurant offering food items with highest average protein content")
df = pd.read_csv("fastfood.csv")

avg_protein = df.groupby("restaurant")["protein"].mean().sort_values(ascending=False)
print("Average Protein by Restaurant:\n")
print(avg_protein.round(2))



print("\nQ5. Restaurant with highest and lowest average total fat")
df = pd.read_csv("fastfood.csv")

avg_fat = df.groupby("restaurant")["total_fat"].mean().sort_values(ascending=False)
print("Highest Average Total Fat:")
print(avg_fat.index[0], "-", round(avg_fat.iloc[0], 2), "g")
print("\nLowest Average Total Fat:")
print(avg_fat.index[-1], "-", round(avg_fat.iloc[-1], 2), "g")



print("\nQ6. Food items containing highest amount of sugar and their calories")
df = pd.read_csv("fastfood.csv")
top_10 = df.nlargest(10, "sugar")
print("Food Items with the Highest Sugar Content:")
for _, row in top_10.iterrows():
    print(f"{row['restaurant']} - {row['item']}")
    print(f"  Sugar: {row['sugar']} g | Calories: {row['calories']}")



print("\nQ7. How food item type (Salad vs Other) affects nutrition")
df = pd.read_csv("fastfood.csv")

print("Food Item Type Counts:\n")
print(df["salad"].value_counts())
print("\nSalad items:", (df["salad"] == "Salad").sum())
print("Other items:", (df["salad"] == "Other").sum())



print("\nQ8. Best combination of low calories and high protein")
df = pd.read_csv("fastfood.csv")
low_cal = df["calories"].median()
high_protein = df["protein"].median()
choices = df[(df["calories"] <= low_cal) & (df["protein"] >= high_protein)].copy()
choices["Protein_per_100cal"] = choices["protein"] / choices["calories"] * 100
best = choices.sort_values("Protein_per_100cal", ascending=False).head(10)
print("Best Low-Calorie, High-Protein Items:")
for _, row in best.iterrows():
    print(f"{row['restaurant']} - {row['item']}")
    print(f"  Kcal: {row['calories']} | Protein: {row['protein']} g | Ratio: {row['Protein_per_100cal']:.2f}")



print("\nQ9. Identify the 10 least healthy food items using a Health Risk Score")
df = pd.read_csv("fastfood.csv")
risk_cols = ["calories", "total_fat", "sat_fat", "trans_fat", "cholesterol", "sodium", "sugar"]
scaled = (df[risk_cols] - df[risk_cols].min()) / (df[risk_cols].max() - df[risk_cols].min())
df["Health_Risk_Score"] = scaled.mean(axis=1) * 100
top_10 = df.sort_values("Health_Risk_Score", ascending=False).head(10)
print("10 Food Items with the Highest Health Risk Score:")
for _, row in top_10.iterrows():
    print(f"{row['restaurant']} - {row['item']}")
    print(f"  Kcal {row['calories']} | Fat {row['total_fat']}g | Na {row['sodium']} | Sugar {row['sugar']}g | Risk {row['Health_Risk_Score']:.2f}")



print("\nQ10. Compare nutritional profiles and rank healthiest overall restaurant menu")
df = pd.read_csv("fastfood.csv")
positive = ["protein", "fiber"]
negative = ["calories", "total_fat", "sat_fat", "trans_fat", "cholesterol", "sodium", "sugar"]
profile = df.groupby("restaurant")[positive + negative].mean()
scaled = profile.copy()
for col in positive:
    scaled[col] = (profile[col] - profile[col].min()) / (profile[col].max() - profile[col].min())
for col in negative:
    scaled[col] = 1 - (profile[col] - profile[col].min()) / (profile[col].max() - profile[col].min())
profile["Health_Index"] = scaled.mean(axis=1) * 100
profile = profile.sort_values("Health_Index", ascending=False)
print("Restaurant Menu Health Ranking:")
for restaurant, row in profile.iterrows():
    print(restaurant)
    print(f"  Kcal {row['calories']:.1f} | Fat {row['total_fat']:.1f}g | Protein {row['protein']:.1f}g")
    print(f"  Fiber {row['fiber']:.1f}g | Index {row['Health_Index']:.2f}")
