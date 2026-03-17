"""
Monitoring and Logging Setup for PDF to Podcast Converter
Includes Prometheus metrics, structured logging, and alerting
"""

import json
import logging
import os
import time
from datetime import datetime
from functools import wraps

import boto3
import psutil
from flask import Flask, g, request
from prometheus_flask_exporter import PrometheusMetrics


# Configure structured logging
class StructuredFormatter(logging.Formatter):
    """Custom formatter for structured JSON logs"""

    def format(self, record):
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        # Add extra fields if present
        if hasattr(record, "job_id"):
            log_data["job_id"] = record.job_id
        if hasattr(record, "user_id"):
            log_data["user_id"] = record.user_id
        if hasattr(record, "duration"):
            log_data["duration"] = record.duration
        if hasattr(record, "error"):
            log_data["error"] = record.error

        return json.dumps(log_data)


def setup_logging(app):
    """Setup structured logging"""

    # Create logs directory
    os.makedirs("logs", exist_ok=True)

    # Console handler with JSON format
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(StructuredFormatter())
    console_handler.setLevel(logging.INFO)

    # File handler with JSON format
    file_handler = logging.FileHandler("logs/app.log")
    file_handler.setFormatter(StructuredFormatter())
    file_handler.setLevel(logging.DEBUG)

    # Error file handler
    error_handler = logging.FileHandler("logs/error.log")
    error_handler.setFormatter(StructuredFormatter())
    error_handler.setLevel(logging.ERROR)

    # Configure root logger
    logging.basicConfig(
        level=logging.INFO, handlers=[console_handler, file_handler, error_handler]
    )

    app.logger.info("Logging configured", extra={"status": "initialized"})


def setup_metrics(app):
    """Setup Prometheus metrics"""

    try:
        metrics = PrometheusMetrics(app)

        # Custom metrics
        metrics.info("app_info", "Application info", version="1.0.0")

        # Track requests by endpoint
        @app.before_request
        def before_request():
            g.start_time = time.time()

        @app.after_request
        def after_request(response):
            if hasattr(g, "start_time"):
                duration = time.time() - g.start_time

                app.logger.info(
                    "Request completed",
                    extra={
                        "method": request.method,
                        "path": request.path,
                        "status": response.status_code,
                        "duration": duration,
                        "ip": request.remote_addr,
                    },
                )

            return response

        return metrics
    except Exception as e:
        app.logger.warning(f"Could not setup Prometheus metrics: {str(e)}")
        return None


# Performance monitoring decorator
def monitor_performance(metric_name):
    """Decorator to monitor function performance"""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()

            try:
                result = func(*args, **kwargs)
                duration = time.time() - start_time

                logging.info(
                    f"{metric_name} completed",
                    extra={
                        "metric": metric_name,
                        "duration": duration,
                        "status": "success",
                    },
                )

                return result

            except Exception as e:
                duration = time.time() - start_time

                logging.error(
                    f"{metric_name} failed",
                    extra={
                        "metric": metric_name,
                        "duration": duration,
                        "status": "error",
                        "error": str(e),
                    },
                )

                raise

        return wrapper

    return decorator


# System metrics collector
class SystemMetrics:
    """Collect system-level metrics"""

    @staticmethod
    def get_cpu_usage():
        """Get CPU usage percentage"""
        return psutil.cpu_percent(interval=1)

    @staticmethod
    def get_memory_usage():
        """Get memory usage"""
        memory = psutil.virtual_memory()
        return {
            "total": memory.total,
            "available": memory.available,
            "percent": memory.percent,
            "used": memory.used,
        }

    @staticmethod
    def get_disk_usage():
        """Get disk usage"""
        disk = psutil.disk_usage("/")
        return {
            "total": disk.total,
            "used": disk.used,
            "free": disk.free,
            "percent": disk.percent,
        }

    @staticmethod
    def get_network_io():
        """Get network I/O stats"""
        net_io = psutil.net_io_counters()
        return {
            "bytes_sent": net_io.bytes_sent,
            "bytes_recv": net_io.bytes_recv,
            "packets_sent": net_io.packets_sent,
            "packets_recv": net_io.packets_recv,
        }


# Application metrics
class ApplicationMetrics:
    """Track application-specific metrics"""

    def __init__(self):
        self.metrics = {
            "total_pdfs_processed": 0,
            "total_podcasts_generated": 0,
            "total_voices_uploaded": 0,
            "total_errors": 0,
            "average_processing_time": 0,
        }
        self.processing_times = []

    def increment(self, metric_name):
        """Increment a counter metric"""
        if metric_name in self.metrics:
            self.metrics[metric_name] += 1

    def record_processing_time(self, duration):
        """Record processing time"""
        self.processing_times.append(duration)
        if len(self.processing_times) > 100:
            self.processing_times.pop(0)

        if len(self.processing_times) > 0:
            self.metrics["average_processing_time"] = sum(self.processing_times) / len(
                self.processing_times
            )

    def get_metrics(self):
        """Get all metrics"""
        return self.metrics


