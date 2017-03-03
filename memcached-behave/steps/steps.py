from behave import *
import socket


@given(u'connected to module')
def step_impl(context):
    context.backend.start()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost', context.backend.config['service']['port']))
    s.settimeout(4)
    context.socket = s


@when(u"send data '{text}'")
def step_impl(context, text):
    context.socket.sendall(text)
    # context.socket.close()


@when(u"send '{query}'")
def step_imp(context, query):
    context.socket.sendall(query.decode('string_escape'))


@then(u"receive '{expected_reply}'")
def step_impl(context, expected_reply):
    data = context.socket.recv(1024)
    expected = expected_reply.decode('string_escape')
    print("got '{0}' expected '{1}'".format(repr(data), repr(expected)))
    assert data == expected


@when(u"run '{text}'")
def step_impl(context, text):
    print(context.backend.docker_id)
    print(context.backend.run(text))
