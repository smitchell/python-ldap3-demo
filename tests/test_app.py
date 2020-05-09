from .context import python_ldap3_demo


def test_app(capsys, example_fixture):
    # pylint: disable=W0612,W0613
    python_ldap3_demo.Blueprint.run()
    captured = capsys.readouterr()

    assert "Hello World..." in captured.out
