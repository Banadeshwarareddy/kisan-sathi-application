import logging
import os

from groq import Groq

logger = logging.getLogger(__name__)

FARMING_SYSTEM_PROMPT = """You are Kisan Sathi AI (किसान साथी AI),
a dedicated smart farming assistant built exclusively for
Indian farmers. You are warm, helpful, and speak like a
trusted agricultural expert friend.

YOUR EXPERTISE AREAS:
- Crop diseases: identification, treatment, prevention
- Fertilizer management: NPK, urea, DAP, organic
- Soil health: pH, testing, improvement techniques
- Irrigation: drip, sprinkler, flood, water conservation
- Seasonal crops: Kharif, Rabi, Zaid calendar
- Pest and insect control: organic and chemical
- Seeds and varieties: hybrid, desi, recommended
- Weather impact on farming decisions
- Government schemes: PM-KISAN, Fasal Bima Yojana,
  Kisan Credit Card, MSP, eNAM, PMKSY
- Mandi prices and selling strategies
- Organic farming and natural pesticide preparation
- Animal husbandry: cow, buffalo, goat, poultry
- Water harvesting and conservation
- Post-harvest: storage, grading, value addition
- Modern techniques: greenhouse, hydroponics, SRI

LANGUAGE RULES:
- User writes in Hindi or Hinglish -> reply in Hindi
- User writes in English -> reply in English
- Mix Hindi + English naturally like farmers speak
- Use local crop names: gehun, dhan, makka, sarso,
  arhar, moong, urad, bajra, jowar, ganna, kapas
- Keep language simple, no complex technical terms

RESPONSE FORMAT:
- Answer in 150-250 words maximum
- Use bullet points with • symbol for lists
- Add helpful emojis: 🌱 🌾 💧 🌿 ☀️ 🐛 🧪 💊 🏛
- Bold important words using **word**
- End every response with one practical actionable tip
  starting with: 💡 Tip:
- For crop diseases always cover:
  1. Symptoms identification
  2. Cause (fungus/bacteria/virus/pest)
  3. Treatment with dosage
  4. Prevention for future

STRICT OFF-TOPIC RULE:
If the question is NOT related to farming, agriculture,
crops, soil, irrigation, weather (farming context),
rural livelihoods, or animal husbandry - respond with
EXACTLY this message, nothing else:

"🌾 मैं केवल खेती से जुड़े सवालों में मदद कर सकता हूँ।
I can only help with farming and agriculture questions.
Please ask me about crops, soil, pests, weather,
fertilizers, or government farming schemes!"

NEVER discuss: politics, movies, cricket scores,
relationships, coding, technology, finance (non-farming),
or any topic unrelated to agriculture.
Always stay in character as a farming expert."""

FALLBACK_RESPONSES = {
    ("tomato", "tamatar", "blight", "yellow leaf", "curl"): """🍅 Tomato Disease Guide:

- **Yellow spots** -> Early Blight (Alternaria fungus)
- **Brown patches + white ring** -> Late Blight
- **Curling leaves** -> Virus or mite attack

💊 Treatment:
- Spray Mancozeb 75WP @ 2g per liter water
- For late blight: Metalaxyl + Mancozeb 2.5g/L
- Remove and burn infected leaves immediately

🛡 Prevention:
- Maintain 45-60cm plant spacing
- Avoid overhead watering
- Rotate crops every 2 seasons

💡 Tip: Spray neem oil 5ml/L every
15 days as disease prevention.""",
    ("wheat", "gehun", "fertilizer", "urea", "dap"): """🌾 Wheat Fertilizer Schedule:

- **At sowing:** DAP 50kg + MOP 25kg per acre
- **21 days after:** Urea 30kg per acre
- **At jointing:** Urea 25kg per acre

📊 Total NPK needed: 120:60:40 kg/hectare

🌿 Organic alternative:
- FYM 10 tonnes/hectare before sowing
- Vermicompost 2-3 tonnes/hectare

💡 Tip: Split urea in 2 applications
increases wheat yield by 15-20%.""",
    ("pest", "keeda", "insect", "aphid", "whitefly"): """🐛 Pest Control Guide:

- Monitor crop every 3-4 days
- Act only when pest crosses Economic Threshold

🌿 Organic methods first:
- Neem oil 5ml + liquid soap 1ml per liter
- Yellow sticky traps for whitefly
- Pheromone traps for stem borer

💊 Chemical (only if needed):
- Aphids: Imidacloprid 0.5ml/L water
- Whitefly: Thiamethoxam 0.3g/L water
- Stem borer: Chlorpyrifos 2ml/L water

💡 Tip: Always spray in evening to
protect honeybees and reduce evaporation.""",
    ("soil", "mitti", "ph", "test"): """🌱 Soil Management Guide:

- Ideal pH for most crops: 6.0 to 7.5
- Get free soil test at nearest KVK center

📊 pH correction:
- Below 6 (acidic): Add agricultural lime
- Above 7.5 (alkaline): Add gypsum or sulfur

🌿 Improve soil health:
- Add FYM or compost every season
- Grow green manure crops (dhaincha, sunhemp)
- Never burn crop residue, mix it in soil

💡 Tip: Healthy soil has earthworms.
Add vermicompost to increase their count.""",
    ("scheme", "yojana", "pm kisan", "subsidy", "bima", "kcc"): """🏛 Government Farming Schemes:

💰 **PM-KISAN:**
- ₹6000/year in 3 installments of ₹2000
- Apply at: pmkisan.gov.in or CSC center

🛡 **Fasal Bima Yojana:**
- Crop insurance at 1.5-5% premium only
- Apply at your bank before sowing

💳 **Kisan Credit Card:**
- Crop loan up to ₹3 lakh at 7% interest
- Apply at any nationalized bank

📈 **eNAM:**
- Sell crop online at better prices
- Register at: enam.gov.in

💡 Tip: Keep Aadhaar + land papers
ready for all scheme applications.""",
}


