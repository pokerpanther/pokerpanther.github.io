import unittest
from unittest.mock import patch, call, MagicMock, mock_open
import pandas as pd


class TestGoogleSheetsRetry(unittest.TestCase):

    def setUp(self):
        self.mock_data_input = [["Date",   "Type",  "Location",       "Game Type", "Level/Guarantee",                                 "Duration (min)","Cash In",  "Cash Out","Net",       "Place","Bullets"],
                                ["5/30/24","Online","Ignition",       "Tournament","MonsterStack Series - $5k Guaranteed",            "60",            "$11.00",   "$22.80",  "$11.80",    "60th", "1"],
                                ["3/8/24", "Live",  "Hardrock Casino","Tournament","Escalator Series #5: $500k Guaranteed Main Event","300",           "$1,465.00","$0.00",   "-$1,465.00","DNC",  "1"]]  

        self.mock_sleep = patch("time.sleep", return_value = None).start()

    def tearDown(self):
        patch.stopall()

    @patch('gspread.Spreadsheet.get_worksheet', side_effect=Exception("API Error"))
    def test_retry_mechanism(self, mock_get_worksheet):
        # Import the script to test, but catch SystemExit to prevent it from stopping the tests
        with self.assertRaises(SystemExit): 
            import main 

        # Check that the get_worksheet method was called exactly 3 times
        self.assertEqual(mock_get_worksheet.call_count, 3)

        # Check that time.sleep was called exactly 3 times with 10 seconds each
        self.assertEqual(self.mock_sleep.call_count, 3)
        self.mock_sleep.assert_has_calls([call(30), call(30), call(30)])

    @patch('gspread.service_account_from_dict')
    @patch('py.helpers.get_google_creds', return_value=None)
    @patch('builtins.open', new_callable=mock_open)  # Mock file open
    def test_successful_worksheet_fetch(self, 
                                        mock_open_file, 
                                        mock_get_creds, 
                                        mock_from_dict,
                                        ):
        
        mock_gc = MagicMock()
        mock_wkbk = MagicMock()
        mock_sheet = MagicMock()

        mock_from_dict.return_value = mock_gc
        mock_gc.open_by_url.return_value = mock_wkbk
        mock_wkbk.get_worksheet.return_value = mock_sheet
        mock_sheet.get_all_values.return_value = self.mock_data_input
        
        import main  

        self.assertEqual(self.mock_sleep.call_count, 0)

        self.assertEqual(mock_get_creds.call_count, 1)
        self.assertEqual(mock_from_dict.call_count, 1)
        self.assertEqual(mock_gc.open_by_url.call_count, 1)
        self.assertEqual(mock_wkbk.get_worksheet.call_count, 1)

        # Ensure get_all_values was called on the mock sheet
        mock_sheet.get_all_values.assert_called_once()

        # Check that results.yml is opened once and written to with expected content
        mock_open_file.assert_any_call('_data/results.yml', 'w')

        # Check that col_name_map.csv is opened once and written to with expected content
        mock_open_file.assert_any_call('_data/col_name_map.csv', 'w', newline='')
        mock_open_file.assert_any_call('_data/stats.csv', 'w')


if __name__ == '__main__':
    unittest.main()