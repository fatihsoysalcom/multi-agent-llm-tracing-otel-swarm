# Multi Agent LLM Tracing otel-swarm

This example demonstrates how to use the `otel-swarm` library with OpenTelemetry to trace interactions within a simulated multi-agent LLM system. It shows how to instrument both LLM calls and agent actions, printing the resulting traces to the console. This setup is the foundation for sending observability data to platforms like SigNoz.

## Language

`python`

## How to Run

1. Install dependencies: `pip install opentelemetry-sdk opentelemetry-exporter-console otel-swarm`
2. Run the script: `python main.py`
3. Observe the OpenTelemetry traces printed to the console.

## Original Article

This example accompanies the Turkish article: [Multi-Agent LLM Sistemlerini otel-swarm ve SigNoz ile İzleme Rehberi](https://fatihsoysal.com/blog/multi-agent-llm-sistemlerini-otel-swarm-ve-signoz-ile-izleme-rehberi/).

## License

MIT — see [LICENSE](LICENSE).
