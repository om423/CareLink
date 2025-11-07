from __future__ import annotations

import json
import re
import time
from typing import Any, Dict, Optional

try:
    # New SDK style: from google import genai
    from google import genai as genai_new  # type: ignore
except Exception:  # pragma: no cover
    genai_new = None

try:
    # Legacy SDK: google.generativeai
    import google.generativeai as genai_legacy  # type: ignore
except Exception:  # pragma: no cover
    genai_legacy = None


DEFAULT_MODEL = "gemini-2.0-flash"
FALLBACK_MODELS = [
    "gemini-2.5-flash",
    "gemini-1.5-flash-8b",
    "gemini-1.5-flash-latest",
    "gemini-1.5-pro",
]

SYSTEM_INSTRUCTIONS = (
    "ROLE: You are a conservative medical triage assistant.\n"
    "OUTPUT: Return ONLY compact JSON with keys: severity, summary, "
    "advice, red_flags, differential, rationale.\n"
    "severity MUST be one of: Mild, Moderate, Severe, Critical.\n"
    "CONTEXT: Use patient context carefully (age, weight, allergies, "
    "medical_history) to inform risk, red flags, and level of care.\n"
    "ALLERGIES: If allergies are present, note interactions or risks "
    "relevant to symptoms.\n"
    "COMORBIDITIES: From medical_history, factor chronic conditions "
    "that may increase severity.\n"
    "SAFETY: When in doubt, recommend contacting a healthcare "
    "professional. This is NOT medical advice.\n"
    "STYLE: Be concise, plain language, no markdown, no extra keys.\n"
)

JSON_OPEN = re.compile(r"\{", re.MULTILINE)
JSON_CLOSE = re.compile(r"\}", re.MULTILINE)


def _strip_code_fences(s: str) -> str:
    s = s.strip()
    if s.startswith("```"):
        s = re.sub(r"^```(?:json)?\s*|\s*```$", "", s, flags=re.IGNORECASE | re.DOTALL)
    return s.strip()


def _extract_json_block(s: str) -> str | None:
    start_iter = [m.start() for m in JSON_OPEN.finditer(s)]
    for start in start_iter:
        depth = 0
        for i in range(start, len(s)):
            if s[i] == "{":
                depth += 1
            elif s[i] == "}":
                depth -= 1
                if depth == 0:
                    chunk = s[start : i + 1]
                    return chunk
    return None


