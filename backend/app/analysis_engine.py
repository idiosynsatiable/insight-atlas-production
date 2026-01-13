from __future__ import annotations
import re, math, statistics
from dataclasses import dataclass
from typing import Dict, Any, List, Tuple

# Deterministic, explainable, offline engine.
# Produces "style signals" and Big Five-ish proxy scores.
# Not diagnostic; outputs hypotheses + suggestions.

WORD_RE = re.compile(r"[A-Za-z']+")

def _words(text: str) -> List[str]:
    return WORD_RE.findall(text.lower())

def _sentences(text: str) -> List[str]:
    parts = re.split(r"[.!?]+", text)
    return [p.strip() for p in parts if p.strip()]

def _clamp(x: float, lo: float = 0.0, hi: float = 100.0) -> float:
    return max(lo, min(hi, x))

@dataclass
class Feature:
    name: str
    value: float
    note: str

def extract_features(free_text: str, survey: Dict[str, Any]) -> List[Feature]:
    w = _words(free_text)
    s = _sentences(free_text)
    n_words = len(w)
    n_sent = max(1, len(s))
    avg_sent_len = n_words / n_sent

    # simple lexicons (tiny but effective)
    intensifiers = set("very really absolutely totally insanely extremely super so".split())
    modal = set("maybe might could perhaps likely".split())
    certainty = set("always never must definitely certain".split())
    emotion = set("love hate fear hope excited anxious calm".split())
    technical = set("api cli github json yaml docker deploy auth stripe".split())
    creative = set("poetic metaphor vibe aesthetic dreamy mythic".split())

    intens_count = sum(1 for x in w if x in intensifiers)
    modal_count = sum(1 for x in w if x in modal)
    cert_count = sum(1 for x in w if x in certainty)
    emo_count = sum(1 for x in w if x in emotion)
    tech_count = sum(1 for x in w if x in technical)
    cre_count = sum(1 for x in w if x in creative)

    caps_ratio = (sum(1 for ch in free_text if ch.isupper()) / max(1, sum(1 for ch in free_text if ch.isalpha())))
    punct_density = (sum(1 for ch in free_text if ch in ",;:—-()<>" ) / max(1, len(free_text)))

    # Survey signals (expected keys; safe defaults)
    # Values should be 1-5 Likert in UI.
    novelty = float(survey.get("novelty_seeking", 3))
    structure = float(survey.get("structure_preference", 3))
    social = float(survey.get("social_energy", 3))
    sensitivity = float(survey.get("sensory_sensitivity", 3))
    focus = float(survey.get("hyperfocus", 3))

    feats = [
        Feature("word_count", float(n_words), "Total words in free-text." ),
        Feature("avg_sentence_len", float(avg_sent_len), "Average sentence length (words)." ),
        Feature("intensifier_rate", (intens_count / max(1, n_words))*100.0, "Percent of words that are intensifiers." ),
        Feature("modal_rate", (modal_count / max(1, n_words))*100.0, "Percent of words that express uncertainty." ),
        Feature("certainty_rate", (cert_count / max(1, n_words))*100.0, "Percent of words that express certainty/absolutes." ),
        Feature("emotion_rate", (emo_count / max(1, n_words))*100.0, "Percent of emotion-laden words." ),
        Feature("technical_rate", (tech_count / max(1, n_words))*100.0, "Percent of technical lexicon words." ),
        Feature("creative_rate", (cre_count / max(1, n_words))*100.0, "Percent of creative/aesthetic lexicon words." ),
        Feature("caps_ratio", caps_ratio*100.0, "Uppercase letters as % of alphabetic characters." ),
        Feature("punct_density", punct_density*100.0, "Punctuation density proxy." ),
        Feature("survey_novelty", novelty, "Self-reported novelty seeking (1-5)." ),
        Feature("survey_structure", structure, "Self-reported preference for structure (1-5)." ),
        Feature("survey_social", social, "Self-reported social energy (1-5)." ),
        Feature("survey_sensitivity", sensitivity, "Self-reported sensory sensitivity (1-5)." ),
        Feature("survey_focus", focus, "Self-reported hyperfocus tendency (1-5)." ),
    ]
    return feats

