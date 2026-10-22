"""Nebius Token Factory client (OpenAI-compatible).

Talks to the endpoint with nothing but the standard library, so there is no
hard dependency on the openai SDK -- one less package that can fail to
install is one less risk in the nine days before the deadline. The request
shape follows OpenAI's Chat Completions API, so swapping in the official
SDK later means replacing the implementation of ``_post``.

Configuration (all three read environment variables, no CLI flags needed):

    NEBIUS_API_KEY    required, of the form nb-...
    NEBIUS_BASE_URL   optional, default https://api.tokenfactory.nebius.com/v1
    NEBIUS_MODEL      optional, default nvidia/nemotron-3-super-120b-a12b

To see which models the platform currently offers:

    python -m src.nebius_client --list-models

Without an API key this module still imports: it switches itself to mock
mode (see ``MockResponse``), so the whole pipeline can be run, reviewed
and debugged before an account exists.
"""

import json
import os
import time
import urllib.error
import urllib.request

DEFAULT_BASE_URL = "https://api.tokenfactory.nebius.com/v1"
DEFAULT_MODEL = "nvidia/nemotron-3-super-120b-a12b"

# Common fallback model IDs -- the public NVIDIA Nemotron endpoints on Token
# Factory. The spelling of these names (underscores vs hyphens) is not
# consistent across the platform's own pages, so all of them are kept and
# tried in order.
FALLBACK_MODELS = [
    "nvidia/nemotron-3-super-120b-a12b",
    "nvidia/nemotron-3-nano-30b-a3b",
    "nvidia/nemotron-3-ultra-550b-a55b",
    "nvidia/nemotron-3_5-lightning",
]


class NebiusError(RuntimeError):
    """A Token Factory call failed."""


def _get_env(*names, default=None):
    for n in names:
        v = os.environ.get(n)
        if v:
            return v
    return default


def api_key():
    return _get_env("NEBIUS_API_KEY", "NEB_TOKEN_FACTORY_KEY")


def base_url():
    return (_get_env("NEBIUS_BASE_URL", default=DEFAULT_BASE_URL) or DEFAULT_BASE_URL).rstrip("/")


def default_model():
    return _get_env("NEBIUS_MODEL", default=DEFAULT_MODEL) or DEFAULT_MODEL


def is_mock():
    """True when there is no API key, i.e. mock mode is active."""
    return not api_key()


class MockResponse:
    """A stand-in response used to exercise the pipeline without an account.

    It does not pretend to be a model. It answers one specific kind of
    request -- "what should I change?" -- with a fixed, plausible value, so
    that the end-to-end flow (read metrics -> propose -> re-run -> compare)
    can be demonstrated locally. Real runs use the real model.
    """

    def __init__(self, content):
        self.content = content
        self.usage = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}


def _mock_content(messages):
    """Return a structurally valid suggestion, keyed off the prompt text."""
    blob = " ".join(
        m.get("content", "") if isinstance(m.get("content"), str) else json.dumps(m.get("content", ""))
        for m in messages
    ).lower()

    if "cross-track" in blob or "crosstrack" in blob:
        return json.dumps({
            "diagnosis": "cross-track error dominates the residual; the heading gain is too low "
                         "for the requested speed",
            "changes": {"Kp": 12.0},
            "confidence": 0.72,
        })
    return json.dumps({
        "diagnosis": "baseline parameters are near-optimal for this map",
        "changes": {},
        "confidence": 0.55,
    })


