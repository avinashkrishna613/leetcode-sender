import os

# Email Configuration (from GitHub Secrets)
SENDER_EMAIL = os.environ.get('SENDER_EMAIL', 'your_email@gmail.com')
SENDER_PASSWORD = os.environ.get('SENDER_PASSWORD', 'your_app_password')
RECIPIENT_EMAIL = os.environ.get('RECIPIENT_EMAIL', 'your_email@gmail.com')

# File Paths
CSV_FILE_PATH = "leetcode_dataset-lc.csv"
PROGRESS_FILE = "progress.json"
RANKED_QUESTIONS_FILE = "ranked_questions.json"

# Prioritization Settings
FAANG_WEIGHT = 100
FREQUENCY_WEIGHT = 2.0
LIKES_WEIGHT = 0.01
COMPANY_COUNT_WEIGHT = 5.0
RATING_WEIGHT = 10.0