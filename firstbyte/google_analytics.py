import os

def ga_tracking_id(request):
    return {'GA_TRACKING_ID': os.environ.get('GA_TRACKING_ID')}