import github
import urllib.request
from random import randint
import smtplib
from email.mime.text import MIMEText


def verify_user(mob):

    g = github.Github('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')
    repo = g.get_user().get_repo("baseoca_backoffice")
    contents = repo.get_contents("contact.csv", ref="main")

    lines = contents.decoded_content.decode("utf-8")
    data_arr = lines.splitlines()
    lookup = mob

    for i in range(len(data_arr)):
        ref_arr = data_arr[i].split(',')
        if mob == ref_arr[0]:
            data_arr = lines.splitlines()
            lookup = mob
            otp = randint(10000, 99999)

            for i in range(len(data_arr)):
                ref_arr = data_arr[i].split(',')
                if ref_arr[0] == lookup:
                    curr_arr = data_arr[i].split(',')
                    curr_arr[0] = lookup
                    curr_arr[1] = otp
                    curr_arr[2] = 'unverified'
                    curr_arr[3] = ref_arr[3]
                    data_arr[i] = str(curr_arr[0]) + ',' + str(curr_arr[1]) + ',' + str(curr_arr[2]) + ',' + str(
                        curr_arr[3])
                    break

            updated_data = ''
            for i in range(len(data_arr)):
                updated_data = updated_data + data_arr[i] + '\n'

            # print(contents.decoded_content)
            repo.update_file("mob_name.csv", "update otp activty", updated_data, contents.sha, branch="main")

        else:
            repo.update_file("mob_name.csv", "update otp activity",
                             contents.decoded_content.decode("utf-8") + "" + str(mob) + "," + '12345' + ",unverified,0\n",
                             contents.sha, branch="main")

    return False



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

    g = github.Github('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')
    repo = g.get_user().get_repo("baseoca_backoffice")
    contents = repo.get_contents("contact.csv", ref="main")

    lookup = mob

    if str(contents.decoded_content).find(lookup) == -1:
        enter_mob(mob, otp)
    else:
        update_only_otp_to_user(mob, otp)


def enter_mob(mob, otp):
    '''

    Adding data to database when unverified mobile number is encountered for first time

    :param mob: Mobile number of user
    :param otp: OTP of current instance
    :return: None
    '''

    g = github.Github('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')
    repo = g.get_user().get_repo("baseoca_backoffice")
    contents = repo.get_contents("contact.csv", ref="main")

    repo.update_file("contact.csv", "update otp activty",
                     contents.decoded_content.decode("utf-8") + "" + str(mob) + "," + str(otp) + ",0\n",
                     contents.sha, branch="main")


def update_only_otp_to_user(mob, otp):

    '''

    Updating existing unverified mobile number with session OTP and incrementing counter by 1.
    Max 10 OTP messages are allowed. After that mobile number will be blocked.

    :param mob: Mobile of user
    :param otp: OTP of current session
    :return: None
    '''

    g = github.Github('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')
    repo = g.get_user().get_repo("baseoca_backoffice")
    contents = repo.get_contents("contact.csv", ref="main")

    lines = contents.decoded_content.decode("utf-8")
    data_arr = lines.splitlines()
    lookup = mob
    otp = otp

    for i in range(len(data_arr)):
        ref_arr = data_arr[i].split(',')
        if ref_arr[0] == lookup:
            curr_arr = data_arr[i].split(',')
            curr_arr[0] = lookup
            curr_arr[1] = otp
            curr_arr[2] = int(ref_arr[-1])+1
            data_arr[i] = str(curr_arr[0]) + ',' + str(curr_arr[1]) + ',' + str(curr_arr[2])
            break

    updated_data = ''
    for i in range(len(data_arr)):
        updated_data = updated_data + data_arr[i] + '\n'

    # print(contents.decoded_content)
    repo.update_file("contact.csv", "update otp activty", updated_data, contents.sha, branch="main")


def user_counter(mob):
    g = github.Github('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')
    repo = g.get_user().get_repo("shop35")
    contents = repo.get_contents("mob_name.csv", ref="main")

    lines = contents.decoded_content.decode("utf-8")
    data_arr = lines.splitlines()
    lookup = mob

    for i in range(len(data_arr)):
        ref_arr = data_arr[i].split(',')
        if ref_arr[0] == lookup:
            curr_arr = data_arr[i].split(',')
            curr_arr[0] = lookup
            curr_arr[1] = ref_arr[1]
            curr_arr[2] = ref_arr[2]
            curr_arr[3] = str(int(ref_arr[3]) + 1)
            data_arr[i] = curr_arr[0] + ',' + curr_arr[1] + ',' + curr_arr[2] + ',' + curr_arr[3]
            break

    updated_data = ''
    for i in range(len(data_arr)):
        updated_data = updated_data + data_arr[i] + '\n'

    # print(contents.decoded_content)
    repo.update_file("mob_name.csv", "update otp activty", updated_data, contents.sha, branch="main")


def check_otp_of_user(mob,otp):

    '''

    To verify that mobile number and OTP provided by user matches with each other.

    :param mob: Mobile number of user
    :param otp: OTP of current session
    :return: true if matches, false if vice versa

    '''

    # updating data post otp verification

    g = github.Github('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')
    repo = g.get_user().get_repo("baseoca_backoffice")
    contents = repo.get_contents("contact.csv", ref="main")

    lines = contents.decoded_content.decode("utf-8")
    data_arr = lines.splitlines()
    lookup = mob

    for i in range(len(data_arr)):
        ref_arr = data_arr[i].split(',')
        if ref_arr[0] == lookup:
            curr_arr = data_arr[i].split(',')
            curr_arr[0] = lookup
            if int(curr_arr[1]) == int(otp):
                return True
            else:
                return False
            break

    updated_data = ''
    for i in range(len(data_arr)):
        updated_data = updated_data + data_arr[i] + '\n'

    # print(contents.decoded_content)
    repo.update_file("mob_name.csv", "update otp activity", updated_data, contents.sha, branch="main")
    return True



def send_mail_to_backoffice(session_state):
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login("baseoca.frontoffice@gmail.com", "Reven@nt@1985")
    message = '<html></html>'
    my_email = MIMEText(message, "html")
    my_email["Subject"] = "Test Status : "
    s.sendmail("baseoca.frontoffice@gmail.com", "baseoca.backoffice@gmail.com", 'Test')
    s.quit()