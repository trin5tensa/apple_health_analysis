"""Test module."""

#  Copyright ©2021. Stephen Rigden.
#  Last modified 1/1/22, 9:00 AM by stephen.
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

from contextlib import contextmanager
import pytest
import utilities


class TestTimeCategory:
    @contextmanager
    def three_bucket_context(self):
        start = utilities.pandas.Timestamp(2021, 11, 26)
        end = utilities.pandas.Timestamp(2021, 12, 5)
        interval = 3
        time_categories = utilities.TimeCategories(start, end, interval)
        yield time_categories
        
    def test_too_large_date_returns_none(self):
        date = utilities.pandas.Timestamp(2021, 12, 6)
        with self.three_bucket_context() as time_categories:
            assert time_categories.get_bucket(date) is None

    def test_too_small_date_returns_none(self):
        date = 2021, 10, 6
        with self.three_bucket_context() as time_categories:
            assert time_categories.get_bucket(date) is None
            
    def test_date_in_invalid_bucket(self):
        start = utilities.pandas.Timestamp(2021, 12, 10)
        end = utilities.pandas.Timestamp(2021, 12, 15)
        interval = 4
        time_categories = utilities.TimeCategories(start, end, interval)
        date = 2021, 12, 10
        assert time_categories.get_bucket(date) is None

    def test_date_not_in_invalid_bucket(self):
        start = utilities.pandas.Timestamp(2021, 12, 10)
        end = utilities.pandas.Timestamp(2021, 12, 15)
        interval = 6
        time_categories = utilities.TimeCategories(start, end, interval)
        date = 2021, 12, 10
        assert time_categories.get_bucket(date) == '2021-12-15'
        
    def test_end_date(self):
        date = 2021, 12, 5
        with self.three_bucket_context() as time_categories:
            assert time_categories.get_bucket(date) == '2021-12-05'
            
    def test_2021_12_02(self):
        date = 2021, 12, 2
        with self.three_bucket_context() as time_categories:
            assert time_categories.get_bucket(date) == '2021-12-02'
            
    def test_2021_12_01(self):
        date = 2021, 12, 1
        with self.three_bucket_context() as time_categories:
            assert time_categories.get_bucket(date) == '2021-12-02'
            
    def test_2021_11_30(self):
        date = 2021, 11, 30
        with self.three_bucket_context() as time_categories:
            assert time_categories.get_bucket(date) == '2021-12-02'
           
    def test_2021_11_29(self):
        date = 2021, 11, 29
        with self.three_bucket_context() as time_categories:
            assert time_categories.get_bucket(date) == '2021-11-29'
            
    def test_normalized_start_date(self):
        date = 2021, 11, 27
        with self.three_bucket_context() as time_categories:
            assert time_categories.get_bucket(date) == '2021-11-29'
        
    def test_end_date_lt_start_date_raises_value_error(self):
        start = utilities.pandas.Timestamp(2021, 11, 8)
        end = utilities.pandas.Timestamp(2021, 11, 7)
        interval = 10
        
        expected = f'The start date {start} must precede the end date {end}.'
        with pytest.raises(ValueError) as cm:
            utilities.TimeCategories(start, end, interval)
        assert str(cm.value) == expected
       
    def test_invalid_bucket_size_raises_value_error(self):
        start = utilities.pandas.Timestamp(2021, 11, 8)
        end = utilities.pandas.Timestamp(2021, 11, 10)
        interval = 42
        
        expected = (f"The bucket_size '42' must be less than the time span between "
                    f"the start and end dates (3).")
        with pytest.raises(ValueError) as cm:
            utilities.TimeCategories(start, end, interval)
        assert str(cm.value) == expected
      
    def test_invalid_date_type_raises_type_error(self):
        start = utilities.pandas.Timestamp(2021, 11, 8)
        end = utilities.pandas.Timestamp(2021, 11, 10)
        interval = 42
        
        date = 'garbage'
        expected = "Valid date types are pandas.Timestamp or tuple('YYYY', 'MM', 'DD')."
        with pytest.raises(TypeError) as cm:
            with self.three_bucket_context() as time_categories:
                time_categories.get_bucket(date)
        
        assert str(cm.value) == expected
