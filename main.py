import quickfix as fix
import logging
import time
import cred
from fix_messages import (
    create_logon_message, create_heartbeat_message, create_logout_message,
    create_order_message, send_message
)

SENDER_DATA_COMP_ID = cred.SENDER_DATA_COMP_ID

TARGET_COMP_ID = cred.TARGET_COMP_ID

USERNAME = cred.USERNAME

PASSWORD = cred.PASSWORD

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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
    sender_comp_id = SENDER_DATA_COMP_ID
    target_comp_id = TARGET_COMP_ID
    initiator = create_fix_session(config_file)

    if initiator:
        time.sleep(5)  # Wait for the session to be established
        sessionID = fix.SessionID('FIX.4.4', sender_comp_id, target_comp_id)  # Modify as per your configuration

        logon_message = create_logon_message(username, password, sender_comp_id, target_comp_id)
        send_message(sessionID, logon_message)
        time.sleep(2)  # Wait for logon acknowledgment

        heartbeat_message = create_heartbeat_message(sender_comp_id, target_comp_id)
        send_message(sessionID, heartbeat_message)
        time.sleep(10)  # Keep the session alive for some time

        order_message = create_order_message(sender_comp_id, target_comp_id, 'AAPL', 100, 150.00, fix.Side_BUY, fix.OrdType_LIMIT)
        send_message(sessionID, order_message)
        time.sleep(2)  # Wait for order acknowledgment

        logout_message = create_logout_message(sender_comp_id, target_comp_id)
        send_message(sessionID, logout_message)

        initiator.stop()
        logging.info('FIX session stopped')
