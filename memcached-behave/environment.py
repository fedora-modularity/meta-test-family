import moduleframework


def before_scenario(context, scenario):
    context.backend.setUp()


def after_scenario(context, scenario):
    try:
        context.socket.close()
    except:
        pass
    context.backend.tearDown()


def before_all(context):
    context.backend = moduleframework.get_correct_backend()
