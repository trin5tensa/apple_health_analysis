"""Test module."""

# ##################################################################################################
#  Copyright ©2022. Stephen Rigden.                                                                #
#  Last modified 2/23/22, 7:26 AM by stephen.                                                      #
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

from heart_health import utilities


class TestTimeCategory:
    
    @contextmanager
    def three_category_context(self):
        """
        Set up a ten day inclusive date range which will produce three buckets:
        2021-12-5, 2021-12-2, and 2021-11-29. 2021-11-26 is discarded.
        """
        start = utilities.pandas.Timestamp(2021, 11, 26)
        end = utilities.pandas.Timestamp(2021, 12, 5)
        bin_size = 3
        time_bins = utilities.TimeBins(start_date=start, end_date=end, bin_size=bin_size)
        yield time_bins
    
    @contextmanager
    def twelve_day_context(self, bin_count: int):
        """
        Set up a date range with a caller specified bin count. A twelve days is requested but the exact range is
        determined by the bin size.
        """
        one_day = utilities.pandas.Timedelta('1 day')
        length = utilities.pandas.Timedelta('12 day')
        start = utilities.pandas.Timestamp(2022, 1, 1)
        end = start + length - one_day
        time_bins = utilities.TimeBins(start_date=start, end_date=end, bin_count=bin_count)
        yield time_bins
    
    def test_late_date_returns_none(self):
        date = utilities.pandas.Timestamp(2021, 12, 6)
        with self.three_category_context() as time_bins:
            assert time_bins.get_bin(date) is None
    
    def test_early_date_returns_none(self):
        date = 2021, 10, 6
        with self.three_category_context() as time_bins:
            assert time_bins.get_bin(date) is None
    
    def test_discarded_date_returns_none(self):
        date = 2021, 11, 26
        with self.three_category_context() as time_bins:
            assert time_bins.get_bin(date) is None
    
    def test_end_date(self):
        date = 2021, 12, 5
        with self.three_category_context() as time_bins:
            assert time_bins.get_bin(date) == '2021-12-05'
    
    def test_2021_12_02(self):
        date = 2021, 12, 2
        with self.three_category_context() as time_bins:
            assert time_bins.get_bin(date) == '2021-12-02'
    
    def test_2021_12_01(self):
        date = 2021, 12, 1
        with self.three_category_context() as time_bins:
            assert time_bins.get_bin(date) == '2021-12-02'
    
    def test_2021_11_30(self):
        date = 2021, 11, 30
        with self.three_category_context() as time_bins:
            assert time_bins.get_bin(date) == '2021-12-02'
    
    def test_2021_11_29(self):
        date = 2021, 11, 29
        with self.three_category_context() as time_bins:
            assert time_bins.get_bin(date) == '2021-11-29'
    
    def test_normalized_start_date(self):
        date = 2021, 11, 27
        with self.three_category_context() as time_bins:
            assert time_bins.get_bin(date) == '2021-11-29'
    
    def test_end_date_lt_start_date_raises_value_error(self):
        start = utilities.pandas.Timestamp(2021, 11, 8)
        end = utilities.pandas.Timestamp(2021, 11, 7)
        
        expected = f'The start date {start} must precede the end date {end}.'
        with pytest.raises(ValueError) as cm:
            utilities.TimeBins(start_date=start, end_date=end)
        assert str(cm.value) == expected
    
    def test_invalid_date_type_raises_type_error(self):
        date = 'garbage'
        expected = "Valid date types are pandas.Timestamp or tuple('YYYY', 'MM', 'DD')."
        with pytest.raises(TypeError) as cm:
            with self.three_category_context() as time_bins:
                time_bins.get_bin(date)
        assert str(cm.value) == expected
    
    def test_default_category_size_creates_a_category_count_of_ten(self):
        start = utilities.pandas.Timestamp(2021, 11, 1)
        end = utilities.pandas.Timestamp(2021, 11, 20)
        
        categories = utilities.TimeBins(start_date=start, end_date=end)
        assert categories.bin_size == 2
    
    def test_one_bin(self):
        with self.twelve_day_context(bin_count=1) as time_bins:
            assert time_bins.bin_size == 12
    
    def test_three_bins(self):
        with self.twelve_day_context(bin_count=3) as time_bins:
            assert time_bins.bin_size == 4
    
    def test_twelve_bins(self):
        with self.twelve_day_context(bin_count=12) as time_bins:
            assert time_bins.bin_size == 1


