#!/usr/bin/env python3
"""
Script de monitoreo y health check para el sistema de Triaje IA.
Uso: python healthcheck.py [--verbose] [--notify]
"""

import sys
import json
import time
import socket
import urllib.request
import urllib.error
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import Optional, List
import subprocess


@dataclass
class HealthResult:
    name: str
    status: str  # OK, WARNING, ERROR
    endpoint: str
    response_time_ms: float
    message: str
    details: Optional[dict] = None

    def to_dict(self):
        return asdict(self)


class HealthChecker:
    """Verifica el estado de todos los servicios del sistema."""

    def __init__(self, base_timeout: int = 5):
        self.base_timeout = base_timeout
        self.results: List[HealthResult] = []
        self.checks_passed = 0
        self.checks_failed = 0
        self.checks_warning = 0

    def _check_http(self, name: str, url: str, expected_status: int = 200,
                    timeout: Optional[int] = None) -> HealthResult:
        """Verifica un endpoint HTTP."""
        timeout = timeout or self.base_timeout
        start = time.time()
        try:
            req = urllib.request.Request(url, method='GET')
            req.add_header('User-Agent', 'TriageHealthCheck/1.0')
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                elapsed = (time.time() - start) * 1000
                status = "OK" if resp.status == expected_status else "WARNING"
                if resp.status != expected_status:
                    self.checks_warning += 1
                else:
                    self.checks_passed += 1

                body = resp.read(2048).decode('utf-8', errors='replace')
                try:
                    details = json.loads(body)
                except:
                    details = {"raw": body[:500]}

                return HealthResult(
                    name=name,
                    status=status,
                    endpoint=url,
                    response_time_ms=round(elapsed, 2),
                    message=f"HTTP {resp.status} en {elapsed:.0f}ms",
                    details=details if isinstance(details, dict) else None
                )
        except urllib.error.HTTPError as e:
            elapsed = (time.time() - start) * 1000
            self.checks_failed += 1
            return HealthResult(
                name=name,
                status="ERROR",
                endpoint=url,
                response_time_ms=round(elapsed, 2),
                message=f"HTTP Error {e.code}: {e.reason}"
            )
        except urllib.error.URLError as e:
            elapsed = (time.time() - start) * 1000
            self.checks_failed += 1
            return HealthResult(
                name=name,
                status="ERROR",
                endpoint=url,
                response_time_ms=round(elapsed, 2),
                message=f"Connection failed: {e.reason}"
            )
        except socket.timeout:
            elapsed = timeout * 1000
            self.checks_failed += 1
            return HealthResult(
                name=name,
                status="ERROR",
                endpoint=url,
                response_time_ms=round(elapsed, 2),
                message=f"Timeout after {timeout}s"
            )
        except Exception as e:
            elapsed = (time.time() - start) * 1000
            self.checks_failed += 1
            return HealthResult(
                name=name,
                status="ERROR",
                endpoint=url,
                response_time_ms=round(elapsed, 2),
                message=f"Exception: {str(e)}"
            )

    def _check_tcp(self, name: str, host: str, port: int,
                   timeout: Optional[int] = None) -> HealthResult:
        """Verifica conectividad TCP básica (para PostgreSQL, etc.)."""
        timeout = timeout or self.base_timeout
        start = time.time()
        try:
            with socket.create_connection((host, port), timeout=timeout):
                elapsed = (time.time() - start) * 1000
                self.checks_passed += 1
                return HealthResult(
                    name=name,
                    status="OK",
                    endpoint=f"{host}:{port}",
                    response_time_ms=round(elapsed, 2),
                    message=f"TCP port {port} open"
                )
        except socket.timeout:
            self.checks_failed += 1
            return HealthResult(
                name=name,
                status="ERROR",
                endpoint=f"{host}:{port}",
                response_time_ms=timeout * 1000,
                message=f"TCP timeout after {timeout}s"
            )
        except Exception as e:
            self.checks_failed += 1
            return HealthResult(
                name=name,
                status="ERROR",
                endpoint=f"{host}:{port}",
                response_time_ms=0,
                message=f"TCP failed: {str(e)}"
            )

    def _check_docker(self, container_name: str) -> HealthResult:
        """Verifica estado de un contenedor Docker."""
        start = time.time()
        try:
            result = subprocess.run(
                ["docker", "ps", "--filter", f"name={container_name}",
                 "--format", "{{.Status}}"],
                capture_output=True, text=True, timeout=10
            )
            elapsed = (time.time() - start) * 1000
            status_output = result.stdout.strip()

            if result.returncode != 0:
                self.checks_failed += 1
                return HealthResult(
                    name=f"Docker: {container_name}",
                    status="ERROR",
                    endpoint=container_name,
                    response_time_ms=round(elapsed, 2),
                    message=f"docker ps failed: {result.stderr.strip()}"
                )

            if status_output:
                if "Up" in status_output and "unhealthy" not in status_output.lower():
                    self.checks_passed += 1
                    status = "OK"
                elif "unhealthy" in status_output.lower():
                    self.checks_warning += 1
                    status = "WARNING"
                else:
                    self.checks_failed += 1
                    status = "ERROR"
                return HealthResult(
                    name=f"Docker: {container_name}",
                    status=status,
                    endpoint=container_name,
                    response_time_ms=round(elapsed, 2),
                    message=status_output
                )
            else:
                self.checks_failed += 1
                return HealthResult(
                    name=f"Docker: {container_name}",
                    status="ERROR",
                    endpoint=container_name,
                    response_time_ms=round(elapsed, 2),
                    message="Container not running"
                )
        except FileNotFoundError:
            self.checks_warning += 1
            return HealthResult(
                name=f"Docker: {container_name}",
                status="WARNING",
                endpoint=container_name,
                response_time_ms=0,
                message="Docker CLI not found (skipping)"
            )
        except Exception as e:
            self.checks_failed += 1
            return HealthResult(
                name=f"Docker: {container_name}",
                status="ERROR",
                endpoint=container_name,
                response_time_ms=0,
                message=f"Exception: {str(e)}"
            )

    def run_all(self) -> List[HealthResult]:
        """Ejecuta todas las verificaciones del sistema."""
        print(f"\n{'='*60}")
        print(f"  TRIAJE IA - Health Check")
        print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}\n")

        # 1. Base de datos (TCP)
        print("[1/6] Verificando PostgreSQL...")
        self.results.append(self._check_tcp(
            "PostgreSQL", "localhost", 5432, timeout=3
        ))

        # 2. FastAPI Backend
        print("[2/6] Verificando FastAPI Backend...")
        self.results.append(self._check_http(
            "FastAPI", "http://localhost:8000/api/v1/healthz"
        ))
        # Fallback si no hay /healthz
        if self.results[-1].status == "ERROR":
            self.results[-1] = self._check_http(
                "FastAPI", "http://localhost:8000/docs"
            )

        # 3. Streamlit
        print("[3/6] Verificando Streamlit...")
        self.results.append(self._check_http(
            "Streamlit", "http://localhost:8501/_stcore/health"
        ))

        # 4. React Admin
        print("[4/6] Verificando React Admin...")
        self.results.append(self._check_http(
            "React Admin", "http://localhost:5173"
        ))

        # 5. n8n
        print("[5/6] Verificando n8n Workflow Engine...")
        self.results.append(self._check_http(
            "n8n", "http://localhost:5678/healthz"
        ))

        # 6. Mock HCE
        print("[6/6] Verificando Mock HCE...")
        self.results.append(self._check_http(
            "Mock HCE", "http://localhost:8080"
        ))

        # Docker containers (opcional)
        print("[Extra] Verificando contenedores Docker...")
        containers = [
            "triage-postgres",
            "triage-fastapi",
            "triage-streamlit",
            "triage-react",
            "triage-n8n",
            "triage-mock-hce"
        ]
        for container in containers:
            self.results.append(self._check_docker(container))

        return self.results

    def print_summary(self, verbose: bool = False):
        """Imprime el resumen de resultados."""
        print(f"\n{'='*60}")
        print("  RESUMEN")
        print(f"{'='*60}\n")

        for r in self.results:
            icon = "✅" if r.status == "OK" else ("⚠️ " if r.status == "WARNING" else "❌")
            print(f"{icon} {r.name:25s} | {r.status:8s} | {r.response_time_ms:6.1f}ms | {r.message}")
            if verbose and r.details:
                print(f"    └─ Details: {json.dumps(r.details, indent=2, ensure_ascii=False)[:200]}")

        total = len(self.results)
        print(f"\n{'='*60}")
        print(f"  OK: {self.checks_passed} | WARNING: {self.checks_warning} | ERROR: {self.checks_failed} / Total: {total}")

        if self.checks_failed > 0:
            print(f"  Estado: 🔴 CRÍTICO")
            return 1
        elif self.checks_warning > 0:
            print(f"  Estado: 🟠 DEGRADADO")
            return 2
        else:
            print(f"  Estado: 🟢 SALUDABLE")
            return 0

    def to_json(self) -> str:
        """Exporta resultados a JSON."""
        return json.dumps({
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "passed": self.checks_passed,
                "warning": self.checks_warning,
                "failed": self.checks_failed,
                "total": len(self.results)
            },
            "checks": [r.to_dict() for r in self.results]
        }, indent=2, ensure_ascii=False)


