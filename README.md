# 📧 LeetCode Daily Challenge Email Automation

Automatically sends 2 LeetCode questions daily at 9 AM IST via email, prioritized by:
- FAANG company frequency
- Question importance/rating
- Number of companies asking
- Popularity (likes)

## 🚀 Setup Instructions

### 1. Fork/Clone this repository

### 2. Generate Gmail App Password
1. Go to [Google Account Security](https://myaccount.google.com/security)
2. Enable **2-Step Verification**
3. Go to **App passwords** and generate one for "Mail"
4. Copy the 16-character password

### 3. Add GitHub Secrets
Go to your repository → **Settings** → **Secrets and variables** → **Actions** → **New repository secret**

Add these 3 secrets:
- `SENDER_EMAIL`: Your Gmail address
- `SENDER_PASSWORD`: The 16-char app password from step 2
- `RECIPIENT_EMAIL`: Email where you want to receive questions (can be same as sender)

### 4. Prepare your data

#### Option A: First time setup (local)
```bash
# Install dependencies
pip install -r requirements.txt

# Generate rankings (run once)
python prioritizer.py

# Test email locally
python send_daily_email.py
```

#### Option B: Commit files to GitHub
```bash
git add leetcode_questions.csv ranked_questions.json progress.json
git commit -m "Initial setup"
git push
```

### 5. Enable GitHub Actions
- Go to **Actions** tab in your repository
- Click "I understand my workflows, go ahead and enable them"

### 6. Test the workflow
- Go to **Actions** → **Send Daily LeetCode Questions** → **Run workflow**
- Click "Run workflow" button to test immediately

## ⏰ Schedule
- Runs daily at **9:00 AM IST** (3:30 AM UTC)
- Modify schedule in `.github/workflows/daily_email.yml` if needed

## 📊 How it works
1. Loads ranked questions from `ranked_questions.json`
2. Selects next 2 unsent questions (different difficulties)
3. Sends beautiful HTML email via Gmail
4. Updates `progress.json` with sent questions
5. Commits progress back to repository

## 🛠️ Local Development

### Test locally:
```bash
# Set environment variables
export SENDER_EMAIL="your@gmail.com"
export SENDER_PASSWORD="your-app-password"
export RECIPIENT_EMAIL="your@gmail.com"

# Run
python send_daily_email.py
```

### Re-prioritize questions:
```bash
python prioritizer.py
```

## 📝 File Structure
- `leetcode_questions.csv` - Your question database
- `ranked_questions.json` - Prioritized questions (generated)
- `progress.json` - Tracks which questions were sent
- `send_daily_email.py` - Main script
- `.github/workflows/daily_email.yml` - GitHub Actions config

## 🔧 Troubleshooting

**Email not sending?**
- Check GitHub Secrets are set correctly
- Verify Gmail App Password is correct
- Check Actions logs for errors

**Wrong timezone?**
- Modify cron schedule in `daily_email.yml`
- Use [crontab.guru](https://crontab.guru/) to calculate UTC time

**Questions repeating?**
- Check `progress.json` is being committed
- Verify GitHub Actions has write permissions

## 📜 License
MIT