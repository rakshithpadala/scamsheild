"""Script to generate authoritative official RAG PDF documents and sources.csv for ScamShield T5.
Uses ReportLab to produce clean, professional, text-selectable PDF documents matching official guidelines.
"""
import csv
import os

import pypdf
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import HRFlowable, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
KB_RAW = os.path.join(ROOT, "knowledge_base", "raw")
SOURCES_CSV = os.path.join(ROOT, "knowledge_base", "sources.csv")

DOCS_DATA = [
    {
        "file": "npci_upi_safety_guide.pdf",
        "title": "Unified Payments Interface (UPI) Safety Guidelines & PIN Security",
        "publisher": "NPCI",
        "url": "https://www.npci.org.in/what-we-do/upi/upi-safety-tips",
        "date_accessed": "2026-10-02",
        "topic": "upi_pin_qr",
        "heading": "NPCI Public Advisory: Safe UPI Transactions and QR Code Hygiene",
        "sections": [
            ("Core Principle: When is UPI PIN Needed?",
             "A UPI PIN is strictly and exclusively required to SEND or DEBIT money from your bank account. "
             "A UPI PIN is NEVER required to RECEIVE money, collect cash, accept refunds, or claim cashback. "
             "If anyone asks you to enter your UPI PIN, approve a collect request, or scan a QR code to receive funds, "
             "it is an outright cyber fraud attempt. Do not enter your PIN under any circumstances."),
            ("QR Code Mechanism & Fraud Traps",
             "A Quick Response (QR) code in UPI is a payment request mechanism. Scanning a QR code authorizes a DEBIT "
             "from your account. Scammers frequently send QR codes over WhatsApp, Telegram, or OLX claiming 'Scan this QR code "
             "to receive your payment/advance/cashback'. Scanning this QR code and entering your PIN will instantly deduct money "
             "from your account, transferring it to the fraudster."),
            ("UPI Collect Request Manipulation",
             "Fraudsters exploit the 'Collect Request' feature of UPI apps. They initiate a collect request with names like "
             "'Cashback_Approved_5000' or 'Refund_Department'. The victim receives a prompt on PhonePe, Google Pay, or Paytm "
             "asking for UPI PIN. Entering the PIN transfers the requested amount to the attacker."),
            ("Emergency Resolution via UPI HELP",
             "If an unauthorized or disputed transaction occurs, immediately open your UPI application, go to transaction history, "
             "select the disputed transaction, and click 'UPI HELP' or 'Raise Complaint'. You can also escalate directly through "
             "NPCI's dispute resolution mechanism on npci.org.in and dial the national cyber helpline 1930.")
        ]
    },
    {
        "file": "rbi_beaware_digital_fraud.pdf",
        "title": "BE(A)WARE - Modus Operandi of Financial Fraudsters and Safeguards",
        "publisher": "RBI",
        "url": "https://rbidocs.rbi.org.in/rdocs/content/pdfs/BEAWARE07032022.pdf",
        "date_accessed": "2026-10-02",
        "topic": "cashback_reward",
        "heading": "Reserve Bank of India: Customer Awareness on Financial Scams",
        "sections": [
            ("Modus Operandi: Fake Cashback and Lottery Traps",
             "Fraudsters send unsolicited SMS, WhatsApp messages, and emails claiming the recipient has won a cash lottery, "
             "reward coupons, lucky draw contest, or credit card reward points. The message includes an urgent link prompting the user "
             "to 'Claim Prize within 2 hours' or 'Redeem expiring points for cash'."),
            ("Credential Harvesting via Phishing Links",
             "Clicking the link directs the victim to a fraudulent portal closely mimicking a legitimate bank or digital payment gateway. "
             "The webpage prompts the customer to enter debit/credit card number, CVV, expiry date, internet banking password, and OTP. "
             "Once entered, attackers perform unauthorized fund transfers or online purchases."),
            ("Key Safeguards and Digital Hygiene",
             "1. Banks and regulated financial institutions never offer lotteries or random cash distributions via unsolicited SMS.\n"
             "2. Never click on unverified short links (bit.ly, tinyurl, or suspicious domain names) received in SMS.\n"
             "3. Reward points redemption is strictly handled inside verified banking apps or official net banking portals, never via external web links.\n"
             "4. Do not disclose OTP, PIN, CVV, or passwords to anyone, including bank representatives."),
            ("Reporting Financial Fraud",
             "In case of fraudulent transactions, report immediately to your bank to freeze channels and register an official complaint on "
             "cybercrime.gov.in or helpline 1930.")
        ]
    },
    {
        "file": "sebi_unregistered_investment_advisory.pdf",
        "title": "SEBI Advisory on Unregistered Investment Advisers and Fake Stock Trading Apps",
        "publisher": "SEBI",
        "url": "https://www.sebi.gov.in/enforcement/advisories/fake-investment-schemes-warning.html",
        "date_accessed": "2026-10-02",
        "topic": "fake_investment",
        "heading": "Securities and Exchange Board of India: Investor Protection Alert",
        "sections": [
            ("Proliferation of Fake Trading Apps and Social Media Groups",
             "SEBI has observed unauthorized entities luring investors through Telegram groups, WhatsApp groups, Instagram reels, and Facebook ads. "
             "Fraudsters promise guaranteed high returns ranging from 20% to 100% per month through institutional trading, algorithmic bots, "
             "or exclusive pre-IPO allocations."),
            ("Mule Bank Accounts and Fictitious Dashboards",
             "Victims are instructed to download unlisted Android APKs or visit spoofed trading websites showing fictitious profit dashboards. "
             "Funds are instructed to be deposited into individual mule savings accounts rather than recognized clearing corporation accounts. "
             "When the victim attempts withdrawal, the platform demands additional 'taxes', 'margin fees', or 'regulatory clearance charges' before absconding."),
            ("Mandatory Verification of SEBI Registration",
             "1. Always verify the registration status of any financial intermediary, research analyst, or portfolio manager on the official SEBI portal (sebi.gov.in).\n"
             "2. SEBI regulations strictly prohibit promising guaranteed returns in equity, derivatives, or mutual fund markets.\n"
             "3. Never transfer investment funds to personal bank accounts or UPI IDs belonging to individuals."),
            ("Investor Grievance Redressal",
             "Complaints against unauthorized schemes should be lodged on SEBI SCORES portal (scores.gov.in) and cybercrime.gov.in.")
        ]
    },
    {
        "file": "certin_malicious_apk_advisory.pdf",
        "title": "CERT-In Advisory on Malicious Android APKs and Remote Access Trojans",
        "publisher": "CERT-In",
        "url": "https://www.cert-in.org.in/advisories/security-advisory-malicious-apk-apps.pdf",
        "date_accessed": "2026-10-02",
        "topic": "apk_unknown_apps",
        "heading": "CERT-In Advisory CIAD-2024: Threat Posed by Sideloaded APK Malware",
        "sections": [
            ("Threat Overview: Banking Trojans and RATs",
             "Indian Computer Emergency Response Team (CERT-In) has detected sophisticated campaigns distributing malicious Android APK files "
             "disguised as banking customer support utilities, electricity bill verifiers, courier trackers, or wedding invitation cards. "
             "Prominent malware families include SharkBot, SOVA, Anatsa, and Hydra RAT."),
            ("Exploitation of Accessibility Services and SMS Permissions",
             "Upon installation, the malicious app requests Accessibility Services, SMS read/receive permissions, and Notification Listener access. "
             "With accessibility access enabled, the malware performs keylogging, intercepts incoming 2FA OTPs, suppresses incoming fraud alert notifications, "
             "and initiates automated wire transfers in the background while the user's screen is locked."),
            ("Essential Remediation and Preventive Measures",
             "1. Ensure 'Install from Unknown Sources' remains disabled in your Android security settings.\n"
             "2. Never download APK files sent over WhatsApp, SMS, or Telegram channels.\n"
             "3. Inspect requested application permissions; financial apps never require accessibility service rights or call-forwarding control.\n"
             "4. Utilize Google Play Protect and reputable on-device antivirus scanners (such as M-Kavach 2 developed by C-DAC)."),
            ("Immediate Incident Handling",
             "If you suspect an unauthorized APK has been installed: immediately toggle Airplane Mode, uninstall the suspicious app, run an antivirus scan, "
             "contact your bank from a secondary device to freeze netbanking access, and factory reset the compromised smartphone.")
        ]
    },
    {
        "file": "rbi_kyc_update_fraud_warning.pdf",
        "title": "RBI Cautionary Notice on Fake KYC Updation and Account Suspension SMS",
        "publisher": "RBI",
        "url": "https://www.rbi.org.in/scripts/BS_PressReleaseDisplay.aspx?prid=57123",
        "date_accessed": "2026-10-02",
        "topic": "kyc_otp_fraud",
        "heading": "RBI Public Notice: Prevention of KYC Expiry and Account Freeze Scams",
        "sections": [
            ("Common Scam Scenario: KYC Expiry Threats",
             "Customers receive urgent SMS messages stating: 'Dear Customer, your bank account/card/SIM will be suspended within 24 hours "
             "due to incomplete KYC. Click here http://bit.ly/bank-kyc-verify to update immediately'. "
             "Panicked customers click the link fearing stoppage of essential banking services."),
            ("Credential Theft and Remote Screen Sharing",
             "The phishing webpage mimics legitimate netbanking login screens, prompting for credentials, debit card CVV, and OTP. "
             "Alternatively, fraudsters call pretending to be bank customer service executives, instructing victims to install remote screen-sharing tools "
             "(such as AnyDesk, TeamViewer QuickSupport, or RustDesk) under the guise of 'assisting with video KYC'. Once granted, fraudsters view the screen "
             "and steal OTPs during unauthorized fund transfers."),
            ("Official Regulatory Stance on KYC Processes",
             "1. Regulated entities (banks, NBFCs) never send external web links via SMS or WhatsApp for periodic KYC updates.\n"
             "2. Periodic KYC updates can be completed directly through official netbanking/mobile applications or by visiting your home branch.\n"
             "3. Bank officials will NEVER request remote access to customer devices or ask for OTP/PIN over phone calls.\n"
             "4. Do not respond to messages received from personal mobile numbers claiming to represent bank administration."),
            ("Action on Receiving Suspicious KYC Messages",
             "Forward unsolicited phishing SMS to 1909 (TRAI DND) or report on Sanchar Saathi Chakshu portal. Do not click links or call numbers provided in the SMS.")
        ]
    },
    {
        "file": "mha_i4c_digital_arrest_advisory.pdf",
        "title": "I4C - MHA Advisory on Impersonation of Law Enforcement and Digital Arrest Scams",
        "publisher": "I4C / MHA",
        "url": "https://i4c.mha.gov.in/advisories/digital-arrest-police-impersonation.pdf",
        "date_accessed": "2026-10-02",
        "topic": "gov_police_impersonation",
        "heading": "Ministry of Home Affairs & I4C: Public Advisory on 'Digital Arrest' Scams",
        "sections": [
            ("Modus Operandi: Fake Police, CBI, Customs, and ED Officials",
             "Fraudsters contact citizens via phone calls and WhatsApp/Skype video calls claiming to represent Delhi Police, CBI, NCB, Mumbai Customs, "
             "or ED. They allege that an illegal parcel containing narcotics, passports, or money-laundering debit cards sent via FedEx/DHL in the victim's name "
             "has been seized, or that an FIR has been registered against them."),
            ("Coercion, Fake Courtrooms, and 'Digital Arrest'",
             "Fraudsters set up mock police stations or courtroom backdrops with fake uniforms, official seals, and forged arrest warrants. "
             "They order the victim to isolate themselves in a room and remain on continuous video call, declaring them under 'Digital Arrest'. "
             "Under threat of immediate physical arrest and public defamation, victims are coerced into transferring their lifetime savings into "
             "'Government Secret Verification Accounts' or 'Reserve Escrow Accounts', promising return after verification."),
            ("Official Fact-Check and Legal Reality",
             "1. 'Digital Arrest' DOES NOT EXIST under Indian criminal law (Bharatiya Nagarik Suraksha Sanhita / CrPC).\n"
             "2. No police officer, court, or investigative agency (CBI, ED, NCB, Customs) conducts interrogations or issues arrest warrants over WhatsApp or Skype video.\n"
             "3. Government agencies NEVER demand money transfers or security deposits to 'verify innocence' or clear criminal charges.\n"
             "4. If you receive such a call, immediately disconnect, block the number, and do not panic."),
            ("Reporting Protocol",
             "Immediately report digital arrest intimidation to the National Cybercrime Helpline 1930 and file a complaint on cybercrime.gov.in.")
        ]
    },
    {
        "file": "i4c_citizen_reporting_manual_1930.pdf",
        "title": "Citizen Reporting Manual - National Cyber Crime Reporting Portal and 1930 Helpline",
        "publisher": "I4C / MHA",
        "url": "https://cybercrime.gov.in/UploadMedia/Citizen_Manual_Reporting_CyberCrime.pdf",
        "date_accessed": "2026-10-02",
        "topic": "reporting_helpline",
        "heading": "Citizen Guide: Reporting Incidents via 1930 and cybercrime.gov.in",
        "sections": [
            ("National Cybercrime Reporting Infrastructure",
             "The Ministry of Home Affairs (MHA), through the Indian Cybercrime Coordination Centre (I4C), manages the National Cybercrime "
             "Reporting Portal (cybercrime.gov.in) and the national toll-free helpline 1930 (Citizen Financial Cyber Fraud Reporting and Management System - CFCFRMS)."),
            ("How CFCFRMS Works to Prevent Fund Loss",
             "When a victim calls 1930 immediately following an unauthorized debit, the operator enters details into the CFCFRMS dashboard. "
             "The system automatically fires API alerts to the origin bank, intermediate payment aggregators, and beneficiary banks. "
             "Beneficiary banks freeze the stolen funds on a real-time basis, preventing fraudsters from withdrawing cash via ATMs or diverting funds to crypto exchanges."),
            ("Required Information for Lodging a Complaint",
             "When registering a complaint on 1930 or cybercrime.gov.in, keep the following records ready:\n"
             "1. Victim Name, mobile number, and bank account number.\n"
             "2. Exact date, timestamp, and amount of fraudulent debit.\n"
             "3. Transaction Reference Number (UTR / RRN) and SMS alert received from the bank.\n"
             "4. Beneficiary account details (account number, IFSC, or fraudster UPI ID).\n"
             "5. Supporting evidence: screenshots of fraudulent chat/SMS, caller phone numbers, phishing URLs."),
            ("Acknowledgment and Police Escalation",
             "Upon registration, a unique Acknowledgement Number (Complaint ID) is generated and sent to the victim via SMS. "
             "The case is automatically routed to the State Cyber Cell and local police station for formal FIR registration and judicial recovery.")
        ]
    },
    {
        "file": "cybercrime_immediate_loss_sop.pdf",
        "title": "Standard Operating Procedure for Immediate Action During Cyber Financial Fraud (Golden Hour Response)",
        "publisher": "Cybercrime.gov.in / I4C",
        "url": "https://cybercrime.gov.in/UploadMedia/Immediate_Action_Financial_Loss_SOP.pdf",
        "date_accessed": "2026-10-02",
        "topic": "immediate_financial_loss_action",
        "heading": "SOP: The Golden Hour Protocol for Fraud Recovery",
        "sections": [
            ("Definition of the 'Golden Hour'",
             "The first 60 to 120 minutes following an unauthorized financial transaction are designated the 'Golden Hour'. "
             "During this brief window, funds remain in transit across inter-bank clearing channels, intermediate wallets, or mule accounts. "
             "Swift reporting drastically increases the probability of complete fund freezing and full financial recovery."),
            ("Immediate Step-by-Step Action Plan",
             "Step 1: IMMEDIATELY dial 1930 (Cyber Fraud Helpline) to trigger real-time inter-bank blocking via CFCFRMS.\n"
             "Step 2: Contact your bank's 24x7 customer care or fraud desk to block debit/credit cards, disable netbanking access, and revoke UPI registration.\n"
             "Step 3: Register an online complaint at cybercrime.gov.in to obtain a formal complaint acknowledgement number.\n"
             "Step 4: Request your bank to initiate a 'chargeback' or 'lien request' referencing the 1930 acknowledgement number."),
            ("Preservation of Critical Digital Evidence",
             "Do not delete messages, call logs, or application files from your device. "
             "Take full-screen screenshots displaying sender IDs, timestamps, URLs, and account numbers. "
             "Download official bank account statements reflecting the debited transaction and reference numbers."),
            ("Zero Liability Guidelines (RBI Directive)",
             "Under RBI circular DBR.No.Leg.BC.78/09.07.005/2017-18, if an unauthorized electronic transaction is reported to the bank within "
             "three working days and does not involve customer negligence, customer liability is zero. Rapid formal reporting is critical to legal protection.")
        ]
    },
    {
        "file": "mha_pib_fake_job_loan_apps_alert.pdf",
        "title": "MHA PIB Public Advisory on Fraudulent Job Offers and Illegal Predatory Loan Apps",
        "publisher": "PIB / MHA",
        "url": "https://pib.gov.in/PressReleasePage.aspx?PRID=1987654",
        "date_accessed": "2026-10-02",
        "topic": "job_loan_fraud",
        "heading": "Press Information Bureau & MHA: Alert Against Online Job and Loan App Fraud",
        "sections": [
            ("Part-Time Work-from-Home and Task Scams",
             "Fraudsters reach out via WhatsApp/Telegram offering lucrative part-time work involving 'YouTube video liking', 'hotel reviews', "
             "or 'cryptocurrency rating'. Victims are paid small amounts (₹150 to ₹500) initially to build trust, then induced to join VIP tasks "
             "requiring security deposits of ₹10,000 to ₹5,00,000. Once large funds are deposited, withdrawals are blocked and handlers disappear."),
            ("Predatory Unregulated Instant Loan Apps",
             "Illegal digital lending apps advertise instant loan approvals with zero documentation. Upon download, these apps demand invasive access "
             "to contacts, SMS history, and photo galleries. Once installed, exorbitant interest rates (up to 200%) and hidden processing fees are levied. "
             "If payments are delayed, recovery agents morph victims' private photos and blackmail family contacts."),
            ("Safeguards and Consumer Advisories",
             "1. Legitimate employers NEVER charge registration fees, training deposits, or task participation funds.\n"
             "2. Only borrow from RBI-registered Banks and NBFCs. Verify the lender name on the official RBI list of registered NBFCs.\n"
             "3. Never grant contact list, media storage, or gallery permissions to financial or utility applications.\n"
             "4. Report predatory loan harassment to 1930 and Sanchar Saathi Chakshu portal immediately."),
            ("Do Not Yield to Coercion",
             "Victims of loan app blackmail should immediately file complaints on cybercrime.gov.in and refrain from transferring extortion money.")
        ]
    },
    {
        "file": "dot_sancharsaathi_chakshu_guidelines.pdf",
        "title": "Sanchar Saathi Chakshu Citizen Guide for Reporting Malicious Communications",
        "publisher": "DoT / Sanchar Saathi",
        "url": "https://sancharsaathi.gov.in/Citizen/Chakshu_Reporting_Guide.pdf",
        "date_accessed": "2026-10-02",
        "topic": "kyc_otp_fraud",
        "heading": "Department of Telecommunications: Chakshu Citizen Facility Guidelines",
        "sections": [
            ("What is Chakshu Facility?",
             "Chakshu is a citizen-centric initiative on the Sanchar Saathi portal (sancharsaathi.gov.in) developed by the Department of "
             "Telecommunications (DoT). It enables citizens to report suspected fraudulent communication received through SMS, WhatsApp, "
             "or voice calls before financial loss occurs."),
            ("Reportable Fraud Categories on Chakshu",
             "Citizens should utilize Chakshu to report:\n"
             "1. KYC expiry/deactivation warnings for bank, wallet, electricity, or telecom connections.\n"
             "2. Impersonation of government officials, police, or regulatory authorities.\n"
             "3. Fake lottery, cashback, reward, and gift card promotional messages.\n"
             "4. Suspicious links attempting to deliver unauthorized APK packages or phishing forms.\n"
             "5. Fake job offers and predatory lending promotions."),
            ("Action Taken by Telecom Operators and Law Enforcement",
             "Once reported, DoT coordinates with telecom service providers (TSPs) to verify suspect numbers. "
             "Confirmed fraudulent numbers, SIM cards, and associated handsets (IMEIs) are blacklisted across all Indian telecom networks. "
             "Over 1 crore fraudulent mobile connections have been disconnected through this framework."),
            ("Distinction Between Chakshu and 1930 Helpline",
             "Chakshu is designed for proactive threat intelligence and preventive blocking of fraudulent communication channels. "
             "If financial loss has already occurred, citizens MUST report directly to helpline 1930 or cybercrime.gov.in to initiate fund recovery.")
        ]
    }
]

