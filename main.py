import quickfix as fix
import logging
import time
from fix_messages import create_logon_message, create_heartbeat_message, create_logout_message, send_message
import cred

SENDER_DATA_COMP_ID = cred.SENDER_DATA_COMP_ID

TARGET_COMP_ID = cred.TARGET_COMP_ID

USERNAME = cred.USERNAME

PASSWORD = cred.PASSWORD


class Application(fix.Application):
    def onCreate(self, sessionID):
        logging.info(f'Session created: {sessionID}')
    
    def onLogon(self, sessionID):
        logging.info(f'Successfully logged on: {sessionID}')
    
    def onLogout(self, sessionID):
        logging.info(f'Successfully logged out: {sessionID}')
    
    def toAdmin(self, message, sessionID):
        msgType = fix.MsgType()
        message.getHeader().getField(msgType)
        logging.info(f'Sending admin message: {msgType}')
    
    def fromAdmin(self, message, sessionID):
        msgType = fix.MsgType()
        message.getHeader().getField(msgType)
        logging.info(f'Received admin message: {msgType}')
    
    def toApp(self, message, sessionID):
        logging.info(f'Sending application message: {message}')
    
    def fromApp(self, message, sessionID):
        logging.info(f'Received application message: {message}')
    
    def onMessage(self, message, sessionID):
        logging.info(f'Received message: {message}')

def create_fix_session(config_file):
    try:
        settings = fix.SessionSettings(config_file)
        application = Application()
        storeFactory = fix.FileStoreFactory(settings)
        logFactory = fix.ScreenLogFactory(settings)
        initiator = fix.SocketInitiator(application, storeFactory, settings, logFactory)
        initiator.start()
        logging.info('FIX session started')
        return initiator
    except Exception as e:
        logging.error(f'Error creating FIX session: {e}')
        return None

if __name__ == '__main__':
    config_file = 'data_config.cfg'
    username = USERNAME
    password = PASSWORD
    initiator = create_fix_session(config_file)

    if initiator:
        time.sleep(5)  # Wait for the session to be established
        sessionID = fix.SessionID('FIX.4.4', SENDER_DATA_COMP_ID, TARGET_COMP_ID)  # Modify as per your configuration

        logon_message = create_logon_message(username, password, SENDER_DATA_COMP_ID, TARGET_COMP_ID)
        send_message(sessionID, logon_message)
        time.sleep(2)  # Wait for logon acknowledgment

        heartbeat_message = create_heartbeat_message()
        send_message(sessionID, heartbeat_message)
        time.sleep(10)  # Keep the session alive for some time

        logout_message = create_logout_message()
        send_message(sessionID, logout_message)

        initiator.stop()
        logging.info('FIX session stopped')
