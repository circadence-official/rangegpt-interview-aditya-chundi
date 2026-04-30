from django.urls import path
from app.views import (
    health_check,
    LLMModelListView,
    LLMModelDetailView,
    LLMModelCreateView,
    add_result,
    LeaderboardView,
    ModelSummaryView,
    ModelResultsHistoryView,  # history API import
)

urlpatterns = [
    # Basic health check endpoint
    path("health/", health_check, name="health-check"),

    # Existing model APIs
    path("models/", LLMModelListView.as_view(), name="model-list"),
    path("models/create/", LLMModelCreateView.as_view(), name="model-create"),
    path("models/<int:pk>/", LLMModelDetailView.as_view(), name="model-detail"),

    # API to store benchmark results
    # Each call creates a new record (keeps history of runs)
    path("results/", add_result),

    # Leaderboard API
    # Returns models ranked by latest score per benchmark
    path("leaderboard/", LeaderboardView.as_view(), name="leaderboard"),

    # Model Summary API
    # Returns latest score per benchmark for a model
    path("models/<int:pk>/summary/", ModelSummaryView.as_view(), name="model-summary"),

    # Model Results History API
    # Returns full chronological run history
    # Includes timestamps to distinguish runs
    path("models/<int:pk>/results/", ModelResultsHistoryView.as_view(), name="model-results-history"),
]
