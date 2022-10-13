"""

Todo:
Docstrings
Clean up
Protect email details etc once have a proper account and not a rubbish disposable gmail
Improve report emails - yagmail has better formatting options
Wider reporting emails
Update this to reflect the structure required for pythonanywhere so can just zip and upload
Have email kept in session automatically entered into forms w/ disabled boxes <- Low prio, probably dont bother
Same w/ date
    Email/date can also just be hidden fields

Styling out of HTML files and into static CSS files within blueprint dirs
Uploaded files stored in memory as bytesIO instead of saving to disk

PDF reports: https://github.com/Edinburgh-Genome-Foundry/pdf_reports
Notification width lower

https://pypi.org/project/flask-bigapp/
Remove text from cards, only have items in it?
add validators to forms, mandatory fields etc
use tempfile.gettempdir() etc for temp file storage

"""

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0")
