from django.core.management.base import BaseCommand
from sentiment_analysis.models import SelfCareSuggestion

class Command(BaseCommand):
    help = 'Adds initial self-care suggestions to the database'

    def handle(self, *args, **kwargs):
        suggestions = [
            # Happy
            {'emotion': 'happy', 'category': 'social', 'suggestion': 'Share your joy with friends or family - positive emotions are contagious!'},
            {'emotion': 'happy', 'category': 'creative', 'suggestion': 'Channel your positive energy into a creative project you enjoy.'},
            {'emotion': 'happy', 'category': 'mindfulness', 'suggestion': 'Practice gratitude by writing down three things that made you happy today.'},
            
            # Sad
            {'emotion': 'sad', 'category': 'physical', 'suggestion': 'Take a gentle walk in nature - it can help lift your mood.'},
            {'emotion': 'sad', 'category': 'social', 'suggestion': 'Reach out to a trusted friend or family member - you don\'t have to face this alone.'},
            {'emotion': 'sad', 'category': 'mindfulness', 'suggestion': 'Practice self-compassion meditation and remember that it\'s okay to feel this way.'},
            
            # Angry
            {'emotion': 'angry', 'category': 'physical', 'suggestion': 'Release tension through exercise or punching a pillow.'},
            {'emotion': 'angry', 'category': 'mindfulness', 'suggestion': 'Take deep breaths and count to ten before reacting.'},
            {'emotion': 'angry', 'category': 'creative', 'suggestion': 'Express your feelings through art or writing.'},
            
            # Anxious
            {'emotion': 'anxious', 'category': 'mental', 'suggestion': 'Break down overwhelming tasks into smaller, manageable steps.'},
            {'emotion': 'anxious', 'category': 'physical', 'suggestion': 'Try the 5-4-3-2-1 grounding technique: name 5 things you see, 4 you feel, 3 you hear, 2 you smell, and 1 you taste.'},
            {'emotion': 'anxious', 'category': 'mindfulness', 'suggestion': 'Practice box breathing: inhale for 4 counts, hold for 4, exhale for 4, hold for 4.'},
            
            # Stressed
            {'emotion': 'stressed', 'category': 'physical', 'suggestion': 'Take a relaxing bath or shower to release tension.'},
            {'emotion': 'stressed', 'category': 'mental', 'suggestion': 'Make a list of priorities and focus on one task at a time.'},
            {'emotion': 'stressed', 'category': 'mindfulness', 'suggestion': 'Find a quiet space and practice progressive muscle relaxation.'},
            
            # Calm
            {'emotion': 'calm', 'category': 'creative', 'suggestion': 'Use this peaceful state to work on a hobby you enjoy.'},
            {'emotion': 'calm', 'category': 'mindfulness', 'suggestion': 'Practice mindful observation of your surroundings.'},
            {'emotion': 'calm', 'category': 'mental', 'suggestion': 'Set intentions or goals for yourself while in this clear state of mind.'},
            
            # Excited
            {'emotion': 'excited', 'category': 'creative', 'suggestion': 'Channel your energy into planning or starting a new project.'},
            {'emotion': 'excited', 'category': 'physical', 'suggestion': 'Dance or move to your favorite upbeat music.'},
            {'emotion': 'excited', 'category': 'social', 'suggestion': 'Share your enthusiasm with others who support your goals.'},
            
            # Tired
            {'emotion': 'tired', 'category': 'physical', 'suggestion': 'Take a power nap (15-20 minutes) if possible.'},
            {'emotion': 'tired', 'category': 'mental', 'suggestion': 'Prioritize tasks and postpone non-essential activities.'},
            {'emotion': 'tired', 'category': 'mindfulness', 'suggestion': 'Practice gentle stretching or yoga to boost energy.'},
            
            # Confused
            {'emotion': 'confused', 'category': 'mental', 'suggestion': 'Write down your thoughts to help organize them.'},
            {'emotion': 'confused', 'category': 'social', 'suggestion': 'Discuss your thoughts with someone you trust to gain perspective.'},
            {'emotion': 'confused', 'category': 'mindfulness', 'suggestion': 'Take a break and return to the situation with fresh eyes.'},
            
            # Hopeful
            {'emotion': 'hopeful', 'category': 'creative', 'suggestion': 'Create a vision board for your aspirations.'},
            {'emotion': 'hopeful', 'category': 'mental', 'suggestion': 'Write down your goals and break them into actionable steps.'},
            {'emotion': 'hopeful', 'category': 'social', 'suggestion': 'Share your optimism and inspire others.'},
        ]

        for suggestion in suggestions:
            SelfCareSuggestion.objects.get_or_create(
                emotion=suggestion['emotion'],
                category=suggestion['category'],
                suggestion=suggestion['suggestion']
            )
            
        self.stdout.write(self.style.SUCCESS('Successfully added self-care suggestions')) 