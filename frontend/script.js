let profitChartInstance = null;
let cashChartInstance = null;

/* =========================================
   LOAD COMPANY SUGGESTIONS
========================================= */

loadCompanySuggestions();

async function loadCompanySuggestions() {

    try {

        const response = await fetch(
            "https://financial-intelligence-pjgt.onrender.com/company-list/"
        );

        const data = await response.json();

        if (data.status === "success") {

            const datalist =
                document.getElementById("companySuggestions");

            datalist.innerHTML = "";

            data.companies.forEach(company => {

                const option =
                    document.createElement("option");

                option.value = company;

                datalist.appendChild(option);
            });
        }

    }

    catch (error) {

        console.log(
            "Suggestion loading failed"
        );
    }
}

/* =========================================
   SEARCH COMPANY
========================================= */

async function searchCompany() {

    const company =
        document.getElementById("companyInput")
        .value
        .trim()
        .toUpperCase();

    const panel =
        document.getElementById("companyInfo");

    if (!company) {

        panel.classList.remove("hidden");

        panel.innerHTML = `
            <div class="metric-card company-main">

                <h2>
                    ⚠️ Enter company symbol
                </h2>

                <p>
                    Example:
                    TCS,
                    INFY,
                    WIPRO
                </p>

            </div>
        `;

        return;
    }

    panel.classList.remove("hidden");

    panel.innerHTML = `
        <div class="metric-card company-main">

            <h2>
                ⏳ Loading...
            </h2>

            <p>
                Fetching financial intelligence for ${company}
            </p>

        </div>
    `;

    try {

        const response = await fetch(
            `https://financial-intelligence-pjgt.onrender.com/companies/${company}/details/`
        );

        const data = await response.json();

        if (data.status !== "success") {

            panel.innerHTML = `
                <div class="metric-card company-main">

                    <h2>
                        ❌ Company not found
                    </h2>

                    <p>
                        Please check symbol and try again
                    </p>

                </div>
            `;

            clearCharts();

            return;
        }

        const healthScore =
            Number(
                data.health.health_score
            ).toFixed(2);

        const profitMargin =
            Number(
                data.health.profit_margin
            ).toFixed(2);

        const sales =
            Number(
                data.health.sales
            ).toLocaleString("en-IN");

        panel.innerHTML = `

            <div class="metric-card company-main">

                <h2>
                    ${data.company}
                </h2>

                <p>
                    Financial intelligence profile
                </p>

                <span class="badge">
                    ${data.health.health_label}
                </span>

            </div>

            <div class="metric-card">

                <div class="metric-label">
                    Health Score
                </div>

                <div class="metric-value">
                    ${healthScore}
                </div>

            </div>

            <div class="metric-card">

                <div class="metric-label">
                    Profit Margin
                </div>

                <div class="metric-value">
                    ${profitMargin}%
                </div>

            </div>

            <div class="metric-card">

                <div class="metric-label">
                    Sales
                </div>

                <div class="metric-value">
                    ₹${sales}
                </div>

            </div>
        `;

        const profitLabels =
            data.profit.map(
                p => p.year
            );

        const profitValues =
            data.profit.map(
                p => Number(p.net_profit)
            );

        const cashLabels =
            data.cashflow.map(
                c => c.year
            );

        const cashValues =
            data.cashflow.map(
                c => Number(c.net_cash_flow)
            );

        clearCharts();

        /* =========================
           PROFIT CHART
        ========================= */

        profitChartInstance =
            new Chart(
                document.getElementById("profitChart"),
                {

                    type: "line",

                    data: {

                        labels: profitLabels,

                        datasets: [{

                            label: "Net Profit",

                            data: profitValues,

                            borderWidth: 4,

                            tension: 0.35,

                            pointRadius: 5,

                            fill: true
                        }]
                    },

                    options: {

                        responsive: true,

                        maintainAspectRatio: false
                    }
                }
            );

        /* =========================
           CASH FLOW CHART
        ========================= */

        cashChartInstance =
            new Chart(
                document.getElementById("cashChart"),
                {

                    type: "bar",

                    data: {

                        labels: cashLabels,

                        datasets: [{

                            label: "Cash Flow",

                            data: cashValues,

                            borderWidth: 1
                        }]
                    },

                    options: {

                        responsive: true,

                        maintainAspectRatio: false
                    }
                }
            );

                    /* =========================
            LOAD EXTRA FEATURES
            ========================= */

            updateRiskMeter(data);

            loadAIInsights(company);

            loadCompanyNews(company);

    }

    catch (error) {

        panel.innerHTML = `
            <div class="metric-card company-main">

                <h2>
                    🚫 Backend not connected
                </h2>

                <p>
                    Make sure Django server is running
                </p>

            </div>
        `;

        clearCharts();
    }
}

