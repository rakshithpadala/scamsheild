"""Synthetic scam and benign message generator for ScamShield AI.
Generates diverse, realistic Indian scam and benign messages across 11 categories:
- bank_kyc_account
- upi_payment
- cashback_reward_lottery
- job
- investment
- loan
- delivery
- gov_police_impersonation
- tech_support
- other
- benign

Ensures:
1. Category-specific realistic URLs (no mismatched links like loan URLs in police summons).
2. Zero overlap with ml/data/handwritten_test.csv.
3. Zero real PII (no 10-digit phone numbers starting with 6-9, no real emails).
4. Realistic Indian context, varied vocabulary, Hinglish phrasing, and realistic scams.
"""

import csv
import os
import random
import re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUTPUT_PATH = os.path.join(ROOT, "ml", "data", "synthetic", "synthetic_scams.csv")
HANDWRITTEN_PATH = os.path.join(ROOT, "ml", "data", "handwritten_test.csv")

random.seed(42)

# Load handwritten texts to strictly avoid overlap
handwritten_set = set()
if os.path.exists(HANDWRITTEN_PATH):
    with open(HANDWRITTEN_PATH, "r", encoding="utf-8", errors="ignore") as f:
        reader = csv.DictReader(f)
        for r in reader:
            if r.get("text"):
                handwritten_set.add(re.sub(r"\W+", " ", r["text"].lower()).strip())

print(f"Loaded {len(handwritten_set)} handwritten references to avoid overlap.")

BANKS = ["SBI", "HDFC", "ICICI", "Axis Bank", "PNB", "Bank of Baroda", "Kotak", "Canara Bank", "Union Bank", "IndusInd"]
WALLET_APPS = ["Google Pay", "PhonePe", "Paytm", "BHIM UPI", "Amazon Pay", "Cred"]
COURIERS = ["IndiaPost", "BlueDart", "Delhivery", "DTDC", "Shadowfax", "Ecom Express"]
ECOM_BRANDS = ["Amazon", "Flipkart", "Myntra", "Meesho", "Ajio", "Tata Cliq"]
TELECOM = ["Jio", "Airtel", "Vi", "BSNL"]
CITIES = ["Mumbai", "Delhi", "Bengaluru", "Hyderabad", "Pune", "Kolkata", "Ahmedabad", "Jaipur"]
POLICE_AGENCIES = ["Delhi Police Cyber Crime Branch", "CBI Cyber Cell", "Mumbai Crime Branch", "Narcotics Control Bureau (NCB)", "Enforcement Directorate (ED)"]

