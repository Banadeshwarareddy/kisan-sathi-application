# 🌤️ Quick Setup: Weather API

## Get Your FREE API Key (2 minutes)

### Step 1: Sign Up
1. Go to: **https://openweathermap.org/api**
2. Click **"Sign Up"** (top right)
3. Fill in:
   - Username
   - Email
   - Password
4. Click **"Create Account"**

### Step 2: Verify Email
1. Check your email inbox
2. Click verification link
3. Account activated!

### Step 3: Get API Key
1. Login to OpenWeatherMap
2. Go to: **https://home.openweathermap.org/api_keys**
3. You'll see a default API key already created
4. **Copy the API key**

### Step 4: Add to Your Project
1. Open `.env` file in your project
2. Find this line:
   ```
   OPENWEATHERMAP_API_KEY=
   ```
3. Paste your API key:
   ```
   OPENWEATHERMAP_API_KEY=your_actual_key_here
   ```
4. Save the file

### Step 5: Restart Server
```bash
# Stop server (Ctrl+C in terminal)
# Start again:
python manage.py runserver
```

### Step 6: Test It!
1. Go to: http://127.0.0.1:8000/weather/
2. Search for any city
3. See real-time weather! 🎉

---

## ⚡ Quick Test

**Without API Key:**
- Shows demo data (Indore, India)
- All features work
- Perfect for testing

**With API Key:**
- Real-time weather worldwide
- Live updates
- Accurate forecasts

---

## 🆓 Free Plan Limits

OpenWeatherMap Free Plan:
- ✅ 60 calls/minute
- ✅ 1,000,000 calls/month
- ✅ Current weather
- ✅ 5-day forecast
- ✅ More than enough for your app!

---

## 🔑 API Key Example

Your API key looks like this:
```
a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
```

**Keep it secret!** Never share publicly.

---

## ✅ Verification

After adding API key, check:

1. **Browser Console** (F12)
   - No API errors
   - Weather data loading

2. **Django Terminal**
   - No error messages
   - API calls successful

3. **Weather Page**
   - Real city names
   - Accurate temperatures
   - Live updates

---

## 🎯 You're Done!

Your weather module is now connected to real-time data! 🌍

**Test cities:**
- New York, US
- London, UK
- Tokyo, JP
- Mumbai, IN
- Sydney, AU

Enjoy! 🌤️
