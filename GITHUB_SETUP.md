# מדריך הגדרה ל-GitHub

## שלב 1: יצירת Repository ב-GitHub

1. לך ל-[GitHub](https://github.com) והתחבר לחשבון שלך
2. לחץ על הכפתור הירוק **New** (או **+** → **New repository**)
3. מלא את הפרטים:
   - **Repository name**: `diraLottery` (או כל שם אחר)
   - **Description**: "בוט לבדיקת מיקום בהגרלת דירות"
   - בחר **Private** (מומלץ) או **Public**
   - אל תסמן את "Initialize with README" (כי כבר יש לנו קבצים)
4. לחץ על **Create repository**

## שלב 2: העלאת הקוד ל-GitHub

### אופציה A: דרך Git Command Line

```bash
# נווט לתיקיית הפרויקט
cd C:\Users\Eli Yakar\Documents\diraLottery

# אתחל repository מקומי
git init

# הוסף את כל הקבצים
git add .

# צור commit ראשון
git commit -m "Initial commit: Lottery position checker"

# הוסף את ה-remote של GitHub (החלף <your-username> ו-<repo-name>)
git remote add origin https://github.com/<your-username>/<repo-name>.git

# העלה את הקוד
git branch -M main
git push -u origin main
```

**אם אתה רוצה להעלות לחשבון אחר:**

1. **התחבר לחשבון ה-GitHub האחר** ב-GitHub Desktop או דרך הדפדפן
2. צור repository חדש בחשבון הזה (שלב 1)
3. אם כבר יש לך repository מקומי עם remote אחר, שנה את ה-URL:

```bash
# בדוק את ה-remote הנוכחי
git remote -v

# שנה את ה-URL לחשבון החדש (החלף <new-username> ו-<repo-name>)
git remote set-url origin https://github.com/<new-username>/<repo-name>.git

# או אם זה repository חדש לגמרי, מחק את ה-remote הישן והוסף חדש:
git remote remove origin
git remote add origin https://github.com/<new-username>/<repo-name>.git

# העלה את הקוד
git push -u origin main
```

### אופציה B: דרך GitHub Desktop

1. הורד והתקן [GitHub Desktop](https://desktop.github.com/)
2. **התחבר לחשבון ה-GitHub הרצוי**:
   - לחץ על **File** → **Options** → **Accounts**
   - לחץ על **Sign out** אם אתה מחובר לחשבון אחר
   - לחץ על **Sign in** והתחבר לחשבון הרצוי
3. פתח את GitHub Desktop
4. לחץ על **File** → **Add Local Repository**
5. בחר את התיקייה `C:\Users\Eli Yakar\Documents\diraLottery`
6. לחץ על **Publish repository**
7. בחר את ה-repository שיצרת ב-GitHub (בחשבון החדש)
8. לחץ על **Publish Repository**

**אם כבר יש לך repository מקומי:**
1. פתח את GitHub Desktop
2. לחץ על **Repository** → **Repository Settings**
3. לחץ על **Remote** ושנה את ה-URL לחשבון החדש
4. או לחץ על **File** → **Options** → **Git** ושנה את החשבון

## שלב 3: הגדרת GitHub Secrets

1. לך ל-repository שלך ב-GitHub
2. לחץ על **Settings** (בתפריט העליון)
3. בתפריט הצד, לחץ על **Secrets and variables** → **Actions**
4. לחץ על **New repository secret**

הוסף את המשתנים הבאים (לחץ על **New repository secret** לכל אחד):

### 1. LOTTERY_USERNAME
- **Name**: `LOTTERY_USERNAME`
- **Secret**: `314963364`
- לחץ **Add secret**

### 2. LOTTERY_PASSWORD
- **Name**: `LOTTERY_PASSWORD`
- **Secret**: `Yakar3364`
- לחץ **Add secret**

### 3. LOTTERY_NUMBER
- **Name**: `LOTTERY_NUMBER`
- **Secret**: `2591`
- לחץ **Add secret**

### 4. TELEGRAM_BOT_TOKEN
- **Name**: `TELEGRAM_BOT_TOKEN`
- **Secret**: `8441298085:AAGgqBjU7sPUgZ70B-wUJnZjsk16gs-hHUc`
- לחץ **Add secret**

### 5. TELEGRAM_CHAT_ID
- **Name**: `TELEGRAM_CHAT_ID`
- **Secret**: `6386268689`
- לחץ **Add secret**

## שלב 4: בדיקת ה-Workflow

1. לך ל-tab **Actions** ב-GitHub repository שלך
2. לחץ על **Lottery Position Check** בתפריט הצד
3. לחץ על **Run workflow** (כפתור כחול למעלה מימין)
4. בחר את ה-branch **main**
5. לחץ על **Run workflow**

הקוד ירוץ עכשיו ותוכל לראות את הלוגים בזמן אמת.

## שלב 5: הגדרת הרצה אוטומטית

ה-workflow כבר מוגדר לרוץ מדי יום בשעה 10:00 UTC (12:00 שעון ישראל בחורף).

אם תרצה לשנות את השעה, ערוך את הקובץ `.github/workflows/lottery-check.yml`:

```yaml
schedule:
  # פורמט: דקה שעה יום חודש יום-שבוע
  # דוגמה: 10:00 UTC = 12:00 ישראל בחורף
  - cron: '0 10 * * *'  # שנה את המספרים לפי הצורך
```

### טבלת המרת שעות (UTC → ישראל):
- 10:00 UTC = 12:00 ישראל (חורף) / 13:00 ישראל (קיץ)
- 08:00 UTC = 10:00 ישראל (חורף) / 11:00 ישראל (קיץ)
- 12:00 UTC = 14:00 ישראל (חורף) / 15:00 ישראל (קיץ)

## בדיקת סטטוס

לבדוק מתי הקוד רץ בפעם האחרונה:
1. לך ל-tab **Actions**
2. לחץ על ה-run האחרון
3. תראה את הלוגים והתוצאות

## פתרון בעיות

### ה-workflow לא רץ

1. ודא שכל ה-Secrets הוגדרו נכון
2. בדוק את הלוגים ב-tab **Actions**
3. ודא שה-workflow מופעל (יש סימון ירוק ליד השם)

### שגיאת "Missing secrets"

ודא שהוספת את כל ה-5 Secrets:
- LOTTERY_USERNAME
- LOTTERY_PASSWORD
- LOTTERY_NUMBER
- TELEGRAM_BOT_TOKEN
- TELEGRAM_CHAT_ID

### הקוד לא מוצא את המשתנים

ודא שהשמות של ה-Secrets זהים בדיוק למה שמופיע ב-workflow file.

## עדכון הקוד

כשאתה משנה את הקוד:

```bash
git add .
git commit -m "תיאור השינויים"
git push
```

ה-workflow יעדכן אוטומטית.

## אבטחה

✅ כל הפרטים הרגישים נשמרים ב-GitHub Secrets (מוצפנים)
✅ הקובץ `last_position.txt` לא יועלה ל-GitHub (נמצא ב-.gitignore)
✅ ה-repository יכול להיות Private

## תמיכה

אם יש בעיות, בדוק את הלוגים ב-tab **Actions** ב-GitHub.

