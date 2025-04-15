from django.shortcuts import render
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from .models import SentimentEntry, SelfCareSuggestion
import random
from django.db.models import Count, Avg
from django.utils import timezone
from datetime import timedelta
import json

# Download required data (only once)
nltk.download('vader_lexicon')

def get_emotion_from_text(text, sentiment_score):
    # Simple emotion detection based on keywords and sentiment
    text_lower = text.lower()
    
    if sentiment_score > 0.5:
        if any(word in text_lower for word in ['happy', 'joy', 'excited', 'great', 'wonderful']):
            return 'excited'
        return 'happy'
    elif sentiment_score < -0.5:
        if any(word in text_lower for word in ['angry', 'mad', 'furious', 'hate']):
            return 'angry'
        elif any(word in text_lower for word in ['anxious', 'worried', 'nervous', 'stress']):
            return 'anxious'
        return 'sad'
    else:
        if any(word in text_lower for word in ['tired', 'exhausted', 'sleepy']):
            return 'tired'
        elif any(word in text_lower for word in ['confused', 'unsure', 'doubt']):
            return 'confused'
        return 'calm'

def get_self_care_suggestions(emotion):
    suggestions = SelfCareSuggestion.objects.filter(emotion=emotion)
    if suggestions.exists():
        return random.sample(list(suggestions), min(3, len(suggestions)))
    return []

def get_icon_for_category(category):
    icon_mapping = {
        'physical': 'fa-running',
        'mental': 'fa-brain',
        'social': 'fa-users',
        'creative': 'fa-paint-brush',
        'mindfulness': 'fa-medkit'
    }
    return icon_mapping.get(category, 'fa-heart')  # Default to fa-heart if category not found

def get_sentiment_trends():
    # Get data for the last 7 days
    end_date = timezone.now()
    start_date = end_date - timedelta(days=7)
    
    try:
        # Get daily sentiment averages
        daily_sentiments = SentimentEntry.objects.filter(
            created_at__range=(start_date, end_date)
        ).extra(
            select={'date': 'date(created_at)'}
        ).values('date').annotate(
            avg_sentiment=Avg('intensity'),
            count=Count('id')
        ).order_by('date')
        
        # Get emotion distribution
        emotion_distribution = SentimentEntry.objects.filter(
            created_at__range=(start_date, end_date)
        ).values('emotion').annotate(
            count=Count('id')
        ).order_by('-count')
        
        # Get sentiment distribution
        sentiment_distribution = SentimentEntry.objects.filter(
            created_at__range=(start_date, end_date)
        ).values('sentiment').annotate(
            count=Count('id')
        ).order_by('-count')
        
        # Format data for Chart.js
        daily_averages = {
            'labels': [str(entry['date']) for entry in daily_sentiments],
            'data': [float(entry['avg_sentiment']) for entry in daily_sentiments]
        }
        
        # Enforce consistent order for emotions and sentiments
        emotion_order = ['Happy', 'Sad', 'Angry', 'Anxious', 'Calm', 'Excited', 'Tired', 'Confused', 'Hopeful']
        sentiment_order = ['Positive', 'Neutral', 'Negative']

        # Build emotion_dist with all emotions, even if count is zero
        emotion_counts = {entry['emotion'].title(): entry['count'] for entry in emotion_distribution}
        emotion_dist = {
            'labels': emotion_order,
            'data': [emotion_counts.get(emotion, 0) for emotion in emotion_order]
        }

        # Build sentiment_dist with all sentiments, even if count is zero
        sentiment_counts = {entry['sentiment'].title(): entry['count'] for entry in sentiment_distribution}
        sentiment_dist = {
            'labels': sentiment_order,
            'data': [sentiment_counts.get(sentiment, 0) for sentiment in sentiment_order]
        }
        
        # Add default data if no entries exist
        if not daily_sentiments:
            dates = [(end_date - timedelta(days=i)).date() for i in range(7, -1, -1)]
            daily_averages = {
                'labels': [str(date) for date in dates],
                'data': [0] * len(dates)
            }
        
        if not emotion_distribution:
            emotions = ['Happy', 'Sad', 'Angry', 'Anxious', 'Calm']
            emotion_dist = {'labels': emotions, 'data': [0] * len(emotions)}
        
        if not sentiment_distribution:
            sentiments = ['Positive', 'Neutral', 'Negative']
            sentiment_dist = {'labels': sentiments, 'data': [0, 0, 0]}
        
        print("Daily averages:", daily_averages)
        print("Emotion distribution:", emotion_dist)
        print("Sentiment distribution:", sentiment_dist)
        
        sentiment_trends = {
            'daily_averages': json.dumps(daily_averages),
            'emotion_distribution': json.dumps(emotion_dist),
            'sentiment_distribution': json.dumps(sentiment_dist)
        }
        print("Sentiment Trends Data:", sentiment_trends)  # Debug log
        return sentiment_trends
    except Exception as e:
        print(f"Error in trend data preparation: {e}")
        # Return default data if there's an error
        dates = [(end_date - timedelta(days=i)).date() for i in range(7, -1, -1)]
        return {
            'daily_averages': json.dumps({
                'labels': [str(date) for date in dates],
                'data': [0] * len(dates)
            }),
            'emotion_distribution': json.dumps({
                'labels': ['Happy', 'Sad', 'Angry', 'Anxious', 'Calm'],
                'data': [0, 0, 0, 0, 0]
            }),
            'sentiment_distribution': json.dumps({
                'labels': ['Positive', 'Neutral', 'Negative'],
                'data': [0, 0, 0]
            })
        }