/* =========================================
   CLEAR CHARTS
========================================= */

function clearCharts() {

    if (profitChartInstance) {

        profitChartInstance.destroy();

        profitChartInstance = null;
    }

    if (cashChartInstance) {

        cashChartInstance.destroy();

        cashChartInstance = null;
    }
}

/* =========================================
   ENTER KEY SEARCH
========================================= */

document
    .getElementById("companyInput")
    .addEventListener(
        "keydown",
        function(event){

            if(event.key === "Enter"){

                searchCompany();
            }
        }
    );

/* =========================================
   AI INSIGHTS
========================================= */

async function loadAIInsights(company){

    const container =
        document.getElementById(
            "aiInsightsContainer"
        );

    container.innerHTML = `
        <div class="ai-loading">

            Generating AI financial insights...

        </div>
    `;

    try{

        const response = await fetch(
            `https://financial-intelligence-pjgt.onrender.com/insights/${company}/`
        );

        const data = await response.json();

        if(data.status !== "success"){

            container.innerHTML = `
                <div class="battle-error">

                    Failed to generate AI insights

                </div>
            `;

            return;
        }

        /* =========================
           AI INSIGHTS HTML
        ========================= */

        let insightsHTML = "";

        data.insights.forEach(insight=>{

            insightsHTML += `
                <div class="insight-item">

                    ✅ ${insight}

                </div>
            `;
        });

        /* =========================
           SCORE BREAKDOWN
        ========================= */

        const scores =
            data.score_breakdown;

        function getScoreColor(value){

            if(value >= 70){

                return "score-green";
            }

            else if(value >= 40){

                return "score-yellow";
            }

            return "score-red";
        }

        function getDescription(name){

            if(name === "profitability"){

                return "Measures how efficiently the company generates profit.";
            }

            if(name === "growth"){

                return "Represents overall business expansion and revenue momentum.";
            }

            if(name === "stability"){

                return "Indicates long-term financial consistency and operational strength.";
            }

            if(name === "liquidity"){

                return "Shows the company’s short-term financial flexibility.";
            }

            return "Higher value indicates stronger risk exposure in the company.";
        }

        let scoreHTML = "";

        Object.entries(scores).forEach(
            ([key,value])=>{

                scoreHTML += `

                    <div class="score-card">

                        <div class="score-header">

                            <div class="score-name">

                                ${
                                    key.charAt(0)
                                    .toUpperCase()
                                    +
                                    key.slice(1)
                                }

                            </div>

                            <div class="score-percent">

                                ${value}%

                            </div>

                        </div>

                        <div class="score-bar">

                            <div
                                class="score-fill ${getScoreColor(value)}"
                                style="width:${value}%"
                            ></div>

                        </div>

                        <div class="score-description">

                            ${getDescription(key)}

                        </div>

                    </div>
                `;
            }
        );

        container.innerHTML = `

            <div class="ai-card">

                <div class="ai-header">

                    <div>

                        <h2>
                            ${data.company}
                        </h2>

                        <p>
                            AI Financial Analysis
                        </p>

                    </div>

                    <div class="ai-badge">

                        ${data.recommendation}

                    </div>

                </div>
                                <div class="report-download-section">

                    <button
                        class="report-download-btn"
                        onclick="
                            window.open(
                                'https://financial-intelligence-pjgt.onrender.com/report/${data.company}/',
                                '_blank'
                            )
                        "
                    >

                        📄 Download Financial Report

                    </button>

                </div>

                <div class="ai-risk">

                    ${data.risk_level}

                </div>

                <div class="insights-list">

                    ${insightsHTML}

                </div>
                                <div class="market-mood-section">

                    <div class="market-mood-title">

                        🧠 Market Mood Analysis

                    </div>

                    <div class="market-mood-card">

                        <div class="market-mood-left">

                            <div class="market-mood-badge
                                ${
                                    data.market_mood.label === "POSITIVE"
                                    ? "mood-positive"
                                    :
                                    data.market_mood.label === "NEUTRAL"
                                    ? "mood-neutral"
                                    :
                                    "mood-negative"
                                }
                            ">

                                ${data.market_mood.label}

                            </div>

                            <div class="market-mood-score">

                                ${data.market_mood.score}%

                            </div>

                            <div class="market-mood-label">

                                Market Confidence Score

                            </div>

                        </div>

                        <div
                            class="market-mood-meter"
                            style="
                                background:
                                conic-gradient(
                                    ${
                                        data.market_mood.color === "green"
                                        ? "#00ff99"
                                        :
                                        data.market_mood.color === "yellow"
                                        ? "#ffd500"
                                        :
                                        "#ff4d4d"
                                    }
                                    ${data.market_mood.score * 3.6}deg,
                                    rgba(255,255,255,0.08)
                                    0deg
                                );
                            "
                        >

                            <span>

                                ${data.market_mood.score}%

                            </span>

                        </div>

                    </div>

                    <div class="market-mood-reason">

                        ${data.market_mood.reason}

                    </div>

                </div>
                <div class="score-breakdown">

                    <div class="score-breakdown-title">

                        📊 Financial Score Breakdown

                    </div>

                    <div class="score-grid">

                        ${scoreHTML}

                    </div>

                </div>

            </div>
        `;
    }

    catch(error){

    console.log(
        "AI Insights Error:",
        error
    );

    container.innerHTML = `

        <div class="preview-card">

            <div class="preview-icon">
                ⚠
            </div>

            <h2>
                AI Analysis Unavailable
            </h2>

            <p>

                Some financial indicators for this
                company are incomplete or currently
                unsupported by the AI engine.

            </p>

            <div class="risk-preview-points">

                <div>
                    📊 Financial data missing
                </div>

                <div>
                    🧠 AI engine protected
                </div>

                <div>
                    ⚡ Platform still operational
                </div>

            </div>

        </div>
    `;
}
}

