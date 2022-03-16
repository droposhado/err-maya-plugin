
pytest_plugins = ["errbot.backends.test"]

extra_plugin_dir = '.'


def test_command_coffee_add_missing_args(testbot):
    testbot.push_message('!maya liquid add coffee')
    assert "Please use '/maya liquid add <type> <quantity>'" == testbot.pop_message()


def test_command_water_add_missing_args(testbot):
    testbot.push_message('!maya liquid add water')
    assert "Please use '/maya liquid add <type> <quantity>'" == testbot.pop_message()


def test_command_coffee_add_invalid_amount(testbot):
    testbot.push_message('!maya liquid add coffee xx')
    assert "Please enter a valid quantity" == testbot.pop_message()


def test_command_water_add_invalid_amount(testbot):
    testbot.push_message('!maya liquid add water xx')
    assert "Please enter a valid quantity" == testbot.pop_message()


def test_command_notexistliquid_add_not_supported_type(testbot):
    testbot.push_message('!maya liquid add notexistliquid 250')
    assert "Not supported type" == testbot.pop_message()


def test_command_water_add_ok(testbot):
    quantity = 250
    testbot.push_message(f"!maya liquid add water {quantity}")
    poped = testbot.pop_message()
    assert str(quantity) in poped
    assert "water" in poped
    assert "was drunk" in poped


def test_command_coffee_add_ok(testbot):
    quantity = 250
    testbot.push_message(f"!maya liquid add coffee {quantity}")
    poped = testbot.pop_message()
    assert str(quantity) in poped
    assert "coffee" in poped
    assert "was drunk" in poped


def test_command_water_add_with_datetime_ok(testbot):
    quantity = 250
    testbot.push_message(f"!maya liquid add water {quantity} 2022-05-25T15:21:56Z")
    poped = testbot.pop_message()
    assert str(quantity) in poped
    assert "water" in poped
    assert "was drunk" in poped


def test_command_coffee_add_with_datetime_ok(testbot):
    quantity = 250
    testbot.push_message(f"!maya liquid add coffee {quantity} 2022-05-25T15:21:56Z")
    poped = testbot.pop_message()
    assert str(quantity) in poped
    assert "coffee" in poped
    assert "was drunk" in poped
