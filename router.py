# ============================================================
#  router.py  –  Core Logic with 8 Domains + Memory
# ============================================================

import json
import os
import re
import datetime
from openai import OpenAI
from dotenv import load_dotenv
from prompts import SYSTEM_PROMPTS, CLASSIFIER_PROMPT

# ── Load .env file ───────────────────────────────────────────
load_dotenv()

# ── Groq client (OpenAI compatible) ──────────────────────────
client = OpenAI(
    api_key=os.environ.get("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

CLASSIFIER_MODEL     = "llama-3.3-70b-versatile"
GENERATION_MODEL     = "llama-3.3-70b-versatile"
CONFIDENCE_THRESHOLD = 0.65
LOG_FILE             = "route_log.jsonl"


# ============================================================
#  1.  classify_intent
# ============================================================
def classify_intent(message: str, history: list = []) -> dict:
    fallback = {"intent": "unclear", "confidence": 0.0}

    if not message or not message.strip():
        return fallback

    # ── Build context from history ──
    context = ""
    if history:
        recent = history[-4:]
        context = "Recent conversation context:\n"
        for h in recent:
            role = "User" if h["role"] == "user" else "Assistant"
            context += f"{role}: {h['content'][:100]}\n"
        context += "\nUse this context to better understand the user's intent.\n\n"

    try:
        response = client.chat.completions.create(
            model=CLASSIFIER_MODEL,
            temperature=0.0,
            max_tokens=60,
            messages=[
                {"role": "system", "content": CLASSIFIER_PROMPT},
                {"role": "user",   "content": f"{context}User message: {message}"},
            ],
        )

        raw = response.choices[0].message.content.strip()
        raw = re.sub(r"^```[a-z]*\n?", "", raw)
        raw = re.sub(r"\n?```$", "", raw)
        raw = raw.strip()

        parsed = json.loads(raw)

        if "intent" not in parsed or "confidence" not in parsed:
            print(f"[WARN] Missing keys in classifier response: {raw}")
            return fallback

        valid_intents = set(SYSTEM_PROMPTS.keys())
        if parsed["intent"] not in valid_intents:
            print(f"[WARN] Unknown intent '{parsed['intent']}', defaulting to unclear.")
            parsed["intent"] = "unclear"

        if float(parsed["confidence"]) < CONFIDENCE_THRESHOLD:
            print(f"[INFO] Low confidence ({parsed['confidence']:.2f}), routing to unclear.")
            parsed["intent"] = "unclear"

        return {"intent": parsed["intent"], "confidence": float(parsed["confidence"])}

    except json.JSONDecodeError as e:
        print(f"[ERROR] JSON parse failed: {e}")
        return fallback
    except Exception as e:
        print(f"[ERROR] classify_intent failed: {e}")
        return fallback


# ============================================================
#  2.  route_and_respond
# ============================================================
def route_and_respond(message: str, intent: dict, history: list = []) -> str:
    label = intent.get("intent", "unclear")
    system_prompt = SYSTEM_PROMPTS.get(label, SYSTEM_PROMPTS["unclear"])

    messages = [{"role": "system", "content": system_prompt}]

    if history:
        for h in history[-6:]:
            messages.append({"role": h["role"], "content": h["content"]})

    messages.append({"role": "user", "content": message})

    try:
        response = client.chat.completions.create(
            model=GENERATION_MODEL,
            max_tokens=1000,
            messages=messages,
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"[ERROR] route_and_respond failed: {e}")
        return "I'm sorry, I encountered an error. Please try again."


# ============================================================
#  3.  log_route
# ============================================================
def log_route(user_message: str, intent: dict, final_response: str):
    entry = {
        "timestamp":      datetime.datetime.utcnow().isoformat() + "Z",
        "user_message":   user_message,
        "intent":         intent.get("intent"),
        "confidence":     intent.get("confidence"),
        "final_response": final_response,
    }
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")


# ============================================================
#  4.  handle_message
# ============================================================
def handle_message(message: str, history: list = []) -> dict:
    # ── Manual override: @code, @data, @writing, @career,
    #                     @general, @chat, @math, @health ──
    override_match = re.match(
        r"^@(code|data|writing|career|general|chat|math|health)\s+(.*)",
        message, re.DOTALL | re.IGNORECASE
    )
    if override_match:
        label   = override_match.group(1).lower()
        message = override_match.group(2).strip()
        intent  = {"intent": label, "confidence": 1.0}
        print(f"[OVERRIDE] Routing directly to '{label}'")
    else:
        intent = classify_intent(message, history)

    response = route_and_respond(message, intent, history)
    log_route(message, intent, response)

    return {
        "intent":     intent["intent"],
        "confidence": intent["confidence"],
        "response":   response,
    }