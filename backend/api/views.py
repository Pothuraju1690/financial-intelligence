from django.http import JsonResponse
import pandas as pd
import json
import requests
from pathlib import Path

from django.http import HttpResponse

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet

from reportlab.lib.pagesizes import letter

# =====================================================
# PATHS
# =====================================================

BASE_DIR = Path(__file__).resolve().parents[2]

DATA_DIR = BASE_DIR / "data" / "clean"


# =====================================================
# HELPER
# =====================================================

def df_to_records(df):

    return json.loads(
        df.to_json(orient="records")
    )


# =====================================================
# ALL COMPANIES
# =====================================================

def get_companies(request):

    df = pd.read_csv(
        DATA_DIR / "company_health_scores.csv"
    )

    df = df[[
        "company_id",
        "sales",
        "profit_margin",
        "health_score",
        "health_label"
    ]]

    company = request.GET.get("company")

    if company:

        df = df[
            df["company_id"]
            .astype(str)
            .str.upper()
            .str.contains(
                company.upper(),
                na=False
            )
        ]

    health = request.GET.get("health")

    if health:

        df = df[
            df["health_label"]
            .astype(str)
            .str.upper()
            == health.upper()
        ]

    sort = request.GET.get("sort")

    if sort in [
        "sales",
        "profit_margin",
        "health_score"
    ]:

        df = df.sort_values(
            by=sort,
            ascending=False
        )

    top = request.GET.get("top")

    try:

        top = int(top)

    except:

        top = 10

    data = df_to_records(
        df.head(top)
    )

    return JsonResponse({

        "status": "success",

        "count": len(data),

        "data": data
    })


# =====================================================
# SINGLE COMPANY
# =====================================================

def get_single_company(request, symbol):

    df = pd.read_csv(
        DATA_DIR / "company_health_scores.csv"
    )

    df = df[[
        "company_id",
        "sales",
        "profit_margin",
        "health_score",
        "health_label"
    ]]

    df = df[
        df["company_id"]
        .astype(str)
        .str.upper()
        == symbol.upper()
    ]

    if df.empty:

        return JsonResponse({

            "status": "error",

            "message": "Company not found"

        }, status=404)

    return JsonResponse({

        "status": "success",

        "data": df_to_records(df)[0]
    })


# =====================================================
# COMPANY DETAILS
# =====================================================

def get_company_details(request, symbol):

    symbol = symbol.upper()

    profit = pd.read_csv(
        DATA_DIR / "profit_loss_transformed.csv"
    )

    balance = pd.read_csv(
        DATA_DIR / "balance_sheet_transformed.csv"
    )

    cash = pd.read_csv(
        DATA_DIR / "cash_flow_transformed.csv"
    )

    health = pd.read_csv(
        DATA_DIR / "company_health_scores.csv"
    )

    profit_data = profit[
        profit["company_id"]
        .astype(str)
        .str.upper()
        == symbol
    ].tail(5)

    balance_data = balance[
        balance["company_id"]
        .astype(str)
        .str.upper()
        == symbol
    ].tail(5)

    cash_data = cash[
        cash["company_id"]
        .astype(str)
        .str.upper()
        == symbol
    ].tail(5)

    health_data = health[
        health["company_id"]
        .astype(str)
        .str.upper()
        == symbol
    ]

    if health_data.empty:

        return JsonResponse({

            "status": "error",

            "message": "Company not found"

        }, status=404)

    return JsonResponse({

        "status": "success",

        "company": symbol,

        "health": df_to_records(
            health_data
        )[0],

        "profit": df_to_records(
            profit_data
        ),

        "balance": df_to_records(
            balance_data
        ),

        "cashflow": df_to_records(
            cash_data
        ),
    })


# =====================================================
# COMPANY COMPARISON
# =====================================================

def compare_companies(request):

    company1 = request.GET.get(
        "company1",
        ""
    ).upper()

    company2 = request.GET.get(
        "company2",
        ""
    ).upper()

    if not company1 or not company2:

        return JsonResponse({

            "status": "error",

            "message": "Both companies required"

        }, status=400)

    df = pd.read_csv(
        DATA_DIR / "company_health_scores.csv"
    )

    df = df[[
        "company_id",
        "sales",
        "profit_margin",
        "health_score",
        "health_label"
    ]]

    comparison = df[
        df["company_id"]
        .astype(str)
        .str.upper()
        .isin([company1, company2])
    ]

    if comparison.empty:

        return JsonResponse({

            "status": "error",

            "message": "Companies not found"

        }, status=404)

    return JsonResponse({

        "status": "success",

        "companies": [
            company1,
            company2
        ],

        "data": df_to_records(comparison)
    })


# =====================================================
# COMPANY LIST
# =====================================================

def get_company_list(request):

    df = pd.read_csv(
        DATA_DIR / "company_health_scores.csv"
    )

    companies = sorted(

        df["company_id"]

        .dropna()

        .astype(str)

        .str.upper()

        .unique()

        .tolist()
    )

    return JsonResponse({

        "status": "success",

        "count": len(companies),

        "companies": companies
    })


