import smtplib
sender = "suhavangupta@gmail.com"
receivers = ["suhavangupta@gmail.com"]
yourname = "proHUB team"
recvname = "receptionist"
sub = "Testing email"
body = "who cares"
message = "From: " + yourname + "\n" 
message = message + "To: " + recvname + "\n"
message = message + "Subject: " + sub + "\n" 
message = message + body
try:
    print "Sending email to " + recvname + "...",
    server = smtplib.SMTP(host='smtp.gmail.com', port=587)
    username = 'suhavangupta@gmail.com'  
    password = 'wfK3&;sr'  
    server.ehlo()
    server.starttls()  
    server.login(username,password)  
    server.sendmail(sender, receivers, message)         
    server.quit()
    print "successfully sent!"
except  Exception:
    print "Error: unable to send email"