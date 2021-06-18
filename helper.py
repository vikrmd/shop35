from email import encoders
import github
import urllib.request
from random import randint
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
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

def create_cart_entry(session_state, cur_date, cart_id, name, pincode, email, address, total_final_actual_cost, item_count):

    with open('cart_book.csv', 'a', newline='\n') as f:
        writer = csv.writer(f)
        writer.writerow([cart_id, cur_date, str(name).replace(',',' '), str(address).replace(',',' '), session_state.mobile, pincode, str(email).replace(',',' '), total_final_actual_cost, item_count])

    return [cart_id, cur_date, str(name).replace(',',' '), str(address).replace(',',' '), session_state.mobile, pincode, str(email).replace(',',' '), total_final_actual_cost, item_count]


def create_order_entry(session_state, cur_date, cart_id, name, pincode, email, address, total_final_actual_cost, item_count, item_info):
    item_arr = []
    with open('order_book.csv', 'a', newline='\n') as f:
        writer = csv.writer(f)
        for k in range(len(item_info)):
            writer.writerow([cart_id, str(cart_id) + '_' + str(k+1),cur_date, str(name).replace(',', ' '), str(address).replace(',', ' '), session_state.mobile, pincode, str(email).replace(',', ' '), total_final_actual_cost, item_count, 'NA', 'Order Processing in Progress',item_info[k][0], item_info[k][1], item_info[k][2], item_info[k][3], item_info[k][4], item_info[k][5]])
            item_arr.append([cart_id, str(cart_id) + '_' + str(k+1),cur_date, str(name).replace(',', ' '), str(address).replace(',', ' '), session_state.mobile, pincode, str(email).replace(',', ' '), total_final_actual_cost, item_count, 'NA', 'Order Processing in Progress',item_info[k][0], item_info[k][1], item_info[k][2], item_info[k][3], item_info[k][4], item_info[k][5]])

    return item_arr


