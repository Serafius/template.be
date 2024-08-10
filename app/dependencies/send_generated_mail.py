import requests

def send_generated_mail(receiver, name, link):
    MAILGUN_API_KEY = ""
    MAILGUN_DOMAIN = ""

    message = f"Hey {name},\nThank you for using template. Your video is ready. Click the link below to watch!\n\n\n\n {link}\n\n\n\n\n\n--  AI"

    response = requests.post(
        f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages",
        auth=("api", MAILGUN_API_KEY),
        data={
            "from": "  AI <noreply@ .app>",
            "to": receiver,
            "subject": "  AI template Video Information.",
            "text": message,
        },
    )
    if response.status_code == 200:
        print("E-mail succeed.")
    else:
        print("E-mail failed.")