# -*- coding: utf-8 -*-


def test_c3_fixture(testdir):
    """Make sure that pytest accepts our fixture."""

    # create a temporary pytest test module
    testdir.makepyfile("""
        def test_c3_my_user(c3: object):
            assert c3.User.myUser().id == 'BA'
    """)

    # run pytest with the following cmd args
    result = testdir.runpytest(
        '--user=BA',
        '--password=BA',
        '--tenant=c3',
        '--tag=c3',
        '-v'
    )

    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines([
        '*::test_c3_my_user PASSED*',
    ])

    # make sure that that we get a '0' exit code for the testsuite
    assert result.ret == 0


def test_c3_help_message(testdir):

    # create a temporary pytest test module
    testdir.makepyfile("""
        def test_c3_my_user(c3: object):
            assert c3.User.myUser().id == 'BA'
    """)

    result = testdir.runpytest(
        # '-v',
        # '--fixtures',
        '--help',
    )

    print(result.stdout)
    assert False

    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines([
        '*c3-lyb*',
        # 'c3-lyb:',
        # '*--foo=DEST_FOO*Set the value for the fixture "bar".',
    ])


# def test_hello_ini_setting(testdir):
#     testdir.makeini("""
#         [pytest]
#         HELLO = world
#     """)

#     testdir.makepyfile("""
#         import pytest

#         @pytest.fixture
#         def hello(request):
#             return request.config.getini('HELLO')

#         def test_hello_world(hello):
#             assert hello == 'world'
#     """)

#     result = testdir.runpytest('-v')

#     # fnmatch_lines does an assertion internally
#     result.stdout.fnmatch_lines([
#         '*::test_hello_world PASSED*',
#     ])

#     # make sure that that we get a '0' exit code for the testsuite
#     assert result.ret == 0
