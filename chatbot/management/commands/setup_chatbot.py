from django.core.management.base import BaseCommand
from chatbot.models import QuickQuestion, FarmingTip


class Command(BaseCommand):
    help = 'Setup initial chatbot data - quick questions and farming tips'

    def handle(self, *args, **kwargs):
        self.stdout.write('Setting up Kisan AI Chatbot data...\n')
        
        # Quick Questions
        questions = [
            {
                'question': 'Which crop is best for rainy season?',
                'question_hi': 'बरसात में कौन सी फसल बोएं?',
                'question_kn': 'ಮಳೆಗಾಲಕ್ಕೆ ಯಾವ ಬೆಳೆ ಉತ್ತಮ?',
                'category': 'crop',
                'icon': '🌧️',
                'order': 1,
            },
            {
                'question': 'How to treat tomato leaf disease?',
                'question_hi': 'टमाटर की पत्ती रोग का उपाय?',
                'question_kn': 'ಟೊಮ್ಯಾಟೋ ಎಲೆ ರೋಗ ಹೇಗೆ ಗುಣಪಡಿಸುವುದು?',
                'category': 'disease',
                'icon': '🍅',
                'order': 2,
            },
            {
                'question': 'Best fertilizer for wheat crop?',
                'question_hi': 'गेहूं के लिए सबसे अच्छा खाद?',
                'question_kn': 'ಗೋಧಿ ಬೆಳೆಗೆ ಉತ್ತಮ ಗೊಬ್ಬರ?',
                'category': 'fertilizer',
                'icon': '🌾',
                'order': 3,
            },
            {
                'question': 'How to apply for PM-KISAN scheme?',
                'question_hi': 'पीएम किसान के लिए कैसे आवेदन करें?',
                'question_kn': 'PM-KISAN ಯೋಜನೆಗೆ ಹೇಗೆ ಅರ್ಜಿ ಸಲ್ಲಿಸಬೇಕು?',
                'category': 'scheme',
                'icon': '🏛️',
                'order': 4,
            },
            {
                'question': 'How to save water in farming?',
                'question_hi': 'खेती में पानी कैसे बचाएं?',
                'question_kn': 'ಕೃಷಿಯಲ್ಲಿ ನೀರು ಉಳಿಸುವುದು ಹೇಗೆ?',
                'category': 'irrigation',
                'icon': '💧',
                'order': 5,
            },
            {
                'question': 'How to improve soil health?',
                'question_hi': 'मिट्टी की सेहत कैसे सुधारें?',
                'question_kn': 'ಮಣ್ಣಿನ ಆರೋಗ್ಯ ಹೇಗೆ ಸುಧಾರಿಸುವುದು?',
                'category': 'soil',
                'icon': '🌱',
                'order': 6,
            },
            {
                'question': 'How to prepare organic compost?',
                'question_hi': 'जैविक खाद कैसे बनाएं?',
                'question_kn': 'ಸಾವಯವ ಗೊಬ್ಬರ ತಯಾರಿಸುವ ವಿಧಾನ?',
                'category': 'organic',
                'icon': '🌿',
                'order': 7,
            },
            {
                'question': 'Current mandi prices for wheat?',
                'question_hi': 'गेहूं का आज का मंडी भाव?',
                'question_kn': 'ಗೋಧಿ ಮಾರ್ಕೆಟ್ ಬೆಲೆ ಎಷ್ಟು?',
                'category': 'market',
                'icon': '📊',
                'order': 8,
            },
            {
                'question': 'How to start drip irrigation?',
                'question_hi': 'ड्रिप सिंचाई कैसे शुरू करें?',
                'question_kn': 'ಡ್ರಿಪ್ ನೀರಾವರಿ ಹೇಗೆ ಪ್ರಾರಂಭಿಸಬೇಕು?',
                'category': 'irrigation',
                'icon': '🚿',
                'order': 9,
            },
            {
                'question': 'Rice paddy disease treatment?',
                'question_hi': 'धान के रोगों का इलाज?',
                'question_kn': 'ಭತ್ತದ ರೋಗ ಚಿಕಿತ್ಸೆ?',
                'category': 'disease',
                'icon': '🌾',
                'order': 10,
            },
            {
                'question': 'Weather impact on rabi crops?',
                'question_hi': 'रबी फसलों पर मौसम का असर?',
                'question_kn': 'ರಬಿ ಬೆಳೆಗಳ ಮೇಲೆ ಹವಾಮಾನ ಪರಿಣಾಮ?',
                'category': 'weather',
                'icon': '🌤️',
                'order': 11,
            },
            {
                'question': 'Kisan Credit Card benefits?',
                'question_hi': 'किसान क्रेडिट कार्ड के फायदे?',
                'question_kn': 'ಕಿಸಾನ್ ಕ್ರೆಡಿಟ್ ಕಾರ್ಡ್ ಪ್ರಯೋಜನಗಳು?',
                'category': 'scheme',
                'icon': '💳',
                'order': 12,
            },
        ]
        
        created_questions = 0
        for q_data in questions:
            _, created = QuickQuestion.objects.get_or_create(
                question=q_data['question'],
                defaults=q_data
            )
            if created:
                created_questions += 1
        
        self.stdout.write(
            self.style.SUCCESS(
                f'✅ Created {created_questions} quick questions'
            )
        )
        
        # Farming Tips
        tips = [
            {
                'tip': 'Always test your soil before the sowing season. Free soil testing is available at Krishi Vigyan Kendras.',
                'tip_hi': 'बुवाई से पहले मिट्टी जरूर जांचें। कृषि विज्ञान केंद्र में मुफ्त जांच होती है।',
                'tip_kn': 'ಬಿತ್ತನೆಗೆ ಮೊದಲು ಮಣ್ಣು ಪರೀಕ್ಷಿಸಿ. ಕೃಷಿ ವಿಜ್ಞಾನ ಕೇಂದ್ರದಲ್ಲಿ ಉಚಿತ ಪರೀಕ್ಷೆ ಲಭ್ಯ.',
                'icon': '🌱',
                'season': 'all',
                'category': 'soil',
            },
            {
                'tip': 'Drip irrigation saves 40-60% water compared to flood irrigation. Apply for PMKSY subsidy for free installation.',
                'tip_hi': 'ड्रिप सिंचाई से 40-60% पानी बचता है। PMKSY योजना से सब्सिडी पाएं।',
                'tip_kn': 'ಡ್ರಿಪ್ ನೀರಾವರಿ 40-60% ನೀರು ಉಳಿಸುತ್ತದೆ. PMKSY ಸಬ್ಸಿಡಿ ಪಡೆಯಿರಿ.',
                'icon': '💧',
                'season': 'all',
                'category': 'irrigation',
            },
            {
                'tip': 'Neem oil spray (5ml/L water) prevents most fungal diseases. Spray in early morning or evening for best results.',
                'tip_hi': 'नीम तेल स्प्रे (5ml/लीटर पानी) अधिकतर फफूंद रोगों से बचाता है।',
                'tip_kn': 'ಬೇವಿನ ಎಣ್ಣೆ ಸ್ಪ್ರೇ (5ml/ಲೀ) ಹೆಚ್ಚಿನ ಶಿಲೀಂಧ್ರ ರೋಗಗಳನ್ನು ತಡೆಯುತ್ತದೆ.',
                'icon': '🌿',
                'season': 'all',
                'category': 'organic',
            },
            {
                'tip': 'Crop rotation improves soil health and reduces pest pressure. Never grow the same crop twice in the same field.',
                'tip_hi': 'फसल चक्र से मिट्टी की सेहत सुधरती है और कीट-रोग कम होते हैं।',
                'tip_kn': 'ಬೆಳೆ ಸರದಿ ಮಣ್ಣಿನ ಆರೋಗ್ಯ ಸುಧಾರಿಸುತ್ತದೆ ಮತ್ತು ಕೀಟ ಒತ್ತಡ ಕಡಿಮೆ ಮಾಡುತ್ತದೆ.',
                'icon': '🔄',
                'season': 'all',
                'category': 'crop',
            },
            {
                'tip': 'Apply PM-KISAN if you have agricultural land. You get ₹6000/year directly in your bank account. Visit pmkisan.gov.in',
                'tip_hi': 'अगर आपके पास खेती योग्य जमीन है तो पीएम-किसान के लिए आवेदन करें। ₹6000/साल मिलेंगे।',
                'tip_kn': 'ಕೃಷಿ ಭೂಮಿ ಇದ್ದರೆ PM-KISAN ಗೆ ಅರ್ಜಿ ಸಲ್ಲಿಸಿ. ₹6000/ವರ್ಷ ಬ್ಯಾಂಕ್ ಖಾತೆಗೆ ಬರುತ್ತದೆ.',
                'icon': '🏛',
                'season': 'all',
                'category': 'scheme',
            },
            {
                'tip': 'Vermicompost is rich in nutrients and improves soil structure. You can prepare it at home using kitchen waste.',
                'tip_hi': 'वर्मीकम्पोस्ट पोषक तत्वों से भरपूर है। इसे घर पर रसोई के कचरे से बना सकते हैं।',
                'tip_kn': 'ವರ್ಮಿಕಂಪೋಸ್ಟ್ ಪೋಷಕಾಂಶಗಳಿಂದ ಸಮೃದ್ಧವಾಗಿದೆ. ಮನೆಯಲ್ಲಿ ತಯಾರಿಸಬಹುದು.',
                'icon': '🪱',
                'season': 'all',
                'category': 'organic',
            },
            {
                'tip': 'Monitor your crop every 3-4 days for early pest detection. Early action prevents major damage.',
                'tip_hi': 'हर 3-4 दिन में फसल की जांच करें। शुरुआत में ही कीट-रोग पकड़ लें तो नुकसान कम होगा।',
                'tip_kn': 'ಪ್ರತಿ 3-4 ದಿನಗಳಿಗೊಮ್ಮೆ ಬೆಳೆ ಪರಿಶೀಲಿಸಿ. ಆರಂಭಿಕ ಕ್ರಮ ದೊಡ್ಡ ಹಾನಿ ತಡೆಯುತ್ತದೆ.',
                'icon': '🔍',
                'season': 'all',
                'category': 'disease',
            },
            {
                'tip': 'Mulching conserves soil moisture and reduces weed growth. Use crop residue or dry grass as mulch.',
                'tip_hi': 'मल्चिंग से मिट्टी में नमी बनी रहती है और खरपतवार कम होते हैं।',
                'tip_kn': 'ಮಲ್ಚಿಂಗ್ ಮಣ್ಣಿನ ತೇವಾಂಶ ಉಳಿಸುತ್ತದೆ ಮತ್ತು ಕಳೆ ಬೆಳವಣಿಗೆ ಕಡಿಮೆ ಮಾಡುತ್ತದೆ.',
                'icon': '🍂',
                'season': 'all',
                'category': 'soil',
            },
        ]
        
        created_tips = 0
        for tip_data in tips:
            _, created = FarmingTip.objects.get_or_create(
                tip=tip_data['tip'],
                defaults=tip_data
            )
            if created:
                created_tips += 1
        
        self.stdout.write(
            self.style.SUCCESS(
                f'✅ Created {created_tips} farming tips'
            )
        )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\n🎉 Chatbot setup complete! '
                f'{created_questions} questions and {created_tips} tips added.'
            )
        )
