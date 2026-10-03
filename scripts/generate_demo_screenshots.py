"""Script to generate realistic demo screenshots for ScamShield AI (Task T8).
Produces 6 distinct screenshots in ml/data/demo_screenshots/ covering:
- Light mode
- Dark mode
- Cropped
- Slightly blurry
- With link
- Two messages
"""

import os

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DEST_DIR = os.path.join(ROOT, "ml", "data", "demo_screenshots")
os.makedirs(DEST_DIR, exist_ok=True)

def get_font(size=18, bold=False):
    # Try common Windows TrueType fonts, fallback to default
    font_names = ["segoeui.ttf", "arial.ttf", "calibri.ttf"]
    if bold:
        font_names = ["segoeuib.ttf", "arialbd.ttf", "calibrib.ttf"]
    for fn in font_names:
        try:
            return ImageFont.truetype(fn, size)
        except Exception:
            continue
    return ImageFont.load_default()

def draw_rounded_rect(draw, bbox, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(bbox, radius=radius, fill=fill, outline=outline, width=width)

def generate_screenshot_1_light_kyc():
    # 1. Light mode Android SMS with link
    img = Image.new("RGB", (650, 420), color="#f4f6f8")
    d = ImageDraw.Draw(img)

    font_title = get_font(20, bold=True)
    font_sub = get_font(13)
    font_text = get_font(16)
    font_time = get_font(12)

    # App Header
    d.rectangle([(0, 0), (650, 70)], fill="#ffffff")
    d.text((30, 16), "VM-SBIIN (State Bank of India)", font=font_title, fill="#1a1a1a")
    d.text((30, 44), "Official Banking Service SMS", font=font_sub, fill="#757575")
    d.line([(0, 70), (650, 70)], fill="#e0e0e0", width=1)

    # Date Pill
    d.rounded_rectangle([(270, 90), (380, 115)], radius=12, fill="#e8eaed")
    d.text((288, 95), "Today, 11:42 AM", font=font_time, fill="#5f6368")

    # Chat Bubble (Light Mode)
    bubble_box = [(40, 135), (610, 315)]
    draw_rounded_rect(d, bubble_box, radius=16, fill="#ffffff", outline="#dadce0", width=1)

    msg_lines = [
        "Dear Customer,",
        "Your SBI account has been suspended due to pending KYC",
        "documents. Update PAN immediately to avoid permanent",
        "blockage: http://sbi-kyc-update.example.xyz/pan",
        "",
        "Treat as urgent to maintain active NetBanking facility."
    ]
    y = 150
    for line in msg_lines:
        color = "#1a73e8" if "http://" in line else "#202124"
        d.text((60, y), line, font=font_text, fill=color)
        y += 24

    d.text((540, 290), "11:42 AM", font=font_time, fill="#70757a")

    out_path = os.path.join(DEST_DIR, "screenshot_01_kyc_sms_light.png")
    img.save(out_path)
    print(f"Saved {out_path}")

def generate_screenshot_2_dark_upi():
    # 2. Dark mode WhatsApp message (UPI refund collect request)
    img = Image.new("RGB", (650, 400), color="#121b22")
    d = ImageDraw.Draw(img)

    font_title = get_font(20, bold=True)
    font_sub = get_font(13)
    font_text = get_font(16)
    font_time = get_font(12)

    # Header
    d.rectangle([(0, 0), (650, 70)], fill="#1f2c34")
    d.text((30, 16), "PhonePe Customer Support", font=font_title, fill="#e9edef")
    d.text((30, 44), "Online • +91 91234 56789", font=font_sub, fill="#8696a0")

    # Dark Bubble (#005c4b is WhatsApp dark sent, #202c33 is received)
    draw_rounded_rect(d, [(40, 110), (610, 320)], radius=12, fill="#202c33")

    msg_lines = [
        "Congratulations!",
        "You received Rs 2,500 cashback reward in GooglePay.",
        "Click here to approve collect request and enter UPI PIN:",
        "http://gpay-reward-collect.example.xyz",
        "",
        "Note: Funds will be credited directly to your bank."
    ]
    y = 125
    for line in msg_lines:
        color = "#53bdeb" if "http://" in line else "#e9edef"
        d.text((60, y), line, font=font_text, fill=color)
        y += 26

    d.text((535, 295), "14:15", font=font_time, fill="#8696a0")

    out_path = os.path.join(DEST_DIR, "screenshot_02_upi_collect_dark.png")
    img.save(out_path)
    print(f"Saved {out_path}")

def generate_screenshot_3_two_messages():
    # 3. Two messages in one chat (Job scam)
    img = Image.new("RGB", (650, 520), color="#efeae2")
    d = ImageDraw.Draw(img)

    font_title = get_font(19, bold=True)
    font_sub = get_font(13)
    font_text = get_font(15)
    font_time = get_font(11)

    # Header
    d.rectangle([(0, 0), (650, 65)], fill="#075e54")
    d.text((25, 14), "HR Talent Acquisition Team", font=font_title, fill="#ffffff")
    d.text((25, 40), "+91 82345 67890 • Amazon Recruiter", font=font_sub, fill="#d1e7dd")

    # Bubble 1: Offer
    draw_rounded_rect(d, [(30, 95), (620, 235)], radius=10, fill="#ffffff")
    b1_lines = [
        "Dear Candidate,",
        "Work From Home Opportunity: Earn Rs 3,000 to Rs 8,000 daily",
        "by simply liking YouTube videos and rating hotels on Google.",
        "Immediate same-day payments directly to your UPI ID."
    ]
    y = 110
    for line in b1_lines:
        d.text((45, y), line, font=font_text, fill="#111b21")
        y += 25
    d.text((560, 215), "10:05 AM", font=font_time, fill="#667781")

    # Bubble 2: Trap / Fee
    draw_rounded_rect(d, [(30, 255), (620, 455)], radius=10, fill="#ffffff")
    b2_lines = [
        "To activate your employee portal and begin tasks,",
        "please transfer a one-time refundable uniform & ID kit",
        "security registration fee of Rs 1,450.",
        "Join VIP Telegram group: http://t-telegram.example.xyz/earn-daily",
        "",
        "Limited slots available for today's batch."
    ]
    y = 270
    for line in b2_lines:
        color = "#027eb5" if "http://" in line else "#111b21"
        d.text((45, y), line, font=font_text, fill=color)
        y += 25
    d.text((560, 435), "10:06 AM", font=font_time, fill="#667781")

    out_path = os.path.join(DEST_DIR, "screenshot_03_job_offer_two_msgs.png")
    img.save(out_path)
    print(f"Saved {out_path}")

def generate_screenshot_4_cropped_delivery():
    # 4. Cropped screenshot of delivery scam
    img = Image.new("RGB", (560, 240), color="#ffffff")
    d = ImageDraw.Draw(img)

    font_badge = get_font(13, bold=True)
    font_text = get_font(15)
    font_time = get_font(11)

    # Card Border
    draw_rounded_rect(d, [(10, 10), (550, 230)], radius=12, fill="#fdfefe", outline="#cbd5e1", width=2)

    # Top Alert Badge
    d.rounded_rectangle([(25, 22), (180, 46)], radius=6, fill="#fee2e2")
    d.text((35, 26), "POSTAL DISPATCH ALERT", font=font_badge, fill="#991b1b")
    d.text((460, 26), "Just now", font=font_time, fill="#64748b")

    lines = [
        "IndiaPost: Your package IND938201 could not be delivered",
        "due to wrong address details. Update address and pay",
        "re-delivery fee Rs 48: http://indiapost-parcel-update.example.xyz",
        "Unclaimed parcels are returned to sender within 24 hours."
    ]
    y = 65
    for line in lines:
        color = "#2563eb" if "http://" in line else "#0f172a"
        d.text((25, y), line, font=font_text, fill=color)
        y += 28

    out_path = os.path.join(DEST_DIR, "screenshot_04_delivery_cropped.png")
    img.save(out_path)
    print(f"Saved {out_path}")

def generate_screenshot_5_blurry_police():
    # 5. Slightly blurry police impersonation
    img = Image.new("RGB", (620, 360), color="#f1f5f9")
    d = ImageDraw.Draw(img)

    font_header = get_font(18, bold=True)
    font_text = get_font(15)
    font_time = get_font(12)

    # Notification Box
    draw_rounded_rect(d, [(30, 40), (590, 320)], radius=14, fill="#ffffff", outline="#94a3b8", width=1)

    d.text((50, 60), "CENTRAL BUREAU OF INVESTIGATION (CBI)", font=font_header, fill="#b91c1c")
    d.line([(50, 90), (570, 90)], fill="#e2e8f0", width=1)

    lines = [
        "LEGAL NOTICE / DIGITAL ARREST WARRANT:",
        "An illegal parcel containing banned narcotics and fake passports",
        "has been seized under your Aadhaar registration at Mumbai Customs.",
        "You are placed under immediate Digital Arrest.",
        "Connect with investigating officer on Skype immediately.",
        "Failure to appear within 1 hour will result in local police raid."
    ]
    y = 105
    for line in lines:
        color = "#b91c1c" if "DIGITAL ARREST" in line else "#1e293b"
        d.text((50, y), line, font=font_text, fill=color)
        y += 28

    d.text((500, 290), "16:48 PM", font=font_time, fill="#64748b")

    # Apply subtle blur to test OCR robustness under realistic camera conditions
    blurred = img.filter(ImageFilter.GaussianBlur(radius=0.75))

    out_path = os.path.join(DEST_DIR, "screenshot_05_police_digital_arrest_blurry.png")
    blurred.save(out_path)
    print(f"Saved {out_path}")

def generate_screenshot_6_electricity():
    # 6. Electricity disconnection notice (Android Notification Banner)
    img = Image.new("RGB", (600, 260), color="#f8fafc")
    d = ImageDraw.Draw(img)

    font_header = get_font(16, bold=True)
    font_text = get_font(14)
    font_time = get_font(11)

    draw_rounded_rect(d, [(20, 20), (580, 240)], radius=16, fill="#ffffff", outline="#e2e8f0", width=1)

    d.text((40, 35), "⚡ Electricity Department (Urgent Notice)", font=font_header, fill="#c2410c")
    d.text((500, 38), "19:10", font=font_time, fill="#94a3b8")
    d.line([(40, 65), (560, 65)], fill="#f1f5f9", width=1)

    lines = [
        "Dear Consumer, power supply to your meter connection will be",
        "disconnected tonight at 9:30 PM due to unpaid previous month bill.",
        "Immediate bill settlement required to prevent line cancellation.",
        "Call Electricity Line Officer immediately or visit your local sub-division office."
    ]
    y = 80
    for line in lines:
        d.text((40, y), line, font=font_text, fill="#334155")
        y += 26

    out_path = os.path.join(DEST_DIR, "screenshot_06_electricity_cutoff.png")
    img.save(out_path)
    print(f"Saved {out_path}")

if __name__ == "__main__":
    generate_screenshot_1_light_kyc()
    generate_screenshot_2_dark_upi()
    generate_screenshot_3_two_messages()
    generate_screenshot_4_cropped_delivery()
    generate_screenshot_5_blurry_police()
    generate_screenshot_6_electricity()
    print("All 6 demo screenshots generated successfully!")
