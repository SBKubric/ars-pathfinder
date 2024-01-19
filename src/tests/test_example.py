import pytest

pytestmark = pytest.mark.asyncio(scope="module")


@pytest.fixture
def example_fixture():
    return "foobar"


async def test_example(example_fixture):
    assert example_fixture == "foobar"
