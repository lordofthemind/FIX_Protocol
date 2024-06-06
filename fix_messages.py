import quickfix as fix
import logging

def create_logon_message(username, password, sender_comp_id, target_comp_id):
    message = fix.Message()
    header = message.getHeader()
    header.setField(fix.BeginString(fix.BeginString_FIX44))
    header.setField(fix.MsgType(fix.MsgType_Logon))
    header.setField(fix.SenderCompID(sender_comp_id))
    header.setField(fix.TargetCompID(target_comp_id))
    
    # Set logon message fields
    message.setField(fix.HeartBtInt(30))
    message.setField(fix.Username(username))
    message.setField(fix.Password(password))
    
    return message

def create_heartbeat_message(sender_comp_id, target_comp_id):
    message = fix.Message()
    header = message.getHeader()
    header.setField(fix.BeginString(fix.BeginString_FIX44))
    header.setField(fix.MsgType(fix.MsgType_Heartbeat))
    header.setField(fix.SenderCompID(sender_comp_id))
    header.setField(fix.TargetCompID(target_comp_id))
    return message

def create_logout_message(sender_comp_id, target_comp_id):
    message = fix.Message()
    header = message.getHeader()
    header.setField(fix.BeginString(fix.BeginString_FIX44))
    header.setField(fix.MsgType(fix.MsgType_Logout))
    header.setField(fix.SenderCompID(sender_comp_id))
    header.setField(fix.TargetCompID(target_comp_id))
    return message

def create_order_message(sender_comp_id, target_comp_id, symbol, quantity, price, side, order_type):
    message = fix.Message()
    header = message.getHeader()
    header.setField(fix.BeginString(fix.BeginString_FIX44))
    header.setField(fix.MsgType(fix.MsgType_NewOrderSingle))
    header.setField(fix.SenderCompID(sender_comp_id))
    header.setField(fix.TargetCompID(target_comp_id))
    
    # Set order fields
    message.setField(fix.ClOrdID(generate_order_id()))
    message.setField(fix.Symbol(symbol))
    message.setField(fix.OrderQty(quantity))
    message.setField(fix.Price(price))
    message.setField(fix.Side(side))  # 1 = Buy, 2 = Sell
    message.setField(fix.OrdType(order_type))  # 1 = Market, 2 = Limit
    
    return message

def generate_order_id():
    import uuid
    return str(uuid.uuid4())

def send_message(sessionID, message):
    try:
        fix.Session.sendToTarget(message, sessionID)
        logging.info(f'Message sent: {message}')
    except Exception as e:
        logging.error(f'Error sending message: {e}')
