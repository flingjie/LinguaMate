import lark_oapi as lark
from config import APP_ID, APP_SECRET
from log import logger
from controllers.event import do_p2_im_message_receive_v1


event_handler = lark.EventDispatcherHandler.builder("", "") \
    .register_p2_im_message_receive_v1(do_p2_im_message_receive_v1) \
    .build()

def main():
    cli = lark.ws.Client(APP_ID, APP_SECRET,
                         event_handler=event_handler,
                         log_level=lark.LogLevel.ERROR)
    cli.start()

if __name__ == "__main__":
    main()