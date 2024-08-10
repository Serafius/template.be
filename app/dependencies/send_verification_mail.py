import requests

def send_verification_mail(name,verify_code):
    MAILGUN_API_KEY = ""
    MAILGUN_DOMAIN = ""

    message = f"Hey {name},\nThank you for registering at template, to continue your registration, please use the code below to verify your account.\n\n\n\n {verify_code}\n\n\n\n If you did not register please ignore this email...\n\n--  AI"

    response = requests.post(
        f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages",
        auth=("api", MAILGUN_API_KEY),
        data={
            "from": "  AI <noreply@ .app>",
            "to": "talhadoga@hotmail.com",
            "subject": "  AI template E-Mail Verification.",
            "text": message,
        },
    )
    if response.status_code == 200:
        print("E-mail succeed.")
    else:
        print("E-mail failed.")