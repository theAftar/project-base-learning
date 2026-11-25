from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
DATA = ROOT
OUT = ROOT / "Visualization"
OUT.mkdir(exist_ok=True)

cricket = pd.read_csv(DATA / "teams_clean.csv")
food = pd.read_csv(DATA / "fastfood.csv")
mobile = pd.read_excel(DATA / "mobile_sales.xlsx")

for col in ["R", "B", "4s", "6s"]:
    cricket[col] = pd.to_numeric(cricket[col], errors="coerce").fillna(0)

# Cricket visualizations
runs = cricket.groupby("Player")["R"].sum().sort_values(ascending=False).head(10).sort_values()
fig, ax = plt.subplots(figsize=(10, 5.5))
runs.plot(kind="barh", ax=ax)
ax.set_title("Top 10 Batsmen by Total Runs")
ax.set_xlabel("Total runs")
ax.set_ylabel("Player")
ax.grid(axis="x", alpha=.25)
fig.tight_layout(); fig.savefig(OUT / "cricket_top10_runs.png", dpi=180); plt.close(fig)

players = cricket.groupby("Player").agg(Runs=("R", "sum"), Balls=("B", "sum"))
players = players[players["Balls"] >= 50].copy()
players["Strike Rate"] = players["Runs"] / players["Balls"] * 100
sr = players["Strike Rate"].sort_values(ascending=False).head(10).sort_values()
fig, ax = plt.subplots(figsize=(10, 5.5))
sr.plot(kind="barh", ax=ax)
ax.set_title("Top 10 Strike Rates (Minimum 50 Balls)")
ax.set_xlabel("Strike rate")
ax.set_ylabel("Player")
ax.grid(axis="x", alpha=.25)
fig.tight_layout(); fig.savefig(OUT / "cricket_top10_strike_rate.png", dpi=180); plt.close(fig)

boundaries = cricket.groupby("Player").agg(Fours=("4s", "sum"), Sixes=("6s", "sum"))
boundaries["Boundary Runs"] = boundaries["Fours"] * 4 + boundaries["Sixes"] * 6
bnd = boundaries["Boundary Runs"].sort_values(ascending=False).head(10).sort_values()
fig, ax = plt.subplots(figsize=(10, 5.5))
bnd.plot(kind="barh", ax=ax)
ax.set_title("Top 10 Players by Runs from Boundaries")
ax.set_xlabel("Boundary runs")
ax.set_ylabel("Player")
ax.grid(axis="x", alpha=.25)
fig.tight_layout(); fig.savefig(OUT / "cricket_boundary_runs.png", dpi=180); plt.close(fig)

# Food visualizations
food["calories"] = pd.to_numeric(food["calories"], errors="coerce")
food["protein"] = pd.to_numeric(food["protein"], errors="coerce")
cal = food.groupby("restaurant")["calories"].mean().sort_values()
fig, ax = plt.subplots(figsize=(10, 5.5))
cal.plot(kind="barh", ax=ax)
ax.set_title("Average Calories per Menu Item by Restaurant")
ax.set_xlabel("Average calories")
ax.set_ylabel("Restaurant")
ax.grid(axis="x", alpha=.25)
fig.tight_layout(); fig.savefig(OUT / "food_avg_calories_by_restaurant.png", dpi=180); plt.close(fig)

top_food = food.nlargest(10, "calories").set_index("item")["calories"].sort_values()
fig, ax = plt.subplots(figsize=(10, 5.5))
top_food.plot(kind="barh", ax=ax)
ax.set_title("10 Highest-Calorie Food Items")
ax.set_xlabel("Calories")
ax.set_ylabel("Menu item")
ax.grid(axis="x", alpha=.25)
fig.tight_layout(); fig.savefig(OUT / "food_top10_calories.png", dpi=180); plt.close(fig)

protein = food.groupby("restaurant")["protein"].mean().sort_values()
fig, ax = plt.subplots(figsize=(10, 5.5))
protein.plot(kind="barh", ax=ax)
ax.set_title("Average Protein per Menu Item by Restaurant")
ax.set_xlabel("Average protein (g)")
ax.set_ylabel("Restaurant")
ax.grid(axis="x", alpha=.25)
fig.tight_layout(); fig.savefig(OUT / "food_avg_protein_by_restaurant.png", dpi=180); plt.close(fig)

# Mobile visualizations
mobile["Selling Price"] = pd.to_numeric(mobile["Selling Price"], errors="coerce")
mobile["Rating"] = pd.to_numeric(mobile["Rating"], errors="coerce")
brand_counts = mobile["Brands"].value_counts().head(10).sort_values()
fig, ax = plt.subplots(figsize=(10, 5.5))
brand_counts.plot(kind="barh", ax=ax)
ax.set_title("Top 10 Brands by Number of Listings")
ax.set_xlabel("Number of listings")
ax.set_ylabel("Brand")
ax.grid(axis="x", alpha=.25)
fig.tight_layout(); fig.savefig(OUT / "mobile_top10_brand_counts.png", dpi=180); plt.close(fig)

brand_price = mobile.groupby("Brands")["Selling Price"].mean().sort_values(ascending=False).head(10).sort_values()
fig, ax = plt.subplots(figsize=(10, 5.5))
brand_price.plot(kind="barh", ax=ax)
ax.set_title("10 Brands with Highest Average Selling Price")
ax.set_xlabel("Average selling price (INR)")
ax.set_ylabel("Brand")
ax.grid(axis="x", alpha=.25)
fig.tight_layout(); fig.savefig(OUT / "mobile_top10_average_selling_price.png", dpi=180); plt.close(fig)

fig, ax = plt.subplots(figsize=(10, 5.5))
ax.scatter(mobile["Selling Price"], mobile["Rating"], alpha=.55)
ax.set_title("Mobile Selling Price vs Customer Rating")
ax.set_xlabel("Selling price (INR)")
ax.set_ylabel("Rating")
ax.grid(alpha=.25)
fig.tight_layout(); fig.savefig(OUT / "mobile_price_vs_rating.png", dpi=180); plt.close(fig)

print(f"Saved 9 visualization images in: {OUT}")
