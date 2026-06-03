"""Tests for the tool-calling agent loop in BaseLLMProvider.

The agent loop (run_agent_turn) lets the kholleur query the knowledge graph
through tools. These tests use a scripted fake provider so they run without
any API key or network access.
"""

from core.entities.agent import AgentResponse, ToolCall
from infrastructure.llm.base import BaseLLMProvider


class FakeAgentProvider(BaseLLMProvider):
    """Provider that replays scripted tool-calling responses in order."""

    def __init__(self, scripted_responses):
        super().__init__(model_name="fake-model")
        self._scripted = list(scripted_responses)
        self.plain_calls = 0

    @property
    def name(self) -> str:
        return "Fake"

    def _init_client(self):
        return None

    def _call_api(self, messages, system_prompt, temperature=0.7):
        # Plain (no-tools) fallback path.
        self.plain_calls += 1
        return "PLAIN_FALLBACK"

    def _call_api_with_tools(self, messages, system_prompt, tools, temperature=0.7):
        return self._scripted.pop(0)


class NoToolProvider(BaseLLMProvider):
    """Provider that never overrides _call_api_with_tools (no tool support)."""

    @property
    def name(self) -> str:
        return "NoTool"

    def _init_client(self):
        return None

    def _call_api(self, messages, system_prompt, temperature=0.7):
        return "FALLBACK_TEXT"


def test_agent_loop_executes_tool_then_returns_text():
    """The loop should run a requested tool, feed the result back, and return final text."""
    provider = FakeAgentProvider([
        AgentResponse(
            tool_calls=[ToolCall(id="1", name="lire_definition", arguments={"concept_id": "x"})],
            stop_reason="tool_use",
        ),
        AgentResponse(text="Voici l'explication finale.", stop_reason="end_turn"),
    ])

    executed = []

    def executor(name, arguments):
        executed.append((name, arguments))
        return '{"found": true}'

    result = provider.run_agent_turn(
        user_message="aide-moi",
        system_prompt="sys",
        tools=[{"type": "function"}],
        tool_executor=executor,
    )

    assert result == "Voici l'explication finale."
    assert executed == [("lire_definition", {"concept_id": "x"})]


def test_agent_loop_returns_text_without_tools():
    """A direct text answer (no tool calls) is returned immediately."""
    provider = FakeAgentProvider([
        AgentResponse(text="Réponse directe.", stop_reason="end_turn"),
    ])

    result = provider.run_agent_turn(
        user_message="salut",
        system_prompt="sys",
        tools=[],
        tool_executor=lambda name, args: "{}",
    )

    assert result == "Réponse directe."


def test_agent_loop_falls_back_when_provider_has_no_tool_support():
    """If a provider does not implement tools, the loop degrades to a plain call."""
    provider = NoToolProvider(model_name="x")

    result = provider.run_agent_turn(
        user_message="salut",
        system_prompt="sys",
        tools=[{"type": "function"}],
        tool_executor=lambda name, args: "{}",
    )

    assert result == "FALLBACK_TEXT"


def test_agent_loop_stops_at_max_iterations():
    """A model that keeps requesting tools is capped, then answers once in plain mode."""
    always_tool = AgentResponse(
        tool_calls=[ToolCall(id="1", name="chercher_concepts", arguments={"query": "q"})],
        stop_reason="tool_use",
    )
    provider = FakeAgentProvider([always_tool for _ in range(10)])

    result = provider.run_agent_turn(
        user_message="boucle",
        system_prompt="sys",
        tools=[{"type": "function"}],
        tool_executor=lambda name, args: "{}",
        max_iterations=3,
    )

    assert result == "PLAIN_FALLBACK"
    assert provider.plain_calls == 1
