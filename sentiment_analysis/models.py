from django.db import models

class SentimentEntry(models.Model):
    text = models.TextField()
    sentiment = models.CharField(max_length=20, choices=[
        ('positive', 'Positive'),
        ('neutral', 'Neutral'),
        ('negative', 'Negative')
    ])
    emotion = models.CharField(max_length=50, choices=[
        ('happy', 'Happy'),
        ('sad', 'Sad'),
        ('angry', 'Angry'),
        ('anxious', 'Anxious'),
        ('stressed', 'Stressed'),
        ('calm', 'Calm'),
        ('excited', 'Excited'),
        ('tired', 'Tired'),
        ('confused', 'Confused'),
        ('hopeful', 'Hopeful')
    ], default='neutral')
    intensity = models.FloatField(default=0.0)  # For storing sentiment intensity
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.text[:50]} - {self.emotion} ({self.sentiment})"

class SelfCareSuggestion(models.Model):
    emotion = models.CharField(max_length=50, choices=[
        ('happy', 'Happy'),
        ('sad', 'Sad'),
        ('angry', 'Angry'),
        ('anxious', 'Anxious'),
        ('stressed', 'Stressed'),
        ('calm', 'Calm'),
        ('excited', 'Excited'),
        ('tired', 'Tired'),
        ('confused', 'Confused'),
        ('hopeful', 'Hopeful')
    ])
    suggestion = models.TextField()
    category = models.CharField(max_length=50, choices=[
        ('physical', 'Physical Activity'),
        ('mental', 'Mental Wellness'),
        ('social', 'Social Connection'),
        ('creative', 'Creative Expression'),
        ('mindfulness', 'Mindfulness')
    ])
    
    @property
    def icon_class(self):
        """Return the appropriate Font Awesome icon class based on category."""
        icon_mapping = {
            'physical': 'fa-running',
            'mental': 'fa-brain',
            'social': 'fa-users',
            'creative': 'fa-paint-brush',
            'mindfulness': 'fa-medkit',
            'relaxation': 'fa-couch',
            'nutrition': 'fa-apple-alt',
            'sleep': 'fa-bed'
        }
        return icon_mapping.get(self.category.lower(), 'fa-heart')  # Default to fa-heart
    
    def __str__(self):
        return f"{self.emotion} - {self.category}"

# Create your models here.