def get_fallback_response(message: str) -> str:
    msg = message.lower()
    for keywords, response in FALLBACK_RESPONSES.items():
        if any(keyword in msg for keyword in keywords):
            return response

    return """🌾 Namaskar! I am Kisan Sathi AI.

I can help you with:
- 🌿 Crop diseases and organic treatment
- 🧪 Fertilizer and soil management
- 💧 Irrigation and water conservation
- 🐛 Pest and insect control
- 🌤 Weather impact on your crops
- 🏛 Government schemes and subsidies
- 📊 Mandi prices and selling tips

Please ask a specific farming question!
**Example:** "My tomato leaves are turning yellow"
or "How much urea should I use for wheat?" """


class GroqChatService:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY", "")
        self.model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
        self.conversation_history = {}

        if not api_key:
            logger.error("GROQ_API_KEY not found in .env file!")
            self.client = None
        else:
            self.client = Groq(api_key=api_key)
            logger.info("Groq client ready. Model: %s", self.model)

    def get_history(self, session_id: str) -> list:
        return self.conversation_history.get(session_id, [])[-10:]

    def save_to_history(self, session_id: str, role: str, content: str):
        if session_id not in self.conversation_history:
            self.conversation_history[session_id] = []
        self.conversation_history[session_id].append({"role": role, "content": content})
        if len(self.conversation_history[session_id]) > 20:
            self.conversation_history[session_id] = self.conversation_history[session_id][-20:]

    def _build_messages(self, message: str, session_id: str) -> list:
        messages = [{"role": "system", "content": FARMING_SYSTEM_PROMPT}]
        for msg in self.get_history(session_id):
            messages.append(msg)
        messages.append({"role": "user", "content": message})
        return messages

    def _call_groq(self, message: str, session_id: str) -> str:
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=self._build_messages(message, session_id),
            temperature=0.7,
            max_tokens=500,
            top_p=0.9,
            stream=False,
            stop=None,
        )
        return completion.choices[0].message.content

    def get_response(self, message: str, session_id: str) -> dict:
        source = "rule_based"
        if self.client:
            try:
                response_text = self._call_groq(message, session_id)
                source = f"groq ({self.model})"
                logger.info("Groq response OK - session: %s", session_id)
            except Exception as exc:
                error_msg = str(exc).lower()
                logger.error("Groq API error: %s", exc)
                if "rate_limit" in error_msg:
                    response_text = (
                        "🌾 बहुत सारे सवाल आ रहे हैं! Please wait 1 minute and try again.\n\n"
                        + get_fallback_response(message)
                    )
                else:
                    response_text = get_fallback_response(message)
        else:
            response_text = get_fallback_response(message)

        self.save_to_history(session_id, "user", message)
        self.save_to_history(session_id, "assistant", response_text)
        return {
            "success": True,
            "response": response_text,
            "session_id": session_id,
            "source": source,
        }

    def clear_session(self, session_id: str):
        if session_id in self.conversation_history:
            del self.conversation_history[session_id]
            logger.info("Cleared session: %s", session_id)


chatbot_service = GroqChatService()
