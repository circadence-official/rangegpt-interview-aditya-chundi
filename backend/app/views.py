from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView  # using APIView for custom response handling
from django.db.models import Max


from app.models import LLMModel, BenchmarkResult
from app.serializers import LLMModelSerializer, LLMModelListSerializer


@api_view(["GET"])
def health_check(request):
    return Response({"status": "ok"})


class LLMModelListView(generics.ListAPIView):
    queryset = LLMModel.objects.select_related("provider").all()
    serializer_class = LLMModelListSerializer


class LLMModelDetailView(generics.RetrieveAPIView):
    queryset = LLMModel.objects.select_related("provider").all()
    serializer_class = LLMModelSerializer


class LLMModelCreateView(generics.CreateAPIView):
    queryset = LLMModel.objects.all()
    serializer_class = LLMModelSerializer


# API to store benchmark results
# Each POST creates a new row (history preserved)
# No overwrite → supports multiple runs over time
@api_view(["POST"])
def add_result(request):
    data = request.data

    BenchmarkResult.objects.create(
        model_id=data["model"],
        benchmark=data["benchmark"],
        score=data["score"]
    )

    return Response({"message": "Result added"})


# Leaderboard API
# Returns models ranked by their most recent score for a given benchmark.
# Includes models with no runs and marks them clearly.

class LeaderboardView(APIView):
    def get(self, request):
        benchmark = request.query_params.get("benchmark")

        results = []

        # iterate through all models so we can include ones with no evaluations
        models = LLMModel.objects.all()

        for model in models:
            latest = (
                BenchmarkResult.objects
                .filter(model=model, benchmark=benchmark)
                .order_by("-created_at")  # pick most recent run
                .first()
            )

            if latest:
                results.append({
                    "model_id": model.id,
                    "model_name": model.name,
                    "latest_score": latest.score,
                    "timestamp": latest.created_at
                })
            else:
                results.append({
                    "model_id": model.id,
                    "model_name": model.name,
                    "latest_score": None,
                    "status": "not_evaluated"
                })

        # sort evaluated models first, then by score descending
        results.sort(
            key=lambda x: (x["latest_score"] is None, -(x["latest_score"] or 0))
        )

        return Response(results)


# Model Summary API
# Purpose
# Returns the latest score for each benchmark for a given model
# This helps provide a consolidated view of model performance across benchmarks
# in a single API call (avoids multiple frontend requests)

class ModelSummaryView(APIView):
    def get(self, request, pk):

        results = []

        # Get all unique benchmarks this model has participated in
        benchmarks = set(
            BenchmarkResult.objects
            .filter(model_id=pk)
            .values_list("benchmark", flat=True)
        )

        # For each benchmark, fetch the latest run (based on timestamp)
        for b in benchmarks:
            latest = (
                BenchmarkResult.objects
                .filter(model_id=pk, benchmark=b)
                .order_by("-created_at")  # latest run first
                .first()
            )

            # Append structured response per benchmark
            results.append({
                "benchmark": b,
                "latest_score": latest.score,
                "timestamp": latest.created_at  # Added metadata to distinguish runs
            })

        return Response(results)


# Model Results History API
# Returns ALL runs for a model
# Ordered chronologically (old → new)
# Includes timestamp → distinguishes runs clearly
class ModelResultsHistoryView(generics.ListAPIView):
    def get(self, request, pk):
        results = (
            BenchmarkResult.objects
            .filter(model_id=pk)
            .order_by("created_at")
            .values(
                "benchmark",
                "score",
                "created_at"
            )
        )

        return Response(results)
