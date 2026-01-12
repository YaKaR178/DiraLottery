from playwright.sync_api import sync_playwright
import requests
import os
import sys

# קריאת משתני סביבה (עובד גם ב-GitHub Actions וגם מקומית)
USERNAME = os.getenv("LOTTERY_USERNAME", "")
PASSWORD = os.getenv("LOTTERY_PASSWORD", "")
LOTTERY_NUMBER = os.getenv("LOTTERY_NUMBER", "")

# פרטי טלגרם
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

# קובץ לשמירת המיקום הקודם
POSITION_FILE = os.getenv("POSITION_FILE", "last_position.txt")

# בדיקה שכל המשתנים החיוניים הוגדרו
required_vars = {
    "LOTTERY_USERNAME": USERNAME,
    "LOTTERY_PASSWORD": PASSWORD,
    "LOTTERY_NUMBER": LOTTERY_NUMBER,
    "TELEGRAM_BOT_TOKEN": TELEGRAM_BOT_TOKEN,
    "TELEGRAM_CHAT_ID": TELEGRAM_CHAT_ID
}

missing_vars = [var for var, value in required_vars.items() if not value]
if missing_vars:
    print(f"❌ שגיאה: המשתנים הבאים לא הוגדרו: {', '.join(missing_vars)}")
    print("אנא הגדר אותם כמשתני סביבה או ב-GitHub Secrets")
    sys.exit(1)

def send_telegram_message(message):
    """שליחת הודעה לטלגרם"""
    if not TELEGRAM_CHAT_ID:
        print("⚠️  TELEGRAM_CHAT_ID לא הוגדר - לא ניתן לשלוח הודעה")
        return False
    
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    
    try:
        response = requests.post(url, json=data, timeout=10)
        if response.status_code == 200:
            print("✅ הודעה נשלחה בהצלחה לטלגרם")
            return True
        else:
            print(f"❌ שגיאה בשליחת הודעה: {response.status_code}")
            print(response.text)
            return False
    except Exception as e:
        print(f"❌ שגיאה בשליחת הודעה: {e}")
        return False

def get_last_position():
    """קריאת המיקום הקודם מהקובץ"""
    if os.path.exists(POSITION_FILE):
        try:
            with open(POSITION_FILE, 'r', encoding='utf-8') as f:
                return f.read().strip()
        except:
            return None
    return None

def save_position(position):
    """שמירת המיקום הנוכחי לקובץ"""
    try:
        with open(POSITION_FILE, 'w', encoding='utf-8') as f:
            f.write(str(position))
    except Exception as e:
        print(f"❌ שגיאה בשמירת המיקום: {e}")