def score_traits(features: List[Feature]) -> Dict[str, Any]:
    # Map features -> trait proxies (0-100)
    f = {x.name: x.value for x in features}

    # Proxy computations (deterministic)
    openness = _clamp(40 + 6*f.get("creative_rate",0) + 8*(f.get("survey_novelty",3)-3) + 0.2*f.get("avg_sentence_len",0))
    conscientious = _clamp(45 + 10*(f.get("survey_structure",3)-3) + 2*(1.5 - f.get("punct_density",0)/10))
    extraversion = _clamp(40 + 10*(f.get("survey_social",3)-3) + 2*f.get("caps_ratio",0)/10)
    agreeableness = _clamp(50 + 3*(f.get("modal_rate",0)) - 2*(f.get("certainty_rate",0)) )
    neuroticism = _clamp(45 + 8*(f.get("survey_sensitivity",3)-3) + 2*f.get("emotion_rate",0))

    intensity = _clamp(30 + 12*f.get("intensifier_rate",0) + 4*f.get("caps_ratio",0)/10 + 8*(f.get("survey_focus",3)-3))
    systems_thinking = _clamp(35 + 10*f.get("technical_rate",0) + 4*(f.get("avg_sentence_len",0)))
    ambiguity_tolerance = _clamp(50 + 4*f.get("modal_rate",0) - 4*f.get("certainty_rate",0))

    return {
        "big_five": {
            "openness": round(openness,1),
            "conscientiousness": round(conscientious,1),
            "extraversion": round(extraversion,1),
            "agreeableness": round(agreeableness,1),
            "neuroticism": round(neuroticism,1),
        },
        "style_signals": {
            "intensity": round(intensity,1),
            "systems_thinking": round(systems_thinking,1),
            "ambiguity_tolerance": round(ambiguity_tolerance,1),
        }
    }

def generate_narrative(scores: Dict[str, Any], features: List[Feature]) -> Dict[str, Any]:
    bf = scores["big_five"]
    ss = scores["style_signals"]

    # Hypothesis statements (non-diagnostic, cautious)
    bullets = []
    if bf["openness"] >= 65:
        bullets.append("High novelty/idea-connection tendency; you likely enjoy remixing concepts across domains.")
    if ss["systems_thinking"] >= 65:
        bullets.append("Strong systems orientation; you may prefer end-to-end plans and dislike vague placeholders.")
    if ss["intensity"] >= 65:
        bullets.append("High intensity signal; your engagement often runs 'all in' when something matters.")
    if bf["conscientiousness"] >= 65:
        bullets.append("Preference for structure and execution; checklists and automation may feel soothing.")
    if bf["neuroticism"] >= 65:
        bullets.append("Higher sensitivity signal; sensory overload or stress spikes may be more likely under chaos.")
    if not bullets:
        bullets.append("Mixed/balanced profile; you may flex styles depending on context.")

    # Suggestions
    suggestions = [
        "Use a two-pass workflow: (1) wild ideation, (2) ruthless reduction into a minimal shippable unit.",
        "If you feel overwhelmed, reduce inputs: dim light, fewer tabs, single-task timers, simple ambient audio.",
        "When communicating, state: goal → constraints → definition of done. It lowers friction dramatically.",
    ]
    if ss["ambiguity_tolerance"] < 45:
        suggestions.append("Ambiguity may feel costly—ask for concrete examples, timelines, and acceptance criteria.")
    if bf["agreeableness"] < 45:
        suggestions.append("Directness can be a superpower; add a 1-line 'warm wrapper' to reduce misreads.")
    if bf["extraversion"] > 60:
        suggestions.append("You may ideate best out loud—voice notes or co-working can amplify output.")

    explain = []
    for ft in features:
        if ft.name in ("intensifier_rate","technical_rate","creative_rate","survey_focus","survey_structure","survey_novelty"):
            explain.append({
                "feature": ft.name,
                "value": round(ft.value,2),
                "note": ft.note
            })

    return {
        "hypotheses": bullets,
        "suggestions": suggestions,
        "explainability": explain,
        "disclaimer": "This report is a self-reflection aid, not a diagnosis. If you suspect a clinical condition, consult a qualified professional."
    }

def analyze(free_text: str, survey: Dict[str, Any]) -> Dict[str, Any]:
    feats = extract_features(free_text, survey)
    scores = score_traits(feats)
    narrative = generate_narrative(scores, feats)
    return {
        "scores": scores,
        "narrative": narrative
    }
