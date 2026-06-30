import os
import time
import logging
import re
from groq import Groq
from django.conf import settings

logger = logging.getLogger(__name__)

# ─── MASTER SYSTEM PROMPT ──────────────────────────────────────
KISAN_SYSTEM_PROMPT = """You are KISAN AI (किसान AI), the most intelligent and helpful agricultural assistant for Indian farmers. You are built into the "Kisan Sathi" Smart Farming Platform.

YOUR IDENTITY:
- Name: Kisan AI / किसान AI
- Role: Expert Agricultural Advisor for Indian farmers
- Personality: Warm, knowledgeable, practical, encouraging
- Speaking style: Simple, clear, farmer-friendly language

YOUR COMPLETE EXPERTISE:
1. CROP MANAGEMENT:
- All major Indian crops: wheat, rice, maize, cotton, sugarcane, mustard, soybean, pulses, vegetables, fruits
- Kharif, Rabi, Zaid seasonal planning
- Seed selection and sowing techniques
- Crop rotation and intercropping
- Yield improvement strategies

2. DISEASE & PEST CONTROL:
- Identify diseases from symptoms described
- Organic and chemical treatment options
- Preventive measures and IPM techniques
- Fungicides, pesticides with correct dosage
- Bio-pesticides and natural remedies

3. SOIL & FERTILIZER:
- Soil testing interpretation
- NPK recommendations per crop
- Micronutrient deficiency diagnosis
- Organic manure preparation
- Soil pH management
- Vermicompost and green manure

4. IRRIGATION:
- Crop-wise water requirements
- Drip and sprinkler guidance
- Critical irrigation stages
- Water conservation techniques
- Rainwater harvesting

5. WEATHER & CLIMATE:
- Weather impact on crop decisions
- Monsoon farming calendar
- Climate-smart agriculture
- Frost, drought, flood management

6. GOVERNMENT SCHEMES:
- PM-KISAN (₹6000/year)
- Fasal Bima Yojana (crop insurance)
- Kisan Credit Card (KCC)
- eNAM (electronic mandi)
- PMKSY (irrigation subsidy)
- Soil Health Card scheme
- PM Kisan Mandhan Yojana
- State-specific schemes

7. MARKET & MANDI:
- MSP (Minimum Support Price) guidance
- Selling strategies
- Post-harvest management
- Value addition
- agmarknet.gov.in guidance
- Farmer Producer Organizations

8. ORGANIC FARMING:
- Transition to organic
- Certification process
- Organic pest control
- Composting methods
- Natural farming techniques

9. ANIMAL HUSBANDRY:
- Dairy cow management
- Poultry basics
- Goat farming
- Animal health and nutrition

LANGUAGE_RULES:
- If user writes in Hindi (Devanagari script) → respond FULLY in Hindi
- If user writes in Kannada script → respond FULLY in Kannada
- If user writes in English (Latin script) → respond FULLY in English
- If user mixes Hindi + English → respond in Hinglish
- Use local crop names when appropriate: wheat/gehun, rice/dhan, maize/makka
- Keep responses in the SAME language as the user's question

RESPONSE FORMAT:
- Keep answers 150-300 words (not too long)
- Use bullet points • for lists
- Add emojis for visual clarity: 🌱🌾💧🌿☀️🐛💊🏛📊
- Bold **important terms**
- End with one practical 💡 Tip
- For diseases: Symptoms → Cause → Treatment → Prevention

STRICT RULES:
- ONLY answer farming/agriculture/rural livelihood questions
- If asked anything non-farming, politely redirect:
  "🌾 I'm specialized in farming only! Ask me about crops, soil, weather, pests, or farming schemes."
- Never make up statistics or government scheme amounts
- Always recommend consulting local KVK for serious issues
- KVK helpline: 1800-180-1551

TONE: Be like a knowledgeable elder farmer who is also scientifically educated — practical wisdom + modern science."""

# Language-specific system prompt additions
LANGUAGE_ADDITIONS = {
    'hi': """

CRITICAL: The farmer has selected HINDI language preference.
Respond ENTIRELY in Hindi (Devanagari script).
Use simple Hindi words that rural farmers understand.
Do NOT use English unless the user specifically asks in English.""",
    'kn': """

CRITICAL: The farmer has selected KANNADA language preference.
Respond ENTIRELY in Kannada script.
Use simple Kannada words that Karnataka farmers understand.
Do NOT use English unless the user specifically asks in English.""",
    'en': """

CRITICAL: The farmer has selected ENGLISH language preference.
Respond ENTIRELY in English.
Use simple English that farmers can understand.
Do NOT use Hindi or Kannada unless the user specifically asks in those languages."""
}

