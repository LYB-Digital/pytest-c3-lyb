import base64
import os

from _pytest.pytester import Testdir


def test_c3_fixture(testdir: Testdir):
    """Test basic usage of the c3 fixture.

    Parameters
    ----------
    testdir : Testdir
        Testdir fixture
    """
    # create a temporary pytest test module
    testdir.makepyfile("""
        def test_c3_my_user(c3: object):
            assert c3.User.myUser().id == 'BA'
    """)

    basic_auth = os.environ['C3_BASIC_AUTH']
    user_pass = base64.b64decode(basic_auth).decode('utf-8').split(':')

    # Test using either the user/pass or basic auth string command-line options
    core_clopts = ['--tenant=c3', '--tag=c3', '-v']
    add_clopts_list = [
        [f'--basic-auth={basic_auth}'],
        [f'--user={user_pass[0]}', f'--password={user_pass[1]}'],
    ]
    for add_clopts in add_clopts_list:
        # run pytest with the following cmd args
        result = testdir.runpytest(*(core_clopts + add_clopts))

        # fnmatch_lines does an assertion internally
        result.stdout.fnmatch_lines([
            '*::test_c3_my_user PASSED*',
        ])

        # make sure that that we get a '0' exit code for the testsuite
        assert result.ret == 0


def test_c3_help_message(testdir: Testdir):
    """Test the c3 fixture help message.

    Parameters
    ----------
    testdir : Testdir
        Testdir fixture
    """
    result = testdir.runpytest(
        '--help',
    )

    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines([
        'c3-lyb:',
        '*--url=URL*URL for the C3 test environment',
    ])
