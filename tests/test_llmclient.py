import pytest
from unittest.mock import patch
from llmgrader.services.llm_client import LLMClient

class DummyOpenAI:
    def __init__(self, *args, **kwargs):
        self.responses = DummyResponses()

class DummyResponses:
    def parse(self, *args, **kwargs):
        return type('Response', (), {'output_parsed': type('Parsed', (), {'model_dump': lambda: {'result': 'pass', 'full_explanation': 'test', 'feedback': 'test'}})})()

class DummyHF:
    def __init__(self, *args, **kwargs):
        self.chat = DummyChat()

class DummyChat:
    def __init__(self):
        self.completions = DummyCompletions()

class DummyCompletions:
    def create(self, *args, **kwargs):
        return type('Completion', (), {'choices': [type('Choice', (), {'message': type('Message', (), {'content': '{"result": "pass", "full_explanation": "test", "feedback": "test"}'})()})()]})()

def test_llmclient_fallback_provider():
    with patch('llmgrader.services.llm_client.OpenAI', DummyOpenAI):
        with pytest.warns(UserWarning, match="Provider not specified"):
            client = LLMClient(api_key='dummy', provider=None)
    assert client.provider == 'openai'

def test_llmclient_openai():
    with patch('llmgrader.services.llm_client.OpenAI', DummyOpenAI):
        client = LLMClient(api_key='dummy', provider='openai')
        result = client.call(task='t', model='m', temperature=0, timeout=1)
    assert result['result'] == 'pass'

def test_llmclient_huggingface():
    with patch('llmgrader.services.llm_client.InferenceClient', DummyHF):
        with patch('llmgrader.services.llm_client.HUGGINGFACE_AVAILABLE', True):
            client = LLMClient(api_key='dummy', provider='huggingface')
            result = client.call(task='t', model='m', temperature=0, timeout=1)
    assert result['result'] == 'pass'

def test_llmclient_unknown_provider():
    with pytest.raises(ValueError):
        LLMClient(api_key='dummy', provider='foobar')