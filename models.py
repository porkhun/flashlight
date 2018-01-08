import logging


logger = logging.getLogger(__name__)


# TODO: singleton
class Flashlight():

    def on(self):
        print('on')
        logger.debug('Turn on')

    def off(self):
        print('on')
        logger.debug('Turn off')

    def color(self, data_value):
        msg = 'Change color to {}'.format(data_value)
        print(msg)
        logger.debug(msg)


# TODO: singleton
class FlashlightManager():

    COMMANDS = {
        0x12: 'on',
        0x13: 'off',
        0x20: 'color'
    }

    def __init__(self):
        self.flashlight = Flashlight()

    def handle_command(self, operation, *args, **kwargs):
        method = None
        method_name = self.COMMANDS.get(operation, None)
        if not method_name:
            logger.debug('Unknown command')
            return
        try:
            method = getattr(self.flashlight, method_name)
        except AttributeError:
            raise NotImplementedError('Method {} is not implemented yet'.format(method_name))
        method(*args, **kwargs)