/* =========================================
   COMPANY NEWS
========================================= */

async function loadCompanyNews(company) {

    const container =
        document.getElementById(
            "newsContainer"
        );

    container.innerHTML = `
        <div class="news-loading">

            Loading latest financial news...

        </div>
    `;

    try {

        const response = await fetch(
            `https://financial-intelligence-pjgt.onrender.com/news/${company}/`
        );

        const data = await response.json();

        if (data.status !== "success") {

            container.innerHTML = `
                <div class="news-loading">

                    Unable to fetch news.

                </div>
            `;

            return;
        }

        let newsHTML = "";

        data.news.forEach(article => {

            newsHTML += `

                <div class="news-card">

                    <img
                        src="${article.image}"
                        class="news-image"
                    >

                    <div class="news-content">

                        <div class="news-source">
                            ${article.source}
                        </div>

                        <div class="news-headline">
                            ${article.title}
                        </div>

                        <div class="news-description">
                            ${article.description || "No description available."}
                        </div>

                        <a
                            href="${article.url}"
                            target="_blank"
                            class="news-link"
                        >
                            Read Full Article →
                        </a>

                    </div>

                </div>

            `;
        });

        container.innerHTML = newsHTML;

    }

    catch (error) {

        container.innerHTML = `
            <div class="news-loading">

                Failed to load news.

            </div>
        `;
    }
}

