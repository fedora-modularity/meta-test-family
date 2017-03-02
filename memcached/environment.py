import moduleframework

def get_correct_backend():
    # FIXME this should shared IMHO
    MODULE = moduleframework.MODULE if moduleframework.MODULE else "docker"
    if MODULE == 'docker':
        return moduleframework.ContainerHelper()
    elif MODULE == 'rpm':
        return moduleframework.RpmHelper()
    else:
        raise ValueError("Unsupported MODULE={0}".format(MODULE))


def before_scenario(context, scenario):
    context.backend.setUp()

def after_scenario(context, scenario):
    if context.socket is None:
        context.socket.close()
    context.backend.tearDown()

def before_all(context):
    context.backend = get_correct_backend()
