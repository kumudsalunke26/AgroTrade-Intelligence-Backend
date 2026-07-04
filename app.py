

# from flask import Flask, request, jsonify
# import joblib
# import pandas as pd
# from flask_cors import CORS
# import os

# app = Flask(__name__)

# # ✅ Restrict CORS (change after frontend deploy)
# CORS(app, origins=["*"])  # later replace with your Vercel URL

# # # ✅ Load model safely
# # model = joblib.load("crop_price_model.pkl")

# # # ✅ Load dataset
# # df = pd.read_csv("AgroTrade_Maharashtra_Crop_Prices_Profit.csv")
# # df.columns = df.columns.str.strip()

# import os

# model = None
# df = None

# def load_resources():
#     global model, df

#     BASE_DIR = os.path.dirname(os.path.abspath(__file__))

#     model_path = os.path.join(BASE_DIR, "crop_price_model_clean.pkl")
#     csv_path = os.path.join(BASE_DIR, "AgroTrade_Maharashtra_Crop_Prices_Profit.csv")

#     print("Loading model and dataset...")
#     print(os.listdir(BASE_DIR))

#     model = joblib.load(model_path)
#     df = pd.read_csv(csv_path)

#     print("Loaded successfully ✔")


# load_resources()
# @app.route("/")
# def home():
#     return "Backend Running ✅"


# # ===============================
# # 🔹 PREDICT
# # ===============================
# @app.route("/predict", methods=["POST"])
# def predict():
#     try:
#         data = request.json

#         crop = data.get("crop") or data.get("Crop")
#         season = data.get("season") or data.get("Season")
#         state = data.get("state") or data.get("State")
#         market = data.get("market") or data.get("Market")
#         month = data.get("month") or data.get("Month")
#         year = data.get("year") or data.get("Year")
#         cost = data.get("cost") or data.get("Cost_per_Quintal")

#         if not all([crop, season, state, market, month, year, cost]):
#             return jsonify({"error": "Missing required fields"})

#         input_data = pd.DataFrame([{
#             "Month": int(month),
#             "State": state.capitalize(),
#             "Cost_per_Quintal": float(cost),
#             "Season": season.capitalize(),
#             "Crop": crop.capitalize(),
#             "Market": market.capitalize(),
#             "Year": int(year)
#         }])

#         prediction = model.predict(input_data)[0]
#         profit = float(prediction) - float(cost)

#         return jsonify({
#             "predicted_price": float(prediction),
#             "profit": float(profit)
#         })

#     except Exception as e:
#         return jsonify({"error": str(e)})


# # ===============================
# # 🔹 SEASONAL ANALYSIS
# # ===============================
# @app.route("/seasonal-analysis", methods=["POST"])
# def seasonal_analysis():
#     try:
#         data = request.json
#         season = data["season"].capitalize()

#         filtered = df[df["Season"] == season]

#         if filtered.empty:
#             return jsonify({"error": "No data for this season"})

#         avg_price = filtered["Price_per_Quintal"].mean()

#         sample = filtered.iloc[0:1].copy()

#         sample_input = pd.DataFrame([{
#             "Month": int(sample["Month"].values[0]),
#             "State": sample["State"].values[0],
#             "Cost_per_Quintal": float(sample["Cost_per_Quintal"].values[0]),
#             "Season": sample["Season"].values[0],
#             "Crop": sample["Crop"].values[0],
#             "Market": sample["Market"].values[0],
#             "Year": int(sample["Year"].values[0])
#         }])

#         predicted_price = model.predict(sample_input)[0]
#         overall_avg = df["Price_per_Quintal"].mean()

#         insight = "Prices are generally HIGHER in this season 📈" if avg_price > overall_avg else "Prices are generally LOWER in this season 📉"

#         return jsonify({
#             "average_price": float(avg_price),
#             "predicted_price": float(predicted_price),
#             "insight": insight
#         })

#     except Exception as e:
#         return jsonify({"error": str(e)})


# # ===============================
# # 🔹 DASHBOARD
# # ===============================
# @app.route("/dashboard", methods=["GET"])
# def dashboard():
#     try:
#         df["Profit"] = df["Price_per_Quintal"] - df["Cost_per_Quintal"]