/* =========================================
   COMPANY COMPARISON
========================================= */

async function compareCompanies() {

    const company1 =
        document.getElementById("company1")
        .value
        .trim()
        .toUpperCase();

    const company2 =
        document.getElementById("company2")
        .value
        .trim()
        .toUpperCase();

    const resultDiv =
        document.getElementById("comparisonResult");

    if (!company1 || !company2) {

        resultDiv.classList.remove("hidden");

        resultDiv.innerHTML = `
            <div class="battle-error">

                ⚠ Please enter both companies

            </div>
        `;

        return;
    }

    try {

        const response = await fetch(
            `https://financial-intelligence-pjgt.onrender.com/compare/?company1=${company1}&company2=${company2}`
        );

        const data = await response.json();

        if (data.status !== "success") {

            resultDiv.innerHTML = `
                <div class="battle-error">

                    ❌ Companies not found

                </div>
            `;

            return;
        }

        const companies = data.data;

        const c1 = companies[0];
        const c2 = companies[1];

        const winner1 =
            c1.health_score >
            c2.health_score;

        const winner2 =
            c2.health_score >
            c1.health_score;

        resultDiv.classList.remove("hidden");

        resultDiv.innerHTML = `

            <h2 class="battle-title">

                ⚔ Financial Battle Arena

            </h2>

            <div class="battle-container">

                <div class="battle-card ${winner1 ? 'winner-glow' : ''}">

                    <h1>
                        ${c1.company_id}
                    </h1>

                    <span class="battle-badge">
                        ${c1.health_label}
                    </span>

                    <div class="battle-score">
                        ${c1.health_score.toFixed(2)}
                    </div>

                    <p class="battle-label">
                        Health Score
                    </p>

                </div>

                <div class="vs-section">

                    <div class="vs-circle">
                        VS
                    </div>

                </div>

                <div class="battle-card ${winner2 ? 'winner-glow' : ''}">

                    <h1>
                        ${c2.company_id}
                    </h1>

                    <span class="battle-badge">
                        ${c2.health_label}
                    </span>

                    <div class="battle-score">
                        ${c2.health_score.toFixed(2)}
                    </div>

                    <p class="battle-label">
                        Health Score
                    </p>

                </div>

            </div>

            <div class="metrics-battle">

                <div class="metric-battle-row">

                    <div class="metric-company">
                        ₹${Number(c1.sales).toLocaleString()}
                    </div>

                    <div class="metric-center">
                        SALES
                    </div>

                    <div class="metric-company">
                        ₹${Number(c2.sales).toLocaleString()}
                    </div>

                </div>

                <div class="metric-battle-row">

                    <div class="metric-company">
                        ${c1.profit_margin.toFixed(2)}%
                    </div>

                    <div class="metric-center">
                        PROFIT MARGIN
                    </div>

                    <div class="metric-company">
                        ${c2.profit_margin.toFixed(2)}%
                    </div>

                </div>

            </div>
        `;

    }

    catch(error){

        resultDiv.classList.remove("hidden");

        resultDiv.innerHTML = `
            <div class="battle-error">

                🚫 Backend Error

            </div>
        `;
    }
}

/* =========================================
   LEADERBOARD
========================================= */

loadLeaderboard();