class GeminiClient:
    """
    Minimal Gemini wrapper for preliminary triage generation.
    Returns a parsed dict with keys:
      - severity: "Mild"|"Moderate"|"Severe"|"Critical"
      - summary: str
      - advice: str
      - red_flags: list[str]
      - differential: list[str]
      - rationale: str
    """

    def __init__(self, api_key: Optional[str] = None, model: str = DEFAULT_MODEL) -> None:
        self.api_key = api_key
        self.model = model
        self.enabled = bool(api_key) and (genai_new is not None or genai_legacy is not None)
        self._api_variant = None  # "new" | "legacy" | None
        self._client = None
        self._model_obj = None

        if not self.enabled:
            return

        # Prefer new client if available
        if genai_new is not None:
            try:
                self._client = genai_new.Client(api_key=api_key)
                self._api_variant = "new"
            except Exception:
                self._client = None
                self._api_variant = None

        # Fallback to legacy library
        if self._api_variant is None and genai_legacy is not None:
            try:
                genai_legacy.configure(api_key=api_key)
                self._model_obj = genai_legacy.GenerativeModel(
                    model,
                    system_instruction=(
                        "You are a careful, conservative medical "
                        "triage assistant.\n"
                        "Respond ONLY in compact JSON with keys: severity, "
                        "summary, advice, red_flags, differential, "
                        "rationale.\n"
                        "severity must be one of: Mild, Moderate, "
                        "Severe, Critical.\n"
                        "Keep advice general and instruct patients to seek "
                        "professional care for concerning symptoms.\n"
                        "This is NOT medical advice or diagnosis. "
                        "Be concise."
                    ),
                )
                self._api_variant = "legacy"
            except Exception:
                self._model_obj = None
                self._api_variant = None

    def generate_triage(
        self, symptoms_text: str, patient_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Returns a dict; if API missing/unavailable, raises RuntimeError.
        """
        if not self.enabled:
            raise RuntimeError(
                "Gemini not configured. Set GEMINI_API_KEY and install "
                "google-genai / google-generativeai."
            )

        prompt = self._build_prompt(symptoms_text, patient_context=patient_context)
        raw = self._request_with_retry(prompt)
        try:
            data = self._parse_or_repair(raw, prompt)
            return {
                "severity": data.get("severity", "Moderate"),
                "summary": data.get("summary", "No summary provided."),
                "advice": data.get(
                    "advice", "Consider contacting a healthcare professional " "for guidance."
                ),
                "red_flags": data.get("red_flags", []) or [],
                "differential": data.get("differential", []) or [],
                "rationale": data.get("rationale", "No rationale provided."),
            }
        except Exception:
            return {
                "severity": "Moderate",
                "summary": "Unable to parse model response.",
                "advice": ("Consider contacting a healthcare professional " "for guidance."),
                "red_flags": [],
                "differential": [],
                "rationale": "Fallback response.",
            }

    def _request_with_retry(self, prompt: str) -> str:
        if not self.enabled:
            raise RuntimeError(
                "Gemini not configured. Set GEMINI_API_KEY and install "
                "google-genai / google-generativeai."
            )

        last_err: Exception | None = None
        for attempt in range(2):
            try:
                # New client path with model fallbacks
                if self._api_variant == "new" and self._client is not None:
                    last_err = None
                    for model_name in [self.model] + FALLBACK_MODELS:
                        try:
                            contents = [{"role": "user", "parts": [{"text": prompt}]}]
                            resp = self._client.models.generate_content(
                                model=model_name, contents=contents
                            )
                            text = getattr(resp, "text", "") or ""
                            if not text:
                                try:
                                    parts = getattr(resp, "candidates", [])[
                                        0
                                    ].content.parts  # type: ignore
                                    text = "".join(
                                        getattr(p, "text", "") for p in parts if hasattr(p, "text")
                                    )
                                except Exception:
                                    text = ""
                            return text
                        except Exception as e:
                            last_err = e
                            # Continue to next model
                            continue
                    # If we exhausted all models, check if we should retry
                    if attempt == 0 and last_err is not None:
                        # Retry if it's a transient error
                        if "Transient" in str(last_err):
                            time.sleep(0.6)
                            continue
                    # If we can't retry, raise the error
                    if last_err is not None:
                        raise RuntimeError(f"Gemini error: {last_err}")
                    raise RuntimeError("No models available")

                # Legacy path with model fallbacks
                elif self._api_variant == "legacy" and self._model_obj is not None:
                    last_err = None
                    model_obj = self._model_obj
                    for model_name in [self.model] + FALLBACK_MODELS:
                        try:
                            if (
                                model_obj is None
                                or getattr(model_obj, "model_name", None) != model_name
                            ):
                                model_obj = genai_legacy.GenerativeModel(
                                    model_name, system_instruction=SYSTEM_INSTRUCTIONS
                                )
                            resp = model_obj.generate_content(prompt)
                            text = getattr(resp, "text", "") or ""
                            if not text:
                                try:
                                    parts = getattr(resp, "candidates", [])[
                                        0
                                    ].content.parts  # type: ignore
                                    text = "".join(
                                        getattr(p, "text", "") for p in parts if hasattr(p, "text")
                                    )
                                except Exception:
                                    text = ""
                            return text
                        except Exception as e:
                            last_err = e
                            # Continue to next model
                            continue
                    # If we exhausted all models, check if we should retry
                    if attempt == 0 and last_err is not None:
                        # Retry if it's a transient error
                        if "Transient" in str(last_err):
                            time.sleep(0.6)
                            continue
                    # If we can't retry, raise the error
                    if last_err is not None:
                        raise RuntimeError(f"Gemini error: {last_err}")
                    raise RuntimeError("No models available")

                else:
                    raise RuntimeError(
                        "Gemini not configured. Set GEMINI_API_KEY and "
                        "install google-generativeai."
                    )
            except Exception as e:
                last_err = e
                # Retry on first attempt for transient errors
                if attempt == 0:
                    if "Transient" in str(e) or "transient" in str(e).lower():
                        time.sleep(0.6)
                        continue
                    # For other errors, also retry once
                    time.sleep(0.6)
                    continue
                # On second attempt, raise the error
                raise

    def _parse_or_repair(self, raw_text: str, original_prompt: str) -> dict:
        cleaned = _strip_code_fences(raw_text)
        try:
            return json.loads(cleaned)
        except Exception:
            pass

        chunk = _extract_json_block(cleaned)
        if chunk:
            try:
                return json.loads(chunk)
            except Exception:
                pass

        repair_prompt = (
            f"{SYSTEM_INSTRUCTIONS}\n\n"
            "Return STRICT JSON only. No prose, no markdown fences. "
            "If prior output was malformed, rewrite it as valid JSON "
            "with the exact required keys.\n\n"
            "PRIOR_REQUEST:\n"
            f"{original_prompt}\n"
        )
        try:
            repaired = self._request_with_retry(repair_prompt)
            repaired_clean = _strip_code_fences(repaired)
            try:
                return json.loads(repaired_clean)
            except Exception:
                chunk2 = _extract_json_block(repaired_clean)
                if chunk2:
                    return json.loads(chunk2)
        except Exception:
            pass

        return {
            "severity": "Moderate",
            "summary": cleaned.strip() or "Unable to parse model response.",
            "advice": "Consider contacting a healthcare professional for guidance.",
            "red_flags": [],
            "differential": [],
            "rationale": ("Fallback response; JSON parsing failed after repair."),
        }

    # Explicit prompt builder for testability
    def _build_prompt(
        self, symptoms_text: str, patient_context: Optional[Dict[str, Any]] = None
    ) -> str:
        def safe(val: Any) -> str:
            if val is None:
                return "Unknown"
            if isinstance(val, str):
                val = val.strip()
                return val or "Unknown"
            return str(val)

        ctx = patient_context or {}
        age = safe(ctx.get("age"))
        weight = safe(ctx.get("weight"))
        allergies = safe(ctx.get("allergies") or "None reported")
        med_hist = safe(ctx.get("medical_history") or "None reported")

        patient_context_block = (
            "{\n"
            f'  "age": "{age}",\n'
            f'  "weight": "{weight}",\n'
            f'  "allergies": "{allergies}",\n'
            f'  "medical_history": "{med_hist}"\n'
            "}"
        )

        prompt = (
            f"{SYSTEM_INSTRUCTIONS}\n\n"
            f"PATIENT_CONTEXT:\n{patient_context_block}\n\n"
            "PATIENT_SYMPTOM_DESCRIPTION:\n"
            f"{(symptoms_text or '').strip()}\n\n"
            "RESPONSE_FORMAT:\n"
            "{\n"
            '  "severity": "Mild|Moderate|Severe|Critical",\n'
            '  "summary": "short summary",\n'
            '  "advice": "next steps for patient",\n'
            '  "red_flags": ["..."],\n'
            '  "differential": ["..."],\n'
            '  "rationale": "plain-language reasoning"\n'
            "}\n"
        )
        return prompt
