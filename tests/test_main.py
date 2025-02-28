import src.NoKeeA.main as main


def test_main(capfd):
    main.main()
    out, err = capfd.readouterr()
    assert out == "Hello World\n"