CATEGORY_URLS = {
    "bank_kyc_account": [
        "http://sbi-kyc-update.example.xyz/pan",
        "http://hdfc-security-portal.example.in/login",
        "http://icici-pan-link.example.org/kyc",
        "http://pnb-customer-auth.example.net/portal",
        "http://axis-netbanking-verify.example.xyz/auth",
        "http://bank-kyc-renewal.example.in/verify",
        "http://yono-sbi-login.example.xyz/re-kyc",
        "http://secure-banking-alert.example.net/reactivate"
    ],
    "upi_payment": [
        "http://gpay-cashback-claim.example.xyz/reward",
        "http://phonepe-reward-scratch.example.org/claim",
        "http://paytm-refund-desk.example.net/accept",
        "http://bhim-collect-auth.example.xyz/token",
        "http://upi-refund-clearance.example.in/settle",
        "http://gpay-festive-voucher.example.xyz/approve"
    ],
    "cashback_reward_lottery": [
        "http://kbc-lottery-winner.example.org/prize",
        "http://amazon-scratch-card.example.xyz/festive",
        "http://flipkart-voucher-bonus.example.net/claim",
        "http://diwali-bumper-reward.example.xyz/spin",
        "http://jio-sim-winner.example.org/collect",
        "http://reward-points-cashout.example.in/redeem"
    ],
    "job": [
        "http://workfromhome-tasks.example.xyz/join",
        "http://telegram-earn-daily.example.org/vip",
        "http://parttime-rating-jobs.example.net/register",
        "http://video-review-earning.example.xyz/start",
        "http://amazon-hiring-partner.example.org/apply",
        "http://daily-payout-remote.example.net/onboarding"
    ],
    "investment": [
        "http://institutional-wealth-club.example.xyz/invest",
        "http://crypto-arbitrage-robot.example.org/trade",
        "http://forex-trading-bonus.example.net/gold",
        "http://multibagger-stock-tips.example.xyz/vip",
        "http://high-yield-staking-pool.example.org/join",
        "http://sebi-stock-advisory.example.in/plans"
    ],
    "loan": [
        "http://instant-paperless-loan.example.xyz/apply",
        "http://speedy-rupee-loan.example.org/download",
        "http://mudra-subsidy-clearance.example.net/portal",
        "http://zero-cibil-credit.example.xyz/disburse",
        "http://fast-cash-personal-loan.example.in/get",
        "http://express-mobile-loan-app.example.net/apk"
    ],
    "delivery": [
        "http://indiapost-parcel-reschedule.example.xyz/address",
        "http://bluedart-redirection.example.org/tracking",
        "http://dtdc-consignment-fee.example.net/pay",
        "http://delhivery-sorting-update.example.xyz/pincode",
        "http://express-courier-clearance.example.in/dispatch",
        "http://customs-parcel-duty.example.org/settle"
    ],
    "gov_police_impersonation": [
        "http://cybercell-investigation.example.xyz/summons",
        "http://incometax-recovery-portal.example.org/notice",
        "http://cbi-online-hearing.example.xyz/portal",
        "http://digital-arrest-court.example.org/bail",
        "http://mumbai-police-cybercrime.example.in/fir",
        "http://trai-telecom-verification.example.xyz/case"
    ],
    "tech_support": [
        "http://device-cleaner-antivirus.example.xyz/fix",
        "http://google-security-recovery.example.org/auth",
        "http://whatsapp-security-patch.example.net/update",
        "http://android-malware-repair.example.xyz/clean",
        "http://windows-defender-helpline.example.org/scan",
        "http://instagram-account-support.example.net/verify"
    ],
    "other": [
        "http://echallan-parivahan-pay.example.xyz/fine",
        "http://ott-free-recharge.example.net/activate",
        "http://electricity-bill-portal.example.org/settle",
        "http://fastag-recharge-recovery.example.xyz/unblock",
        "http://matrimony-vip-contact.example.org/profiles",
        "http://lpg-subsidy-update.example.in/bank"
    ],
    "benign": [
        "https://www.tatapower.com",
        "https://www.bluedart.com/track",
        "https://www.goindigo.in",
        "https://www.netflix.com",
        "https://www.hdfcbank.com/offers",
        "https://blinkit.com/feedback"
    ]
}

