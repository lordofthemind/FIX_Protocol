import quickfix as fix
import logging

def create_logon_message(username, password, sender_comp_id, target_comp_id):
    message = fix.Message()
    header = message.getHeader()
    header.setField(fix.MsgType(fix.MsgType_Logon))
    header.setField(fix.SenderCompID(sender_comp_id))  # Replace with your SenderCompID
    header.setField(fix.TargetCompID(target_comp_id))  # Replace with your TargetCompID
    
    # Set logon message fields
    body = fix.MsgType_Logon()
    body.setField(fix.HeartBtInt(30))
    body.setField(fix.RawDataLength(len(password)))  # Set RawDataLength for password
    body.setField(fix.RawData(password))             # Set RawData to password
    message.setField(body)
    
    # Set username and password fields
    message.setField(fix.Username(username))
    message.setField(fix.Password(password))

def create_heartbeat_message():
    message = fix.Message()
    header = message.getHeader()
    header.setField(fix.MsgType(fix.MsgType_Heartbeat))
    return message

def create_logout_message():
    message = fix.Message()
    header = message.getHeader()
    header.setField(fix.MsgType(fix.MsgType_Logout))
    return message

# Add more message generation functions as needed

def send_message(sessionID, message):
    try:
        fix.Session.sendToTarget(message, sessionID)
        logging.info(f'Message sent: {message}')
    except Exception as e:
        logging.error(f'Error sending message: {e}')