# ─── FARMING KEYWORDS for category detection ─────────────────
CATEGORY_KEYWORDS = {
    'crop': ['crop', 'seed', 'sow', 'plant', 'harvest', 'yield',
             'variety', 'hybrid', 'fasal', 'beej', 'ugana', 'fsal',
             'wheat', 'rice', 'maize', 'cotton', 'sugarcane',
             'gehun', 'dhan', 'makka', 'kapas', 'ganna'],
    'disease': ['disease', 'pest', 'insect', 'fungus', 'virus',
                'blight', 'rot', 'wilt', 'rust', 'spot',
                'rog', 'keeda', 'makdi', 'tele', 'dawai'],
    'weather': ['weather', 'rain', 'monsoon', 'drought', 'flood',
                'temperature', 'frost', 'mausam', 'baarish', 'sukha'],
    'soil': ['soil', 'mitti', 'ph', 'test', 'sandy', 'clay',
             'loam', 'organic', 'earthworm', 'bhumi'],
    'fertilizer': ['fertilizer', 'NPK', 'urea', 'DAP', 'potash',
                   'nitrogen', 'phosphorus', 'khaad', 'uriya'],
    'irrigation': ['water', 'irrigation', 'drip', 'sprinkler',
                   'sinchai', 'pani', 'bore', 'canal', 'pump'],
    'scheme': ['scheme', 'yojana', 'pm-kisan', 'insurance', 'bima',
               'subsidy', 'loan', 'kcc', 'government', 'sarkar'],
    'market': ['price', 'mandi', 'sell', 'market', 'MSP', 'rate',
               'bhav', 'bikri', 'enam', 'trader', 'buyer'],
    'organic': ['organic', 'natural', 'compost', 'vermicompost',
                'neem', 'bio', 'jeevamrit', 'khad', 'gobar'],
}


def detect_category(message: str) -> str:
    msg_lower = message.lower()
    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(kw in msg_lower for kw in keywords):
            return category
    return 'general'


def detect_weather_query(message: str) -> dict:
    """
    Detect if user is asking about weather and extract location
    Returns: {'is_weather': bool, 'location': str or None}
    """
    msg_lower = message.lower()
    
    # Weather keywords
    weather_keywords = ['weather', 'temperature', 'rain', 'forecast', 
                       'mausam', 'baarish', 'garmi', 'sardi', 'climate',
                       'hot', 'cold', 'sunny', 'cloudy', 'humidity']
    
    # Check if it's a weather query
    is_weather = any(keyword in msg_lower for keyword in weather_keywords)
    
    if not is_weather:
        return {'is_weather': False, 'location': None}
    
    # Try to extract location
    # Common patterns: "weather in Delhi", "Delhi weather", "weather of Mumbai"
    location_patterns = [
        r'weather (?:in|of|at|for) ([a-zA-Z\s]+)',
        r'([a-zA-Z\s]+) (?:weather|mausam)',
        r'(?:in|at) ([a-zA-Z\s]+)',
    ]
    
    location = None
    for pattern in location_patterns:
        match = re.search(pattern, msg_lower)
        if match:
            location = match.group(1).strip()
            # Clean up common words
            location = re.sub(r'\b(the|today|tomorrow|current|now)\b', '', location).strip()
            if len(location) > 2:
                break
    
    return {'is_weather': is_weather, 'location': location}


def get_weather_data(location: str = None) -> str:
    """
    Fetch real weather data from the weather service
    Returns formatted weather information
    """
    try:
        from weather.services import WeatherService
        weather_service = WeatherService()
        
        # Default to user's location or a fallback city
        if not location:
            location = "Indore,IN"
        elif ',' not in location:
            # Add India country code if not specified
            location = f"{location},IN"
        
        logger.info(f"Fetching weather data for: {location}")
        
        # Get current weather
        weather = weather_service.get_current_weather(city=location)
        
        if not weather:
            logger.error("Weather service returned no data")
            return None
        
        # Check if it's demo data
        is_demo = weather.get('demo', False)
        demo_note = "\n\n⚠️ **Note:** This is simulated weather data. API key may not be working." if is_demo else ""
        
        # Format weather data for AI
        weather_info = f"""
**Current Weather in {weather['city']}, {weather['country']}:**
- 🌡️ Temperature: {weather['temperature']}°C (Feels like {weather['feels_like']}°C)
- 🌤️ Condition: {weather['description']}
- 💧 Humidity: {weather['humidity']}%
- 💨 Wind Speed: {weather['wind_speed']} km/h
- ☁️ Cloud Cover: {weather['clouds']}%
- 👁️ Visibility: {weather['visibility']} km
- 🌅 Sunrise: {weather['sunrise']} | 🌇 Sunset: {weather['sunset']}
- 📊 Pressure: {weather['pressure']} hPa

**Temperature Range Today:**
Min: {weather['temp_min']}°C | Max: {weather['temp_max']}°C{demo_note}
"""
        
        logger.info(f"Successfully formatted weather data for {weather['city']}")
        return weather_info.strip()
        
    except ImportError as e:
        logger.error(f"Weather service import error: {e}")
        return None
    except Exception as e:
        logger.error(f"Error fetching weather: {e}")
        return None


