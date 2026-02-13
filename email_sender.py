import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from config import SENDER_EMAIL, SENDER_PASSWORD, RECIPIENT_EMAIL

def create_email_content(questions):
    """Create HTML email content for the questions"""
    html = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 800px; margin: 0 auto; }}
            .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
            .header h1 {{ margin: 0; font-size: 28px; }}
            .header p {{ margin: 10px 0 0 0; opacity: 0.9; }}
            .question {{ border: 2px solid #e0e0e0; margin: 20px; padding: 25px; border-radius: 10px; background-color: #fafafa; }}
            .question h2 {{ color: #333; margin-top: 0; }}
            .difficulty {{ display: inline-block; padding: 6px 12px; border-radius: 5px; color: white; font-weight: bold; font-size: 14px; }}
            .easy {{ background-color: #5cb85c; }}
            .medium {{ background-color: #f0ad4e; }}
            .hard {{ background-color: #d9534f; }}
            .faang-badge {{ display: inline-block; background-color: #ff9800; color: white; padding: 6px 12px; border-radius: 5px; margin-left: 10px; font-weight: bold; font-size: 14px; }}
            .companies {{ background-color: #e3f2fd; padding: 15px; margin: 15px 0; border-radius: 5px; border-left: 4px solid #2196F3; }}
            .companies strong {{ color: #1976D2; }}
            .stats {{ color: #666; font-size: 14px; margin: 15px 0; padding: 10px; background-color: #f5f5f5; border-radius: 5px; }}
            .description {{ background-color: white; padding: 20px; border-left: 4px solid #667eea; margin: 15px 0; white-space: pre-wrap; font-family: 'Courier New', monospace; font-size: 14px; line-height: 1.6; }}
            .solve-button {{ display: inline-block; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 12px 30px; border-radius: 25px; text-decoration: none; margin-top: 15px; font-weight: bold; }}
            .solve-button:hover {{ opacity: 0.9; }}
            .footer {{ text-align: center; margin-top: 30px; padding: 25px; background-color: #f5f5f5; border-radius: 0 0 10px 10px; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🚀 Daily LeetCode Challenge</h1>
            <p>{datetime.now().strftime('%A, %B %d, %Y')}</p>
        </div>
"""

    for i, q in enumerate(questions, 1):
        difficulty_class = q['difficulty'].lower()
        companies = q.get('companies', 'N/A')
        if companies and companies != 'N/A':
            # Limit company list if too long
            company_list = str(companies).split(',')
            if len(company_list) > 10:
                companies = ', '.join(company_list[:10]) + f' and {len(company_list) - 10} more'

        # Truncate description for email
        description = q.get('description', 'No description available')
        if len(description) > 800:
            description = description[:800] + '...\n\n[View full problem on LeetCode]'

        html += f"""
        <div class="question">
            <h2>Question {i}: {q['title']}</h2>
            <p>
                <span class="difficulty {difficulty_class}">{q['difficulty'].upper()}</span>
                {'<span class="faang-badge">⭐ FAANG FAVORITE</span>' if q.get('asked_by_faang') == 1 else ''}
            </p>

            <div class="companies">
                <strong>💼 Asked by:</strong> {companies}
            </div>

            <div class="stats">
                📊 <strong>Frequency:</strong> {q.get('frequency', 0):.1f}/100 |
                👍 <strong>Likes:</strong> {q.get('likes', 0):,} |
                ✅ <strong>Acceptance:</strong> {q.get('acceptance_rate', 0)}% |
                ⭐ <strong>Rating:</strong> {q.get('rating', 0):.1f}
            </div>

            <div class="description">{description}</div>

            <p style="text-align: center;">
                <a href="{q['url']}" class="solve-button" target="_blank">
                    Solve on LeetCode →
                </a>
            </p>
        </div>
"""

    html += """
        <div class="footer">
            <p style="font-size: 18px; margin: 0;"><strong>💪 Keep grinding!</strong></p>
            <p style="color: #666; margin: 10px 0 0 0;"><em>Consistency is the key to mastering DSA.</em></p>
        </div>
    </body>
    </html>
"""

    return html

def send_email(questions):
    """Send email with daily questions"""
    try:
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f" Daily LeetCode - {datetime.now().strftime('%b %d, %Y')}"
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECIPIENT_EMAIL

        # Create HTML content
        html_content = create_email_content(questions)
        html_part = MIMEText(html_content, 'html')
        msg.attach(html_part)

        # Send email
        print(" Connecting to Gmail SMTP...")
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)

        print(f" Email sent successfully to {RECIPIENT_EMAIL}")
        return True

    except Exception as e:
        print(f" Failed to send email: {str(e)}")
        print("\n Troubleshooting tips:")
        print("1. Make sure you're using Gmail App Password (not regular password)")
        print("2. Enable 2FA on your Google account")
        print("3. Generate App Password: Google Account → Security → 2-Step Verification → App passwords")
        return False