TEMPLATES = {
    "bank_kyc_account": [
        ("Dear {bank} customer, your account ending {acc} is restricted due to pending KYC validation. Update PAN/Aadhaar at {url} to prevent account freeze.", 1),
        ("{bank} Alert: Immediate action required. Your NetBanking access will be blocked within {hours} hrs due to outdated re-KYC. Visit {url} now.", 1),
        ("Urgent: Apka {bank} khata temporary block kar diya gaya hai. Aadhar card update karne ke liye turant link open kare {url}", 1),
        ("Dear Customer, {bank} YONO app access has been revoked. Re-verify your registered mobile number and credentials at {url}", 1),
        ("Notice from {bank}: Submit 16-digit debit card number and CVV to customer verification executive to reactivate dormant savings account {acc}.", 0),
        ("Dear account holder, your {bank} credit card point redemption is linked to KYC renewal. Complete verification at {url} to claim cash credit.", 1),
        ("Security Warning: Unauthorized access attempt detected on {bank} NetBanking account {acc}. Verify login identity immediately at {url}", 1),
        ("{bank} e-KYC Pending: Upload electricity bill and PAN copy on {url} within 24 hours to resume IMPS/NEFT transfer facility.", 1),
        ("Bank Notice: Incomplete KYC document status. Download verification apk tool {url} to complete video biometric verification from home.", 1),
        ("Aadhar Biometric mismatch reported on your {bank} account. Visit {url} or your NetBanking will be suspended tonight at 11:59 PM.", 1),
        ("Warning from {bank}: Your bank account is marked for freezing under regulatory audit. Enter netbanking password at {url} to unlock.", 1),
        ("Dear User, your {bank} cheque book and ATM debit card are on hold due to missing KYC. Validate identity at {url} immediately.", 1),
    ],

    "upi_payment": [
        ("Congratulations! You received Rs {amount} cashback reward on {wallet}. Click {url} to accept collect request and enter UPI PIN.", 1),
        ("Sir, I sent Rs {amount} to your {wallet} number by mistake. Please approve the collect request and enter your PIN to return it.", 0),
        ("Advance payment of Rs {amount} for your OLX listing is waiting. Scan the QR code sent on WhatsApp and enter PIN to receive money.", 0),
        ("{wallet} Notification: Rs {amount} refund voucher approved for your recent failed order. Click {url} and submit UPI PIN to claim credit.", 1),
        ("Cashback reward of Rs {amount} credited in your scratch card! Authorize collect request in {wallet} app to deposit directly into bank.", 0),
        ("Your pending UPI refund of Rs {amount} is waiting for clearance. Open {url} and enter your 4/6 digit secret PIN to authorize transfer.", 1),
        ("Buyer sent money order Rs {amount}. Open {wallet}, click on 'Pay' prompt to approve credit into your account balance.", 0),
        ("{wallet} Merchant Alert: You received promotional bonus of Rs {amount}. Tap {url} to confirm transaction with your security PIN.", 1),
        ("Notice: Unclaimed balance Rs {amount} in {wallet} will expire today. Scan QR code in attached PDF and authorize PIN to credit account.", 0),
        ("Refund clearance department: Rs {amount} ready for immediate credit to bank. Verify transaction request on {url} with secret PIN.", 1),
        ("GooglePay Lucky Draw: You are awarded Rs {amount}. Click to accept transfer and enter bank UPI PIN: {url}", 1),
        ("Dear User, an incoming UPI credit of Rs {amount} requires PIN verification due to high transaction limit. Click {url}", 1),
    ],

    "cashback_reward_lottery": [
        ("KBC All India Sim Card Lucky Draw! Aapka mobile no jeeta hai Rs {lakh} Lakh ka cash prize. Claim karne ke liye click kare {url}", 1),
        ("Dear user, you won Rs {amount} in {ecom} Grand Festive Scratch Card. Redeem your winning voucher before midnight at {url}", 1),
        ("Congratulations! Your mobile number won 1st prize Maruti Brezza or cash Rs {lakh} Lakh in Diwali Maha Dhamaka. Call lottery manager.", 0),
        ("Special Loyalty Bonus: You have {pts} reward points worth Rs {amount} expiring tonight. Convert points to instant cash at {url}", 1),
        ("Amazon Pay Spin & Win Winner! You have won an Apple iPhone 15 Pro. Pay handling and customs registration charge Rs {fee} at {url}", 1),
        ("Dear customer, your registered SIM has won Rs {lakh} Lakh in telecom lucky lottery draw. Contact helpline or click {url} to claim.", 1),
        ("Shoppers Stop Mega Bonanza: Selected customer for free gold coin voucher. Pay courier dispatch charges Rs {fee} at {url}", 1),
        ("Congratulations! Rs {amount} cashback credited to your wallet balance. Click {url} within 15 minutes before the offer expires.", 1),
        ("Kaun Banega Crorepati Official Winner notice: Claim cash reward of Rs {lakh} Lakh. Pay processing clearance fee Rs {fee} to release.", 0),
        ("Festive Scratch & Win: You unlocked a bumper reward of Rs {amount}. Redeem directly into your bank account via {url}", 1),
        ("Gift Voucher Alert: You have an unredeemed Flipkart shopping gift card of Rs {amount}. Claim voucher code at {url}", 1),
        ("Dear user, claim your free Rs {amount} fuel voucher courtesy of Indian Oil Diwali contest. Register details at {url}", 1),
    ],

    "job": [
        ("Work From Home Opportunity: Earn Rs {daily_job} daily by simply liking YouTube videos and subscribing to channels. Join Telegram: {url}", 1),
        ("Part-time job vacancy: Review hotels and restaurants on Google Maps and earn Rs {daily_job} per day. Contact HR on WhatsApp now.", 0),
        ("Amazon India hiring part-time remote data entry assistants. Flexible hours, salary Rs {monthly_job}/month. Register here: {url}", 1),
        ("Selected for Indigo Airlines ground handling staff at {city} airport. Salary Rs {monthly_job}/pm. Deposit uniform & gate pass fee Rs {fee}.", 0),
        ("Earn Rs 500 per review! Simple typing & rating tasks from mobile. Daily instant payment via UPI. Start now at {url}", 1),
        ("Freelance digital marketing work: Earn Rs {daily_job} daily. No prior experience needed. Join VIP training group on Telegram: {url}", 1),
        ("Tata Consultancy Services: Online resume shortlisted for administrative role. Transfer interview screening fee Rs {fee} to proceed.", 0),
        ("Earn daily passive income watching movie trailers. Payouts processed every evening. Register your demo account at {url}", 1),
        ("Work 20 minutes daily on Instagram promotion and earn Rs {daily_job}. Instant withdrawal to UPI. Click {url} to start tasks.", 1),
        ("Job Confirmation: Railway Group D vacancy appointment letter ready. Deposit medical verification fee Rs {fee} to dispatch letter.", 0),
        ("Global Ecommerce Partner: Assist merchants in rating products online. Earn Rs {daily_job} daily. Start onboarding at {url}", 1),
        ("Work from home voice process job: Rs {monthly_job}/month. Laptop and Wi-Fi provided by company. Pay courier security deposit Rs {fee}.", 0),
    ],

    "investment": [
        ("Institutional VIP Stock Club: Guaranteed {roi}% weekly returns with insider breakout trading calls. Join private Telegram: {url}", 1),
        ("Exclusive Pre-IPO equity allotment open for retail investors. Double your invested capital in 30 days with zero downside. Join {url}", 1),
        ("Automated AI crypto arbitrage trading system: Deposit Rs {inv_amt} and receive guaranteed daily payout Rs {daily_roi}. Safe & regulated.", 0),
        ("SEBI registered institutional investment plan: Earn fixed monthly profit of {roi}% on stock options. Register portfolio account at {url}", 1),
        ("Forex Trading Special Promotion: Deposit $100 and get $300 welcome margin bonus. Guaranteed profit withdrawals within 24 hours: {url}", 1),
        ("Earn daily compound interest of 5% on USDT tether staking pool. Instant automated withdrawal anytime. Join smart contract platform {url}", 1),
        ("Elite Wealth Advisory: 100% accurate intraday jackpot share tips with money-back guarantee. Subscribe now at {url}", 1),
        ("Government green energy solar bonds offering 24% annual fixed dividend payout. Invest starting from Rs {inv_amt} at {url}", 1),
        ("Gold bullion spot trading scheme: Invest Rs {inv_amt} today and receive physical gold deliverable in 45 days plus 20% bonus return.", 0),
        ("Algorithmic high-frequency trading bot: Proven track record with zero losing days. Start trading with small capital at {url}", 1),
        ("Private hedge fund VIP allocation: Minimum investment Rs {inv_amt}, guaranteed return of 40% every quarter. Contact fund manager on Telegram.", 0),
        ("Crypto trading pool: Multiply your Bitcoin / Ethereum by 3x within 7 days. Verified blockchain contract: {url}", 1),
    ],

    "loan": [
        ("Instant Personal Loan approved up to Rs {loan_amt} at 0.5% monthly interest with zero CIBIL score requirement. Apply here: {url}", 1),
        ("Pre-approved paperless cash loan of Rs {loan_amt} ready in bank. Disbursal in 5 minutes. Transfer 1% file documentation fee Rs {fee}.", 0),
        ("Emergency loan alert: Get Rs {loan_amt} transferred directly to account without salary slips or guarantor. Download APK app at {url}", 1),
        ("Pradhan Mantri Mudra Loan scheme: Rs {loan_amt} approved at 2% annual subsidy. Pay sanction verification fee Rs {fee} to release funds.", 0),
        ("Need fast money? Instant credit line of Rs {loan_amt} available for immediate UPI transfer. Complete 2-minute form at {url}", 1),
        ("Dear Customer, your {bank} pre-approved jumbo personal loan of Rs {loan_amt} is expiring today. Claim disbursal at {url}", 1),
        ("Bad credit history? No problem! Get instant loan up to Rs {loan_amt} deposited in bank account. Download express loan app: {url}", 1),
        ("Student and homemaker special credit card loan: Disburse Rs {loan_amt} without income proof. Apply online at {url}", 1),
        ("Dhani quick credit loan approved: Rs {loan_amt} waiting for disbursement. Pay GST and insurance clearance fee Rs {fee} to agent.", 0),
        ("Zero interest business loan under government scheme sanctioned: Rs {loan_amt}. Submit processing token amount Rs {fee} to loan officer.", 0),
        ("Low CIBIL personal loan approved: Disburse Rs {loan_amt} instantly to bank. Complete one-step Aadhaar KYC at {url}", 1),
        ("Special festive paperless cash advance: Get Rs {loan_amt} credited in 10 minutes. Click {url} to download official application.", 1),
    ],

    "delivery": [
        ("{courier} Delivery Alert: Your package {tracking} could not be delivered due to incomplete street address. Update address at {url} to prevent return.", 1),
        ("Customs detained an overseas parcel {tracking} sent to your name at {city} airport. Pay clearance customs fee Rs {fee} to avoid confiscation.", 0),
        ("{courier}: Consignment {tracking} delivery rescheduled on request. Pay redelivery rescheduling charge Rs {fee_small} online at {url}", 1),
        ("India Post Notice: Parcel {tracking} arrived at sorting hub with missing pincode. Update destination address within 24 hours at {url}", 1),
        ("DHL Express: High-value parcel delivery pending signature. Recipient tax fee Rs {fee} payable online to release shipment: {url}", 1),
        ("{courier} Courier: Driver attempted delivery for order {tracking} but recipient unavailable. Click {url} to choose preferred delivery time.", 1),
        ("Speed Post consignment {tracking} on hold due to incorrect house number. Pay unpaid postal stamp charges Rs {fee_small} at {url}", 1),
        ("International courier package held by inspection officer. Transfer clearance penalty Rs {fee} within 2 hours or shipment will be destroyed.", 0),
        ("Your consignment {tracking} is out for re-dispatch. Confirm your GPS delivery address and pay re-routing fee Rs {fee_small} at {url}", 1),
        ("Urgent notice: Unclaimed festive gift parcel {tracking} will be returned to sender tonight. Confirm recipient details at {url}", 1),
        ("{courier} tracking update: Address not found by courier associate. Please verify complete home address at {url} within 12 hours.", 1),
        ("FedEx shipment {tracking} awaiting customs clearance at foreign exchange office. Settle statutory import duty Rs {fee} at {url}", 1),
    ],

    "gov_police_impersonation": [
        ("CBI Investigation Notice: A consignment containing narcotics and contraband was booked using your Aadhaar. Digital arrest warrant issued. Join Skype call.", 0),
        ("{police}: Your phone number is found linked to an ongoing money laundering criminal investigation. Join interrogation video room {url} immediately.", 1),
        ("Department of Telecommunications (DoT) Warning: All SIM cards issued against your identity will be disconnected in 2 hours by court order. Dial 9.", 0),
        ("Income Tax Department: Penalty order of Rs {tax_fine} issued for undeclared foreign financial assets. Pay demand notice at {url} to avoid attachment.", 1),
        ("Narcotics Control Bureau (NCB) Summons: Illegal package intercepted at courier warehouse with your name. Contact investigating officer on Skype immediately.", 0),
        ("Supreme Court of India e-Notice: Arrest warrant issued in financial fraud case FIR-{fir_no}. Review case details and settle bail bond at {url}", 1),
        ("Mumbai Customs: Foreign currency remittance of $50,000 seized in your name. Deposit clearance verification fee Rs {fee} to avoid prosecution.", 0),
        ("Cyber Police Headquarters: You are placed under 24-hour Digital Arrest. Do not disconnect video call or leave your residence under penalty of law.", 0),
        ("TRAI Telecom Regulatory Order: Your mobile number will be terminated due to cybercrime complaints. Verify identity with officer at {url}", 1),
        ("Enforcement Directorate (ED) summons: Appear for interrogation regarding illegal hawala transactions or submit security bond at {url}", 1),
        ("Delhi Police Cyber Cell: Final warning before police team dispatch to your registered address for cyber extortion charges. Call officer now.", 0),
        ("National Crime Records Bureau alert: Compromised banking credentials used in terrorist financing. Verify clearance certificate at {url}", 1),
    ],

    "tech_support": [
        ("Microsoft Windows Security: Severe Trojan Spyware malware detected on your computer IP {ip_addr}. Computer locked. Call helpline immediately.", 0),
        ("Security Warning: Your Android smartphone is infected with {virus_count} critical banking malware viruses. Install certified cleaner APK now: {url}", 1),
        ("Google Security Team: Unauthorized sign-in attempt from Russia on your Gmail account. Secure your Google account immediately at {url}", 1),
        ("WhatsApp Account Notice: Your account will be banned in 24 hours for spam policy violation. Verify account ownership at {url} to keep access.", 1),
        ("Apple Security Alert: Your iCloud account is locked due to suspicious login attempts. Verify Apple ID and security answers at {url}", 1),
        ("Norton Antivirus: Your subscription has automatically renewed for Rs {amount}. If you did not authorize this charge, call billing desk immediately.", 0),
        ("Device Alert: Battery and memory damaged by {virus_count} malicious files. Download Android system repair tool immediately from {url}", 1),
        ("Instagram Help Center: Copyright infringement report filed against your profile. Confirm identity at {url} within 24 hours to prevent deletion.", 1),
        ("System Firewall Alert: Suspicious network connection detected downloading personal photos. Install security patch from {url} to terminate.", 1),
        ("McAfee Total Protection: 3 trojans found stealing passwords from web browser. Activate cleanup scan immediately at {url}", 1),
        ("Facebook Security Team: Someone tried to reset your password from unknown location. Verify your account credentials at {url}", 1),
        ("Router Firmware Warning: WiFi router compromised by external hackers. Download security update patch at {url} to secure home network.", 1),
    ],

    "other": [
        ("Electricity Department Alert: Power supply to your connection will be disconnected tonight at 9:30 PM due to unpaid electricity bill. Call electricity officer.", 0),
        ("Traffic Police e-Challan: Pending traffic violation penalty of Rs {challan_amt} registered on vehicle. Pay immediately to avoid court summons: {url}", 1),
        ("Matrimonial Alert: 8 verified NRI doctor profiles expressed interest in your profile on BharatMatrimony. Pay VIP contact token Rs {fee} at {url}", 1),
        ("Free 1-Year OTT Subscription: Jio special offer for active users. Activate free Netflix, Amazon Prime and Hotstar pass at {url}", 1),
        ("Mahanagar Gas (MGL): Your piped gas connection will be disconnected today due to pending meter verification. Contact field officer immediately.", 0),
        ("Voter ID Card Update: Election Commission notification. Verify digital EPIC voter identity card online before upcoming elections at {url}", 1),
        ("Free Recharge Offer: Government is distributing free 28-day 5G data recharge to all Indian citizens. Claim free recharge at {url}", 1),
        ("Toll Plaza Fastag Notice: Your Fastag wallet is blacklisted due to negative balance. Re-activate Fastag within 2 hours at {url} to travel.", 1),
        ("Property Tax Dept: Final notice before property attachment for outstanding municipal tax Rs {tax_fine}. Pay online discount rate at {url}", 1),
        ("LPG Gas Subsidy Alert: Your cooking gas subsidy of Rs {amount} has bounced. Update bank account details at {url} to receive subsidy.", 1),
        ("Housing Society Notice: Outstanding maintenance penalty notice issued for flat. Review settlement invoice and pay via portal: {url}", 1),
        ("BSNL Landline & Broadband: Service suspension order issued. Settle overdue bill payment immediately via customer payment gateway {url}", 1),
    ],

    "benign": [
        ("Dear SBI Customer, your A/c ending in {acc} is debited by Rs {amount}.00 on {date} by UPI/Ref {ref}. Available Bal: Rs {bal}. If not done by you, dial 1930.", 0),
        ("{otp} is your secret One Time Password (OTP) for transaction of Rs {amount} on {ecom}. Valid for 10 minutes. Do not share OTP with anyone.", 0),
        ("Your {courier} package {tracking} is out for delivery today with courier partner Suresh. Track shipment at https://www.{courier_domain}/track", 1),
        ("Hey, I just transferred the Rs {amount} for yesterday's dinner bill to your Google Pay. Please check your account.", 0),
        ("{bank} Festive Delight: Enjoy 15% instant cashback up to Rs 2000 on lifestyle shopping with your debit card. T&C apply. Visit https://www.{bank_domain}/offers", 1),
        ("Dear Cardmember, your {bank} credit card ending {card} statement for month of September is generated. Minimum due: Rs {fee_small}. Due date: 20-Oct-2026.", 0),
        ("State Bank of India: Available balance in savings account ending {acc} as of {date} is Rs {bal}. Thank you for banking with SBI.", 0),
        ("Tata Power: Payment of Rs {amount} received towards Consumer No {cons_no} on {date}. Payment successful. Download receipt: https://www.tatapower.com", 1),
        ("Hi team, please find the meeting agenda for tomorrow's engineering sprint retro at 2:00 PM attached in Slack.", 0),
        ("Zomato: Your food order from Punjab Grill has been picked up and is arriving in approximately 20 minutes.", 0),
        ("IndiGo flight 6E-284 from {city} to Delhi: Web check-in is now open. Select seats and download your boarding pass at https://www.goindigo.in", 1),
        ("Salary credit: Rs {salary}.00 credited to your corporate salary account {acc} for September 2026. Avail balance: Rs {bal}.", 0),
        ("Airtel Thanks: Recharge of Rs 349 successful for mobile connection. 1.5GB/day + unlimited 5G data activated for 28 days.", 0),
        ("Hey, are we still meeting at the library at 4 PM to work on our cloud computing project presentation?", 0),
        ("Your Uber ride is arriving now. Driver Manoj in silver WagonR registration DL01-EA-3921. Share OTP {otp_short} to start trip.", 0),
        ("Apollo Clinic: Appointment with Dr. Sharma confirmed for Wednesday at 11:30 AM. Please arrive 10 minutes prior to consultation.", 0),
        ("Blinkit: Order delivered! Your groceries were handed over at your doorstep. We hope you enjoyed our service.", 0),
        ("Nippon India Mutual Fund: SIP installment of Rs {sip_amt} for Flexi Cap Fund successfully processed. Units allotted: {units}.", 0),
        ("Dear customer, your request for physical account statement has been processed. Password for PDF is your date of birth.", 0),
        ("Netflix: Subscription renewal of Rs 649 successful. Next billing date is 03-Nov-2026. Manage account at https://www.netflix.com", 1),
        ("IRCTC: E-ticket booking confirmed for PNR {pnr}. Train 12951 Mumbai Rajdhani, Coach B3 Berth 42. Charting status: Chart Not Prepared.", 0),
        ("Swiggy Instamart: Delivery partner is on the way with your grocery items. Expected arrival in 9 minutes.", 0),
        ("Electricity bill for Consumer No {cons_no} generated. Total amount payable Rs {amount} by due date 15-Oct-2026 via official discom portal.", 0),
        ("Can you please send me the class notes from yesterday's statistics lecture? I missed the afternoon session.", 0),
    ]
}

