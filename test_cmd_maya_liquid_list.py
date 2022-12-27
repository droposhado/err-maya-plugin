
pytest_plugins = ["errbot.backends.test"]

extra_plugin_dir = '.'


def test_command_list_missing_args(testbot):
    testbot.push_message('!maya liquid list')
    assert "Please use '/maya liquid list <type>'" == testbot.pop_message()


def test_command_list_coffee_ok(testbot):
    quantity = 250
    testbot.pop_message()
    testbot.push_message(f"!maya liquid add coffee {quantity}")
    testbot.pop_message()
    testbot.push_message(f"!maya liquid add coffee {quantity}")
    testbot.pop_message()
    testbot.push_message('!maya liquid list coffee')
    output = testbot.pop_message()
    assert "Total 500" in output
    assert str(quantity) in output


def test_command_list_water_ok(testbot):
    quantity = 250
    testbot.pop_message()
    testbot.push_message(f"!maya liquid add water {quantity}")
    testbot.pop_message()
    testbot.push_message(f"!maya liquid add water {quantity}")
    testbot.pop_message()
    testbot.push_message('!maya liquid list water')
    output = testbot.pop_message()
    assert "Total 500" in output
    assert str(quantity) in output


def test_command_list_coffee_with_date_param_ok(testbot):
    quantity = 250
    date = "2022-03-25"
    testbot.push_message(f"!maya liquid add coffee {quantity} {date}T01:01:01Z")
    testbot.pop_message()
    testbot.push_message(f"!maya liquid add coffee {quantity} {date}T01:01:01Z")
    testbot.pop_message()
    testbot.push_message(f"!maya liquid list coffee {date}")
    output = testbot.pop_message()
    assert "Total 500" in output
    assert str(quantity) in output


def test_command_list_water_with_date_param_ok(testbot):
    quantity = 250
    date = "2022-03-25"
    testbot.push_message(f"!maya liquid add water {quantity} {date}T01:01:01Z")
    testbot.pop_message()
    testbot.push_message(f"!maya liquid add water {quantity} {date}T01:01:01Z")
    testbot.pop_message()
    testbot.push_message(f"!maya liquid list water {date}")
    output = testbot.pop_message()
    assert "Total 500" in output
    assert str(quantity) in output


def test_command_list_coffee_with_date_param_wrong(testbot):
    date = "error_date_string"
    testbot.push_message(f"!maya liquid list coffee {date}")
    output = testbot.pop_message()
    assert "Please use a valid datetime in ISO8601 (YYYY-MM-DD)" == output


def test_command_list_water_with_date_param_wrong(testbot):
    date = "error_date_string"
    testbot.push_message(f"!maya liquid list water {date}")
    output = testbot.pop_message()
    assert "Please use a valid datetime in ISO8601 (YYYY-MM-DD)" == output
