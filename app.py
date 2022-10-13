"""

Todo:
Docstrings
Clean up
Protect email details etc once have a proper account and not a rubbish disposable gmail
Improve report emails - yagmail has better formatting options
Implement OTP/email verification
Wider reporting emails
Update this to reflect the structure required for pythonanywhere so can just zip and upload
Have email kept in session automatically entered into forms w/ disabled boxes
Same w/ date
    Email/date can also just be hidden fields
Adding in extra forms/pages fairly easy, just can create new templates etc
Styling out of HTML files and into static CSS files within blueprint dirs
Uploaded files stored in memory as bytesIO instead of saving to disk
Add home icon to mobile navbar with hamburger
Main logo needs responsive sizing not fixed
PDF reports: https://github.com/Edinburgh-Genome-Foundry/pdf_reports
Notification width lower
Make datapack file upload less ugly and also files mandatory
Make session expire and invalidate the OTP

"""

from . import create_app

app = create_app()