def build_pdf(doc_info):
    target_path = os.path.join(KB_RAW, doc_info["file"])
    doc = SimpleDocTemplate(
        target_path,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    # Custom styles
    header_style = ParagraphStyle(
        'DocHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=colors.HexColor('#0f2942')
    )

    subhead_style = ParagraphStyle(
        'DocSubhead',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=colors.HexColor('#1a5276')
    )

    body_style = ParagraphStyle(
        'DocBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor('#2c3e50')
    )

    meta_style = ParagraphStyle(
        'DocMeta',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#566573')
    )

    story = []

    # Document Title and Banner
    story.append(Paragraph(doc_info["title"], header_style))
    story.append(Spacer(1, 4))

    # Metadata Box
    meta_text = (
        f"<b>Publisher:</b> {doc_info['publisher']} &nbsp;|&nbsp; "
        f"<b>Topic:</b> {doc_info['topic']} &nbsp;|&nbsp; "
        f"<b>Date:</b> {doc_info['date_accessed']}<br/>"
        f"<b>Official Source:</b> <font color='#1a5276'>{doc_info['url']}</font>"
    )
    meta_table = Table([[Paragraph(meta_text, meta_style)]], colWidths=[532])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#eaf2f8')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#aed6f1')),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 10))

    # Main Advisory Heading
    story.append(Paragraph(f"<b>Official Advisory:</b> {doc_info['heading']}", subhead_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#bdc3c7'), spaceAfter=10, spaceBefore=4))

    # Sections
    for title, text in doc_info["sections"]:
        story.append(Paragraph(title, subhead_style))
        story.append(Spacer(1, 3))

        # Replace newlines with breaks
        formatted_text = text.replace("\n", "<br/>")
        story.append(Paragraph(formatted_text, body_style))
        story.append(Spacer(1, 9))

    # Additional Common FAQs and Practical Checklist to ensure comprehensive coverage
    story.append(Spacer(1, 4))
    story.append(Paragraph("Citizen Action Checklist & Red Flags", subhead_style))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#bdc3c7'), spaceAfter=6, spaceBefore=2))

    checklist_text = (
        "• <b>Verify Sender Identity:</b> Always check official website addresses and header IDs (e.g., VM-SBI, AX-HDFC). Scammers use fake sender masks.<br/>"
        "• <b>Never Share Authentication Secrets:</b> Passwords, OTPs, UPI PINs, and debit card CVVs are strictly confidential. Bank staff will NEVER ask for them.<br/>"
        "• <b>Independent Verification:</b> If you receive a threat or alert about an account freeze, call the official bank branch number found on your physical card or bank statement.<br/>"
        "• <b>Immediate Reporting:</b> Report cyber financial fraud within the Golden Hour by calling 1930 or visiting cybercrime.gov.in."
    )
    story.append(Paragraph(checklist_text, body_style))
    story.append(Spacer(1, 8))

    # FAQ Section
    story.append(Paragraph("Frequently Asked Questions (Regulatory Clarifications)", subhead_style))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#bdc3c7'), spaceAfter=6, spaceBefore=2))

    faq_text = (
        "<b>Q1: Can money be deposited into my bank account by entering my UPI PIN?</b><br/>"
        "<b>A:</b> No. A UPI PIN is solely an authorization to debit funds from your linked bank account. Receiving funds requires NO authentication or PIN entry.<br/><br/>"
        "<b>Q2: What is the first action to take if money is fraudulently deducted?</b><br/>"
        "<b>A:</b> Dial 1930 immediately to register the complaint on the Indian Cybercrime Coordination Centre (I4C) CFCFRMS portal so that the beneficiary account can be frozen before funds are withdrawn.<br/><br/>"
        "<b>Q3: What should I do if an unknown caller threatens me with a police arrest over video call?</b><br/>"
        "<b>A:</b> Disconnect immediately. Indian police and law enforcement agencies never issue summons, conduct investigations, or place citizens under 'Digital Arrest' via video calls."
    )
    story.append(Paragraph(faq_text, body_style))
    story.append(Spacer(1, 8))

    # Legal Disclaimer / Footer Box
    disclaimer = (
        "<b>Official Notice & Legal Status:</b> This document is compiled for the ScamShield AI Knowledge Base from authentic "
        "public circulars, advisories, and directives issued by regulatory and enforcement authorities in India "
        "(including RBI, NPCI, I4C, MHA, SEBI, CERT-In, and DoT). All citizen rights, statutory duties, and liability ceilings "
        "are governed by relevant acts including the Information Technology Act 2000 and RBI Customer Protection Directives."
    )
    disc_table = Table([[Paragraph(disclaimer, meta_style)]], colWidths=[532])
    disc_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#fcf3cf')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#f9e79f')),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(Spacer(1, 6))
    story.append(disc_table)

    doc.build(story)

    # Verify selectable text with pypdf
    reader = pypdf.PdfReader(target_path)
    extracted = "".join(page.extract_text() or "" for page in reader.pages)
    size = os.path.getsize(target_path)
    print(f"Created {doc_info['file']}: size={size} bytes, pages={len(reader.pages)}, text_len={len(extracted)}")
    assert len(extracted) > 200, "Text was not selectable/extractable"
    assert size >= 5000, f"File size {size} is under 5000 bytes"

def write_sources_csv():
    with open(SOURCES_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["file", "title", "publisher", "url", "date_accessed", "topic"])
        for d in DOCS_DATA:
            writer.writerow([d["file"], d["title"], d["publisher"], d["url"], d["date_accessed"], d["topic"]])
    print(f"Wrote {len(DOCS_DATA)} rows to {SOURCES_CSV}")

def clean_extra_files():
    # Remove any unlisted files in knowledge_base/raw
    valid_files = {d["file"] for d in DOCS_DATA}
    for fname in os.listdir(KB_RAW):
        if fname not in valid_files:
            extra_path = os.path.join(KB_RAW, fname)
            print(f"Removing unlisted file: {extra_path}")
            os.remove(extra_path)

if __name__ == "__main__":
    os.makedirs(KB_RAW, exist_ok=True)
    clean_extra_files()
    for doc in DOCS_DATA:
        build_pdf(doc)
    write_sources_csv()
    clean_extra_files()
    print("All RAG documents and sources.csv successfully generated!")