class TestTimeBins:
    start = utilities.pandas.Timestamp(2022, 1, 1)
    end = utilities.pandas.Timestamp(2022, 1, 12)
    bin_size = 2
    bin_count = 6
    default_bin_count = 10
    
    # No bin size tests
    
    def test_start_and_end_arguments(self):
        time_bins = utilities.TimeBins(start_date=self.start, end_date=self.end)
        assert time_bins.start_date == utilities.pandas.Timestamp(2022, 1, 3)
        assert time_bins.end_date == self.end
        assert time_bins.bin_size == 1
        assert time_bins.bin_count == self.default_bin_count
    
    def test_start_end_and_bin_count_arguments(self):
        bin_count = 7
        time_bins = utilities.TimeBins(start_date=self.start, end_date=self.end, bin_count=bin_count)
        assert time_bins.start_date == utilities.pandas.Timestamp(2022, 1, 6)
        assert time_bins.end_date == self.end
        assert time_bins.bin_size == 1
        assert time_bins.bin_count == bin_count
    
    def test_calculated_bin_size_of_0_raises_value_error(self):
        start = utilities.pandas.Timestamp(2022, 1, 6)
        end = utilities.pandas.Timestamp(2022, 1, 10)
        
        expected = (f"The arguments have created a calculated amd invalid bin size of 0. "
                    f"TimeBins(start_date=Timestamp('2022-01-06 00:00:00'), "
                    f"end_date=Timestamp('2022-01-10 00:00:00'), bin_size=0, bin_count=10)")
        with pytest.raises(ValueError) as cm:
            utilities.TimeBins(start_date=start, end_date=end)
        assert str(cm.value) == expected
    
    # No bin count test
    
    def test_start_end_and_bin_size_arguments(self):
        bin_size = 5
        normalized_start_date = utilities.pandas.Timestamp(2022, 1, 3)
        calculated_bin_count = 2
        time_bins = utilities.TimeBins(start_date=self.start, end_date=self.end, bin_size=bin_size)
        assert time_bins.start_date == normalized_start_date
        assert time_bins.end_date == self.end
        assert time_bins.bin_size == bin_size
        assert time_bins.bin_count == calculated_bin_count

    def test_calculated_bin_count_of_0_raises_value_error(self):
        start = utilities.pandas.Timestamp(2022, 1, 6)
        end = utilities.pandas.Timestamp(2022, 1, 10)
        bin_size = 6
    
        expected = (f"The arguments have created a calculated amd invalid bin size of 0. "
                    f"TimeBins(start_date=Timestamp('2022-01-06 00:00:00'), "
                    f"end_date=Timestamp('2022-01-10 00:00:00'), bin_size=6, bin_count=0)")
        with pytest.raises(ValueError) as cm:
            utilities.TimeBins(start_date=start, end_date=end, bin_size=bin_size)
        assert str(cm.value) == expected
        
    # No end date tests
    
    def test_start_and_bin_size_arguments(self):
        bin_size = 3
        time_bins = utilities.TimeBins(start_date=self.start, bin_size=bin_size)
        assert time_bins.start_date == self.start
        assert time_bins.end_date == utilities.pandas.Timestamp(2022, 1, 30)
        assert time_bins.bin_size == bin_size
        assert time_bins.bin_count == self.default_bin_count
    
    def test_start_bin_count_and_bin_size_arguments(self):
        time_bins = utilities.TimeBins(start_date=self.start, bin_size=self.bin_size, bin_count=self.bin_count)
        assert time_bins.start_date == self.start
        assert time_bins.end_date == self.end
        assert time_bins.bin_size == self.bin_size
        assert time_bins.bin_count == self.bin_count
    
    # No start date tests
    
    def test_end_and_bin_size_arguments(self):
        bin_size = 1
        time_bins = utilities.TimeBins(end_date=self.end, bin_size=bin_size)
        assert time_bins.start_date == utilities.pandas.Timestamp(2022, 1, 3)
        assert time_bins.end_date == self.end
        assert time_bins.bin_size == bin_size
        assert time_bins.bin_count == self.default_bin_count
    
    def test_end_bin_count_and_bin_size_arguments(self):
        time_bins = utilities.TimeBins(end_date=self.end, bin_size=self.bin_size, bin_count=self.bin_count)
        assert time_bins.start_date == self.start
        assert time_bins.end_date == self.end
        assert time_bins.bin_size == self.bin_size
        assert time_bins.bin_count == self.bin_count
    
    # Wrong number of parameters test
    
    def test_wrong_argument_count_raises_value_error(self):
        start = utilities.pandas.Timestamp(2021, 11, 8)
        bin_count = 43
        expected = ("Invalid number of arguments. Supply three. If you are using the default bin_size then supply two "
                    "others. You supplied 2. TimeBins(start_date=Timestamp('2021-11-08 00:00:00'), "
                    "end_date=None, bin_size=None, bin_count=43).")
        
        with pytest.raises(ValueError) as cm:
            utilities.TimeBins(start_date=start, bin_count=bin_count)
        assert str(cm.value) == expected


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
            expected = ("No records of type 'HKQuantityTypeIdentifierBloodPressureSystolic' were "
                        "found in the dataset.")
            with pytest.raises(utilities.NoDataSupplied) as cm:
                utilities.create_blood_pressure_dataset(bpds)
            assert str(cm.value) == expected
    
    def test_missing_diastolic_data_raises_value_error(self):
        with self.dummy_heart_dataset() as bpds:
            bpds.type[0] = 'garbage'
            bpds.type[2] = 'garbage'
            expected = ("No records of type 'HKQuantityTypeIdentifierBloodPressureDiastolic' were "
                        "found in the dataset.")
            with pytest.raises(utilities.NoDataSupplied) as cm:
                utilities.create_blood_pressure_dataset(bpds)
            assert str(cm.value) == expected
