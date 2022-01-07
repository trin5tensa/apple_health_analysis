"""Test module."""

# ##################################################################################################
#  Copyright ©2022. Stephen Rigden.                                                                #
#  Last modified 1/7/22, 8:15 AM by stephen.                                                       #
#  This program is free software: you can redistribute it and/or modify                            #
#  it under the terms of the GNU General Public License as published by                            #
#  the Free Software Foundation, either version 3 of the License, or                               #
#  (at your option) any later version.                                                             #
#  This program is distributed in the hope that it will be useful,                                 #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of                                  #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                                   #
#  GNU General Public License for more details.                                                    #
#  You should have received a copy of the GNU General Public License                               #
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.                           #
# ##################################################################################################
import datetime
from contextlib import contextmanager

import pytest
import utilities


class TestTimeCategory:
    @contextmanager
    def three_category_context(self):
        start = utilities.pandas.Timestamp(2021, 11, 26)
        end = utilities.pandas.Timestamp(2021, 12, 5)
        category_size = 3
        time_categories = utilities.TimeCategories(start, end, bin_size=category_size)
        yield time_categories
        
    @contextmanager
    def twelve_day_context(self, bin_count: int):
        one_day = utilities.pandas.Timedelta('1 day')
        length = utilities.pandas.Timedelta('12 day')
        start = utilities.pandas.Timestamp(2022, 1, 1)
        end = start + length - one_day
        time_categories = utilities.TimeCategories(start, end, bin_count=bin_count)
        yield time_categories
        
    def test_too_large_date_returns_none(self):
        date = utilities.pandas.Timestamp(2021, 12, 6)
        with self.three_category_context() as time_categories:
            assert time_categories.get_category(date) is None

    def test_too_small_date_returns_none(self):
        date = 2021, 10, 6
        with self.three_category_context() as time_categories:
            assert time_categories.get_category(date) is None
            
    def test_date_in_invalid_category(self):
        start = utilities.pandas.Timestamp(2021, 12, 10)
        end = utilities.pandas.Timestamp(2021, 12, 15)
        category_size = 4
        time_categories = utilities.TimeCategories(start, end, bin_size=category_size)
        date = 2021, 12, 10
        assert time_categories.get_category(date) is None

    def test_date_not_in_invalid_category(self):
        start = utilities.pandas.Timestamp(2021, 12, 10)
        end = utilities.pandas.Timestamp(2021, 12, 15)
        category_size = 6
        time_categories = utilities.TimeCategories(start, end, bin_size=category_size)
        date = 2021, 12, 10
        assert time_categories.get_category(date) == '2021-12-15'
        
    def test_end_date(self):
        date = 2021, 12, 5
        with self.three_category_context() as time_categories:
            assert time_categories.get_category(date) == '2021-12-05'
            
    def test_2021_12_02(self):
        date = 2021, 12, 2
        with self.three_category_context() as time_categories:
            assert time_categories.get_category(date) == '2021-12-02'
            
    def test_2021_12_01(self):
        date = 2021, 12, 1
        with self.three_category_context() as time_categories:
            assert time_categories.get_category(date) == '2021-12-02'
            
    def test_2021_11_30(self):
        date = 2021, 11, 30
        with self.three_category_context() as time_categories:
            assert time_categories.get_category(date) == '2021-12-02'
           
    def test_2021_11_29(self):
        date = 2021, 11, 29
        with self.three_category_context() as time_categories:
            assert time_categories.get_category(date) == '2021-11-29'
            
    def test_normalized_start_date(self):
        date = 2021, 11, 27
        with self.three_category_context() as time_categories:
            assert time_categories.get_category(date) == '2021-11-29'
        
    def test_end_date_lt_start_date_raises_value_error(self):
        start = utilities.pandas.Timestamp(2021, 11, 8)
        end = utilities.pandas.Timestamp(2021, 11, 7)
        category_size = 10
        
        expected = f'The start date {start} must precede the end date {end}.'
        with pytest.raises(ValueError) as cm:
            utilities.TimeCategories(start, end, bin_size=category_size)
        assert str(cm.value) == expected
       
    def test_invalid_category_size_raises_value_error(self):
        start = utilities.pandas.Timestamp(2021, 11, 8)
        end = utilities.pandas.Timestamp(2021, 11, 10)
        category_size = 42
        
        expected = (f"The bin_size of 42 days must be less than the time span between "
                    f"the start and end dates (3 days).")
        with pytest.raises(ValueError) as cm:
            utilities.TimeCategories(start, end, bin_size=category_size)
        assert str(cm.value) == expected
      
    def test_invalid_date_type_raises_type_error(self):
        date = 'garbage'
        expected = "Valid date types are pandas.Timestamp or tuple('YYYY', 'MM', 'DD')."
        with pytest.raises(TypeError) as cm:
            with self.three_category_context() as time_categories:
                time_categories.get_category(date)
        
        assert str(cm.value) == expected
        
    def test_default_category_size_creates_a_category_count_of_ten(self):
        start = utilities.pandas.Timestamp(2021, 11, 1)
        end = utilities.pandas.Timestamp(2021, 11, 20)
    
        categories = utilities.TimeCategories(start, end)
        assert categories.bin_size == 2

    def test_both_bin_size_and_count_raise_value_error(self):
        start = utilities.pandas.Timestamp(2021, 11, 8)
        end = utilities.pandas.Timestamp(2021, 12, 7)
        bin_size = 1
        bin_count = 1
    
        expected = f'Supply either bin_size (1) or bin_count (1) but not both.'
        with pytest.raises(ValueError) as cm:
            utilities.TimeCategories(start, end, bin_size=bin_size, bin_count=bin_count)
        assert str(cm.value) == expected

    def test_one_bin(self):
        with self.twelve_day_context(bin_count=1) as time_categories:
            assert time_categories.bin_size == 12
            
    def test_three_bins(self):
        with self.twelve_day_context(bin_count=3) as time_categories:
            assert time_categories.bin_size == 4
            
    def test_twelve_bins(self):
        with self.twelve_day_context(bin_count=12) as time_categories:
            assert time_categories.bin_size == 1
            
            
