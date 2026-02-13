#!/usr/bin/env python3
"""
Main script to send daily LeetCode questions.
This runs via GitHub Actions daily at 9 AM IST.
"""

import json
import os
from datetime import datetime
from config import RANKED_QUESTIONS_FILE
from progress_tracker import get_next_questions, mark_questions_sent, get_stats
from email_sender import send_email

def load_ranked_questions():
    """Load ranked questions from file"""
    try:
        with open(RANKED_QUESTIONS_FILE, 'r') as f:
            data = json.load(f)
            return data['questions']
    except FileNotFoundError:
        print(f" Error: {RANKED_QUESTIONS_FILE} not found!")
        print("Please run 'python prioritizer.py' first to generate rankings.")
        return None

def main():
    """Main function to send daily questions"""
    print(f"\n{'='*70}")
    print(f" Running at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*70}\n")

    try:
        # Load ranked questions
        ranked_questions = load_ranked_questions()
        if not ranked_questions:
            print(" No ranked questions found!")
            return 1

        # Get progress stats
        stats = get_stats()
        print(f" Progress: {stats['total_sent']} questions sent so far")
        print(f" Total questions available: {len(ranked_questions)}")
        print(f" Remaining: {len(ranked_questions) - stats['total_sent']}\n")

        # Get next 2 questions (different difficulties)
        questions = get_next_questions(ranked_questions, count=2)

        if not questions:
            print(" All questions completed! No more questions to send!")
            return 0

        print(f" Selected questions for today:")
        for i, q in enumerate(questions, 1):
            faang = " FAANG" if q.get('asked_by_faang') == 1 else ""
            print(f"  {i}. {q['title']}")
            print(f"     Difficulty: {q['difficulty']} | Score: {q.get('priority_score', 0):.1f} {faang}")

        # Send email
        print("\n Sending email...")
        if send_email(questions):
            # Mark as sent
            question_ids = [q['id'] for q in questions]
            mark_questions_sent(question_ids)
            print(f"\n Successfully sent email!")
            print(f" Total questions sent: {stats['total_sent'] + len(questions)}")
            return 0
        else:
            print("\n Failed to send email")
            return 1

    except Exception as e:
        print(f" Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit(main())