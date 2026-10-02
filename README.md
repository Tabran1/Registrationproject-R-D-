# 📱 WhatsApp OTP Registration Project

Register with name, phone and password → get a 6-digit OTP on WhatsApp → verify it.
Built with Python (Flask), MySQL and PyWhatKit.

**Follow the steps in order. Total time: about 30 minutes.**

---

## Step 1: Install Python

1. Download from https://www.python.org/downloads/ and run it.
2. ⚠️ Tick **"Add python.exe to PATH"** before clicking **Install Now**.
3. Check it: open **cmd** (Windows key, type `cmd`, Enter) and run:
   ```
   python --version
   ```
   You should see a version number like `Python 3.12.4`.

## Step 2: Install MySQL + Workbench

1. Download the **bigger** installer from https://dev.mysql.com/downloads/installer/ (click "No thanks, just start my download").
2. Choose **Full** setup and keep clicking **Next / Execute** with the default settings.
3. When it asks for a **Root Password**, set one (e.g. `root1234`) and **write it down**. You need it twice below.

## Step 3: Create the database

1. Open **MySQL Workbench** and double-click **Local instance MySQL80**.
2. Enter your root password.
3. Open a new query tab (**File → New Query Tab**), paste this, and click the ⚡ button:
   ```sql
   CREATE DATABASE college_db;
   USE college_db;

   CREATE TABLE users (
       id INT AUTO_INCREMENT PRIMARY KEY,
       name VARCHAR(100) NOT NULL,
       phone VARCHAR(15) UNIQUE NOT NULL,
       password VARCHAR(255) NOT NULL,
       otp VARCHAR(6) DEFAULT NULL,
       is_verified BOOLEAN DEFAULT FALSE,
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
   );
   ```
   Green ticks at the bottom mean it worked.

## Step 4: Set up the project

1. Right-click the zip → **Extract All**.
2. Open `app.py` in Notepad and change the password to **your MySQL root password**:
   ```python
   'password': 'root1234',
   ```
   Save the file.
3. Open the extracted `whatsapp-otp-project` folder, click its **address bar**, type `cmd` and press Enter. A terminal opens in that folder.
4. Install the libraries:
   ```
   python -m pip install flask pywhatkit mysql-connector-python
   ```
   Wait until you see **"Successfully installed"**.

## Step 5: Log in to WhatsApp Web

1. Open **Chrome** and go to https://web.whatsapp.com
2. On your phone: **WhatsApp → Linked devices → Link a device**, then scan the QR code.

## Step 6: Run it

In the terminal from Step 4:
```
python app.py
```
Keep this window open, then open **http://127.0.0.1:5000** in your browser.

## Step 7: Test it

1. Fill the form. Write the phone number with country code, no spaces, like `+919876543210`. Use your own number for testing.
2. Click **Send WhatsApp OTP**.
3. **Don't touch the keyboard or mouse for about 30 seconds.** A WhatsApp Web tab opens and sends the OTP by itself.
4. Type the OTP from WhatsApp into the page and click **Verify**. You'll see **"Registration Successful!"** 🎉

**To stop:** press `Ctrl + C` in the terminal.
**To run again later:** repeat Step 5 and Step 6 only.

---

## 🛠 Common problems

| Problem | Fix |
|---|---|
| `python is not recognized` | Reinstall Python and tick **Add to PATH** (Step 1). |
| `No module named 'flask'` | Run the `pip install` command from Step 4 again. |
| `Access denied for user 'root'` | The password in `app.py` is wrong (Step 4). |
| `Can't connect to MySQL server` | Press Windows key → type `services` → right-click **MySQL80** → **Start**. |
| `Unknown database 'college_db'` | Do Step 3 again. |
| "Phone number already registered" | In Workbench run: `DELETE FROM college_db.users;` then try again. |
| Tab opens but no message sent | You're not logged in to WhatsApp Web (Step 5), or you touched the keyboard/mouse. Clear the old row (previous fix) and retry. |

---

*Mac users: use `python3` instead of `python`, and install MySQL and Python from their websites.*
*Learning project only: passwords are stored as plain text.*