class TokenFactory:
    """A minimal Token Factory client.

    Three public methods, and no more: ``chat`` (free-form),
    ``chat_json`` (structured output) and ``list_models`` (what the
    platform currently offers).
    """

    def __init__(self, model=None, base=None, key=None, timeout=90, mock=None):
        self.model = model or default_model()
        self.base = (base or base_url()).rstrip("/")
        self.key = key if key is not None else api_key()
        self.timeout = timeout
        self.mock = is_mock() if mock is None else mock
        self._tried_models = []

    # ---------------------------------------------------------------- plumbing

    def _post(self, path, payload):
        url = f"{self.base}{path}"
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            url, data=data, method="POST",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.key}",
                "User-Agent": "nemotron-nav-agent/1.0",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", "replace")
            raise NebiusError(f"HTTP {e.code} from {url}: {body[:600]}") from e
        except urllib.error.URLError as e:
            raise NebiusError(f"cannot reach {url}: {e.reason}") from e

    # ---------------------------------------------------------------- public

    def list_models(self):
        """The model IDs currently available on the platform."""
        if self.mock:
            return list(FALLBACK_MODELS)
        url = f"{self.base}/models"
        req = urllib.request.Request(url, headers={"Authorization": f"Bearer {self.key}"})
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                payload = json.loads(resp.read().decode("utf-8"))
        except Exception as e:                                   # noqa: BLE001
            raise NebiusError(f"cannot list models: {e}") from e
        return [m.get("id") for m in payload.get("data", []) if m.get("id")]

    def chat(self, messages, model=None, temperature=0.2, max_tokens=1200, retries=2):
        """Send one conversation turn, return the assistant's text."""
        if self.mock:
            return _mock_content(messages).strip()

        use_model = model or self.model
        last_err = None
        candidates = [use_model] + [m for m in FALLBACK_MODELS if m != use_model]

        for attempt in range(retries + 1):
            candidate = candidates[min(attempt, len(candidates) - 1)]
            try:
                payload = {
                    "model": candidate,
                    "messages": messages,
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                }
                data = self._post("/chat/completions", payload)
                self._tried_models.append(candidate)
                return (data["choices"][0]["message"]["content"] or "").strip()
            except NebiusError as e:
                last_err = e
                # A 400 usually means a wrong model ID or an illegal
                # parameter -- try a different model and move on.
                if "HTTP 400" in str(e) or "HTTP 404" in str(e):
                    continue
                time.sleep(1.0 + attempt)
        raise last_err

    def chat_json(self, messages, model=None, temperature=0.1, max_tokens=1200, retries=2):
        """Ask for JSON. The model sometimes wraps it in a markdown code
        block, so the extraction is forgiving."""
        text = self.chat(messages, model=model, temperature=temperature,
                         max_tokens=max_tokens, retries=retries)
        return _extract_json(text)

    def usage_report(self):
        """Which models have been tried -- useful when debugging model IDs."""
        return list(self._tried_models)


def _extract_json(text):
    """Pull a JSON object out of the model's output.

    The model sometimes returns the object wrapped in ```json ... ```, and
    sometimes with a sentence of explanation around it. Both are recovered.
    """
    if not text:
        raise NebiusError("empty response from Token Factory")

    text = text.strip()
    if text.startswith("```"):
        text = text.split("```", 2)[1] if text.count("```") >= 2 else text.strip("`")
        if text.lower().startswith("json"):
            text = text[4:]
        text = text.strip("`").strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    for opener, closer in (("{", "}"), ("[", "]")):
        start = text.find(opener)
        end = text.rfind(closer)
        if start != -1 and end > start:
            try:
                return json.loads(text[start:end + 1])
            except json.JSONDecodeError:
                continue

    raise NebiusError(f"could not parse JSON from model output: {text[:300]}")


if __name__ == "__main__":
    import sys

    if "--list-models" in sys.argv:
        tf = TokenFactory()
        print(f"mode: {'mock' if tf.mock else 'live'}   base: {tf.base}")
        for mid in tf.list_models():
            print(" ", mid)
    else:
        tf = TokenFactory()
        print(f"mode: {'mock (no NEBIUS_API_KEY set)' if tf.mock else 'live'}")
        print(tf.chat_json([
            {"role": "system", "content": "You return JSON only."},
            {"role": "user", "content": "Cross-track error is 0.28 m at speed 1.5. "
                                        "Return {\"diagnosis\":..., \"changes\":{...}}."},
        ]))
