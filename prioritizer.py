import pandas as pd
import json
import os
from datetime import datetime
from config import *

def calculate_priority_score(row):
    """Calculate priority score from CSV data only"""
    score = 0

    # FAANG bonus (highest priority)
    if row['asked_by_faang'] == 1:
        score += FAANG_WEIGHT

    # Frequency score (0-100 scale)
    if pd.notna(row['frequency']):
        score += row['frequency'] * FREQUENCY_WEIGHT

    # Rating score
    if pd.notna(row['rating']):
        score += row['rating'] * RATING_WEIGHT

    # Likes score (normalized)
    if pd.notna(row['likes']):
        score += row['likes'] * LIKES_WEIGHT

    # Number of companies asking this question
    if pd.notna(row['companies']) and str(row['companies']).strip():
        company_count = len(str(row['companies']).split(','))
        score += company_count * COMPANY_COUNT_WEIGHT

    return score

def load_and_rank_csv():
    """Load CSV and create ranking based on CSV data only"""
    print(" Loading CSV file...")
    df = pd.read_csv(CSV_FILE_PATH)

    print(f"Total questions in CSV: {len(df)}")

    # Filter out premium questions
    df = df[df['is_premium'] == 0]
    print(f"Non-premium questions: {len(df)}")

    # Calculate priority scores
    print(" Calculating priority scores...")
    df['priority_score'] = df.apply(calculate_priority_score, axis=1)

    # Sort by priority score (highest first)
    df = df.sort_values('priority_score', ascending=False)

    # Statistics
    print(f"\n{'='*60}")
    print(" DATASET STATISTICS:")
    print(f"{'='*60}")
    print(f"Total questions: {len(df)}")
    print(f"FAANG questions: {len(df[df['asked_by_faang'] == 1])}")
    print(f"\nDifficulty distribution:")
    print(df['difficulty'].value_counts())
    print(f"\nTop 5 most frequent questions:")
    for idx, row in df.head(5).iterrows():
        print(f"  {row['title']} | {row['difficulty']} | Score: {row['priority_score']:.2f}")
    print(f"{'='*60}\n")

    return df

def save_ranked_questions(df):
    """Save ranked questions to JSON file"""
    # Convert to list of dicts for JSON serialization
    ranked_data = df.to_dict('records')

    # Handle NaN values
    for question in ranked_data:
        for key, value in question.items():
            if pd.isna(value):
                question[key] = None

    with open(RANKED_QUESTIONS_FILE, 'w') as f:
        json.dump({
            'ranked_at': datetime.now().isoformat(),
            'total_questions': len(ranked_data),
            'ranking_method': 'CSV-based (FAANG, frequency, rating, likes, companies)',
            'questions': ranked_data
        }, f, indent=2)

    print(f" Ranked questions saved to {RANKED_QUESTIONS_FILE}")

def main():
    """Main prioritization workflow"""
    print("\n Starting LeetCode Question Prioritization")
    print("Method: CSV-based ranking (no web search)\n")

    # Load and rank CSV
    df = load_and_rank_csv()

    # Save ranked questions
    save_ranked_questions(df)

    print("\n Prioritization complete!")
    print(f" Results saved to: {RANKED_QUESTIONS_FILE}")

    # Show top 20 questions
    print(f"\n{'='*60}")
    print(" TOP 20 QUESTIONS (by priority score):")
    print(f"{'='*60}")
    for i, (idx, row) in enumerate(df.head(20).iterrows(), 1):
        faang_badge = " FAANG" if row['asked_by_faang'] == 1 else ""
        print(f"{i:2d}. {row['title']:<50} | {row['difficulty']:<6} | Score: {row['priority_score']:>6.1f} {faang_badge}")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    main()