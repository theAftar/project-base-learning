import pandas as pd



print("\nQ1. Top 10 batsmen based on total runs scored across all matches")
df = pd.read_csv("teams_clean.csv")

top_10 = df.groupby("Player")["R"].sum().sort_values(ascending=False).head(10)

print("Top 10 Batsmen by Total Runs:\n")
print(top_10)



print("\nQ2. Top 10 players with highest strike rate (at least 50 balls faced)")
df = pd.read_csv("teams_clean.csv")

player_stats = df.groupby("Player").agg(
    Total_Runs=("R", "sum"),
    Total_Balls=("B", "sum")
)
player_stats = player_stats[player_stats["Total_Balls"] >= 50]
player_stats["Strike_Rate"] = player_stats["Total_Runs"] / player_stats["Total_Balls"] * 100

top_10 = player_stats.sort_values("Strike_Rate", ascending=False).head(10)
print("Top 10 Players with Highest Strike Rate:\n")
print(top_10.round(2))



print("\nQ3. Player with most fours and player with most sixes")
df = pd.read_csv("teams_clean.csv")

player_stats = df.groupby("Player")[["4s", "6s"]].sum()
most_fours = player_stats["4s"].idxmax()
most_sixes = player_stats["6s"].idxmax()

print("Player with Most Fours:")
print(most_fours, "-", player_stats.loc[most_fours, "4s"])
print("\nPlayer with Most Sixes:")
print(most_sixes, "-", player_stats.loc[most_sixes, "6s"])



print("\nQ4. Team with the highest number of match wins")
df = pd.read_csv("teams_clean.csv")
df["Date"] = pd.to_datetime(df["Date"], format="%d.%m.%y")
fix = {"Afganistan": "Afghanistan", "Netherland": "Netherlands", "Zimbawe": "Zimbabwe"}
for col in ["Team", "Vs"]:
    df[col] = df[col].astype(str).str.strip().replace(fix)

wins = df.groupby(["Date", "Team", "Vs"])["Win"].max().reset_index()
team_wins = wins[wins["Win"] == 1]["Team"].value_counts()
print("Team with Highest Number of Match Wins:\n")
print(team_wins.head(10))



print("\nQ5. Highest run scorer for each match")
df = pd.read_csv("teams_clean.csv")
df["Date"] = pd.to_datetime(df["Date"], format="%d.%m.%y")
fix = {"Afganistan": "Afghanistan", "Netherland": "Netherlands", "Zimbawe": "Zimbabwe"}
for col in ["Team", "Vs"]:
    df[col] = df[col].astype(str).str.strip().replace(fix)

df["Match"] = df.apply(lambda x: " vs ".join(sorted([x["Team"], x["Vs"]])), axis=1)
idx = df.groupby(["Date", "Match"])["R"].idxmax()
result = df.loc[idx, ["Date", "Match", "Player", "R"]].sort_values(["Date", "Match"])
print("Highest Run Scorer for Each Match:\n")
print(result.to_string(index=False))



print("\nQ6. Compare performance while Chasing vs Batting First")
df = pd.read_csv("teams_clean.csv")

innings = df.groupby(["Date", "Team", "Vs", "Chase"], as_index=False).agg(
    Runs=("R", "sum"), Balls=("B", "sum"), Win=("Win", "max")
)
comparison = innings.groupby("Chase").agg(
    Innings=("Team", "count"), Total_Runs=("Runs", "sum"),
    Avg_Score=("Runs", "mean"), Total_Balls=("Balls", "sum"), Wins=("Win", "sum")
)
comparison["Strike_Rate"] = comparison["Total_Runs"] / comparison["Total_Balls"] * 100
comparison["Win_Rate"] = comparison["Wins"] / comparison["Innings"] * 100
comparison.index = comparison.index.map({0: "Batting First", 1: "Chasing"})
print("Performance Comparison:\n")
print(comparison.round(2))



print("\nQ7. Top 10 bowlers based on total wickets taken and economy rates")
df = pd.read_csv("teams_clean.csv")

bowlers = df["Dismissal"].str.extract(r"\bb\s+(.+)$", expand=False).dropna().str.strip()
top_10 = bowlers.value_counts().head(10).rename("Wickets").to_frame()
top_10["Average_Economy"] = "Not available"

print("Top 10 Bowlers by Wickets:\n")
print(top_10)
print("\nEconomy rate cannot be calculated from the available columns.")



print("\nQ8. Most runs through boundaries and strike rate comparison")
df = pd.read_csv("teams_clean.csv")

stats = df.groupby("Player").agg(
    Runs=("R", "sum"), Balls=("B", "sum"), Fours=("4s", "sum"), Sixes=("6s", "sum")
)
stats["Boundary_Runs"] = stats["Fours"] * 4 + stats["Sixes"] * 6
stats["Strike_Rate"] = stats["Runs"] / stats["Balls"] * 100

top_10 = stats.sort_values("Boundary_Runs", ascending=False).head(10)
print("Top 10 Players by Boundary Runs:\n")
print(top_10.round(2))



print("\nQ9. Player Performance Score (Top 20 Batsmen)")
df = pd.read_csv("teams_clean.csv")

players = df.groupby("Player").agg(Runs=("R", "sum"), Balls=("B", "sum"))
players["Strike_Rate"] = players["Runs"] / players["Balls"] * 100
players["Run_Score"] = (players["Runs"] - players["Runs"].min()) / (players["Runs"].max() - players["Runs"].min()) * 100
players["SR_Score"] = (players["Strike_Rate"] - players["Strike_Rate"].min()) / (players["Strike_Rate"].max() - players["Strike_Rate"].min()) * 100
players["Performance_Score"] = 0.7 * players["Run_Score"] + 0.3 * players["SR_Score"]

top_20 = players.sort_values("Performance_Score", ascending=False).head(20)
print("Top 20 Batsmen by Performance Score:\n")
print(top_20[["Runs", "Strike_Rate", "Performance_Score"]].round(2))



print("\nQ10. Combine Batting & Bowling Data for Top 10 All-Round Performers")
df = pd.read_csv("teams_clean.csv")
df["Player"] = df["Player"].astype(str).str.strip()

batting = df.groupby("Player")["R"].sum().rename("Runs")
bowlers = df["Dismissal"].str.extract(r"\bb\s+(.+)$", expand=False).dropna().str.strip()
wickets = bowlers.value_counts().rename("Wickets")
all_rounders = pd.concat([batting, wickets], axis=1, join="inner").dropna()
all_rounders = all_rounders[(all_rounders["Runs"] > 0) & (all_rounders["Wickets"] > 0)]
all_rounders["Run_Score"] = (all_rounders["Runs"] - all_rounders["Runs"].min()) / (all_rounders["Runs"].max() - all_rounders["Runs"].min()) * 100
all_rounders["Wicket_Score"] = (all_rounders["Wickets"] - all_rounders["Wickets"].min()) / (all_rounders["Wickets"].max() - all_rounders["Wickets"].min()) * 100
all_rounders["All_Round_Score"] = (all_rounders["Run_Score"] + all_rounders["Wicket_Score"]) / 2

top_10 = all_rounders.sort_values("All_Round_Score", ascending=False).head(10)
print("Top 10 All-Round Performers:\n")
print(top_10[["Runs", "Wickets", "All_Round_Score"]].round(2))