# =====================================================
# LEADERBOARD
# =====================================================

def leaderboard(request):

    df = pd.read_csv(
        DATA_DIR / "company_health_scores.csv"
    )

    top_health = (

        df.sort_values(

            by="health_score",

            ascending=False

        )

        .head(10)

        .to_dict(orient="records")
    )

    top_profit = (

        df.sort_values(

            by="profit_margin",

            ascending=False

        )

        .head(10)

        .to_dict(orient="records")
    )

    top_sales = (

        df.sort_values(

            by="sales",

            ascending=False

        )

        .head(10)

        .to_dict(orient="records")
    )

    return JsonResponse({

        "status": "success",

        "top_health": top_health,

        "top_profit": top_profit,

        "top_sales": top_sales
    })


# =====================================================
# AI INSIGHTS ENGINE
# =====================================================

def ai_insights(request, symbol):

    symbol = symbol.upper()

    df = pd.read_csv(
        DATA_DIR / "company_health_scores.csv"
    )

    company = df[
        df["company_id"]
        .astype(str)
        .str.upper()
        == symbol
    ]

    if company.empty:

        return JsonResponse({

            "status": "error",

            "message": "Company not found"

        }, status=404)

    row = company.iloc[0]

    health_score = float(
        row["health_score"]
    )

    profit_margin = float(
        row["profit_margin"]
    )

    sales = float(
        row["sales"]
    )

    health_label = str(
        row["health_label"]
    )

    insights = []

    # =========================================
    # RECOMMENDATION
    # =========================================

    if health_score >= 75:

        recommendation = "BUY"

        risk_level = "LOW RISK"

        insights.append(
            "Strong financial stability detected."
        )

    elif health_score >= 55:

        recommendation = "HOLD"

        risk_level = "MEDIUM RISK"

        insights.append(
            "Company fundamentals appear stable."
        )

    else:

        recommendation = "WATCH CAREFULLY"

        risk_level = "HIGH RISK"

        insights.append(
            "Financial health appears weak."
        )

    # =========================================
    # PROFIT ANALYSIS
    # =========================================

    if profit_margin >= 20:

        insights.append(
            "Excellent profitability trend."
        )

    elif profit_margin >= 10:

        insights.append(
            "Profitability is moderate."
        )

    else:

        insights.append(
            "Low profitability detected."
        )

    # =========================================
    # SALES ANALYSIS
    # =========================================

    if sales >= 100000:

        insights.append(
            "Large-scale business operations identified."
        )

    elif sales >= 25000:

        insights.append(
            "Company has decent sales performance."
        )

    else:

        insights.append(
            "Sales performance is relatively smaller."
        )

    # =========================================
    # FINANCIAL SCORE BREAKDOWN
    # =========================================

    profitability_score = min(
        max(int(profit_margin * 4), 20),
        100
    )

    growth_score = min(
        max(int((sales / 5000) * 10), 25),
        100
    )

    stability_score = min(
        max(int(health_score * 0.9), 30),
        100
    )

    liquidity_score = min(
        max(
            int(
                (health_score + profit_margin) / 2
            ),
            25
        ),
        100
    )

    risk_score = 100 - int(health_score)

    # =========================================
    # MARKET MOOD ANALYSIS
    # =========================================

    mood_score = 50

    if health_score >= 75:

        mood_score += 35

    elif health_score >= 55:

        mood_score += 20

    else:

        mood_score -= 25

    if profit_margin >= 20:

        mood_score += 30

    elif profit_margin >= 10:

        mood_score += 15

    else:

        mood_score -= 20

    if risk_score <= 30:

        mood_score += 25

    elif risk_score <= 50:

        mood_score += 10

    else:

        mood_score -= 20

    mood_score = max(
        min(mood_score, 100),
        0
    )

    if mood_score >= 75:

        market_mood = "POSITIVE"

        mood_color = "green"

        mood_reason = (
            "Strong financial indicators "
            "and healthy company fundamentals detected."
        )

    elif mood_score >= 40:

        market_mood = "NEUTRAL"

        mood_color = "yellow"

        mood_reason = (
            "Company performance appears stable "
            "with moderate market confidence."
        )

    else:

        market_mood = "NEGATIVE"

        mood_color = "red"

        mood_reason = (
            "Weak financial signals "
            "and elevated business risk detected."
        )

    # =========================================
    # FINAL RESPONSE
    # =========================================

    return JsonResponse({

        "status": "success",

        "company": symbol,

        "health_score": round(
            health_score,
            2
        ),

        "profit_margin": round(
            profit_margin,
            2
        ),

        "sales": round(
            sales,
            2
        ),

        "health_label": health_label,

        "risk_level": risk_level,

        "recommendation": recommendation,

        "insights": insights,

        "score_breakdown": {

            "profitability": profitability_score,

            "growth": growth_score,

            "stability": stability_score,

            "liquidity": liquidity_score,

            "risk": risk_score
        },

        "market_mood": {

            "label": market_mood,

            "score": mood_score,

            "color": mood_color,

            "reason": mood_reason
        }
    })


