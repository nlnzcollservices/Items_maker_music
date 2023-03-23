import pytest
import mock
import os
import sys
script_dir = os.path.dirname(os.getcwd())
sys.path.insert(0,script_dir)
print(script_dir)
import item_maker 
print(dir(item_maker))



@pytest.fixture
def mock_alma_tools(monkeypatch):
    # Mock the AlmaTools class for testing purposes
    class MockAlmaTools:
        def __init__(self, key):
            pass

        def get_holdings(self, mms_id):
            pass

        def get_holding(self, mms_id, holding_id):
            pass

        # Create a mock create_item method
        def create_item(self, mms_id, holding_id, item_data):
            pass

    # Replace AlmaTools with the mock class
    mock_alma_tools = MockAlmaTools()
    monkeypatch.setattr(item_maker, 'AlmaTools', lambda key: mock_alma_tools)
    return mock_alma_tools



@mock.patch('item_maker.AlmaTools')
def test_get_holdings(mock_alma_tools):
    from item_maker import make_item

    # Test case where location is provided
    mock_alma_tools.reset_mock()
    mock_alma_tools.return_value.xml_response_data = "<holding_data><holding_id>23232323</holding_id></holding_data>"
    mms_id = '99999999999'
    holding_id = None
    location = 'WN.NL'  # existing location in the holding
    barcode = '1234567890'
    copy_id = '1'
    key = 'prod'

    result = make_item(mms_id, holding_id, location, copy_id, barcode, key)
    mock_alma_tools.assert_called_once_with(key)
    mock_alma_tools.return_value.get_holdings.assert_called_once_with(mms_id)


@mock.patch('item_maker.AlmaTools')
def test_make_item_with_holdings(mock_alma_tools):
    from item_maker import make_item

    # Test case where location is provided
    mock_alma_tools.reset_mock()
    mock_alma_tools.return_value.xml_response_data = "location>WN.NL</location"
    mms_id = '99999999999'
    holding_id = "232323"
    location = 'WN.NL'  # existing location in the holding
    barcode = '1234567890'
    copy_id = '1'
    key = 'prod'

    result = make_item(mms_id, holding_id, location, copy_id, barcode, key)
    mock_alma_tools.assert_called_once_with(key)
    mock_alma_tools.return_value.get_holding.assert_called_once_with(mms_id, mock.ANY)
    mock_alma_tools.return_value.create_item.assert_called_once_with(mms_id, mock.ANY, mock.ANY)
    assert result != mock_alma_tools.return_value.status_code.startswith("2")



@pytest.fixture
def mocked_gui(monkeypatch):
    # Mock the PySimpleGUI window object to return a mock object that can be checked later
    class MockWindow:
        def __init__(self, **kwargs):
            self.kwargs = kwargs
            self.closed = False
            self.values = None

        def read(self):
            if self.closed:
                raise Exception("Window is closed")

            self.values = {"spreadsheet_name": "test_sheet.xlsx", "if_sb": False}
            return "Run!", self.values

        def close(self):
            self.closed = True

    def mock_window(*args, **kwargs):
        return MockWindow(**kwargs)

    monkeypatch.setattr("item_maker.sg.Window", mock_window)

def test_my_gui(mocked_gui):
    from item_maker import my_gui

    result = my_gui()

    assert result[0] == {"spreadsheet_name": "test_sheet.xlsx", "if_sb": False}
    assert result[2] == "Run!"