def send_mail_to_backoffice(session_state, cart_data, order_data):

    #my_subject = "[Online Order][Cart Id: "+ str(cart_data[0]) +"][Value: "+ str(cart_data[7]) +"][Item Count: "+ str(cart_data[-1]) +"][Mobile: "+ str(cart_data[4]) +"]"
    my_subject = str(cart_data[0])

    data_str = ''
    data_str = data_str + '<table style="width: 100%; background-color: rgb(221, 223, 211); color: rgb(25, 10, 240); border-collapse: collapse;">'
    data_str = data_str + '    <tbody>'
    data_str = data_str + '        <tr>'
    data_str = data_str + '            <td style="width: 33.3333%;"><span style="font-family: Verdana, Geneva, sans-serif; font-size: 13px;"><strong>Cart Id:</strong> '+ cart_data[0] +'</span></td>'
    data_str = data_str + '            <td style="width: 33.3333%;"><span style="font-size: 13px;"><span style="font-family: Verdana, Geneva, sans-serif;"><strong>Date:</strong> '+ str(cart_data[1]) +'</span></span></td>'
    data_str = data_str + '            <td style="width: 33.3333%;"><span style="font-size: 13px;"><span style="font-family: Verdana, Geneva, sans-serif;"><strong>Cart Value:&nbsp;</strong> '+ str(cart_data[7]) +'</span></span></td>'
    data_str = data_str + '        </tr>'
    data_str = data_str + '        <tr>'
    data_str = data_str + '            <td style="width: 33.3333%;"><span style="font-size: 13px;"><span style="font-family: Verdana, Geneva, sans-serif;"><strong>Name:</strong> '+ cart_data[2] +'</span></span></td>'
    data_str = data_str + '            <td style="width: 33.3333%;"><span style="font-size: 13px;"><span style="font-family: Verdana, Geneva, sans-serif;"><strong>Mobile:</strong> '+ cart_data[4] +'</span></span></td>'
    data_str = data_str + '            <td style="width: 33.3333%;"><span style="font-size: 13px;"><span style="font-family: Verdana, Geneva, sans-serif;"><strong>Items:</strong> '+ str(cart_data[8]) +'</span></span></td>'
    data_str = data_str + '        </tr>'
    data_str = data_str + '        <tr>'
    data_str = data_str + '            <td style="width: 33.3333%;"><span style="font-size: 13px;"><span style="font-family: Verdana, Geneva, sans-serif;"><strong>Address:</strong> '+ cart_data[3] +'</span></span></td>'
    data_str = data_str + '            <td style="width: 33.3333%;"><span style="font-size: 13px;"><span style="font-family: Verdana, Geneva, sans-serif;"><strong>Pincode:</strong> '+ cart_data[5] +'</span></span></td>'
    data_str = data_str + '            <td style="width: 33.3333%;"><span style="font-family: Verdana, Geneva, sans-serif; font-size: 13px;"><strong>Email:</strong> '+ cart_data[6] +'</span></td>'
    data_str = data_str + '        </tr>'
    data_str = data_str + '    </tbody>'
    data_str = data_str + '</table>'

    attachments_img = []

    for k in range(len(order_data)):
        data_str = data_str + '<table style="width: 100%; background-color: rgb(251, 255, 0); color: rgb(240, 44, 10); border-collapse: collapse;">'
        data_str = data_str + '    <tbody>'
        data_str = data_str + '        <tr>'
        data_str = data_str + '            <td class="fr-cell-fixed " style="width: 33.3333%;"><span style="font-family: Verdana, Geneva, sans-serif; font-size: 13px;"><strong>Item:</strong> '+ str(k+1) +'</span></td>'
        data_str = data_str + '            <td style="width: 33.3333%;"><span style="font-size: 13px;"><span style="font-family: Verdana, Geneva, sans-serif;"><strong>Qty:</strong> '+ str(order_data[k][-3]) +'</span></span></td>'
        data_str = data_str + '            <td style="width: 33.3333%;"><span style="font-size: 13px;"><span style="font-family: Verdana, Geneva, sans-serif;"><strong>Size:&nbsp;</strong> '+ str(order_data[k][-2]) +'</span></span></td>'
        data_str = data_str + '        </tr>'
        data_str = data_str + '        <tr>'
        data_str = data_str + '            <td colspan="3" style="width: 99.8469%;"><span style="font-size: 13px;"><span style="font-family: Verdana, Geneva, sans-serif;"><strong>url:</strong> '+ str(order_data[k][-6]) +'</span></span></td>'
        data_str = data_str + '        </tr>'
        data_str = data_str + '        <tr>'
        data_str = data_str + '            <td class="fr-cell-handler " style="width: 33.3333%;"><br></td>'
        data_str = data_str + '            <td style="width: 33.3333%;"><br></td>'
        data_str = data_str + '            <td style="width: 33.3333%;"><span style="font-family: Verdana, Geneva, sans-serif; font-size: 13px;"><strong>Amount:</strong> '+ str(order_data[k][-1]) +'</span></td>'
        data_str = data_str + '        </tr>'
        data_str = data_str + '    </tbody>'
        data_str = data_str + '</table>'
        attachments_img.append('img_folder/'+str(order_data[k][-6]).split('/')[-1].strip() +'.jpg')

    # email object that has multiple part:
    msg = MIMEMultipart()
    msg['From'] = 'baseoca.frontoffice@gmail.com'
    msg['To'] = 'baseoca.backoffice@gmail.com'
    if session_state.user_status != 'verified_as_guest':
        msg['Subject'] = "NEW ONLINE ORDER " + my_subject
    else:
        msg['Subject'] = "NEW GUEST ORDER " + my_subject

    # attache a MIMEText object to save email content
    message =  data_str
    msg_content = MIMEText(message, "html")
    msg.attach(msg_content)

    # to add an attachment is just add a MIMEBase object to read a picture locally.

    for h in range(len(attachments_img)):
        with open(attachments_img[h], 'rb') as f:
            # set attachment mime and file name, the image type is png
            mime = MIMEBase('image', 'jpg', filename=attachments_img[h])
            # add required header data:
            mime.add_header('Content-Disposition', 'attachment', filename=attachments_img[h])
            mime.add_header('X-Attachment-Id', '0')
            mime.add_header('Content-ID', '<0>')
            # read attachment file content into the MIMEBase object
            mime.set_payload(f.read())
            # encode with base64
            encoders.encode_base64(mime)
            # add MIMEBase object to MIMEMultipart object
            msg.attach(mime)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("baseoca.frontoffice@gmail.com", "Reven@nt1985")
    server.sendmail("baseoca.frontoffice@gmail.com", "baseoca.backoffice@gmail.com", msg.as_string())
    server.quit()

    # s = smtplib.SMTP('smtp.gmail.com', 587)
    # s.starttls()
    # s.login("baseoca.frontoffice@gmail.com", "Reven@nt1985")

    # my_email["Subject"] = "NEW ONLINE ORDER " + my_subject
    #
    # s.sendmail("baseoca.frontoffice@gmail.com", "baseoca.backoffice@gmail.com", my_email.as_string())
    # s.quit()