def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="Health check para el sistema de Triaje IA"
    )
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Mostrar detalles completos")
    parser.add_argument("--json", "-j", action="store_true",
                        help="Salida en formato JSON")
    parser.add_argument("--notify", "-n", action="store_true",
                        help="Enviar notificación si hay errores")
    parser.add_argument("--timeout", "-t", type=int, default=5,
                        help="Timeout en segundos (default: 5)")
    args = parser.parse_args()

    checker = HealthChecker(base_timeout=args.timeout)
    checker.run_all()

    if args.json:
        print(checker.to_json())
    else:
        exit_code = checker.print_summary(verbose=args.verbose)

    if args.notify and checker.checks_failed > 0:
        print("\n🔔 Notificación: Se detectaron servicios caídos.")
        # Aquí se puede integrar con Telegram/email/webhook
        # Ejemplo: enviar alerta a n8n o canal de Telegram
        try:
            alert_msg = {
                "text": f"🚨 ALERTA HEALTH CHECK\n\n"
                        f"{checker.checks_failed} servicio(s) caído(s):\n" +
                        "\n".join([f"- {r.name}: {r.message}"
                                  for r in checker.results if r.status == "ERROR"]),
                "timestamp": datetime.now().isoformat()
            }
            req = urllib.request.Request(
                "http://localhost:5678/webhook/health-alert",
                data=json.dumps(alert_msg).encode(),
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            urllib.request.urlopen(req, timeout=3)
            print("   Alerta enviada a n8n.")
        except Exception as e:
            print(f"   No se pudo enviar notificación: {e}")

    if not args.json:
        sys.exit(exit_code)
    else:
        sys.exit(0 if checker.checks_failed == 0 else 1)


if __name__ == "__main__":
    main()