async function loadLeaderboard(
    metric = "health_score"
){

    const container =
        document.getElementById(
            "leaderboardContainer"
        );

    container.innerHTML = `
        <div class="battle-error">
            Loading leaderboard...
        </div>
    `;

    try {

        const response = await fetch(
            "https://financial-intelligence-pjgt.onrender.com/leaderboard/"
        );

        const data = await response.json();

        if(data.status !== "success"){

            container.innerHTML = `
                <div class="battle-error">

                    Failed to load leaderboard

                </div>
            `;

            return;
        }

        let companies =
            data.top_health;

        if(metric === "profit_margin"){

            companies =
                [...data.top_health]
                .sort(
                    (a,b)=>
                    b.profit_margin -
                    a.profit_margin
                );
        }

        if(metric === "sales"){

            companies =
                [...data.top_health]
                .sort(
                    (a,b)=>
                    b.sales -
                    a.sales
                );
        }

        companies =
            companies.slice(0,10);

        let html = "";

        companies.forEach(
            (company,index)=>{

                html += `

                <div class="leaderboard-card">

                    <div class="leaderboard-rank">
                        #${index + 1}
                    </div>

                    <div class="leaderboard-company">
                        ${company.company_id}
                    </div>

                    <div class="leaderboard-metrics">

                        <div class="leaderboard-metric">

                            <span>
                                Health
                            </span>

                            <strong>
                                ${Number(company.health_score).toFixed(2)}
                            </strong>

                        </div>

                        <div class="leaderboard-metric">

                            <span>
                                Profit Margin
                            </span>

                            <strong>
                                ${Number(company.profit_margin).toFixed(2)}%
                            </strong>

                        </div>

                        <div class="leaderboard-metric">

                            <span>
                                Sales
                            </span>

                            <strong>
                                ₹${Number(company.sales).toLocaleString()}
                            </strong>

                        </div>

                    </div>

                </div>
                `;
            }
        );

        container.innerHTML = html;
    }

    catch(error){

        container.innerHTML = `
            <div class="battle-error">

                Backend connection failed

            </div>
        `;
    }
}
/* =========================
   PLATFORM NAVIGATION ENGINE
========================= */

function showPage(pageName, element = null){

    // =========================
    // HIDE ALL PAGES
    // =========================

    const pages =
        document.querySelectorAll(".page");

    pages.forEach((page)=>{

        page.classList.remove(
            "active-page"
        );

    });

    // =========================
    // SHOW SELECTED PAGE
    // =========================

    const targetPage =
        document.getElementById(
            pageName + "Page"
        );

    if(targetPage){

        targetPage.classList.add(
            "active-page"
        );

    }

    // =========================
    // SIDEBAR ACTIVE STATE
    // =========================

    const navLinks =
        document.querySelectorAll(
            ".nav-link"
        );

    navLinks.forEach((link)=>{

        link.classList.remove(
            "active"
        );

    });

    if(element){

        element.classList.add(
            "active"
        );

    }

    // =========================
    // AUTO SCROLL TOP
    // =========================

    window.scrollTo({

        top:0,

        behavior:"smooth"

    });
}

/* =========================
   HOME BUTTON FIX
========================= */

document.addEventListener(
    "DOMContentLoaded",
    ()=>{

        showPage("home");

    }
);

/* =========================
   HERO BUTTON SUPPORT
========================= */

const heroButtons =
    document.querySelectorAll(
        ".hero-actions button"
    );

heroButtons.forEach((button)=>{

    button.addEventListener(
        "click",
        ()=>{

            const navLinks =
                document.querySelectorAll(
                    ".nav-link"
                );

            navLinks.forEach((link)=>{

                link.classList.remove(
                    "active"
                );

            });

        }
    );

});

/* =========================================
   SMART PREVIEW STATES ENGINE
========================================= */

document.addEventListener(
    "DOMContentLoaded",
    ()=>{

        setupPreviewStates();

    }
);

    /* =========================================
   RISK METER ENGINE
========================================= */