#         return jsonify({
#             "avg_price": float(df["Price_per_Quintal"].mean()),
#             "most_profitable_crop": df.groupby("Crop")["Profit"].mean().idxmax(),
#             "high_risk_crop": df.groupby("Crop")["Price_per_Quintal"].std().idxmax(),
#             "best_season": df.groupby("Season")["Price_per_Quintal"].mean().idxmax(),
#             "trend": df.groupby("Month")["Price_per_Quintal"].mean().reset_index().to_dict(orient="records"),
#             "crop_data": df.groupby("Crop")["Price_per_Quintal"].mean().reset_index().to_dict(orient="records")
#         })

#     except Exception as e:
#         return jsonify({"error": str(e)})




#     # ✅ IMPORTANT FOR RENDER
# if __name__ == "__main__":
#     port = int(os.environ.get("PORT", 5000))
#     app.run(host="0.0.0.0", port=port)


from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import joblib
import os

app = Flask(__name__)
CORS(app)

# ==========================================================
# LOAD MODEL + DATASET
# ==========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "clean_agri_model_new.pkl")
DATA_PATH = os.path.join(BASE_DIR, "clean_agri_dataset.csv")

model = joblib.load(MODEL_PATH)
df = pd.read_csv(DATA_PATH)


df.columns = df.columns.str.strip().str.lower()

# Profit only for dashboard statistics
if "profit" not in df.columns:
    df["profit"] = df["price_per_quintal"] - df["cost_per_quintal"]

print("===================================")
print("AgroTrade AI Backend Loaded")
print("Rows:", len(df))
print("===================================")


# ==========================================================
# HOME
# ==========================================================

@app.route("/")
def home():
    return "AgroTrade AI Backend Running Successfully"


# ==========================================================
# PREDICT
# ==========================================================

@app.route("/predict", methods=["POST"])
def predict():

    try:

        data = request.json

        crop = str(data["crop"]).title().strip()
        market = str(data["market"]).title().strip()
        season = str(data["season"]).title().strip()

        month = int(data["month"])
        year = int(data["year"])

        cost = float(data["cost"])
        overall_avg = df["price_per_quintal"].mean()

        crop_avg = df.loc[df["crop"] == crop, "crop_avg_price"].mean()
        market_avg = df.loc[df["market"] == market, "market_avg_price"].mean()
        season_avg = df.loc[df["season"] == season, "season_avg_price"].mean()
        month_avg = df.loc[df["month"] == month, "month_avg_price"].mean()

        crop_avg = crop_avg if pd.notna(crop_avg) else overall_avg
        market_avg = market_avg if pd.notna(market_avg) else overall_avg
        season_avg = season_avg if pd.notna(season_avg) else overall_avg
        month_avg = month_avg if pd.notna(month_avg) else overall_avg
        sample = pd.DataFrame([{
    "state": "Maharashtra",
    "market": market,
    "crop": crop,
    "month": month,
    "year": year,
    "cost_per_quintal": cost,
    "season": season,
    "crop_avg_price": crop_avg,
    "market_avg_price": market_avg,
    "season_avg_price": season_avg,
    "month_avg_price": month_avg
}])

        predicted_price = float(model.predict(sample)[0])

        profit = predicted_price - cost

        return jsonify({

            "predicted_price": round(predicted_price, 2),
            "profit": round(profit, 2)

        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        })




@app.route("/dashboard", methods=["GET"])
def dashboard():
    try:
        temp = df.copy()

        avg_price = float(temp["price_per_quintal"].mean())

        most_profitable_crop = str(
            temp.groupby("crop")["profit"].mean().idxmax()
        )

        most_loss_crop = str(
            temp.groupby("crop")["profit"].mean().idxmin()
        )

        best_season = str(
            temp.groupby("season")["profit"].mean().idxmax()
        )

        high_risk_crop = str(
            temp.groupby("crop")["price_per_quintal"].std().idxmax()
        )

        trend = (
            temp.groupby("month")["price_per_quintal"]
            .mean()
            .reset_index()
        )

        crop_data = (
            temp.groupby("crop")["price_per_quintal"]
            .mean()
            .reset_index()
        )

        return jsonify({
            "avg_price": float(avg_price),
            "avg_profit": float(temp["profit"].mean()),
            "total_records": int(len(temp)),

            "most_profitable_crop": most_profitable_crop,
            "most_loss_crop": most_loss_crop,
            "best_season": best_season,
            "high_risk_crop": high_risk_crop,

            "trend": trend.to_dict(orient="records"),
            "crop_data": crop_data.to_dict(orient="records")
        })

    except Exception as e:
        return jsonify({"error": str(e)})
    

