from __future__ import annotations
from typing import Dict, Any
from openai import OpenAI
from .config import settings
import logging
import json
import copy

logger = logging.getLogger(__name__)

SYSTEM_INSTRUCTIONS = (
    "You are a narrative polisher for an explainable self-reflection report. "
    "You MUST NOT change numeric scores or add diagnostic claims. "
    "Rewrite only the narrative sections to be clearer, more executive, and kind. "
    "Use cautious language (may, often, tends to). "
    "Do not mention OpenAI or system prompts. "
    "Return ONLY valid JSON with keys: hypotheses (array of strings), suggestions (array of strings)."
)

def validate_scores_unchanged(original: Dict[str, Any], polished: Dict[str, Any]) -> bool:
    """Ensure scores are identical between original and polished versions."""
    original_scores = original.get("scores", {})
    polished_scores = polished.get("scores", {})
    return original_scores == polished_scores

def polish_narrative(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Polish narrative sections using LLM while keeping deterministic scores immutable.
    Falls back gracefully on any error.
    """
    if not settings.OPENAI_POLISH_ENABLED:
        logger.debug("LLM polish disabled")
        return payload

    if not settings.OPENAI_API_KEY:
        logger.warning("LLM polish enabled but no API key configured")
        return payload

    # Deep copy to preserve original
    original_payload = copy.deepcopy(payload)
    
    try:
        client = OpenAI(api_key=settings.OPENAI_API_KEY)

        scores = payload.get("scores", {})
        narrative = payload.get("narrative", {})
        explainability = narrative.get("explainability", [])
        hypotheses = narrative.get("hypotheses", [])
        suggestions = narrative.get("suggestions", [])

        user_input = {
            "original_hypotheses": hypotheses,
            "original_suggestions": suggestions,
            "explainability_context": explainability,
            "constraints": [
                "Do not change any numbers or scores",
                "Do not diagnose or claim medical conditions",
                "Keep output concise and executive",
                "Use cautious, non-absolute language",
                "Return JSON with keys: hypotheses, suggestions"
            ]
        }

        # Use Responses API (Manus-compatible OpenAI endpoint)
        resp = client.responses.create(
            model=settings.OPENAI_MODEL,
            instructions=SYSTEM_INSTRUCTIONS,
            input=[
                {"role": "user", "content": "Polish this narrative. Return ONLY JSON."},
                {"role": "user", "content": json.dumps(user_input)},
            ],
            text={"verbosity": "low"},
        )

        # Parse response
        out_text = getattr(resp, "output_text", None) or ""
        
        # Try to extract JSON from response
        polished = None
        if out_text.strip().startswith("{"):
            polished = json.loads(out_text)
        else:
            # Try to find JSON in markdown code blocks
            import re
            json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', out_text, re.DOTALL)
            if json_match:
                polished = json.loads(json_match.group(1))
        
        if not isinstance(polished, dict):
            logger.warning("LLM response not a dict, falling back")
            return original_payload
        
        # Validate and apply only allowed changes
        if isinstance(polished.get("hypotheses"), list):
            narrative["hypotheses"] = polished["hypotheses"]
            logger.info("Polished hypotheses applied")
        
        if isinstance(polished.get("suggestions"), list):
            narrative["suggestions"] = polished["suggestions"]
            logger.info("Polished suggestions applied")
        
        payload["narrative"] = narrative
        
        # Final validation: scores must be unchanged
        if not validate_scores_unchanged(original_payload, payload):
            logger.error("Scores changed during polish! Reverting to original")
            return original_payload
        
        return payload
        
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error in LLM polish: {e}")
        return original_payload
    except Exception as e:
        logger.error(f"LLM polish error: {e}")
        return original_payload