# Health check with detailed status
class HealthCheck:
    """Comprehensive health check"""

    @staticmethod
    def check_redis():
        """Check Redis connectivity"""
        try:
            import redis

            r = redis.Redis(
                host=os.getenv("REDIS_HOST", "localhost"),
                port=int(os.getenv("REDIS_PORT", 6379)),
                decode_responses=True,
            )
            start = time.time()
            r.ping()
            latency = (time.time() - start) * 1000
            return {"status": "healthy", "latency_ms": latency}
        except Exception as e:
            return {"status": "unhealthy", "error": str(e)}

    @staticmethod
    def check_s3():
        """Check S3 connectivity"""
        try:
            s3_client = boto3.client(
                "s3",
                aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
                aws_secret_access_key=os.getenv("AWS_SECRET_KEY"),
                region_name=os.getenv("AWS_REGION", "us-east-1"),
            )
            start = time.time()
            s3_client.list_buckets()
            latency = (time.time() - start) * 1000
            return {"status": "healthy", "latency_ms": latency}
        except Exception as e:
            return {"status": "unhealthy", "error": str(e)}

    @staticmethod
    def check_models():
        """Check if ML models are available"""
        try:
            # Check if models directory exists and has files
            cache_dir = os.path.expanduser("~/.cache/huggingface/")
            has_models = os.path.exists(cache_dir) and len(os.listdir(cache_dir)) > 0

            return {
                "status": "healthy" if has_models else "unhealthy",
                "models_cached": has_models,
            }
        except Exception as e:
            return {"status": "unknown", "error": str(e)}

    @classmethod
    def get_health_status(cls):
        """Get comprehensive health status"""
        system_metrics = SystemMetrics()

        health = {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "components": {
                "redis": cls.check_redis(),
                "s3": cls.check_s3(),
                "models": cls.check_models(),
            },
            "system": {
                "cpu_percent": system_metrics.get_cpu_usage(),
                "memory": system_metrics.get_memory_usage(),
                "disk": system_metrics.get_disk_usage(),
            },
        }

        # Overall status based on components
        for component, status in health["components"].items():
            if status["status"] != "healthy":
                health["status"] = "degraded"
                break

        return health


# Alerting system
class AlertManager:
    """Send alerts for critical issues"""

    def __init__(self, webhook_url=None, email_config=None):
        self.webhook_url = webhook_url
        self.email_config = email_config

    def send_alert(self, severity, message, details=None):
        """Send alert"""
        alert_data = {
            "severity": severity,
            "message": message,
            "details": details or {},
            "timestamp": datetime.utcnow().isoformat(),
            "hostname": os.uname().nodename if hasattr(os, "uname") else "unknown",
        }

        logging.error(
            f"Alert: {message}",
            extra={"alert": True, "severity": severity, "details": details},
        )

        # Send to webhook (Slack, Discord, etc.)
        if self.webhook_url:
            self._send_webhook(alert_data)

        # Send email
        if self.email_config:
            self._send_email(alert_data)

    def _send_webhook(self, alert_data):
        """Send alert to webhook"""
        try:
            import requests

            requests.post(self.webhook_url, json=alert_data, timeout=5)
        except Exception as e:
            logging.error(f"Failed to send webhook alert: {e}")

    def _send_email(self, alert_data):
        """Send alert via email"""
        try:
            import smtplib
            from email.mime.text import MIMEText

            msg = MIMEText(json.dumps(alert_data, indent=2))
            msg[
                "Subject"
            ] = f'Alert: {alert_data["severity"]} - {alert_data["message"]}'
            msg["From"] = self.email_config["from"]
            msg["To"] = self.email_config["to"]

            with smtplib.SMTP(
                self.email_config["smtp_host"], self.email_config["smtp_port"]
            ) as server:
                server.starttls()
                server.login(
                    self.email_config["username"], self.email_config["password"]
                )
                server.send_message(msg)
        except Exception as e:
            logging.error(f"Failed to send email alert: {e}")


# Example usage in Flask app
def integrate_monitoring(app):
    """Integrate all monitoring components"""

    # Setup logging
    setup_logging(app)

    # Setup Prometheus metrics
    metrics = setup_metrics(app)

    # Initialize application metrics
    app_metrics = ApplicationMetrics()

    # Initialize alert manager
    alert_manager = AlertManager(
        webhook_url=os.getenv("ALERT_WEBHOOK_URL"),
        email_config={
            "from": os.getenv("ALERT_EMAIL_FROM"),
            "to": os.getenv("ALERT_EMAIL_TO"),
            "smtp_host": os.getenv("SMTP_HOST"),
            "smtp_port": int(os.getenv("SMTP_PORT", 587)),
            "username": os.getenv("SMTP_USERNAME"),
            "password": os.getenv("SMTP_PASSWORD"),
        }
        if os.getenv("ALERT_EMAIL_FROM")
        else None,
    )

    # Add health check endpoint
    @app.route("/api/health/detailed", methods=["GET"])
    def detailed_health():
        """Detailed health check endpoint"""
        return HealthCheck.get_health_status()

    # Add metrics endpoint
    @app.route("/api/metrics", methods=["GET"])
    def get_metrics():
        """Get application metrics"""
        return {
            "application": app_metrics.get_metrics(),
            "system": {
                "cpu": SystemMetrics.get_cpu_usage(),
                "memory": SystemMetrics.get_memory_usage(),
                "disk": SystemMetrics.get_disk_usage(),
                "network": SystemMetrics.get_network_io(),
            },
        }

    # Error handler with alerting
    @app.errorhandler(500)
    def handle_500(error):
        """Handle 500 errors with alerting"""
        alert_manager.send_alert(
            severity="critical",
            message="Internal server error",
            details={
                "error": str(error),
                "path": request.path,
                "method": request.method,
            },
        )
        return {"error": "Internal server error"}, 500

    return {
        "metrics": metrics,
        "app_metrics": app_metrics,
        "alert_manager": alert_manager,
    }


if __name__ == "__main__":
    # Test monitoring
    logging.info("Testing monitoring setup")

    health = HealthCheck.get_health_status()
    print(json.dumps(health, indent=2))

    system_metrics = SystemMetrics()
    print(f"CPU: {system_metrics.get_cpu_usage()}%")
    print(f"Memory: {system_metrics.get_memory_usage()}")