def home(request):
    result = None
    suggestions = None
    error = None
    
    # Handle AJAX requests for chart data
    if request.GET.get('get_charts') == 'true':
        from django.http import JsonResponse
        try:
            sentiment_trends = get_sentiment_trends()
            return JsonResponse({'sentiment_trends': sentiment_trends})
        except Exception as e:
            return JsonResponse({'error': str(e)})
    
    try:
        sentiment_trends = get_sentiment_trends()
        print("Sentiment trends data:", sentiment_trends)  # Debug print
    except Exception as e:
        sentiment_trends = {
            'daily_averages': json.dumps({'labels': ['No Data'], 'data': [0]}),
            'emotion_distribution': json.dumps({'labels': ['No Data'], 'data': [0]}),
            'sentiment_distribution': json.dumps({'labels': ['No Data'], 'data': [0]})
        }
        print(f"Error getting trends: {str(e)}")

    # Check for AJAX request (update this line)
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    # Get theme preference if provided
    theme = request.GET.get('theme', 'light')

    # Add debugging for AJAX requests
    if is_ajax:
        print("Handling AJAX request")

    if request.method == "POST":
        user_text = request.POST.get("text", "").strip()
        print(f"Received text: {user_text}")  # Debug print
        
        if user_text:
            try:
                # Perform sentiment analysis
                sia = SentimentIntensityAnalyzer()
                sentiment_score = sia.polarity_scores(user_text)["compound"]
                print(f"Sentiment score: {sentiment_score}")  # Debug print

                # Determine sentiment label
                if sentiment_score > 0:
                    sentiment_label = "positive"
                elif sentiment_score < 0:
                    sentiment_label = "negative"
                else:
                    sentiment_label = "neutral"

                # Detect emotion
                emotion = get_emotion_from_text(user_text, sentiment_score)
                print(f"Detected emotion: {emotion}")  # Debug print
                
                # Get self-care suggestions
                suggestion_objects = get_self_care_suggestions(emotion)
                print(f"Found {len(suggestion_objects)} suggestions")  # Debug print
                
                # Format suggestions for template
                suggestions = []
                for suggestion in suggestion_objects:
                    suggestions.append({
                        'category': suggestion.category,
                        'text': suggestion.suggestion,  # Map suggestion field to text as expected in template
                        'icon': suggestion.icon_class   # Use the icon_class property
                    })
                
                # Create result object that matches template expectations
                result = {
                    'sentiment_label': sentiment_label,
                    'intensity': sentiment_score,
                    'emotion': emotion
                }

                # Save the entry
                SentimentEntry.objects.create(
                    text=user_text,
                    sentiment=sentiment_label,
                    emotion=emotion,
                    intensity=sentiment_score
                )
                
                print(f"Result: {result}")  # Debug print
                print(f"Suggestions: {suggestions}")  # Debug print

            except Exception as e:
                error = f"An error occurred: {str(e)}"
                print(f"Error in analysis: {str(e)}")  # Debug print
        else:
            error = "Please enter some text before submitting."
            print("Empty text submitted")  # Debug print
        
        # For AJAX requests, return only the result and suggestions sections with theme context
        if is_ajax:
            return render(request, "sentiment_analysis/result_snippet.html", {
                "result": result,
                "suggestions": suggestions,
                "error": error,
                "theme": theme,
                "is_snippet": True
            })

    return render(request, "sentiment_analysis/home.html", {
        "result": result,
        "suggestions": suggestions,
        "error": error,
        "sentiment_trends": sentiment_trends,
        "theme": theme
    })
