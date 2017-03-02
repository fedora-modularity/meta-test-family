import moduleframework

def before_scenario(context, scenario):
    context.backend.setUp()

def after_scenario(context, scenario):
    if context.socket is None:
        context.socket.close()
    context.backend.tearDown()

def before_all(context):
    context.backend = moduleframework.ContainerHelper()
