import github
import urllib.request
from random import randint
import smtplib
from email.mime.text import MIMEText
import csv

from tempfile import NamedTemporaryFile
import shutil



def send_otp(mob, otp):

    '''

    This function is to send sms to mobile number.

    :param mob: Mobile number of user from home screen
    :param otp: OTP generated for mobile number
    :return: true if OTP sent successfully or false, vice versa
    '''

    url = 'https://www.fast2sms.com/dev/bulkV2?authorization=6s5lqvF2opwc3M5IE9s5NCNFBscKPikRbSbMtoPl4jTLa1O9SAmu9SZVyV9M&route=v3&sender_id=TXTIND&message=%0Afrom%20Baseoca.com,%0A%0AOTP%20for%20creating%20order%20is%20:%20'+ str(otp) +'%0A%0A&language=english&flash=0&numbers='+str(mob)

    with urllib.request.urlopen(url) as response:
        html = response.read().decode()
        return str(html).split(":")[1].split(',')[0]


def check_mob_otp(mob, otp):
    '''

    This function is to check whether unverified mobile number exist in list or not.
    If yes, only OTP is updated.
    If no, entire record is created.

    :param mob: Mobile number of user
    :param otp: OTP generated for current session
    :return: None
    '''

    with open('contact.csv', 'r') as file:
        reader = csv.reader(file)
        lookup = mob
        mob_found = False
        for row in reader:
            if lookup in row:
                update_only_otp_to_user(mob, otp)
                mob_found = True
                break

        if mob_found == False:
            enter_mob(mob, otp)



def enter_mob(mob, otp):
    '''

    Adding data to database when unverified mobile number is encountered for first time

    :param mob: Mobile number of user
    :param otp: OTP of current instance
    :return: None
    '''

    with open('contact.csv', 'a', newline='\n') as f:
        writer = csv.writer(f)
        writer.writerow([mob, otp, 0])


def update_only_otp_to_user(mob, otp):

    '''

    Updating existing unverified mobile number with session OTP and incrementing counter by 1.
    Max 10 OTP messages are allowed. After that mobile number will be blocked.

    :param mob: Mobile of user
    :param otp: OTP of current session
    :return: None
    '''

    lines = list()
    with open('contact.csv', 'r') as readFile:
        reader = csv.reader(readFile)
        for row in reader:
            lines.append(row)
            for field in row:
                if field[0] == mob:
                    lines.remove(row)

    with open('contact.csv', 'w' ,newline='\n') as writeFile:
        writer = csv.writer(writeFile)
        for i in range(len(lines)):
            if lines[i][0]!=mob:
                writer.writerow([lines[i][0], lines[i][1], lines[i][2]])
            else:
                writer.writerow([mob, otp, 0])


def check_otp_of_user(mob,otp):

    '''

    To verify that mobile number and OTP provided by user matches with each other.

    :param mob: Mobile number of user
    :param otp: OTP of current session
    :return: true if matches, false if vice versa

    '''

    with open('contact.csv', 'r') as file:
        reader = csv.reader(file)
        lookup = mob
        for row in reader:
            if lookup in row:
                if row[1] == otp:
                    return True
                else:
                    return False



def send_mail_to_backoffice(session_state):
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login("baseoca.frontoffice@gmail.com", "Reven@nt@1985")
    message = '<html></html>'
    my_email = MIMEText(message, "html")
    my_email["Subject"] = "Test Status : "
    s.sendmail("baseoca.frontoffice@gmail.com", "baseoca.backoffice@gmail.com", 'Test')
    s.quit()