# ==========================================================
# SEASONAL ANALYSIS (ENHANCED + CONSISTENT)
# ==========================================================

@app.route("/seasonal-analysis", methods=["POST"])
def seasonal_analysis():

    try:
        season = request.json["season"].title()

        temp = df[df["season"] == season]

        if temp.empty:
            return jsonify({
                "error": "No data found for this season"
            }), 404

        avg_price = float(temp["price_per_quintal"].mean())
        avg_profit = float(temp["profit"].mean())

        crop_perf = temp.groupby("crop")["profit"].mean()

        best_crop = str(crop_perf.idxmax())
        worst_crop = str(crop_perf.idxmin())

        monthly_trend = (
            temp.groupby("month")["price_per_quintal"]
            .mean()
            .reset_index()
            .to_dict(orient="records")
        )

        overall_avg = float(df["price_per_quintal"].mean())

        insight = (
            "This is a HIGH price season 📈"
            if avg_price > overall_avg
            else "This is a LOW price season 📉"
        )

        return jsonify({
            "season": season,
            "average_price": round(avg_price, 2),
            "average_profit": round(avg_profit, 2),
            "best_crop": best_crop,
            "worst_crop": worst_crop,
            "monthly_trend": monthly_trend,
            "insight": insight,
            "total_records": int(len(temp))
        })

    except Exception as e:
        return jsonify({"error": str(e)})
    
    # ==========================================================
# MARKET COMPARISON
# ==========================================================

@app.route("/market-comparison", methods=["POST"])
def market_comparison():

    try:

        crop = request.json["crop"].title().strip()

        temp = df[df["crop"] == crop]

        if temp.empty:
            return jsonify({
                "error": "Crop not found."
            }), 404

        # Average price & profit by market
        market_stats = (
            temp.groupby("market")
            .agg({
                "price_per_quintal": "mean",
                "profit": "mean"
            })
            .reset_index()
            .sort_values("price_per_quintal", ascending=False)
        )

        markets = []

        for _, row in market_stats.iterrows():

            markets.append({

                "market": row["market"],

                "avg_price": round(float(row["price_per_quintal"]), 2),

                "avg_profit": round(float(row["profit"]), 2)

            })

        best_market = market_stats.iloc[0]["market"]

        highest_price = float(
            market_stats["price_per_quintal"].max()
        )

        lowest_price = float(
            market_stats["price_per_quintal"].min()
        )

        avg_profit = float(
            market_stats["profit"].max()
        )

        insight = (
            f"{best_market} is the best market to sell {crop}. "
            f"It offers the highest average selling price "
            f"with an expected average profit of ₹{avg_profit:.2f} per quintal."
        )

        return jsonify({

            "crop": crop,

            "markets": markets,

            "best_market": best_market,

            "highest_price": round(highest_price, 2),

            "lowest_price": round(lowest_price, 2),

            "insight": insight

        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500
    
    # ==========================================================
# CROP RECOMMENDATION
# ==========================================================

@app.route("/crop-recommendation", methods=["POST"])
def crop_recommendation():

    try:

        data = request.json

        season = data["season"].title()
        market = data["market"].title()

        temp = df[
            (df["season"] == season) &
            (df["market"] == market)
        ]

        if temp.empty:
            return jsonify({
                "error": "No data found"
            }), 404

        recommendation = (
            temp.groupby("crop")
            .agg(
                avg_price=("price_per_quintal", "mean"),
                avg_profit=("profit", "mean")
            )
            .reset_index()
            .sort_values(
                by="avg_profit",
                ascending=False
            )
        )

        best = recommendation.iloc[0]

        return jsonify({

            "recommended_crop": best["crop"],

            "expected_price": round(
                best["avg_price"], 2
            ),

            "expected_profit": round(
                best["avg_profit"], 2
            ),

            "reason":
            "Highest average profit in the selected market and season."

        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500
        
# ==========================================================
# GET MARKETS
# ==========================================================

@app.route("/markets", methods=["GET"])
def markets():

    markets = sorted(
        df["market"]
        .dropna()
        .unique()
        .tolist()
    )

    return jsonify(markets)
# ==========================================================
# RUN
# ==========================================================

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=True
    )