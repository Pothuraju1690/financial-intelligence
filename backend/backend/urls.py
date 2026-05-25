from django.contrib import admin
from django.urls import path
from django.http import HttpResponse

from api.views import (

    get_companies,

    get_single_company,

    get_company_details,

    compare_companies,

    get_company_list,

    leaderboard,

    ai_insights,

    company_news,

    export_company_report
)

# =========================================
# HOME PAGE
# =========================================

def home(request):
    return HttpResponse("Financial Intelligence Dashboard Backend Live ✅")


urlpatterns = [

    # =========================================
    # HOME
    # =========================================

    path(
        '',
        home
    ),

    # =========================================
    # ADMIN
    # =========================================

    path(
        'admin/',
        admin.site.urls
    ),

    # =========================================
    # COMPANY APIs
    # =========================================

    path(
        'companies/',
        get_companies
    ),

    path(
        'companies/<str:symbol>/',
        get_single_company
    ),

    path(
        'companies/<str:symbol>/details/',
        get_company_details
    ),

    # =========================================
    # COMPARISON
    # =========================================

    path(
        'compare/',
        compare_companies
    ),

    # =========================================
    # COMPANY LIST
    # =========================================

    path(
        'company-list/',
        get_company_list
    ),

    # =========================================
    # LEADERBOARD
    # =========================================

    path(
        'leaderboard/',
        leaderboard
    ),

    # =========================================
    # AI INSIGHTS
    # =========================================

    path(
        'insights/<str:symbol>/',
        ai_insights
    ),

    # =========================================
    # PDF REPORT EXPORT
    # =========================================

    path(
        'report/<str:symbol>/',
        export_company_report
    ),

    # =========================================
    # LIVE NEWS SYSTEM
    # =========================================

    path(
        'news/<str:symbol>/',
        company_news
    ),
]