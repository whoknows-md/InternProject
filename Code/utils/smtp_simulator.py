from flask import render_template
import os



def simulate_send_email(username, phishing_link, template_name="login_security_notice.html"):
    # Extract the inbox link from the URL
    inbox_link = phishing_link.split("/")[-1]

    phishing_link = f"/user/phishing_page/{inbox_link}"


    rendered_email = render_template(
        f"email/{template_name}", 
        phishing_link=phishing_link, 
        link=inbox_link, 
        username=username
    )

    print(f"\n----- Simulated Email to {username} -----")
    print(rendered_email)
    print("----------------------------------------\n")