# ─── RULE-BASED FALLBACK ──────────────────────────────────────
FALLBACK_RESPONSES = {
    'crop': {
        'en': """🌾 **Crop Advisory**

- **Kharif Season (June-Nov):** Rice, Maize, Cotton, Soybean, Groundnut
- **Rabi Season (Nov-Apr):** Wheat, Mustard, Chickpea, Peas
- **Zaid Season (Apr-Jun):** Cucumber, Watermelon, Moong Dal

**For best results:**
- Choose variety suited to your soil type
- Get soil test done before sowing
- Use certified seeds from government store

🏛 Free soil testing at Krishi Vigyan Kendra

💡 Tip: Rotate crops every season to maintain soil health.""",
        'hi': """🌾 **फसल सलाह**

- **खरीफ (जून-नवंबर):** धान, मक्का, कपास, सोयाबीन, मूंगफली
- **रबी (नवंबर-अप्रैल):** गेहूं, सरसों, चना, मटर
- **जायद (अप्रैल-जून):** खीरा, तरबूज, मूंग दाल

**अच्छी फसल के लिए:**
- अपनी मिट्टी के अनुसार किस्म चुनें
- बुवाई से पहले मिट्टी की जांच कराएं

💡 सुझाव: हर सीजन में फसल बदलें - मिट्टी की सेहत बनी रहेगी।"""
    },
    'scheme': {
        'en': """🏛 **Government Farming Schemes**

💰 **PM-KISAN:** ₹6,000/year in 3 installments
→ Apply: pmkisan.gov.in

🛡 **Fasal Bima Yojana:** Crop insurance at 1.5-2% premium
→ Apply at bank before sowing

💳 **Kisan Credit Card:** Loan up to ₹3 lakh at 7% interest

📱 **eNAM:** Online mandi - better price for crops
→ Register: enam.gov.in

🌊 **PMKSY:** 55-75% subsidy on drip/sprinkler

💡 Tip: Keep Aadhaar + land documents ready for all schemes.

📞 Kisan Helpline: 1800-180-1551 (Free)""",
        'hi': """🏛 **सरकारी कृषि योजनाएं**

💰 **पीएम-किसान:** ₹6,000/साल, 3 किस्तों में
→ आवेदन: pmkisan.gov.in

🛡 **फसल बीमा योजना:** 1.5-2% प्रीमियम पर फसल बीमा
→ बुवाई से पहले बैंक में आवेदन करें

💳 **किसान क्रेडिट कार्ड:** 7% ब्याज पर ₹3 लाख तक ऋण

💡 सुझाव: सभी योजनाओं के लिए आधार + जमीन के कागज रखें।

📞 किसान हेल्पलाइन: 1800-180-1551 (मुफ्त)"""
    },
    'disease': {
        'en': """🐛 **Pest & Disease Control**

**Identify the problem:**
- Yellow leaves → Nitrogen deficiency or fungal
- Brown spots → Blight or bacterial disease
- Wilting → Root rot or stem borer
- Curling leaves → Virus or mites

**Organic solutions first:**
- Neem oil spray: 5ml + soap 1ml per liter
- Yellow sticky traps for whitefly
- Trichoderma for soil diseases

**Chemical (only if needed):**
- Fungicide: Mancozeb 75WP @ 2g/liter
- Insecticide: Imidacloprid 0.5ml/liter
- Always wear mask + gloves

💡 Tip: Spray in early morning or evening only.""",
        'hi': """🐛 **कीट और रोग नियंत्रण**

**समस्या पहचानें:**
- पीली पत्तियां → नाइट्रोजन की कमी या फंगल
- भूरे धब्बे → झुलसा रोग
- पौधा मुरझाना → जड़ सड़न

**जैविक उपाय पहले:**
- नीम तेल: 5ml + साबुन 1ml प्रति लीटर
- येलो स्टिकी ट्रैप व्हाइटफ्लाई के लिए

**रासायनिक (जरूरत पड़ने पर):**
- फफूंदनाशक: मैंकोजेब 75WP @ 2g/लीटर

💡 सुझाव: सुबह या शाम को ही स्प्रे करें।"""
    },
}


def get_fallback_response(category: str, language: str) -> str:
    lang = language if language in ['en', 'hi'] else 'en'
    if category in FALLBACK_RESPONSES:
        return FALLBACK_RESPONSES[category].get(lang, FALLBACK_RESPONSES[category].get('en', ''))
    
    return ("🌾 I'm your Kisan AI assistant! Ask me about:\n"
            "• Crop suggestions\n• Disease treatment\n"
            "• Fertilizer advice\n• Government schemes\n"
            "• Market prices\n• Irrigation tips")


