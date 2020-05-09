from .context import main


def test_app(capsys, example_fixture):
    # pylint: disable=W0612,W0613
    main.Microservice.run()
    captured = capsys.readouterr()

    assert "Hello World..." in captured.out