def get_telegram_chat_id():
    """פונקציה עזר לקבלת Chat ID - להריץ פעם אחת"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('ok') and data.get('result'):
                updates = data['result']
                if updates:
                    # לקחת את ה-Chat ID האחרון
                    chat_id = updates[-1]['message']['chat']['id']
                    print(f"📱 Chat ID שלך: {chat_id}")
                    print(f"העתק את המספר הזה והדבק ב-TELEGRAM_CHAT_ID בקוד")
                    return chat_id
                else:
                    print("⚠️  לא נמצאו הודעות. שלח הודעה לבוט שלך ונסה שוב.")
            else:
                print("❌ שגיאה בקבלת נתונים מהבוט")
        else:
            print(f"❌ שגיאה: {response.status_code}")
    except Exception as e:
        print(f"❌ שגיאה: {e}")
    return None

with sync_playwright() as p:
    # מצב headless לעבודה ב-Task Scheduler
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    # 1. כניסה לאתר
    page.goto("https://www.dira.moch.gov.il/", timeout=60000)
    
    # המתנה לטעינה מלאה של העמוד
    page.wait_for_load_state("networkidle", timeout=60000)

    # 2. התחברות
    print("מחכה לשדות ההתחברות...")
    page.wait_for_selector("#loginNumber", timeout=30000)
    page.wait_for_selector("#loginPassword", timeout=30000)
    page.fill("#loginNumber", USERNAME)
    page.fill("#loginPassword", PASSWORD)
    
    print("מחפש קישור 'כניסה'...")
    # המתנה לקישור להופיע לפני לחיצה (זה קישור <a> לא כפתור)
    page.wait_for_selector('a:has-text("כניסה")', timeout=30000)
    print("קישור נמצא! לוחץ...")
    page.click('a:has-text("כניסה")')

    # 3. המתנה להופעת ההודעה ולחיצה על אישור
    print("מחכה להופעת ההודעה...")
    page.wait_for_selector('div.modal.fade.ng-isolate-scope.in div.modal-footer button', timeout=30000)
    print("לוחץ על אישור בהודעה...")
    page.click('div.modal.fade.ng-isolate-scope.in div.modal-footer button')
    
    # המתנה קצרה לסגירת ההודעה
    page.wait_for_timeout(1000)

    # 4. מעבר דרך סרגל הכלים - לחיצה על האזור האישי
    print("לוחץ על 'האזור האישי'...")
    page.wait_for_selector('#navbar > ul > li:nth-child(9) > a', timeout=30000)
    page.click('#navbar > ul > li:nth-child(9) > a')
    
    # 5. לחיצה על "ההגרלות שלי"
    print("לוחץ על 'ההגרלות שלי'...")
    page.wait_for_selector('#navbar > ul > li:nth-child(9) > ul > li:nth-child(1) > a', timeout=30000)
    page.click('#navbar > ul > li:nth-child(9) > ul > li:nth-child(1) > a')
    
    # המתנה לטעינה מלאה
    page.wait_for_load_state("networkidle")

    # 6. חיפוש לפי מספר הגרלה
    page.wait_for_selector("#lotteryNumber", timeout=30000)
    page.fill("#lotteryNumber", LOTTERY_NUMBER)
    
    # לחיצה על כפתור החיפוש
    page.wait_for_selector('#divView > div > div.row.col-lg-12.col-md-12.col-xs-12.dark-blue-box > div:nth-child(4) > a', timeout=30000)
    page.click('#divView > div > div.row.col-lg-12.col-md-12.col-xs-12.dark-blue-box > div:nth-child(4) > a')

    # 7. המתנה לעדכון הטבלה - מחכים שהטבלה תתעדכן לאחר הפילטר
    page.wait_for_timeout(3000)  # המתנה לעיבוד הפילטר
    page.wait_for_selector("#lotteriesList tbody tr", timeout=30000)

    # 8. שליפת מיקום הזכייה מהעמודה הנכונה
    # חשוב: הקוד רק קורא נתונים - לא לוחץ על כלום! (רק inner_text ו-get_attribute)
    
    # המתנה שהטבלה תתעדכן לאחר החיפוש
    page.wait_for_timeout(1000)
    
    # חפש את השורה הספציפית שמכילה את מספר הגרלה שהמשתמש חיפש
    # ננסה מספר דרכים למצוא את השורה
    try:
        row_locator = page.locator("#lotteriesList tbody tr").filter(has_text=LOTTERY_NUMBER).first
        row_locator.wait_for(state="visible", timeout=10000)
    except:
        # אם לא מצא, נסה לחכות שהטבלה תתעדכן יותר זמן
        page.wait_for_timeout(2000)
        row_locator = page.locator("#lotteriesList tbody tr").filter(has_text=LOTTERY_NUMBER).first
        row_locator.wait_for(state="visible", timeout=15000)
    
    # שליפת המיקום בתור מהתא הנכון
    position = row_locator.locator("td[data-title='**מקומך בתור']").inner_text()
    
    # ניקוי רווחים אם יש
    position = position.strip()

    # קריאת המיקום הקודם
    last_position = get_last_position()
    
    # בדיקה אם המיקום השתנה
    if last_position is None:
        # זו הפעם הראשונה - שמור את המיקום
        print(f"📍 זו הפעם הראשונה - המיקום הנוכחי: {position}")
        save_position(position)
    elif last_position != position:
        # המיקום השתנה - שלח הודעה
        print(f"🔄 המיקום השתנה! {last_position} -> {position}")
        
        # יצירת הודעת טלגרם
        message = f"מיקומך בתור לדירה בהנחה בנתניה מספר הגרלה {LOTTERY_NUMBER}: {position}"
        
        # שליחת הודעה לטלגרם
        send_telegram_message(message)
        
        # שמירת המיקום החדש
        save_position(position)
    else:
        # המיקום לא השתנה
        print(f"✅ המיקום לא השתנה: {position}")
    
    # הדפסת התוצאה
    print(position)

    browser.close()

# אם תרצה לקבל את Chat ID, הרץ את השורה הבאה (לאחר שתשלח הודעה לבוט):
# get_telegram_chat_id()
