"""Script to create and validate ml/data/handwritten_test.csv for Task T6."""
import csv
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CSV_PATH = os.path.join(ROOT, "ml", "data", "handwritten_test.csv")

DATA = [
    # ---------------- 1. bank_kyc_account (4 rows) ----------------
    {
        "text": "Dear Customer your SBI account has been suspended due to pending KYC documents. Update PAN immediately to avoid permanent blockage: http://sbi-kyc-update.example.xyz/pan",
        "label_scam": "1",
        "category": "bank_kyc_account",
        "has_url": "1"
    },
    {
        "text": "HDFC Alert: Your NetBanking service is disabled. Kindly re-verify your KYC within 12 hrs by visiting http://hdfc-verify-portal.example.in",
        "label_scam": "1",
        "category": "bank_kyc_account",
        "has_url": "1"
    },
    {
        "text": "Urgent msg: Apka ICICI bank khata aadhar link na hone ke karan block ho gaya hai. Turant aadhar update kare http://icici-aadhaar-link.example.org",
        "label_scam": "1",
        "category": "bank_kyc_account",
        "has_url": "1"
    },
    {
        "text": "Dear User, your PNB account will be deactivated tonight. Send 16 digit debit card no and ATM pin for immediate online verification.",
        "label_scam": "1",
        "category": "bank_kyc_account",
        "has_url": "0"
    },

    # ---------------- 2. upi_payment (4 rows) ----------------
    {
        "text": "Congratulations! You received Rs 2,500 cashback in GooglePay. Click here to approve collect request and enter UPI PIN: http://gpay-reward-collect.example.xyz",
        "label_scam": "1",
        "category": "upi_payment",
        "has_url": "1"
    },
    {
        "text": "Sir I have sent 5000 by mistake on your PhonePe. Pls accept the collect request and enter PIN to return the money immediately.",
        "label_scam": "1",
        "category": "upi_payment",
        "has_url": "0"
    },
    {
        "text": "Scan this attached QR code in Paytm app to receive your OLX sofa advance payment of Rs 4000 directly into your bank.",
        "label_scam": "1",
        "category": "upi_payment",
        "has_url": "0"
    },
    {
        "text": "Your BHIM UPI refund of Rs 1,499 is pending authorization. Click http://bhim-refund-auth.example.net/accept and enter 6 digit UPI pin.",
        "label_scam": "1",
        "category": "upi_payment",
        "has_url": "1"
    },

    # ---------------- 3. cashback_reward_lottery (4 rows) ----------------
    {
        "text": "KBC Jio Lucky Draw: Congratulations apko mila hai 25 Lakh ka lottery prize. Claim karne ke liye click kare http://kbc-jio-lottery.example.com",
        "label_scam": "1",
        "category": "cashback_reward_lottery",
        "has_url": "1"
    },
    {
        "text": "Dear user, you have won Rs 50,000 Flipkart festive scratch card reward! Claim your voucher before midnight at http://flipkart-scratch-win.example.org/claim",
        "label_scam": "1",
        "category": "cashback_reward_lottery",
        "has_url": "1"
    },
    {
        "text": "Special Diwali Bonus: You have 9,450 unredeemed reward points worth Rs 4,725 expiring today. Redeem instantly into your bank at http://reward-points-cash.example.net",
        "label_scam": "1",
        "category": "cashback_reward_lottery",
        "has_url": "1"
    },
    {
        "text": "Maha bumper prize winner! Your mobile number won Maruti Alto car in annual shoppers draw. Pay processing registration fee of Rs 3,500 to dispatch.",
        "label_scam": "1",
        "category": "cashback_reward_lottery",
        "has_url": "0"
    },

    # ---------------- 4. job (4 rows) ----------------
    {
        "text": "Work from Home Opportunity: Earn Rs 3000 to Rs 8000 daily by simply liking YouTube videos and rating hotels on Google. Join Telegram: http://t-telegram.example.xyz/earn-daily",
        "label_scam": "1",
        "category": "job",
        "has_url": "1"
    },
    {
        "text": "Amazon HR Team: Part-time data entry job available for students and homemakers. Daily payout Rs 2500. No experience needed. Contact HR coordinator.",
        "label_scam": "1",
        "category": "job",
        "has_url": "0"
    },
    {
        "text": "Selected for Indigo Airlines ground staff position. Salary 45,000/pm plus perks. Transfer uniform fee and security deposit Rs 2,200 for appointment letter.",
        "label_scam": "1",
        "category": "job",
        "has_url": "0"
    },
    {
        "text": "Earn 1500 per review in your free time. Complete 5 demo tasks and get paid instantly to UPI. Click http://parttime-reviews.example.org/register",
        "label_scam": "1",
        "category": "job",
        "has_url": "1"
    },

    # ---------------- 5. investment (4 rows) ----------------
    {
        "text": "Exclusive Institutional VIP stock tips group! 100% guaranteed 40% monthly returns on multibagger shares. Join now: http://institutional-wealth-club.example.com/join",
        "label_scam": "1",
        "category": "investment",
        "has_url": "1"
    },
    {
        "text": "Invest in our automated crypto arbitrage trading bot. Deposit Rs 10000 and withdraw daily guaranteed profit of Rs 1200. Zero risk 100% safe.",
        "label_scam": "1",
        "category": "investment",
        "has_url": "0"
    },
    {
        "text": "SEBI approved high-yield private placement scheme open for select investors. Double your capital in 45 days. Contact relationship manager on Telegram.",
        "label_scam": "1",
        "category": "investment",
        "has_url": "0"
    },
    {
        "text": "Forex trading platform special promotion: Deposit $100 get $300 bonus credit. Guaranteed profit withdrawal within 24 hours. Sign up http://fx-trading-gold.example.xyz",
        "label_scam": "1",
        "category": "investment",
        "has_url": "1"
    },

    # ---------------- 6. loan (4 rows) ----------------
    {
        "text": "Instant Personal Loan approved up to Rs 5,00,000 with 0% interest and no CIBIL check. Download quick cash loan app: http://instant-credit-app.example.xyz/get",
        "label_scam": "1",
        "category": "loan",
        "has_url": "1"
    },
    {
        "text": "Pre-approved emergency paperless loan of Rs 2,00,000 is ready for disbursal. Pay 1% file processing charge Rs 2000 to release loan amount.",
        "label_scam": "1",
        "category": "loan",
        "has_url": "0"
    },
    {
        "text": "Need quick cash without documentation? Get 50k in 5 mins directly in bank account. Download APK from http://speedy-rupee-loan.example.org/download",
        "label_scam": "1",
        "category": "loan",
        "has_url": "1"
    },
    {
        "text": "Dear Customer, your Mudra loan subsidy of Rs 3,50,000 has been sanctioned by government. Submit approval fee Rs 1,500 to sanction officer.",
        "label_scam": "1",
        "category": "loan",
        "has_url": "0"
    },

    # ---------------- 7. delivery (4 rows) ----------------
    {
        "text": "IndiaPost: Your package IND938201 could not be delivered due to wrong address details. Update address and pay re-delivery fee Rs 48: http://indiapost-parcel-update.example.xyz",
        "label_scam": "1",
        "category": "delivery",
        "has_url": "1"
    },
    {
        "text": "BlueDart Delivery alert: Shipment pending at sorting facility. Address incomplete. Update your delivery pin code within 24 hours at http://bluedart-redirection.example.org",
        "label_scam": "1",
        "category": "delivery",
        "has_url": "1"
    },
    {
        "text": "Customs clearance notice: An international parcel sent from UK containing electronics is detained at Mumbai airport. Pay custom clearance duty Rs 8,500 to release.",
        "label_scam": "1",
        "category": "delivery",
        "has_url": "0"
    },
    {
        "text": "DTDC Courier: Urgent delivery pending for consignment 847291. Reschedule delivery slot by paying Rs 25 online at http://dtdc-express-slot.example.net",
        "label_scam": "1",
        "category": "delivery",
        "has_url": "1"
    },

    # ---------------- 8. gov_police_impersonation (4 rows) ----------------
    {
        "text": "CBI Investigation Notice: An illegal contraband courier containing banned substances was booked with your Aadhaar. Digital arrest warrant issued. Contact officer immediately on Skype.",
        "label_scam": "1",
        "category": "gov_police_impersonation",
        "has_url": "0"
    },
    {
        "text": "Delhi Police Cyber Cell: Your mobile number is implicated in illegal money laundering transactions. Join video interrogation room http://cybercell-investigation.example.xyz/call or face physical arrest.",
        "label_scam": "1",
        "category": "gov_police_impersonation",
        "has_url": "1"
    },
    {
        "text": "DoT / TRAI Notice: All telecom services and SIM cards issued to your Aadhaar will be disconnected within 2 hours by order of Supreme Court. Dial 9 to connect with verification officer.",
        "label_scam": "1",
        "category": "gov_police_impersonation",
        "has_url": "0"
    },
    {
        "text": "Income Tax Department Alert: Tax evasion penalty case filed against you. Settle outstanding recovery amount Rs 45,000 under amnesty scheme at http://incometax-recovery-portal.example.xyz",
        "label_scam": "1",
        "category": "gov_police_impersonation",
        "has_url": "1"
    },

    # ---------------- 9. tech_support (4 rows) ----------------
    {
        "text": "Microsoft Windows Security: Critical Trojan virus detected on your computer IP address. Your files are being locked. Call Microsoft certified support helpline immediately.",
        "label_scam": "1",
        "category": "tech_support",
        "has_url": "0"
    },
    {
        "text": "Warning: Your Android phone is infected with 7 high-risk spyware viruses. Download official antivirus scanner immediately: http://device-cleaner-antivirus.example.xyz/fix",
        "label_scam": "1",
        "category": "tech_support",
        "has_url": "1"
    },
    {
        "text": "Google Account Alert: Unauthorized login attempt from Russia detected. Secure your Gmail account immediately and verify security credentials at http://google-security-recovery.example.org",
        "label_scam": "1",
        "category": "tech_support",
        "has_url": "1"
    },
    {
        "text": "WhatsApp Support: Your account will be deleted in 24 hours due to community violations. Install security update tool from http://whatsapp-support-patch.example.net to restore access.",
        "label_scam": "1",
        "category": "tech_support",
        "has_url": "1"
    },

    # ---------------- 10. other (4 rows) ----------------
    {
        "text": "Electricity Department Warning: Power supply to your connection will be disconnected tonight at 9:30 PM due to unpaid previous month bill. Call electricity officer immediately.",
        "label_scam": "1",
        "category": "other",
        "has_url": "0"
    },
    {
        "text": "Challan Alert: Traffic e-challan MH-02 fine of Rs 1,000 is pending on vehicle. Pay immediately to avoid court summons: http://echallan-parivahan-pay.example.xyz/mumbai",
        "label_scam": "1",
        "category": "other",
        "has_url": "1"
    },
    {
        "text": "Dear user your matrimonial profile on Shaadi.com has 5 premium interests from NRI profiles. Pay verification token Rs 1200 to view contact details.",
        "label_scam": "1",
        "category": "other",
        "has_url": "0"
    },
    {
        "text": "Free 3-month Netflix and Disney Hotstar VIP subscription exclusively for Jio users. Activate your free coupon now at http://ott-free-recharge.example.net/activate",
        "label_scam": "1",
        "category": "other",
        "has_url": "1"
    },

    # ---------------- 11. benign (20 rows, hard negatives) ----------------
    {
        "text": "Dear SBI Customer, your A/c ending XX4912 is debited by Rs 1,450.00 on 02-Oct-26 by UPI transfer. Avail Bal: Rs 18,240.25. If not done by you, dial 1930.",
        "label_scam": "0",
        "category": "benign",
        "has_url": "0"
    },
    {
        "text": "482913 is your secret One Time Password (OTP) for online purchase of Rs 2,199 on Amazon. Valid for 10 mins. Do not share OTP with anyone, including bank staff.",
        "label_scam": "0",
        "category": "benign",
        "has_url": "0"
    },
    {
        "text": "Your Blue Dart shipment tracking AWBD7491 is out for delivery today with courier associate Ramesh. To manage delivery, visit https://www.bluedart.com/track",
        "label_scam": "0",
        "category": "benign",
        "has_url": "1"
    },
    {
        "text": "Hey bro, I have transferred the 1500 rupees for yesterday's dinner to your Google Pay. Let me know once you receive it.",
        "label_scam": "0",
        "category": "benign",
        "has_url": "0"
    },
    {
        "text": "HDFC Bank Festive Offer: Get 10% instant discount up to Rs 1500 on electronics purchase using your debit card. T&C apply. Visit https://www.hdfcbank.com/festive",
        "label_scam": "0",
        "category": "benign",
        "has_url": "1"
    },
    {
        "text": "State Bank of India: Clear balance in your savings account ending in 8192 as of today is Rs 42,850.50. Thank you for banking with us.",
        "label_scam": "0",
        "category": "benign",
        "has_url": "0"
    },
    {
        "text": "Dear ICICI Bank Cardmember, your credit card statement for card ending 3012 is generated. Total due: Rs 6,840. Due date: 18-Oct-2026. View bill on iMobile app.",
        "label_scam": "0",
        "category": "benign",
        "has_url": "0"
    },
    {
        "text": "Tata Power: Received payment of Rs 1,840 towards Consumer No 90021482 on 02-Oct-2026. Transaction successful. Download receipt from https://www.tatapower.com",
        "label_scam": "0",
        "category": "benign",
        "has_url": "1"
    },
    {
        "text": "Hi team, just a reminder that the sprint planning meeting will start at 3:30 PM today in conference room B. Please update your tickets beforehand.",
        "label_scam": "0",
        "category": "benign",
        "has_url": "0"
    },
    {
        "text": "Zomato: Your order from Biryani Blues is prepared and delivery partner is on the way to your location. Estimated arrival in 15 minutes.",
        "label_scam": "0",
        "category": "benign",
        "has_url": "0"
    },
    {
        "text": "IndiGo flight 6E-402 from Mumbai to Delhi: Web check-in is now open. Choose your preferred seat and obtain boarding pass at https://www.goindigo.in",
        "label_scam": "0",
        "category": "benign",
        "has_url": "1"
    },
    {
        "text": "Salary credit: Rs 78,500.00 has been credited to your salary account XX3910 for the month of September. Available balance: Rs 92,100.00.",
        "label_scam": "0",
        "category": "benign",
        "has_url": "0"
    },
    {
        "text": "Airtel recharge successful! Unlimited 5G pack Rs 349 credited with 28 days validity and 1.5GB/day data. Manage balance on Airtel Thanks app.",
        "label_scam": "0",
        "category": "benign",
        "has_url": "0"
    },
    {
        "text": "Please submit the machine learning assignment submission zip by tomorrow evening on classroom portal before 11 PM.",
        "label_scam": "0",
        "category": "benign",
        "has_url": "0"
    },
    {
        "text": "Your Uber ride is arriving in 3 mins. Driver Sunil in white Dzire MH01-CR-8201. Share ride start PIN 3918 with driver.",
        "label_scam": "0",
        "category": "benign",
        "has_url": "0"
    },
    {
        "text": "Apollo Clinic: Your doctor appointment with Dr. Mehta is confirmed for Monday 10:00 AM at Andheri West clinic. Please arrive 15 minutes early.",
        "label_scam": "0",
        "category": "benign",
        "has_url": "0"
    },
    {
        "text": "Blinkit: Order delivered! Your grocery items were delivered to your door. Rate your delivery experience on the app: https://blinkit.com/feedback",
        "label_scam": "0",
        "category": "benign",
        "has_url": "1"
    },
    {
        "text": "Nippon India Mutual Fund: Your monthly SIP installment of Rs 2,500 for Large Cap Fund has been processed successfully. Units allocated: 42.18.",
        "label_scam": "0",
        "category": "benign",
        "has_url": "0"
    },
    {
        "text": "Dear customer, your new cheque book for account XX5921 has arrived at your home branch. Please collect it during working hours with valid ID.",
        "label_scam": "0",
        "category": "benign",
        "has_url": "0"
    },
    {
        "text": "Netflix: Your monthly subscription payment of Rs 649 was charged to your card ending 4810. Manage your membership at https://www.netflix.com/youraccount",
        "label_scam": "0",
        "category": "benign",
        "has_url": "1"
    }
]

def save_and_verify():
    assert len(DATA) == 60, f"Expected 60 rows, got {len(DATA)}"

    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["text", "label_scam", "category", "has_url"])
        writer.writeheader()
        for row in DATA:
            writer.writerow(row)

    print(f"Saved {len(DATA)} rows to {CSV_PATH}")

if __name__ == "__main__":
    save_and_verify()
