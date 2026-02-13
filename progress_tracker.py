import json
import os
from datetime import datetime
from config import PROGRESS_FILE

def load_progress():
    """Load progress from JSON file"""
    if not os.path.exists(PROGRESS_FILE):
        return {
            'sent_questions': [],
            'last_sent_date': None,
            'total_sent': 0
        }

    with open(PROGRESS_FILE, 'r') as f:
        return json.load(f)

def save_progress(progress):
    """Save progress to JSON file"""
    with open(PROGRESS_FILE, 'w') as f:
        json.dump(progress, f, indent=2)

def mark_questions_sent(question_ids):
    """Mark questions as sent"""
    progress = load_progress()

    for qid in question_ids:
        if qid not in progress['sent_questions']:
            progress['sent_questions'].append(qid)

    progress['last_sent_date'] = datetime.now().isoformat()
    progress['total_sent'] = len(progress['sent_questions'])

    save_progress(progress)

    print(f" Progress updated: {len(progress['sent_questions'])} total questions sent")

def get_next_questions(ranked_questions, count=2):
    """Get next unsent questions with different difficulties"""
    progress = load_progress()
    sent_ids = set(progress['sent_questions'])

    # Filter out sent questions
    unsent = [q for q in ranked_questions if q['id'] not in sent_ids]

    if len(unsent) < count:
        print(f"  Warning: Only {len(unsent)} unsent questions remaining!")
        if len(unsent) == 0:
            return []
        count = len(unsent)

    # Select questions with different difficulties
    selected = []
    difficulties_used = set()

    for question in unsent:
        if question['difficulty'] not in difficulties_used:
            selected.append(question)
            difficulties_used.add(question['difficulty'])

        if len(selected) == count:
            break

    # If we couldn't find enough different difficulties, just pick top unsent
    while len(selected) < count and len(selected) < len(unsent):
        for q in unsent:
            if q not in selected:
                selected.append(q)
                break

    return selected

def get_stats():
    """Get progress statistics"""
    progress = load_progress()
    return {
        'total_sent': progress['total_sent'],
        'last_sent': progress['last_sent_date'],
        'sent_ids': progress['sent_questions']
    }