def generate_row(category):
    tpl_list = TEMPLATES[category]
    tpl, has_url = random.choice(tpl_list)

    bank = random.choice(BANKS)
    bank_domain = bank.lower().replace(" ", "") + ".com"
    courier = random.choice(COURIERS)
    courier_domain = courier.lower().replace(" ", "") + ".in"
    ecom = random.choice(ECOM_BRANDS)
    city = random.choice(CITIES)
    police = random.choice(POLICE_AGENCIES)
    wallet = random.choice(WALLET_APPS)

    acc = "XX" + str(random.randint(1000, 9999))
    card = "XX" + str(random.randint(1000, 9999))
    amount = random.choice([499, 999, 1499, 2450, 3500, 4800, 5200, 7500, 9200, 12500, 18400])
    hours = random.choice([2, 4, 12, 24, 48])
    lakh = random.choice([5, 10, 15, 25, 50])
    fee = random.choice([999, 1450, 2200, 3500, 4800, 8500])
    fee_small = random.choice([25, 38, 48, 75, 95])
    daily_job = random.choice([1500, 2500, 3200, 4500, 6000, 8500])
    monthly_job = random.choice([35000, 42000, 48000, 55000, 65000])
    roi = random.choice([25, 35, 45, 60, 80])
    inv_amt = random.choice([5000, 10000, 25000, 50000, 100000])
    daily_roi = random.choice([800, 1200, 1800, 2500, 4000])
    loan_amt = random.choice(["2,00,000", "3,50,000", "5,00,000", "10,00,000", "50,000"])
    tracking = "IN" + str(random.randint(100000, 999999))
    tax_fine = random.choice(["25,000", "45,000", "65,000", "1,20,000", "35,000", "85,000"])
    challan_amt = random.choice(["500", "1,000", "2,000", "5,000", "1,500", "3,000"])
    pts = random.choice([4250, 6800, 9450, 12800, 5600, 8100])
    fir_no = str(random.randint(1001, 9999))
    case_no = str(random.randint(10001, 99999))
    virus_count = str(random.randint(3, 9))
    ip_addr = f"103.{random.randint(10,250)}.{random.randint(10,250)}.{random.randint(1,250)}"

    # Category-specific fake URLs
    url = random.choice(CATEGORY_URLS[category])

    otp = str(random.randint(100000, 999999))
    otp_short = str(random.randint(1000, 9999))
    bal = f"{random.randint(10, 80)},{random.randint(100, 999)}.{random.randint(10, 99)}"
    ref = str(random.randint(10000000, 99999999))
    cons_no = str(random.randint(10000000, 99999999))
    pnr = str(random.randint(10000000, 99999999))
    date = f"{random.randint(1, 28)}-Oct-2026"
    salary = f"{random.randint(45, 95)},{random.randint(100, 999)}"
    sip_amt = random.choice([1500, 2000, 2500, 5000, 10000])
    units = f"{random.randint(20, 95)}.{random.randint(10, 99)}"

    text = tpl.format(
        bank=bank, bank_domain=bank_domain, courier=courier, courier_domain=courier_domain,
        ecom=ecom, city=city, police=police, wallet=wallet, acc=acc, card=card, amount=amount,
        hours=hours, lakh=lakh, fee=fee, fee_small=fee_small, daily_job=daily_job,
        monthly_job=monthly_job, roi=roi, inv_amt=inv_amt, daily_roi=daily_roi,
        loan_amt=loan_amt, tracking=tracking, tax_fine=tax_fine, challan_amt=challan_amt,
        pts=pts, url=url, otp=otp, otp_short=otp_short, bal=bal, ref=ref, cons_no=cons_no,
        pnr=pnr, date=date, salary=salary, sip_amt=sip_amt, units=units,
        fir_no=fir_no, case_no=case_no, virus_count=virus_count, ip_addr=ip_addr
    )

    label_scam = "0" if category == "benign" else "1"
    url_flag = "1" if ("http://" in text or "https://" in text) else "0"

    return {
        "text": text,
        "label_scam": label_scam,
        "category": category,
        "has_url": url_flag
    }

def generate_all(samples_per_cat=100):
    categories = list(TEMPLATES.keys())
    dataset = []
    seen_texts = set()

    for cat in categories:
        count = 0
        attempts = 0
        while count < samples_per_cat and attempts < 10000:
            attempts += 1
            row = generate_row(cat)
            norm = re.sub(r"\W+", " ", row["text"].lower()).strip()

            if len(norm) < 20:
                continue
            if norm in handwritten_set:
                continue
            if norm in seen_texts:
                continue
            if re.search(r"(?<!\d)[6-9]\d{9}(?!\d)", row["text"]):
                continue
            if re.search(r"[\w.]+@[\w.]+\.\w+", row["text"]):
                continue

            seen_texts.add(norm)
            dataset.append(row)
            count += 1

        print(f"Generated {count} samples for category: {cat}")

    random.shuffle(dataset)

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["text", "label_scam", "category", "has_url"])
        writer.writeheader()
        for r in dataset:
            writer.writerow(r)

    print(f"\nTotal synthetic dataset created: {len(dataset)} rows at {OUTPUT_PATH}")

if __name__ == "__main__":
    generate_all(samples_per_cat=100)
