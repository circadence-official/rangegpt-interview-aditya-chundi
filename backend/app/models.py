from django.db import models


class Provider(models.Model):
    name = models.CharField(max_length=100, unique=True)
    website = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def _str_(self):
        return self.name


class LLMModel(models.Model):
    provider = models.ForeignKey(
        Provider, on_delete=models.CASCADE, related_name="models"
    )
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    context_window = models.IntegerField()
    input_price_per_1m = models.DecimalField(max_digits=10, decimal_places=4)
    output_price_per_1m = models.DecimalField(max_digits=10, decimal_places=4)
    arena_elo_score = models.IntegerField(null=True, blank=True)
    release_date = models.DateField()
    is_open_source = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-arena_elo_score"]
        unique_together = ["provider", "name"]

    def _str_(self):
        return f"{self.provider.name} - {self.name}"



# Model to store benchmark evaluation results for each LLM
# Design choice:
  # Each result is stored as a separate row (no updates/overwrites)
  # This allows tracking performance history over time
  # Supports multiple benchmarks dynamically without schema changes


class BenchmarkResult(models.Model):
    model = models.ForeignKey(
        LLMModel,
        on_delete=models.CASCADE,
        related_name="benchmark_results"
    )

    # Name of the benchmark (e.g., arena_elo, mmlu, etc.)
    # Kept as a flexible string so new benchmarks can be added without schema change
    
    benchmark = models.CharField(max_length=100)

    # Score achieved in that benchmark run

    score = models.FloatField()
    run_id = models.CharField(max_length=100, blank=True, null=True)

    # Timestamp when this result was recorded
    # Used to track history and determine the most recent run
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def _str_(self):
        return f"{self.model.name} - {self.benchmark} - {self.score}"
