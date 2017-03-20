#!/usr/bin/python

from moduleframework import module_framework

def before_scenario(context, scenario):
    context.backend.setUp()


def after_scenario(context, scenario):
    try:
        context.socket.close()
    except:
        pass
    context.backend.tearDown()


def before_all(context):
    context.backend, context.moduletype = module_framework.get_correct_backend()