# =====================================================
# PDF REPORT EXPORT
# =====================================================

def export_company_report(request, symbol):

    symbol = symbol.upper()

    df = pd.read_csv(
        DATA_DIR / "company_health_scores.csv"
    )

    company = df[
        df["company_id"]
        .astype(str)
        .str.upper()
        == symbol
    ]

    if company.empty:

        return JsonResponse({

            "status": "error",

            "message": "Company not found"

        }, status=404)

    row = company.iloc[0]

    response = HttpResponse(
        content_type="application/pdf"
    )

    response[
        "Content-Disposition"
    ] = f'attachment; filename="{symbol}_report.pdf"'


    doc = SimpleDocTemplate(

        response,

        pagesize=letter
    )

    styles = getSampleStyleSheet()

    elements = []


    # =========================================
    # TITLE
    # =========================================

    title = Paragraph(

        f"<b>{symbol} Financial Intelligence Report</b>",

        styles["Title"]
    )

    elements.append(title)

    elements.append(
        Spacer(1,20)
    )


    # =========================================
    # COMPANY DETAILS
    # =========================================

    details = f"""

    <b>Company:</b> {symbol}<br/>

    <b>Health Score:</b>
    {round(float(row['health_score']),2)}<br/>

    <b>Profit Margin:</b>
    {round(float(row['profit_margin']),2)}%<br/>

    <b>Sales:</b>
    ₹{round(float(row['sales']),2)}<br/>

    <b>Health Label:</b>
    {row['health_label']}<br/>

    """

    details_para = Paragraph(

        details,

        styles["BodyText"]
    )

    elements.append(details_para)

    elements.append(
        Spacer(1,20)
    )


    # =========================================
    # AI SUMMARY
    # =========================================

    health_score = float(
        row["health_score"]
    )

    if health_score >= 75:

        recommendation = "BUY"

        risk = "LOW RISK"

    elif health_score >= 55:

        recommendation = "HOLD"

        risk = "MEDIUM RISK"

    else:

        recommendation = "WATCH CAREFULLY"

        risk = "HIGH RISK"

    ai_text = f"""

    <b>AI Recommendation:</b>
    {recommendation}<br/><br/>

    <b>Risk Level:</b>
    {risk}<br/><br/>

    This report was generated using the
    Financial Intelligence Dashboard AI engine.

    """

    ai_para = Paragraph(

        ai_text,

        styles["BodyText"]
    )

    elements.append(ai_para)

    elements.append(
        Spacer(1,20)
    )


    # =========================================
    # FOOTER
    # =========================================

    footer = Paragraph(

        "Generated by Financial Intelligence Dashboard",

        styles["Italic"]
    )

    elements.append(footer)


    doc.build(elements)

    return response

# =====================================================
# LIVE NEWS SYSTEM
# =====================================================

def company_news(request, symbol):

    api_key = "bd93445934e44569a1c29f39404663ba"
        # =========================================
    # COMPANY NAME MAPPING
    # =========================================

    company_names = {

        "TCS":
        "Tata Consultancy Services",

        "INFY":
        "Infosys",

        "WIPRO":
        "Wipro",

        "ITC":
        "ITC Limited",

        "RELIANCE":
        "Reliance Industries",

        "HDFCBANK":
        "HDFC Bank",

        "ICICIBANK":
        "ICICI Bank",

        "SBIN":
        "State Bank of India",

        "LT":
        "Larsen and Toubro",

        "ONGC":
        "Oil and Natural Gas Corporation",

        "BHARTIARTL":
        "Bharti Airtel",

        "AXISBANK":
        "Axis Bank",

        "MARUTI":
        "Maruti Suzuki",

        "TITAN":
        "Titan Company",

        "ULTRACEMCO":
        "UltraTech Cement",

        "POWERGRID":
        "Power Grid Corporation",

        "NTPC":
        "NTPC",

        "BAJFINANCE":
        "Bajaj Finance",

        "KOTAKBANK":
        "Kotak Mahindra Bank"
    }

    query_name = company_names.get(
        symbol.upper(),
        symbol
    )

    url = (
        f"https://newsapi.org/v2/everything?"
        f"q={query_name}&"
        f"sortBy=publishedAt&"
        f"language=en&"
        f"apiKey={api_key}"
    )

    try:

        response = requests.get(url)

        data = response.json()

        articles = []

        if data.get("articles"):

            for article in data["articles"][:10]:

                articles.append({

                    "title": article.get("title"),

                    "source": article.get("source", {}).get("name"),

                    "description": article.get("description"),

                    "url": article.get("url"),

                    "image": article.get("urlToImage"),

                    "published_at": article.get("publishedAt")

                })

        return JsonResponse({

            "status": "success",

            "company": symbol,

            "news": articles

        })

    except Exception as e:

        return JsonResponse({

            "status": "error",

            "message": str(e)

        })

