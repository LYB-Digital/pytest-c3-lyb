import base64
from types import ModuleType
from typing import Optional

import pytest
import requests
from _pytest.config.argparsing import Parser  # noqa: WPS436
from _pytest.fixtures import SubRequest  # noqa: WPS436


def pytest_addoption(parser: Parser):
    """Add command-line options to the Pytest session.

    Parameters
    ----------
    parser : Parser
        Pytest Parser instance
    """
    group = parser.getgroup('c3-lyb')
    group.addoption(
        '--url',
        action='store',
        default='http://localhost:8080',
        help='URL for the C3 test environment',
    )
    group.addoption(
        '--user',
        action='store',
        help='User name to use to authenticate to the target tag (Basic auth)',
    )
    group.addoption(
        '--password',
        action='store',
        help='Password to use to authenticate to the target tag (Basic auth)',
    )
    group.addoption(
        '--basic-auth',
        action='store',
        help='Basic authentication string to the target tag',
    )
    group.addoption(
        '--tenant',
        action='store',
        help='ID of the tenant in which tests should run',
    )
    group.addoption(
        '--tag',
        action='store',
        help='ID of the tag in which tests should run',
    )


@pytest.fixture(name='url', scope='session')
def fixture_url(request: SubRequest) -> Optional[str]:
    """Get the 'url' command line option as a fixture.

    Parameters
    ----------
    request : SubRequest
        SubRequest instance

    Returns
    -------
    str
        The 'url' command line option
    """
    return request.config.getoption('--url')


@pytest.fixture(name='user', scope='session')
def fixture_user(request: SubRequest) -> Optional[str]:
    """Get the 'user' command line option as a fixture.

    Parameters
    ----------
    request : SubRequest
        SubRequest instance

    Returns
    -------
    str
        The 'user' command line option
    """
    return request.config.getoption('--user')


@pytest.fixture(name='password', scope='session')
def fixture_password(request: SubRequest) -> Optional[str]:
    """Get the 'password' command line option as a fixture.

    Parameters
    ----------
    request : SubRequest
        SubRequest instance

    Returns
    -------
    str
        The 'password' command line option
    """
    return request.config.getoption('--password')


@pytest.fixture(name='basic_auth', scope='session')
def fixture_basic_auth(request: SubRequest) -> str:
    """Get the 'auth' command line option as a fixture.

    Parameters
    ----------
    request : SubRequest
        SubRequest instance

    Returns
    -------
    str
        The 'basic-auth' command line option
    """
    return request.config.getoption('--basic-auth')


@pytest.fixture(name='tenant', scope='session')
def fixture_tenant(request: SubRequest) -> str:
    """Get the 'tenant' command line option as a fixture.

    Parameters
    ----------
    request : SubRequest
        SubRequest instance

    Returns
    -------
    str
        The 'tenant' command line option
    """
    return request.config.getoption('--tenant')


@pytest.fixture(name='tag', scope='session')
def fixture_tag(request: SubRequest) -> str:
    """Get the 'tag' command line option as a fixture.

    Parameters
    ----------
    request : SubRequest
        SubRequest instance

    Returns
    -------
    str
        The 'tag' command line option
    """
    return request.config.getoption('--tag')


@pytest.fixture(name='c3auth', scope='session')
def fixture_c3auth(
    basic_auth: str, user: Optional[str], password: Optional[str],
) -> str:
    """Get the auth string to use to authenticate to the test tag. Prefer to
    use the auth string directly if given, but allow use of a user name and
    password as well.

    Parameters
    ----------
    basic_auth : str
        Basic auth string to use to authenticate to the test tag
    user : Optional[str]
        User name to use to authenticate to the test tag
    password : Optional[str]
        Password to use to authenticate to the test tag

    Returns
    -------
    str
        The full auth string to use to authenticate to the test tag
    """
    if basic_auth:
        return f'Basic {basic_auth}'

    # Auth string not provided - generate the basic auth string from the user
    # name and password
    basic_auth = base64.b64encode(
        f'{user}:{password}'.encode('utf-8'),
    ).decode('utf-8')
    return f'Basic {basic_auth}'


@pytest.fixture(name='c3', scope='session')
def fixture_c3(url: str, tenant: str, tag: str, c3auth: str) -> object:
    """Get the C3 connector for the test tag.

    Parameters
    ----------
    url : str
        URL for the C3 environment containing the test tag
    tenant : str
        Tenant for the test tag
    tag : str
        Tag for the test tag
    c3auth : str
        Full auth string to authenticate to the test tag

    Returns
    -------
    object
        Thick C3 client connector
    """
    # The noqas and disables in this method are C3's fault - this is their
    # janky method for getting the Python connector that we are forced to use
    c3iot = ModuleType('c3IoT')
    c3iot.__loader__ = c3iot  # noqa: WPS609
    src = requests.get(
        f'{url}/public/python/c3remote_bootstrap.py',
    ).content
    exec(  # noqa: WPS421 # pylint: disable=exec-used
        src, c3iot.__dict__,  # noqa: WPS609
    )

    return c3iot.C3RemoteLoader.typeSys(  # pylint: disable=no-member
        url=url,
        tenant=tenant,
        tag=tag,
        auth=c3auth,
        define_types=True,
    )
