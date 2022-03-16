
pytest_plugins = ["errbot.backends.test"]

extra_plugin_dir = '.'


def test_command_remove_missing_args(testbot):
    testbot.push_message('!maya liquid remove')
    assert "Please use '/maya liquid remove <type> <uuid>'" == testbot.pop_message()


def test_command_remove_not_supported_type(testbot):
    testbot.push_message('!maya liquid remove notexistliquid 00000000')
    assert "Not supported type" == testbot.pop_message()


def test_command_remove_coffee_invalid_uuid(testbot):
    testbot.push_message('!maya liquid remove water 00000000')
    assert "Please use a valid UUID" == testbot.pop_message()


def test_command_remove_water_invalid_uuid(testbot):
    testbot.push_message('!maya liquid remove coffee 00000000')
    assert "Please use a valid UUID" == testbot.pop_message()


def test_command_remove_water_with_not_found_uuid(testbot):
    valid_uuid = 'd1359543-6b12-4c12-ae18-08f5ea0831ff'
    testbot.push_message(f"!maya liquid remove water {valid_uuid}")
    water_output = testbot.pop_message()
    assert f"UUID {valid_uuid} to water not found" in water_output


def test_command_remove_coffe_with_not_found_uuid(testbot):
    valid_uuid = 'd1359543-6b12-4c12-ae18-08f5ea0831ff'
    testbot.push_message(f"!maya liquid remove coffee {valid_uuid}")
    water_output = testbot.pop_message()
    assert f"UUID {valid_uuid} to coffee not found" in water_output


def test_command_remove_water_ok(testbot):
    testbot.push_message("!maya liquid add water 250")
    water_add_output = testbot.pop_message()
    water_uuid = water_add_output.split(" ")[-1][1:-1]
    print("UUID", water_uuid)
    testbot.push_message(f"!maya liquid remove water {water_uuid}")
    water_remove_output = testbot.pop_message()
    assert f"{water_uuid} was removed." == water_remove_output


def test_command_remove_coffee_ok(testbot):
    testbot.push_message("!maya liquid add coffee 40")
    coffee_add_output = testbot.pop_message()
    coffee_uuid = coffee_add_output.split(" ")[-1][1:-1]
    print("UUID", coffee_uuid)
    testbot.push_message(f"!maya liquid remove coffee {coffee_uuid}")
    coffee_remove_output = testbot.pop_message()
    assert f"{coffee_uuid} was removed." == coffee_remove_output