function updateRiskMeter(data){

    const riskSection =
        document.getElementById(
            "riskMeterSection"
        );

    if(!riskSection) return;

    riskSection.classList.remove(
        "hidden"
    );

    let healthScore = 50;

    /* =========================
       SAFE HEALTH SCORE
    ========================= */

    if(
        data.health &&
        data.health.health_score
    ){

        healthScore =
            Number(
                data.health.health_score
            );
    }

    healthScore = Math.max(
        0,
        Math.min(100, healthScore)
    );

    const riskValue =
        100 - healthScore;

    let riskLevel =
        "MEDIUM RISK";

    let recommendation =
        "HOLD";

    if(riskValue >= 70){

        riskLevel =
            "HIGH RISK";

        recommendation =
            "WATCH CAREFULLY";
    }

    else if(riskValue <= 35){

        riskLevel =
            "LOW RISK";

        recommendation =
            "GOOD STABILITY";
    }

    riskSection.innerHTML = `

        <h2 class="risk-title">
            📊 Risk Meter Visualizer
        </h2>

        <div class="risk-container">

            <div
                class="risk-circle"
                style="
                    background:
                    conic-gradient(
                        #00c3ff ${riskValue}%,
                        rgba(255,255,255,0.08) 0%
                    );
                "
            >

                <div class="risk-inner">

                    <div class="risk-value">

                        ${riskValue.toFixed(0)}%

                    </div>

                </div>

            </div>

            <div class="risk-details">

                <div class="risk-level">

                    ${riskLevel}

                </div>

                <div class="risk-recommendation">

                    ${recommendation}

                </div>

            </div>

        </div>
    `;
}

function setupPreviewStates(){

    /* =========================
       AI PREVIEW
    ========================= */

    const aiContainer =
        document.getElementById(
            "aiInsightsContainer"
        );

    if(aiContainer){

        aiContainer.innerHTML = `

            <div class="preview-card ai-preview">

                <div class="preview-glow"></div>

                <div class="preview-icon">
                    🧠
                </div>

                <h2>
                    AI Engine Ready
                </h2>

                <p>
                    Search any company to generate
                    AI-powered financial intelligence,
                    market mood analysis and score breakdowns.
                </p>

            </div>
        `;
    }


    /* =========================
       NEWS PREVIEW
    ========================= */

    const newsContainer =
        document.getElementById(
            "newsContainer"
        );

    if(newsContainer){

        newsContainer.innerHTML = `

            <div class="preview-card">

                <div class="preview-icon">
                    📰
                </div>

                <h2>
                    Live Financial Intelligence
                </h2>

                <p>
                    Search any company to track
                    real-time financial headlines,
                    company updates and market signals.
                </p>

                <div class="news-preview-grid">

                    <div class="news-skeleton"></div>

                    <div class="news-skeleton"></div>

                    <div class="news-skeleton"></div>

                </div>

            </div>
        `;
    }

    /* =========================
       RISK PREVIEW
    ========================= */

    const riskSection =
        document.getElementById(
            "riskMeterSection"
        );

    if(riskSection){

        riskSection.classList.remove(
            "hidden"
        );

        riskSection.innerHTML = `

            <div class="preview-card risk-preview">

                <div class="risk-preview-circle">

                    <div class="risk-preview-inner">

                        AI

                    </div>

                </div>

                <h2>
                    Financial Risk Analyzer
                </h2>

                <p>
                    Search any company to visualize:
                </p>

                <div class="risk-preview-points">

                    <div>
                        📈 Risk Score
                    </div>

                    <div>
                        🧠 AI Recommendation
                    </div>

                    <div>
                        ⚡ Financial Stability
                    </div>

                    <div>
                        📊 Market Exposure
                    </div>

                </div>

            </div>
        `;
    }

    /* =========================
       COMPARE PREVIEW
    ========================= */

    const compareResult =
        document.getElementById(
            "comparisonResult"
        );

    if(compareResult){

        compareResult.classList.remove(
            "hidden"
        );

        compareResult.innerHTML = `

            <div class="preview-card">

                <div class="preview-icon">
                    ⚔
                </div>

                <h2>
                    Financial Battle Arena
                </h2>

                <p>
                    Compare two companies using:
                </p>

                <div class="risk-preview-points">

                    <div>
                        🏆 Health Score
                    </div>

                    <div>
                        💰 Sales
                    </div>

                    <div>
                        📈 Profit Margin
                    </div>

                    <div>
                        🧠 Financial Strength
                    </div>

                </div>

            </div>
        `;
    }
}