class TestCreateBloodPressureDataset:
    @contextmanager
    def dummy_heart_dataset(self):
        """
        Returns:
               value                                            type       date
            0     80  HKQuantityTypeIdentifierBloodPressureDiastolic 2022-01-01
            1    120   HKQuantityTypeIdentifierBloodPressureSystolic 2022-01-01
            2     90  HKQuantityTypeIdentifierBloodPressureDiastolic 2022-01-02
            3    142   HKQuantityTypeIdentifierBloodPressureSystolic 2022-01-02
        """
        date_1 = datetime.datetime(2022, 1, 1)
        date_2 = datetime.datetime(2022, 1, 2)
        dates = utilities.pandas.to_datetime([date_1, date_1, date_2, date_2])
        types = utilities.pandas.Series(
                ['HKQuantityTypeIdentifierBloodPressureDiastolic',
                 'HKQuantityTypeIdentifierBloodPressureSystolic',
                 'HKQuantityTypeIdentifierBloodPressureDiastolic',
                 'HKQuantityTypeIdentifierBloodPressureSystolic'])
        values = utilities.pandas.Series([80, 120, 90, 142])
        yield utilities.pandas.DataFrame({'value': values, 'type': types, 'date': dates})
    
    def test_correct_conversion_to_blood_pressure_dataset(self):
        with self.dummy_heart_dataset() as bpds:
            # Create the expected return dataset
            #         date  systolic  diastolic  pulse pressure
            # 0 2022-01-01       120         80              40
            # 1 2022-01-02       142         90              52
            date_1 = datetime.datetime(2022, 1, 1)
            date_2 = datetime.datetime(2022, 1, 2)
            dates = utilities.pandas.to_datetime([date_1, date_2])
            systolics = utilities.pandas.Series([120, 142])
            diastolics = utilities.pandas.Series([80, 90])
            pulse_pressures = utilities.pandas.Series([40, 52])
            expected = utilities.pandas.DataFrame({'date': dates, 'systolic': systolics,
                                                   'diastolic': diastolics, 'pulse pressure': pulse_pressures})
 
            assert utilities.create_blood_pressure_dataset(bpds).compare(expected).empty
        
    def test_missing_systolic_data_raises_value_error(self):
        with self.dummy_heart_dataset() as bpds:
            bpds.type[1] = 'garbage'
            bpds.type[3] = 'garbage'
            expected = "Type 'HKQuantityTypeIdentifierBloodPressureSystolic' was not found in the dataset."
            with pytest.raises(ValueError) as cm:
                utilities.create_blood_pressure_dataset(bpds)
            assert str(cm.value) == expected
        
    def test_missing_diastolic_data_raises_value_error(self):
        with self.dummy_heart_dataset() as bpds:
            bpds.type[0] = 'garbage'
            bpds.type[2] = 'garbage'
            expected = "Type 'HKQuantityTypeIdentifierBloodPressureDiastolic' was not found in the dataset."
            with pytest.raises(ValueError) as cm:
                utilities.create_blood_pressure_dataset(bpds)
            assert str(cm.value) == expected
