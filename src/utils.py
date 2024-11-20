import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email_notification(title, notion_url, email, email_pass):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    # Créez le message
    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = email
    msg['Subject'] = title

    # Ajoutez le contenu du message
    html_content = f"""
            <html>
                <body style="font-family: Arial, sans-serif; background-color: #2e2e2e; color: #333; padding: 20px;">
                    <div style="max-width: 600px; margin: 0 auto; background-color: #f0f0f0; padding: 20px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);">
                        <img src="https://img.icons8.com/ios7/600/notion.png" alt="Notion Logo" style="width: 50px; display: block; margin: 0 auto;">
                        <h3 style="color: #000000; text-align: center; font-size: 24px; font-weight: bold;">{title}</h3>
                        <p style="font-size: 16px; color: #000000; line-height: 1.6; text-align: center;">Bonne lecture : 
                            <a href="{notion_url}" style="font-weight: bold;">Cliquez ici pour lire</a>
                        </p>
                    </div>
                </body>
            </html>
            """

    msg.attach(MIMEText(html_content, 'html'))
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Sécuriser la connexion
        server.login(email, email_pass) 
        text = msg.as_string()  
        server.sendmail(email, email, text)  
        server.quit()  

        print("Notification email envoyée avec succès !")
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'email : {e}")
