Feature: Smokish smoke

    Scenario: Running ls in module
        When run 'ls / | grep bin'

    @wip
    Scenario: Set/Get data
        Given connected to module
        When send 'set Test 0 100 4\r\ndata\r\n'
        Then receive 'STORED\r\n'
        When send 'get Test\r\n'
        Then receive 'VALUE Test 0 4\r\ndata\r\nEND\r\n'
