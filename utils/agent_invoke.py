"""
utils/agent_invoke.py
------------------------
Groq's Llama models occasionally emit a malformed, text-based function
call (e.g. "<function=get_transport_options {...}>") instead of using
the real tool-calling mechanism, especially when several tools are
registered at once. This is a known reliability issue with the model
itself, not a bug in the tools/prompt — and it's non-deterministic, so
simply retrying the same request often succeeds the second time.

This wrapper retries automatically before giving up, and only retries on
this SPECIFIC failure (tool_use_failed / malformed tool call) — any other
error is raised immediately, since retrying wouldn't help those.
"""

import time


def invoke_agent_with_retry(agent, messages: dict, max_retries: int = 2, delay_seconds: float = 1.0):
    """
    Call agent.invoke(messages), retrying up to `max_retries` additional
    times if the failure looks like the Groq/Llama malformed-tool-call
    error. Raises the last exception if all attempts fail.
    """
    last_error = None

    for attempt in range(max_retries + 1):
        try:
            return agent.invoke(messages)
        except Exception as e:
            error_text = str(e).lower()
            is_tool_call_error = (
                "tool_use_failed" in error_text
                or "tool call validation failed" in error_text
                or "failed to call a function" in error_text
            )
            last_error = e

            if not is_tool_call_error:
                raise  # different kind of error — don't retry, surface it immediately

            if attempt < max_retries:
                time.sleep(delay_seconds)
                continue

    raise last_error