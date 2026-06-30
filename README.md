# 🌾 Kisan Sathi - Smart Farming Application

## Complete Project Documentation for Interview Presentation

---

## 📋 Table of Contents
1. [Project Overview](#project-overview)
2. [Problem Statement](#problem-statement)
3. [Solution Architecture](#solution-architecture)
4. [Technology Stack](#technology-stack)
5. [Core Features](#core-features)
6. [AI/ML Implementation](#aiml-implementation)
7. [System Architecture](#system-architecture)
8. [Database Design](#database-design)
9. [API Documentation](#api-documentation)
10. [Security Implementation](#security-implementation)
11. [How It Works](#how-it-works)
12. [Installation & Setup](#installation--setup)
13. [Deployment](#deployment)
14. [Challenges & Solutions](#challenges--solutions)
15. [Future Enhancements](#future-enhancements)

---

## 🎯 Project Overview

**Kisan Sathi** is a comprehensive AI-powered smart farming web application designed to help farmers make data-driven decisions for crop health management, financial tracking, and agricultural planning.

### Project Type
Full-stack web application with AI/ML integration

### Duration
[Your timeline here]

### Team Size
[Individual/Team]

### My Role
Full-stack developer responsible for:
- Backend development (Django REST Framework)
- Frontend implementation (HTML, CSS, JavaScript, Alpine.js)
- AI model training and integration (TensorFlow)
- Database design and optimization
- Deployment and DevOps

---

## 🔍 Problem Statement

### The Challenge
Indian farmers face multiple challenges:
1. **Crop Disease Detection** - Unable to identify crop diseases early, leading to yield loss
2. **Weather Uncertainty** - Lack of accurate, localized weather information
3. **Financial Management** - Poor tracking of farm expenses, income, and loans
4. **Limited Expert Access** - Rural areas lack agricultural experts for advice
5. **Data-Driven Decisions** - Farmers rely on traditional methods without data insights

### Our Solution
An integrated platform that provides:
- AI-powered crop disease detection (38 disease classes, 14 crop types)
- Real-time weather monitoring and forecasts
- Farm financial management system
- AI chatbot for 24/7 agricultural guidance
- Comprehensive dashboard for farm analytics

---

## 🏗️ Solution Architecture

### High-Level Architecture
```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend Layer (Browser)                  │
│  HTML5 • TailwindCSS • Alpine.js • JavaScript               │
└───────────────────────┬─────────────────────────────────────┘
                        │ HTTPS/REST API
┌───────────────────────▼─────────────────────────────────────┐
│                  Application Layer (Django)                  │
│  ┌────────────┬────────────┬────────────┬─────────────┐    │
│  │  Accounts  │  Dashboard │   Weather  │   Chatbot   │    │
│  └────────────┴────────────┴────────────┴─────────────┘    │
│  ┌────────────────────┬──────────────────────────────┐     │
│  │  Crop Detector     │   Farm Management            │     │
│  └────────────────────┴──────────────────────────────┘     │
└───────────────────────┬─────────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────────┐
│                    Service Layer                             │
│  ┌──────────────┬────────────────┬───────────────────┐     │
│  │  AI Model    │  Weather API   │   Groq API        │     │
│  │ (TensorFlow) │(OpenWeatherMap)│  (LLM Chatbot)    │     │
│  └──────────────┴────────────────┴───────────────────┘     │
└───────────────────────┬─────────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────────┐
│                    Data Layer                                │
│          SQLite/PostgreSQL • Static Files                   │
└─────────────────────────────────────────────────────────────┘
```

---

## 💻 Technology Stack

### Backend
- **Framework**: Django 4.2.7
- **API**: Django REST Framework 3.14.0
- **Authentication**: JWT (djangorestframework-simplejwt)
- **WSGI Server**: Gunicorn 21.2.0
- **Task Queue**: Celery 5.3.4 (for async tasks)
- **Caching**: Redis 5.0.1

### Frontend
- **HTML5** with semantic markup
- **CSS**: TailwindCSS 3.x (utility-first framework)
- **JavaScript**: Vanilla JS + Alpine.js 3.x (reactive framework)
- **Icons**: Google Material Symbols

### AI/Machine Learning
- **Deep Learning**: TensorFlow 2.14.0
- **Computer Vision**: OpenCV 4.8.1.78
- **Model Architecture**: MobileNetV2 (Transfer Learning)
- **Dataset**: PlantVillage Dataset (87,000+ images)
- **Image Processing**: PIL (Pillow 10.1.0)
- **Numerical Computing**: NumPy 1.26.2

### External APIs
- **Weather Data**: OpenWeatherMap API
- **AI Chatbot**: Groq API (Llama 3.3 70B)
- **Geolocation**: Leaflet.js with OpenStreetMap

### Database
- **Development**: SQLite3
- **Production**: PostgreSQL (recommended)
- **ORM**: Django ORM

### DevOps & Deployment
- **Static Files**: WhiteNoise 6.6.0
- **CORS**: django-cors-headers 4.3.1
- **Environment**: python-dotenv, django-environ
- **PDF Generation**: ReportLab 4.0.0
- **Excel Export**: OpenPyXL 3.1.0

### Security
- **HTTPS/SSL**: Enforced in production
- **CSRF Protection**: Django CSRF middleware
- **XSS Protection**: Django's built-in security
- **Password Hashing**: PBKDF2 algorithm
- **Session Management**: Django sessions with secure cookies

---

## ✨ Core Features

### 1. User Authentication System
**What it does:**
- User registration with email verification
- Secure login/logout with JWT tokens
- Password reset functionality
- Role-based access control

**Technologies Used:**
- Django authentication system
- JWT for token-based auth
- PBKDF2 password hashing

**How it works:**
```python
# User registers → Email validation → Password hashing →
# Store in database → Generate JWT token → Return to client
```

### 2. AI Crop Disease Detector 🔬

**What it does:**
- Detects 38 different crop diseases across 14 crop types
- Provides disease diagnosis with confidence scores
- Offers treatment recommendations
- Suggests fertilizer programs
- Prevention strategies

**Supported Crops:**
- Apple, Blueberry, Cherry, Corn (Maize), Grape
- Orange, Peach, Bell Pepper, Potato, Raspberry
- Soybean, Squash, Strawberry, Tomato

**Technologies Used:**
- TensorFlow 2.14 for deep learning
- MobileNetV2 (pre-trained on ImageNet)
- Transfer learning technique
- Image preprocessing with OpenCV & PIL

**Model Architecture:**
```
Input Image (224x224x3)
↓
MobileNetV2 Base (frozen layers)
↓
Global Average Pooling
↓
Dense Layer (256 units, ReLU)
↓
Dropout (0.3)
↓
Output Layer (38 classes, Softmax)
```

**Training Details:**
- Dataset: 87,000+ images from PlantVillage
- Epochs: 25-30 epochs
- Batch Size: 32
- Optimizer: Adam
- Loss Function: Categorical Crossentropy
- Data Augmentation: Rotation, flip, zoom, shift
- Validation Split: 80-20

**How it works:**
1. User uploads crop leaf image
2. Image preprocessed (resize to 224x224, normalize)
3. Center crop to remove background noise
4. Feed to trained CNN model
5. Model predicts disease class
6. Return confidence score + recommendations
7. Generate PDF report

**Code Flow:**
```python
# crop_detector/ai_model.py
Image Upload → Preprocessing → Model Prediction → 
Disease Matching → Recommendation Lookup → Response
```

### 3. Weather Monitoring System 🌦️

**What it does:**
- Real-time weather data for farmer's location
- 5-day weather forecast
- Temperature, humidity, wind speed, rainfall
- Interactive map with location selection
- Weather alerts and warnings

**Technologies Used:**
- OpenWeatherMap API
- Leaflet.js for interactive maps
- Geolocation API
- AJAX for async data fetching

**How it works:**
```javascript
// 1. Get user location (GPS or manual selection)
navigator.geolocation.getCurrentPosition()
↓
// 2. Fetch weather data from API
fetch(`/weather/api/current/?lat=${lat}&lon=${lon}`)
↓
// 3. Display current weather
// 4. Fetch 5-day forecast
// 5. Update UI dynamically
```

**API Integration:**
```python
# weather/services.py
def get_current_weather(lat, lon):
    api_key = settings.OPENWEATHERMAP_API_KEY
    url = f"https://api.openweathermap.org/data/2.5/weather"
    params = {'lat': lat, 'lon': lon, 'appid': api_key}
    response = requests.get(url, params=params)
    return response.json()
```

### 4. AI Chatbot Assistant 🤖

**What it does:**
- 24/7 agricultural guidance
- Answers farming queries in natural language
- Provides crop recommendations
- Pest management advice
- Fertilizer suggestions

**Technologies Used:**
- Groq API (Llama 3.3 70B model)
- REST API integration
- Session management
- Message history tracking

**How it works:**
```
User Question → Django Backend → Groq API (LLM) →
AI Response → Store in Database → Return to User
```

**Key Features:**
- Context-aware conversations
- Session persistence
- Message history
- Real-time streaming responses
- Automatic categorization

**Implementation:**
```python
# chatbot/ai_service.py
def get_ai_response(message, session_id):
    # Initialize Groq client
    client = Groq(api_key=settings.GROQ_API_KEY)
    
    # Send message to LLM
    response = client.chat.completions.create(
        model=settings.GROQ_MODEL,
        messages=[
            {"role": "system", "content": "Agricultural expert..."},
            {"role": "user", "content": message}
        ]
    )
    return response.choices[0].message.content
```

### 5. Farm Management System 💰

**What it does:**
- Track farm expenses (seeds, fertilizers, labor)
- Record income from crop sales
- Monitor livestock inventory
- Manage loans and debts
- Generate financial reports
- Analytics dashboard with charts

**Technologies Used:**
- Django REST API
- Chart.js for data visualization
- ReportLab for PDF reports
- OpenPyXL for Excel exports

**Database Models:**
```python
# farm_management/models.py
- Crop Model (name, area, planting_date, harvest_date)
- Expense Model (category, amount, date, description)
- Income Model (source, amount, date)
- Livestock Model (type, quantity, value)
- Loan Model (amount, interest_rate, due_date)
```

**How it works:**
```
User Input → Validate Data → Save to Database →
Update Dashboard Stats → Generate Charts → Show Analytics
```

**Key Metrics Tracked:**
- Total farm area
- Active crops
- Total expenses (monthly/yearly)
- Total income
- Net profit/loss
- Outstanding loans
- Livestock value

### 6. Dashboard & Analytics 📊

**What it does:**
- Centralized view of all farm activities
- Quick access to all features
- Recent activity feed
- Financial summary
- Weather widget
- Disease detection stats

**Technologies Used:**
- Django templates
- Alpine.js for reactivity
- Chart.js for visualizations
- REST API for data fetching

---

## 🧠 AI/ML Implementation Details

### Model Training Process

**Step 1: Data Preparation**
```python
# train_model.py
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Data augmentation for training
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    validation_split=0.2
)

train_generator = train_datagen.flow_from_directory(
    DATASET_PATH,
    target_size=(224, 224),
    batch_size=32,
    class_mode='categorical',
    subset='training'
)
```

**Step 2: Model Architecture**
```python
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, Dropout, GlobalAveragePooling2D

# Load pre-trained MobileNetV2
base_model = MobileNetV2(
    weights='imagenet',
    include_top=False,
    input_shape=(224, 224, 3)
)

# Freeze base model layers
base_model.trainable = False

# Add custom classification head
x = GlobalAveragePooling2D()(base_model.output)
x = Dense(256, activation='relu')(x)
x = Dropout(0.3)(x)
predictions = Dense(38, activation='softmax')(x)

model = Model(inputs=base_model.input, outputs=predictions)
```

**Step 3: Training**
```python
model.compile(
    optimizer=Adam(learning_rate=0.001),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

history = model.fit(
    train_generator,
    validation_data=val_generator,
    epochs=25,
    callbacks=[
        ModelCheckpoint('best_model.h5'),
        EarlyStopping(patience=5),
        ReduceLROnPlateau(factor=0.5, patience=3)
    ]
)
```

**Step 4: Evaluation & Saving**
```python
# Save model and class names
model.save('crop_detector/ml/weights/plant_disease_model.h5')

class_names = {v: k for k, v in train_generator.class_indices.items()}
with open('crop_detector/ml/weights/class_names.json', 'w') as f:
    json.dump(class_names, f)
```

### Prediction Pipeline

**Step 1: Image Preprocessing**
```python
# crop_detector/ai_model.py
def predict(self, image_file, crop_type):
    # Load image
    img = Image.open(image_file).convert('RGB')
    
    # Center crop (remove background)
    width, height = img.size
    min_dim = min(width, height)
    left = (width - min_dim) // 2
    top = (height - min_dim) // 2
    img = img.crop((left, top, left + min_dim, top + min_dim))
    
    # Resize and normalize
    img = img.resize((224, 224), Image.LANCZOS)
    img_array = np.array(img, dtype=np.float32) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    
    return img_array
```

**Step 2: Inference**
```python
# Run prediction
predictions = self._model.predict(img_array, verbose=0)
predicted_idx = np.argmax(predictions[0])
confidence = float(predictions[0][predicted_idx]) * 100
disease_name = self._class_names[str(predicted_idx)]
```

**Step 3: Response Formatting**
```python
return {
    'crop': crop_type,
    'status': 'Diseased' if 'healthy' not in disease_name else 'Healthy',
    'disease': clean_disease_name,
    'confidence': round(confidence, 1),
    'severity': calculate_severity(confidence),
    'treatment': get_treatment_recommendation(disease_name),
    'fertilizer': get_fertilizer_suggestion(disease_name),
    'prevention': get_prevention_tips(disease_name)
}
```

---


## 🗄️ Database Design

### Entity Relationship Diagram (ERD)

```
┌──────────────┐         ┌──────────────┐         ┌──────────────┐
│     User     │   
n**: 1.0.024
**Versio20**: January dated
**Last Up--


-l]ai[your-em- Email: n]
-linkedikedIn: [your- Linr-github]
GitHub: [youame]
- r
[Your NDevelope 👨‍💻 oses

##purpfolio porting and se for learn to uel freese - FeIT Licennse
M

## 📝 Lice

---ers."balancoad h lzontally witle horieasily scand can unicorn a Githd weploye's d It practices.stbengo  Djand followedis, aith Redaching wlemented c model, impAIr the ng foadilazy lo I used scale.esigned to on is dati"The appliclity
Scalabi."

### ngcial planniinanlps with f he systemgementmanad the farm anal advice, ultur7 agricdes 24/ot provirated chatbegntsses. The irop losands in csaving thouotentially  early, pop diseases detect crmers far can helplutions so"Thiact
### Impurity."

ion for secauthenticatted JWT mennd I impleeNoise, ahitvia W served  files areaticStng.  learnifor deeporFlow  and TensUI,tive or reacAlpine.js fAPIs, amework for EST Frngo R. I used Djaurefeatch s for eago appparate Djanture with sear architecodulfollows a mn icatio"The applchitecture
Ar."

### cantlynificuracy sigld acored real-which improvlization, ws normahtnesig br andterpolation,S ing, LANCZO croppinenterluding cocessing incnced prepradvating  implemens by solved thi Iages. im real-worldrly onrming poomodel perfo was the AI ngellee major chag
"On Solvin### Problem
ccuracy."
with 92% ap types ross 14 croes acant diseasrent pldiffe 38 entifyes to id imag0+,00 on 87N trainedbileNetV2 CNses a Moem usysthe  using AI. Tseasestect crop difarmers dethat helps sorFlow en Tgo andanng Djusiapplication ack web  full-stt a
"I builcal Depth### Techni

lking Pointsnterview Ta

## 🎤 I
---dation set
n vali92% ocuracy**: ~Ac**Model mages
- 0+ i*: 87,00g Dataset*Trainins
- ** 38 diseaseClasses**:e eas- **Dispes
 typs**: 14rorted C**Suppo**: 25+
-  Endpoints**API*: 12+
- base Tables*
- **Datas**: 150+mber of File00+
- **Nue**: ~15,0 of Cod*Total Linesstics

- *ject Statiro-

## 📊 Ppping

--ld ma fie - GPS-basedFarming**ecision 5. **Prns
atioce recommendrannsu Crop iance** -**Insur
4. ackingtrn ly chaippansparent suchain** - Tr **Blockng
3.torinial crop mon** - Aeriioone Integrate
2. **Drperaturoisture, temfor soil m* - Sensors tion*grate**IoT Inar)
1.  ye (1 Long-term### labs

il analysis soation with Integresting** -5. **Soil Ttimation
yield escrop el for L modction** - MrediYield P **ies
4.idtion on subs** - Informament Schemes **Govern share
3. discuss and canFarmersum** - ty Forommuni**Cnt
2. ipme equs andl cropuy/sel** - Bketplace1. **Marmonths)
rm (6  Mid-te### SMS

rnings viar waeathes** - WS Alert. **SMr chatbot
5o-text foSpeech-t Input** - 
4. **Voiceugu, Kannada Telt** - Hindi,porlanguage Supi-3. **Multce workers
vi with sere** - PWA Mod. **Offlinelutter
2e or Fact Nativ - Reile App***Mobs)
1. * montht 3rm (Nexhort-tents

### Se Enhancemeutur

## 🔮 F

--- (future)tesdame up-tir realebSocket fotes
- W auto-updary foreletask with Ckground ton
- Bac butreshnual refAdded ma
- nutesg every 5 mi AJAX pollinementedn**:
- Implutio*Solgh

*ou fast enngatiata not upd Weather doblem**:PrUpdates
**ime Weather Real-tenge 5: Chall

### n trackingsed sessiot
- UUID-baexM for contssages to LLevious mess prbase
- Paory in datae histsag- Store mesrage
d chat stosession-baseemented n**:
- Impl
**Solutiossions
t across se contexsationng convertaini*: Main
**Problem*ementntext Managtbot Conge 4: Cha# Challe
##vailable
a when adatcached 
- Show API callsry cessaed unnees
- Reduc0 minutta for 1her dahe weat- Cacedis
with R caching entedmplemion**:
- I
**Solut tier
lls on freeI cad APte**: Limi**ProblemtherMap)
(OpenWeaate Limits I Rllenge 3: AP### Chaon

optimizatifuture r ization foel quantsidered modonion)
- Ct predictn firss ol loadoading (mode led lazy- Implementtecture)
weight archiNetV2 (light Mobile Usedution**:
-ols

**Slatform hosting psomefor  large  (87MB) tooelorFlow modlem**: Tensze
**Probodel File Si2: Large Mnge alle

### Chngainietrmages for r-world iecting realollmmended c
- Recozationness normalihtUsed brigpeline
- piprocessing preroved image 
- Impskgroundremove bacng to ppi center cro
- Addedationa augmentive dat aggressmentedmpleion**:
- I
**Soluts
ld photo-worly on real poorutmages bggle ion Ka well odel workedem**: Mobl
**Prtasetgle Da on Kagrfittingveel O 1: AI Modllenge

### ChaSolutions & allengesCh-

## 🎯 tup

--re seRequires mocalable
- control
- Sore roku**
- MS/HelOcean/AW3. Digitale

**tier availabgo
- Free detects Djan
- Auto-ployment- Quick depp**
ay.a Railw`

**2..mdIDET_GUe `DEPLOYMENd
- SeludereSQL inc
- Postgtescertifica Auto SSL 
-bleer availa
- Free tinded)**ecommeder.com (R. Renns

**1Optioyment eplo

### Dingsity settiew secur ] Revsword
- [n pasrong admit sts
- [ ] Sebackuptabase Enable da] )
- [  (Sentryggingerror lo[ ] Set up es CDN
- e static filConfigur
- [ ] p SSL/HTTPS[ ] Set ubase
- greSQL data[ ] Use Postmain
- with doOSTS e ALLOWED_H] Updat
- [ ECRET_KEYe new S Generat
- [ ]se DEBUG=FalSet[ ] 
- istckltion Cheduc# Pro
##loyment
 Dep-

## 🚀
--0/admin/
8001:27.0.0.tp://1nel: htAdmin Pa00/
- 27.0.0.1:80te: http://1ebsiion**
- Wthe Applicat Access ```

**9. runserver
on manage.pybash
pyth**
``` Servervelopmentn De

**8. Ru``-noinput
` -lectstaticpy col manage.python``bash
*
`iles*ct Static F
**7. Colle
```
ssword email, paer username,
# Entatesuperuser.py cre managethon`bash
pyer**
``uperuste S
**6. Crea``

` migrate manage.py
pythongrationsmakemin manage.py `bash
pythos**
``ationgrbase Mitan DaRu

**5. 
```pi-keyur-groq-a_KEY=yoQ_APIy
GROapi-kePI_KEY=your-THERMAP_APENWEA
Olite3te:///db.sqsqli_URL=SEBA1
DATAt,127.0.0.alhoslocSTS=HOue
ALLOWED_ey
DEBUG=Trour-secret-kECRET_KEY=yur values
Sv with yot .en
# Edimple .env
env.exa
cp . env filepy example
# Co
```bashes**ent Variablure Environm**4. Configxt
```

s.tquirement -r restallash
pip in*
```bcies*all Dependen
**3. Instivate
```
n/actvenv/bienv
source env v3 -m vMac
pythonLinux/te

# \activaScripts
venv\venvnv m ve -honindows
pytsh
# Wnt**
```bavironmel Enreate Virtua
**2. Capp
```
arming__smart_fsathiisan_titch_ksathi/sisan-i.git
cd kan-sathisme/k/yourusernathub.come https://gish
git clon```bary**
 Repositothe. Clone on

**1nstallatitep IStep-by-S### ded)

commenent (reonmual envir
- Virt)
- Gitanagern package mytho (Pip
- p.11+on 3ites
- Pythrequis# Pretup

## Se &ionat 📦 Install--

##
-
```
ge historyUpdate messaUI
    ↓
hat in cmessage displays Script 
    ↓
Javaontendonse to frN resp JSOrn↓
Retue
     to databast messagesistan
Save as    ↓I response
↓
Return ALM
    esses with Loq API proc
    ↓
Groes?"
} for tomatlizerti"What fernt":    "conter",
 use: ""
    "role},
{"
. expert..ralcultugri aYou are ant": ""conten
    system",: "    "role"t:
{
contex with .3 70B model Llama 3ssage tome
Send .py)
    ↓ce_servit/aihatboroq API (c   ↓
Call Gdatabase
  message to userave 
    ↓
Sessiont ste cha creaGet or ↓
py)
   ws.atbot/vieackend (ch ↓
Django B"
}
   123": "uuid-on_idssi",
    "se tomatoes?izer fortilfer"What  age":   "mess/
{
 geessaatbot/api/mOST /che
    ↓
Pes messagript captur
JavaSc
    ↓tonbutick Send "
    ↓
Cltomatoes?zer for  fertiliatn: "Whypes questio``
User tion

`ConversatI Chatbot  Alow 4:# F

##tion
```er's locat usker a map mardate ↓
Up  ds
  car forecast
Display   ↓t)
 ueseqel rparall forecast (etch 5-dayn
    ↓
FtioDescrip
- r iconWeatheed
- - Wind speity
- Humid
eratureth:
- Tempdates UI wiavaScript up
    ↓
Jontend JSON to fr↓
Return  response
  nd formats s aprocesse  ↓
Django ta
   weather daurns rettherMap
OpenWea    ↓Map API
therlls OpenWeand ca
Backeuest
    ↓receives reqview  ↓
Django 5
   lon=77.25t=17.0389&ent/?laapi/currher/
GET /weatquest:JAX re Acript sends
JavaSion
    ↓l selectr manuan oiocatlt lo Use defauied →lon
If den→ Get lat/allowed ↓
If   ission
  rmser asks peow    ↓
Br API)
rowsertion (bs geolocat user' ↓
Reques   her page
 Weat
User opensng

```chi Fetata Dther Flow 3: Wea
```

###──────────┘────────────────────────────────────└───────────    │
                          ts       Share resul
│     -   │                    ge       Another Imaalyze 
│     - An  │                            Report  PDF wnload - Do
│      │                                          ns:io  Opt    │
│                                 tions      13. User Ac───────┐
│ ──────────────────────────────────────────┌────────     ▼
              │
             ──┘
      ────────────────────────────────────┬───────────────   │
└───                    ad button PDF downloEnable  │
│     -                                 vention tab     * Pre│          │
                        tab    er * Fertiliz            │
│                        b     atment ta      * Tre
│       │                     ndicator   y iverit    * Se   │
│             bar)    e (progress  scordence  * Confi │
│                                  me      * Disease na │
│                                 h:ard witsults c - Show re    │
│                          tion  g animaide loadin
│     - H           │                 ults Display Res. Frontend─┐
│ 12───────────────────────────────────────────────────────  ▼
┌─                  │
                ──┘
  ─────────────────────────────────────┬───────────────   │
└──                                                  │
│     }      ds..." ase-free seese"Use diion": "prevent     │
│              ...",   itrogen"Reduce n: rtilizer"    "fe     │
│      ",ngicides...copper fu": "Apply "treatment│           │
                     h",      ity": "Hig"sever         │
│                             .5,nce": 94  "confide│            │
      Blight",   Late  "Tomato - disease":   "│     │
                       ",     "Diseased "status":    │           │
                         "Tomato",rop":  "c│          │
                                              {     │
│                                         Return JSON:   │
│                                   n e Formatioespons──┐
│ 11. R───────────────────────────────────────────────▼
┌────────                   │
               ─────┘
    ───────────────────────────────────┬───────────────
└─│                    l      y leveate severitulalc  - C  │
│                    s        n strategieio Prevent       * │
│                         uggestionstilizer sFer * 
│              │           tions    commendant reme * Treat │
│                                              rieve:     - Ret│
│    nary   LS dictioETAIto DISEASE_Ddisease atch  - M    │
│                               ation Lookupcommend│ 10. Re┐
───────────────────────────────────────────────────────    ▼
┌──              
         │       
    ───┘──────────────────────────────────┬──────────────│
└─────           .5%)      re (94fidence scote con- Calcula    
│") │_blightLate"Tomato___g.,  (e.isease name d  - Map to  
││               x (e.g., 30)class inde predicted 
│    - Get│              max)     (argtyabilihest probind hig
│    - F │                               sing      -ProcesPost 9. ┐
│──────────────────────────────────────────────────── ▼
┌─────                   │
                ───────┘
  ─────────────────────────────────┬────────────.] │
└────4..01, 0.9.02, 0.tion [0ibu distrbabilityt pro  - Ge      │
│          ax) s, softmlasselayer (38 cutput │      * O       │
                   (256 units)nse layer       * De   │
│                   ooling     e Pverag* Global A│
│              action)    feature extrNetV2 base (ile     * Mob   │
│           s:       hrough layerprocesses t- Model     │
│     model    orFlowns Teage toprocessed imFeed pre  │
│    -                                nference  del II Mo───┐
│ 8. A─────────────────────────────────────────────
┌─────────▼                        │
             
 ───────┘─────────────────────────────┬───────────────└─────│
            4, 224, 3]  on [1, 22sidimench  Add bat│    f.
         │           lues (0-1)  l va pixee. Normalize   │
│                               4   224x22ze to    d. Resi     │
│               nd)ove backgrou(remp r cro Cente    c.    │
│                            o RGB    . Convert t b
│            │             IL         e with Pagoad im L│    a.      │
                                 eps:         │
│    Sty)     del.p_motector/aig (crop_deessinge Preproc Ima───┐
│ 7.─────────────────────────────────────────────────────  ▼
┌─                  │
                  ────┘
───────────────────────────┬─────────────────────────  │
└         ed)   already load (if not  modeld AIoa    - L   │
│                      ary file     to temporave    - S   │
│                           le   mage fie i  - Receiv     │
│  ws.py)     r/vietecto_dessing (cropd ProceBacken──┐
│ 6. ──────────────────────────────────────────────────────   ▼
┌─                │
              ───┘
     ──────────────────────────────────────────┬─
└──────────    │                kend   st to bacST requeend PO- S │
│            type    ge + crop th ima witae FormDa - Creat  │   │
                          tion imang andi  - Show loa   │
│                                    cript:     
│    JavaS│                        nosis"   ag"Start AI Di│ 5. Click ┐
───────────────────────────────────────────────────
┌──────          ▼       │
             ─┘
        ────────────────────────────────────────┬───────────
└──── │             " button   nosisag AI Diartle "StEnab  -    │
│                        nd size   name ale - Show fi
│              │               d image    ploadey u Displa  -    │
│                                    e Preview  
│ 4. Imag──────────┐────────────────────────────────────┌───────────        ▼
         │
                   ─┘
  ──────────────────────────┬────────────────────────────
└─ │             eraive cam → Lture"Capera am Click "C  C.│
│                              ge     mag & drop ira   B. D│
│              e picker   iles" → F"Browse FilClick A. 
│             │                                       Options:      │
│                                  age  pload Im
│ 3. U────┐─────────────────────────────────────────────────────     ▼
┌          
     │             
     ┘──────────────────────────────────────┬─────────────────     │
└─     der)   e (green borstat selected I shows- U
│            │able    varilectedCrop  seupdates Alpine.js     -    │
│   to)     (e.g., Tomarop card  on cicks User cl │
│    -                                 Type    t Crop. Selec┐
│ 2───────────────────────────────────────────────────────▼
┌──               │
                      
 ─┘────────────────────────────────────┬───────────────────       │
└                        r/   crop-detectoT /
│    GE       │        r       p Detectos to Cro navigate
│ 1. User────────┐───────────────────────────────────────────────
```
┌──on
ease Detecti: Crop Dis 2### Flow──┘
```

───────────────────────────────────────────────────────      │
└            tent     onalized cay person Displ -  │ ity)     │
t activ recen, stats,athergets (we Load wid  - │
│                shboard/)   (GET /dadata Fetch user  -  │
│                           oads        board Page L┐
│ 6. Dash──────────────────────────────────────────────────┌───────
  ▼               │
                ────┘
     ──────────────────────────┬──────────────────────────      │
└              d          DashboarRedirect to 
│    -     │                        ookie r CcalStorage oLo│
│    -                          wser      Bron in Toke. Store ────┐
│ 5─────────────────────────────────────────────────────     ▼
┌   
                   │   
        ┘───────────────────────────────────┬───────────────
└──────      │                 lient     o cs tReturn token│
│    -           )  dayss in 7xpireken (erefresh toCreate 
│    -    │         n 1 day)  ixpiresken (eess toCreate acc-   │
│                                  oken   ate JWT T
│ 4. Gener─────┐─────────────────────────────────────────────────
┌───         ▼           │
              
    ──────────┘────────────────────────────────┬───────
└───────     │           abase     in datct r objete UseCrea   - 
│      │                     F2)   d (PBKDsh passwor  - Ha│
│                  ueness    e/email uniqamheck usern
│    - C   │                     r-side)(serveidate data 
│    - Val    │                    ter/     unts/regisco/ac
│    POST          │           end     go BackForm → Djanit 3. Subm
│ ─┐──────────────────────────────────────────────────┌────── ▼
               │
                
      ──┘──────────────────────────────────────────────┬───   │
└─────                ent-side)   ion (clialidatm v
│    - For   │               assword  mail, pame, eEnter usern   -       │
│           Form   stration Regip" →ign U"SClick ─┐
│ 2. ─────────────────────────────────────────────────── ▼
┌─────                 
     │               ─────────┘
─────────────────────────────┬─────────── │
└───────          e        g Pag→ Landinebsite its wer vis
│ 1. Us────┐────────────────────────────────────────────────────
┌─

```ess Accardto Dashboon stratigiw 1: User Re

### Floow FlmpleteCoorks - ⚙️ How It W
## --
te
```

- per minun attemptslogi # 5 ute' inrate = '5/m
    ttle):hrole(UserRateTnThrottss Logi

claRateThrottle User importrottlingk.th_frameworsts
from reforce attacke brut
# Prevent )
```pythonenthancem (Future Enmiting Li. Rate# 7```

##ET_KEY')
ECR = env('S
SECRET_KEYnv()iron.E
env = envport environn code
imccess i

# A-keyur-api_API_KEY=yo/...
GROQql:/RL=postgresABASE_UG=False
DATy
DEBUm-secret-keT_KEY=randoREo Git)
SECmmitted tle (not conv fiython
# .e`p
``ablesVariironment 
### 6. Env``
t)
`r_inpuscape(uset = epe
safe_texort escampl itils.htmango.u djomneeded
fraping when l escd

# Manua escapellytica}}  # Automat ser_inpuTML
{{ u Ho-escapetes autgo templan
# Djanon
```pythoS Preventi
### 5. XSion
```
 SQL injecties preventered quarameteriz# P)
mena name=crop_ser,est.uer=requ.filter(usbjectsrop.oies
C query escapesautomaticallDjango ORM ``python
# revention
` Injection PSQL## 4. ```

#ken')
}
('csrftookieCo get-CSRFToken':s: {
    'X
headerstsreque AJAX cript

# JavaS %}csrf_tokenforms
{% RF token in c CS# Automati
n
```pythonProtectio3. CSRF 
### ```
 = True
PE_NOSNIFFCONTENT_TYURE_
    SECILTER = TrueOWSER_XSS_FE_BRSECUR= True
    _SECURE OOKIE_C
    CSRFCURE = TrueCOOKIE_SEION_SSe
    SETruEDIRECT = _SSL_RECURE   SEBUG:
 not Dy
if s.pting
# set```python
duction)SL (ProPS & S
### 2. HTT``

]
`,8}
    }th': n_lengONS': {'mi  'OPTI    ,
  dator'ValiengthinimumLion.Mvalidatord_auth.passwo.contrib.djang  'NAME': '  {
          },
  or',
ValidattybuteSimilarion.UserAttritilidaord_vapasswth.ontrib.au 'django.c    'NAME':
     = [
    {D_VALIDATORSSWORASTH_PAUKDF2
ing with PBd hashwor Pass}

#
    ),on',
thenticatition.JWTAu.authentica_simplejwtrameworkst_f  're   ES': (
   LASSCATION_CTITHENEFAULT_AU
    'DORK = {_FRAMEWion
RESTticatauthend ase Token-bWTn
# Jpythoion
```& Authorizatcation 1. Authenti

### ementationty Implcuri## 🔐 Se--



-
```30:00Z"
}-01-15T10:"2024ed_at": 
    "creat",hase seeds purc"Tomato: ription"   "desc
 -15",24-0120"date": 
    "t": 5000,unmo,
    "aeds": "Segory"   "cate 1,
 ":{
    "id Created
 201e:
Respons
hase"
}o seeds purcTomattion": "descrip
    "4-01-15",02"date": "200,
    unt": 50   "amoeds",
 : "Secategory"   "

{
 jsonation/plicent-Type: apCont{token}
er earorization: Buthses/
Am/expeni/v1/farment/apanageT /farm-m
POS``http*
`Expense*ate re

**2. C```25000
}
oans": utstanding_l
    "o: 15,unt"ivestock_co,
    "l00it": 550net_prof,
    "00nses": 950total_expe,
    "": 150000ncome_ital "tos": 3,
   ive_crop,
    "actarea": 10.5otal_
    "t
{: 200 OK
Response {token}
ion: Beareratrizd/
Authoarm/dashboarent/api/v1/farm-managem /fGET```http
**
rd Stats Dashboa**1. Get

 Endpointsmentarm Manage```

### F00Z"
}
1-15T10:30:: "2024-0"timestamp" -id",
   onessiuid-s "usion_id":"ses    ",
commend...reoes, I atr tom": "Foonse   "resp00 OK
{
  2esponse:

Rn-id"
}id-sessio": "uusession_id
    "atoes?",se for tomshould I ur at fertilize"Whge":  "messa
   json

{on/catili-Type: appontentken}
C {to: BearerhorizationAutage/
api/mess /chatbot/p
POST```httsage**
1. Send Mes
**Endpoints
## Chatbot }
```

#]
    ays data
 5 d // ...       },
       y"
 oudrtly cl"Pa": iption  "descr      0,
    ": 7humidity       " 18,
     p_min":      "tem      max": 32,
"temp_         
   4-01-15","202"date":            {
       : [
  "forecast"",
     "Kodla, INon": "locati  K
{
 ponse: 200 Oken}

Res {toon: Bearerthorizati=77.255
Au.0389&lonast/?lat=17orecher/api/f
GET /weat
```http*ast*ecather For Get We`

**2.
}
``1d""icon": "0",
    skyClear "cription": des   "d": 3.5,
 speewind_,
    "": 65humidity   "2,
 : 30.feels_like"
    "28.5,ature": temper",
    "la, INKod": "tion "loca0 OK
{
   20: onseesp
R}
{token Bearer ation:izAuthor255
9&lon=77.7.038lat=1ent/?currather/api/tp
GET /we```hter**
Weathrrent 
**1. Get Cunts
oidpeather En``

### W
`.."
} seeds.-freed disease certifie": "Plant"prevention",
    nitrogen...sive void excesizer": "A   "fertil..",
 es.d fungicidase copper-b"Apply ":"treatment
    : 80,everityVal""s",
    : "Highrity"   "seve 94.5,
 nfidence":
    "cot",Blighate "Tomato - Ldisease": 
    "iseased", "Datus":   "sto",
  "Tomatrop":    "c{
se: 200 OK


Respon"
}Tomato "  "crop":ile],
  ary f: [bin" "imagea

{
   datm-ultipart/forpe: montent-Ty
Cn}Bearer {toketion: rizanose/
Authoiag/api/dctorp-detecroPOST /tp
*
```htase*op Dise Diagnose Cr

**1.ointsr EndpCrop Detecto# 
##
  }
}
```
  m"e.cor1@exampl": "farme"email     1",
   : "farmerme"userna     ",
   : 1"id"
        user": { "
   ,."LCJhbGc..OiJKV1QiAi"eyJ0eX"refresh":    ,
 Gc..."iLCJhbV1Q0eXAiOiJKs": "eyJ "acces OK
{
   se: 200}

Respon123"
ecurePass"Sd": "passworr1",
    armeme": "fserna "u

{
   ation/jsone: applicent-Typ
Cont/ts/loginounPOST /accttp
gin**
```h`

**2. Lo..."
}
``V1QiLCJhbGcJK"eyJ0eXAiOien": "tok    ple.com",
@examr1": "farmeil"ema  
  1",farmername": "
    "user": 1, "idated
{
   201 Cree: pons

Res"
}: "Doe"last_name",
    ": "John"ame "first_n23",
   ePass1"Secur": d"passwor  
  om",xample.c"farmer1@e: "email"",
    mer1ame": "far"usern
    {

on/json: applicatiContent-Type/
s/registeruntST /acco`http
PO``tration**
User Regis
**1. 
on EndpointshenticatiAuton

### tiumenta## 🔌 API Doc`

---

)
);
``r(idse auth_uENCESREFER(user_id) N KEY 
    FOREIGLL,ME NOT NUETIATated_at DL,
    upd NULOTETIME Neated_at DAT),
    crARCHAR(255  title VLL,
  ER NOT NU_id INTEGer  us,
  QUE NOT NULLHAR(255) UNIon_id VARC   sessiY KEY,
 IMAREGER PRINT
    id ion (hatsess chatbot_cLE
CREATE TAB
```sqlsion Table**Ses. Chat*4``

*)
);
`auth_user(idERENCES _id) REFKEY (user    FOREIGN L,
ULT NETIME NOed_at DAT,
    creatRCHAR(50)od VAment_methpay   EXT,
 ption T    descri NOT NULL,
   date DATE
 NULL,10, 2) NOT t DECIMAL(amoun
    L, NOT NULRCHAR(50)y VA    categorOT NULL,
ER N INTEG_ider
    usIMARY KEY,ER PR INTEG  ide (
  nt_expensanagemearm_mBLE f TA
CREATE**
```sqlable T3. Expense`

**
);
``(id)user auth_EFERENCES_id) RuserIGN KEY (ORE,
    F NOT NULLt DATETIMEted_a    creaEXT,
    notes TRCHAR(50),
  status VA
  ,ate DATEed_harvest_d
    expect_date DATE,anting   pl(10, 2),
 MALs DECIacreea_  ar0),
  RCHAR(10VAiety 
    varNOT NULL,(100) RCHAR   name VAL,
 OT NUL INTEGER N_id userY KEY,
   ER PRIMARid INTEG
    rop (gement_cfarm_manaE TABLE ``sql
CREATe**
` Crop Tabl
**2.;
```
T NULL
)TIME NOined DATE
    date_joLT 0,OOLEAN DEFAU  is_staff BLT 1,
  EAN DEFAUive BOOL    is_act(150),
HARame VARCst_n
    la), VARCHAR(150irst_name,
    fT NULLCHAR(128) NO VAR password NULL,
   NIQUE NOT54) URCHAR(2il VA,
    emaNULLE NOT  UNIQURCHAR(150)username VA,
    IMARY KEYINTEGER PR id r (
   uth_useEATE TABLE a
```sql
CR Table**ser

**1. Ue Tablesatabas# Key D```

##
─┘─────└────────   ──┘   ──────
└──────e        │alu      │ v     ││ date    ty     │
quanti    │ │  nt          │
│ amou  pe      │ ty   │    source     FK) │
││ user_id (       (FK) │ user_id
│PK)      │     │ id (   │ PK)   id (──────┤
│ ───────      ├───────────┤───
├─k   │stoc    │  Live  │   Income   
│  ───┐────────      ┌───────┐────────
┌──────┘
───────└──      ───────────┘│
└──scription  │      │ deing   │ plant  │
te      da│      │            │
│ areaunt      │ amo│   ty     ie│ varry    │
catego    │   │       │
│ name _id(FK)  userK) │      │id(Fser_
│ u     │d (PK)  │ i  │  K)     ┤
│ id (P──────────  ├─────┤    ──────────  │
├─Expense     │      │   Crop  │   ──▼──────┐
      ┌──────┐─────▼────
┌─          │             │    ──┐
 ─────────────────       ├──
       │
──────┘─────────────────└─            │      │
                          │                 │───┘
 ───────  └────      │                    ────┘    │─────── │
└───stamp    │ time──┘    │   ──────── │    └────d_at   │   create
│         │le │ ro   │      │ ted_at    │ crea  │    │  rd  asswo │
│ pnt     conte│    │    │  tle       │ ti    │    il        │ │
│ emassion_id   se│    │    │K) _id (F user   │    │rname     │     │
│ use  K)(P──┐    │ id PK)      │── (─┐    │ idK)      │────┤
│ id (P───────────   ├──────┤       ├────────────┤        ───────── │
├───  Message    │ n │        atSessio │  Ch     