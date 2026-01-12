# Lottery Position Checker

בוט אוטומטי לבדיקת מיקום בהגרלת דירות ומשלוח התראות בטלגרם כשהמיקום משתנה.

## תכונות

- ✅ בדיקה אוטומטית של מיקום בהגרלה
- ✅ התראות טלגרם כשהמיקום משתנה
- ✅ הרצה אוטומטית מדי יום דרך GitHub Actions
- ✅ שמירה מאובטחת של פרטי התחברות כמשתני סביבה

## הגדרה

### 1. העתקת הפרויקט

```bash
git clone <your-repo-url>
cd diraLottery
```

### 2. התקנת תלויות

```bash
pip install -r requirements.txt
playwright install chromium
```

### 3. הגדרת משתני סביבה

#### עבור הרצה מקומית:

צור קובץ `.env` (או הגדר משתני סביבה במערכת):

```bash
export LOTTERY_USERNAME="your_username"
export LOTTERY_PASSWORD="your_password"
export LOTTERY_NUMBER="your_lottery_number"
export TELEGRAM_BOT_TOKEN="your_bot_token"
export TELEGRAM_CHAT_ID="your_chat_id"
```

#### עבור GitHub Actions:

1. לך ל-repository שלך ב-GitHub
2. לחץ על **Settings** → **Secrets and variables** → **Actions**
3. לחץ על **New repository secret** והוסף את המשתנים הבאים:
   - `LOTTERY_USERNAME` - שם המשתמש לאתר
   - `LOTTERY_PASSWORD` - סיסמת האתר
   - `LOTTERY_NUMBER` - מספר הגרלה
   - `TELEGRAM_BOT_TOKEN` - Token של בוט טלגרם
   - `TELEGRAM_CHAT_ID` - Chat ID בטלגרם

### 4. קבלת Telegram Bot Token

1. פתח את טלגרם וחפש `@BotFather`
2. שלח `/newbot` ועקוב אחר ההוראות
3. העתק את ה-Token שהתקבל

### 5. קבלת Telegram Chat ID

1. שלח הודעה לבוט שיצרת
2. פתח בדפדפן: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
3. מצא את `"chat":{"id":123456789}` - זה ה-Chat ID שלך

## הרצה

### הרצה מקומית:

```bash
python lotteryCheck.py
```

### הרצה דרך GitHub Actions:

הקוד ירוץ אוטומטית מדי יום בשעה 10:00 UTC (12:00 שעון ישראל בחורף).

ניתן גם להריץ ידנית:
1. לך ל-tab **Actions** ב-GitHub
2. בחר את ה-workflow **Lottery Position Check**
3. לחץ על **Run workflow**

## איך זה עובד

1. **הרצה ראשונה**: הקוד שומר את המיקום הנוכחי (לא שולח הודעה)
2. **הרצות נוספות**: הקוד בודק אם המיקום השתנה
   - אם לא השתנה: לא שולח הודעה
   - אם השתנה: שולח הודעה לטלגרם עם המיקום החדש

## הודעת טלגרם

כשהמיקום משתנה, תקבל הודעה בטלגרם:
```
מיקומך בתור לדירה בהנחה בנתניה מספר הגרלה 2591: [המיקום החדש]
```

## קבצים

- `lotteryCheck.py` - הקוד הראשי
- `requirements.txt` - תלויות Python
- `.github/workflows/lottery-check.yml` - הגדרת GitHub Actions
- `last_position.txt` - קובץ לשמירת המיקום הקודם (נוצר אוטומטית)

## אבטחה

- כל הפרטים הרגישים נשמרים כמשתני סביבה
- הקובץ `last_position.txt` נמצא ב-`.gitignore` ולא יועלה ל-GitHub
- GitHub Secrets מוצפנים ומאובטחים

## פתרון בעיות

### הקוד לא מוצא את המשתנים

ודא שהגדרת את כל המשתנים הנדרשים ב-GitHub Secrets או כמשתני סביבה מקומיים.

### שגיאת Playwright

ודא שהתקנת את הדפדפנים:
```bash
playwright install chromium
```

### הודעות טלגרם לא מגיעות

1. ודא שה-Bot Token נכון
2. ודא שה-Chat ID נכון
3. ודא ששלחת הודעה לבוט לפחות פעם אחת

## רישיון

פרויקט זה הוא לשימוש אישי בלבד.

