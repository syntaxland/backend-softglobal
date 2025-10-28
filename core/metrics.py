# # core/metrics.py
# from prometheus_client import CollectorRegistry, generate_latest, multiprocess, CONTENT_TYPE_LATEST
# from prometheus_client import Gauge, Counter
# import os
# from django.http import HttpResponse

# # If running multiple Gunicorn workers, enable multiprocess mode.
# # Set environment variable PROMETHEUS_MULTIPROC_DIR to a writable dir if using Gunicorn with multiple workers.
# registry = CollectorRegistry()

# # Example metrics — create application metrics you need
# REQUEST_COUNT = Counter("softglobal_request_count", "Total HTTP requests")
# PROCESS_GAUGE = Gauge("softglobal_process_info", "Dummy process gauge", registry=registry)

# def metrics_view(request):
#     """
#     Exposes metrics at /metrics for Prometheus to scrape.
#     If you use gunicorn with multiple workers, configure prometheus_client multiprocess.
#     """
#     # example update (remove in production)
#     PROCESS_GAUGE.set(1)
#     REQUEST_COUNT.inc()

#     # If using multiprocess mode, merge metrics from files in PROMETHEUS_MULTIPROC_DIR
#     if os.environ.get('PROMETHEUS_MULTIPROC_DIR'):
#         registry = CollectorRegistry()
#         multiprocess.MultiProcessCollector(registry)
#         output = generate_latest(registry)
#     else:
#         output = generate_latest()
#     return HttpResponse(output, content_type=CONTENT_TYPE_LATEST)


# # core/urls.py (or project urls)
# from django.urls import path, include
# from core.metrics import metrics_view

# urlpatterns = [
#     # ... your other paths ...
#     path('metrics', metrics_view, name='metrics'),
# ]