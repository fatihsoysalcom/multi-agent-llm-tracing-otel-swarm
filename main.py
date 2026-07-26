import os
import time
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor
# For OTLP export to SigNoz, uncomment these and configure endpoint
# from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

# otel-swarm library for LLM and agent tracing
import otel_swarm

# --- OpenTelemetry Setup ---
# Resource for identifying the service in your observability platform
resource = Resource.create({
    "service.name": "multi-agent-llm-system",
    "service.version": "1.0.0",
    "environment": "development"
})

# Initialize TracerProvider
provider = TracerProvider(resource=resource)
trace.set_tracer_provider(provider)

# Configure a ConsoleSpanExporter to print traces to the console
# This is useful for seeing traces without a collector running
console_exporter = ConsoleSpanExporter()
provider.add_span_processor(SimpleSpanProcessor(console_exporter))

# --- Optional: Configure OTLP Exporter for SigNoz/Collector ---
# Uncomment and configure if you have a SigNoz instance or OTLP collector running
# otlp_exporter = OTLPSpanExporter(
#     endpoint="http://localhost:4317", # Default SigNoz OTLP gRPC endpoint
#     insecure=True
# )
# provider.add_span_processor(SimpleSpanProcessor(otlp_exporter))
# print("OTLP exporter configured for http://localhost:4317 (SigNoz). Make sure it's running.")


tracer = trace.get_tracer(__name__)

# --- Mock LLM and otel-swarm Integration ---

# A simple mock LLM function that will be traced by otel-swarm
@otel_swarm.trace_llm_call(llm_provider="mock_llm_provider", llm_model="mock-gpt-3.5-turbo")
def traced_mock_llm_call(prompt: str) -> str:
    """A mock LLM call that is directly traced by otel-swarm."""
    print(f"  [Traced Mock LLM] Processing prompt: '{prompt[:50]}...' ")
    time.sleep(0.5) # Simulate processing time
    response = f"Response to '{prompt[:20]}...': Simulated output for the task." # Simulate LLM response
    return response


# --- Multi-Agent System Simulation ---

@otel_swarm.trace_agent_action(agent_name="PlannerAgent", action_name="PlanTask")
def planner_agent(user_query: str) -> str:
    """
    Simulates a Planner Agent that decides on a task based on user input.
    Its internal LLM call is automatically traced.
    """
    print(f"[PlannerAgent] Received query: '{user_query}'")
    planning_prompt = f"User wants to '{user_query}'. What is the first step?"
    # The LLM call here is automatically traced due to the @trace_llm_call decorator
    plan_response = traced_mock_llm_call(planning_prompt)
    task_description = f"Plan: {plan_response.split(':')[1].strip()}"
    print(f"[PlannerAgent] Generated task: '{task_description}'")
    return task_description

@otel_swarm.trace_agent_action(agent_name="ExecutorAgent", action_name="ExecuteTask")
def executor_agent(task_description: str) -> str:
    """
    Simulates an Executor Agent that performs a task.
    Its internal LLM call is automatically traced.
    """
    print(f"[ExecutorAgent] Received task: '{task_description}'")
    execution_prompt = f"Execute the task: '{task_description}'. Provide a summary of execution."
    # The LLM call here is automatically traced due to the @trace_llm_call decorator
    execution_response = traced_mock_llm_call(execution_prompt)
    result = f"Execution Result: {execution_response.split(':')[1].strip()}"
    print(f"[ExecutorAgent] Task completed: '{result}'")
    return result

# --- Main Execution Flow ---
if __name__ == "__main__":
    print("Starting Multi-Agent LLM System Simulation with OpenTelemetry and otel-swarm...")
    print("Traces will be printed to the console.")
    print("-" * 60)

    # Start a top-level span for the entire workflow
    with tracer.start_as_current_span("multi_agent_workflow") as workflow_span:
        workflow_span.set_attribute("workflow.name", "UserQueryProcessing")
        user_input = "Find the best restaurant for Italian food in Rome."

        # Planner Agent acts, its action and internal LLM call are traced
        task = planner_agent(user_input)

        # Executor Agent acts, its action and internal LLM call are traced
        final_result = executor_agent(task)

        print("-" * 60)
        print(f"Workflow completed. Final result: {final_result}")
        print("\nCheck the console output above for OpenTelemetry traces.")
        # If OTLP exporter was enabled, traces would also be sent to SigNoz/collector.

