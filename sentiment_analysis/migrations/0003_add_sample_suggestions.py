from django.db import migrations

def add_sample_suggestions(apps, schema_editor):
    SelfCareSuggestion = apps.get_model('sentiment_analysis', 'SelfCareSuggestion')
    
    # Clear existing suggestions
    SelfCareSuggestion.objects.all().delete()
    
    # Add sample suggestions for different emotions
    suggestions = [
        # Happy emotion suggestions
        {'emotion': 'happy', 'suggestion': 'Share your happiness with others through a kind gesture', 'category': 'social'},
        {'emotion': 'happy', 'suggestion': 'Take a moment to appreciate what made you happy', 'category': 'mindfulness'},
        {'emotion': 'happy', 'suggestion': 'Channel your positive energy into a creative project', 'category': 'creative'},
        
        # Sad emotion suggestions
        {'emotion': 'sad', 'suggestion': 'Talk to someone you trust about your feelings', 'category': 'social'},
        {'emotion': 'sad', 'suggestion': 'Practice self-compassion and be gentle with yourself', 'category': 'mental'},
        {'emotion': 'sad', 'suggestion': 'Take a walk in nature to lift your spirits', 'category': 'physical'},
        
        # Angry emotion suggestions
        {'emotion': 'angry', 'suggestion': 'Practice deep breathing to calm your nervous system', 'category': 'mindfulness'},
        {'emotion': 'angry', 'suggestion': 'Write down your thoughts to process your feelings', 'category': 'creative'},
        {'emotion': 'angry', 'suggestion': 'Do some physical exercise to release tension', 'category': 'physical'},
        
        # Anxious emotion suggestions
        {'emotion': 'anxious', 'suggestion': 'Try the 5-4-3-2-1 grounding technique', 'category': 'mindfulness'},
        {'emotion': 'anxious', 'suggestion': 'Break tasks into smaller, manageable steps', 'category': 'mental'},
        {'emotion': 'anxious', 'suggestion': 'Reach out to a friend for support', 'category': 'social'},
        
        # Tired emotion suggestions
        {'emotion': 'tired', 'suggestion': 'Take a short power nap (20 minutes)', 'category': 'physical'},
        {'emotion': 'tired', 'suggestion': 'Have a healthy snack to boost energy', 'category': 'physical'},
        {'emotion': 'tired', 'suggestion': 'Try a quick stretching routine', 'category': 'physical'},
        
        # Confused emotion suggestions
        {'emotion': 'confused', 'suggestion': 'Make a list of pros and cons to clarify your thoughts', 'category': 'mental'},
        {'emotion': 'confused', 'suggestion': 'Talk through the situation with someone you trust', 'category': 'social'},
        {'emotion': 'confused', 'suggestion': 'Take a break and return with fresh perspective', 'category': 'mindfulness'},
        
        # Calm emotion suggestions
        {'emotion': 'calm', 'suggestion': 'Use this peaceful state for creative activities', 'category': 'creative'},
        {'emotion': 'calm', 'suggestion': 'Practice gratitude for this moment of tranquility', 'category': 'mindfulness'},
        {'emotion': 'calm', 'suggestion': 'Set intentions for maintaining this balance', 'category': 'mental'},
        
        # Excited emotion suggestions
        {'emotion': 'excited', 'suggestion': 'Channel your energy into something productive', 'category': 'creative'},
        {'emotion': 'excited', 'suggestion': 'Share your excitement with people who support you', 'category': 'social'},
        {'emotion': 'excited', 'suggestion': 'Document this feeling through journaling or art', 'category': 'creative'}
    ]
    
    for item in suggestions:
        SelfCareSuggestion.objects.create(**item)

class Migration(migrations.Migration):

    dependencies = [
        ('sentiment_analysis', '0002_selfcaresuggestion_sentimententry_emotion_and_more'),
    ]

    operations = [
        migrations.RunPython(add_sample_suggestions),
    ]