# ─── MAIN AI SERVICE CLASS ────────────────────────────────────
class KisanAIService:
    def __init__(self):
        api_key = getattr(settings, 'GROQ_API_KEY', '') or os.getenv('GROQ_API_KEY', '')
        self.model = getattr(settings, 'GROQ_MODEL', 'llama-3.3-70b-versatile')
        self.client = Groq(api_key=api_key) if api_key else None
        self.is_ready = bool(api_key)
        
        if self.is_ready:
            logger.info(f"✅ Kisan AI ready: {self.model}")
        else:
            logger.warning("⚠️ GROQ_API_KEY missing - fallback mode")

    def build_messages(self,
                      user_message: str,
                      history: list,
                      language: str = 'en') -> list:
        """Build message list with system prompt + history"""
        system_content = (KISAN_SYSTEM_PROMPT 
                         + LANGUAGE_ADDITIONS.get(language, ''))
        
        messages = [{'role': 'system', 'content': system_content}]
        
        # Add conversation history (last 8 turns)
        for msg in history[-8:]:
            if msg['role'] in ['user', 'assistant']:
                messages.append({
                    'role': msg['role'],
                    'content': msg['content']
                })
        
        # Add current message
        messages.append({
            'role': 'user',
            'content': user_message
        })
        
        return messages

    def get_response(self,
                    message: str,
                    session_id: str,
                    history: list = None,
                    language: str = 'en') -> dict:
        """Get AI response with timing and fallback
        
        Returns: {response, category, tokens, time, source}
        """
        start_time = time.time()
        history = history or []
        category = detect_category(message)
        
        # Check if user is asking about weather
        weather_query = detect_weather_query(message)
        weather_data = None
        
        if weather_query['is_weather']:
            logger.info(f"Weather query detected for location: {weather_query['location']}")
            weather_data = get_weather_data(weather_query['location'])
            if weather_data:
                category = 'weather'
                logger.info("Real weather data fetched successfully")
        
        # Try Groq AI
        if self.client:
            try:
                messages = self.build_messages(message, history, language)
                
                # If we have weather data, add it to the context
                if weather_data:
                    weather_context = f"\n\n**REAL-TIME WEATHER DATA:**\n{weather_data}\n\nUse this EXACT real-time data to answer the user's weather question. Do not make up weather information."
                    messages[-1]['content'] = messages[-1]['content'] + weather_context
                
                completion = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=0.7,
                    max_tokens=600,
                    top_p=0.9,
                    stream=False,
                )
                
                response_text = (completion.choices[0].message.content)
                tokens = (completion.usage.total_tokens 
                         if completion.usage else 0)
                elapsed = round(time.time() - start_time, 2)
                
                logger.info(f"✅ AI response in {elapsed}s | "
                          f"tokens: {tokens} | category: {category}")
                
                return {
                    'response': response_text,
                    'category': category,
                    'tokens': tokens,
                    'time': elapsed,
                    'source': 'groq_with_weather' if weather_data else 'groq',
                    'confidence': 0.95 if weather_data else 0.92,
                    'success': True
                }
                
            except Exception as e:
                error_str = str(e).lower()
                logger.error(f"Groq error: {e}")
                
                # Rate limit handling
                if 'rate_limit' in error_str:
                    wait_msg = ("🌾 बहुत सारे सवाल आ रहे हैं! "
                              "Please wait 1 minute and try again."
                              if language == 'hi' else
                              "🌾 Too many requests. Please wait 1 minute.")
                    return {
                        'response': wait_msg,
                        'category': category,
                        'tokens': 0,
                        'time': 0,
                        'source': 'rate_limit',
                        'confidence': 0,
                        'success': False
                    }
        
        # Fallback: If we have weather data but AI failed, format it nicely
        if weather_data:
            response_text = f"🌤️ **Weather Update**\n\n{weather_data}\n\n💡 Tip: Based on current conditions, plan your farming activities accordingly!"
            elapsed = round(time.time() - start_time, 2)
            return {
                'response': response_text,
                'category': 'weather',
                'tokens': 0,
                'time': elapsed,
                'source': 'weather_direct',
                'confidence': 0.95,
                'success': True
            }
        
        # Fallback to rule-based
        fallback = get_fallback_response(category, language)
        elapsed = round(time.time() - start_time, 2)
        
        return {
            'response': fallback,
            'category': category,
            'tokens': 0,
            'time': elapsed,
            'source': 'fallback',
            'confidence': 0.7,
            'success': True
        }


# Singleton
kisan_ai = KisanAIService()
