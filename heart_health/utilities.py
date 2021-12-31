"""Utility functions to support Apple Medical notebooks."""

# ##################################################################################################
#  Copyright ©2021. Stephen Rigden.                                                                #
#  Last modified 12/31/21, 9:06 AM by stephen.                                                     #
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

from dataclasses import dataclass
from typing import Literal, Optional, Union

import pandas


PRESSURE_SYSTOLIC = 'HKQuantityTypeIdentifierBloodPressureSystolic'
PRESSURE_DIASTOLIC = 'HKQuantityTypeIdentifierBloodPressureDiastolic'
TOLICS = Literal[PRESSURE_SYSTOLIC: str, PRESSURE_DIASTOLIC: str]
TOLIC_COL = Literal['systolic', 'diastolic']


@dataclass
class TimeCategories:
    """
    Support the conversion of matplotlib date ranges into matplotlib categories. The categories are
    represented by 'buckets' of date sequences. They are identified by the last date in each category.
    
    The categories are aligned with the end_date. Since this could lead to the first category containing less
    than the full number of days defined by 'category_size' the 'start_date' will be normalized to the
    beginning of the first complete category.
    For example, with start date = 2021-12-10, end_date = 2021-12-15, category_size = 4 the start date
    will be normalized to 2021-12-12.
    Also with start date = 2021-12-10, end_date = 2021-12-15, category_size = 6 the start date
    will be unchanged at 2121-12-10.

    Example usage within matplotlib or seaborn:
        # Create a TimeCategories object
        start = pandas.Timestamp(2021, 11, 26)
        end = pandas.Timestamp(2021, 12, 5)
        category_size = 3
        time_categories = TimeCategories(start, end, category_size)
        
        # Create a new column 'category'
        df['category'] = df['date'].apply(time_categories.get_category)
    """
    start_date:  pandas.Timestamp
    end_date:  pandas.Timestamp
    
    # Category size in days. The default category size is calculated to provide ten time categories.
    category_size: int = None
    
    def __post_init__(self):
        if self.end_date < self.start_date:
            msg = f'The start date {self.start_date} must precede the end date {self.end_date}.'
            raise ValueError(msg)

        one_day = pandas.Timedelta('1 day')
        if not self.category_size:
            # Calculate a category size which will create ten categories
            period_of_interest = self.end_date - self.start_date + one_day
            self.category_size = int(str(period_of_interest.days)) // 10

        # Is the category too large to fit into the date range?
        date_range = (self.end_date - self.start_date).days + 1
        if self.category_size > date_range:
            msg = (f"The category_size of {self.category_size} days must be less than the time span between the "
                   f"start and end dates ({date_range} days).")
            raise ValueError(msg)
        
        # Normalize the start date to the first day of the first full category.
        start_date_category = self._category(self.start_date)
        yesterdays_category = self._category(self.start_date - one_day)
        if start_date_category == yesterdays_category:
            self.start_date = start_date_category + one_day

    def get_category(self, date: Union[pandas.Timestamp, tuple[int, int, int]]) -> Optional[str]:
        """
        Return the category that contains the date.
        
        Args:
            date: pandas,Timestamp or ('YYYY', 'MM', 'DD') tuple are acceptable types.
            
        Raises:
            TypeError: If the date is not an acceptable type.

        Returns:
            The last day of the time category formatted as a date string (YYYY-MM-DD) or
            None if date is later than the self.end_date or earlier than the normalized self.start_date.
        """
        if isinstance(date, pandas.Timestamp):
            valid_date = self.start_date <= date <= self.end_date
        elif isinstance(date, tuple):
            date = pandas.Timestamp(*date)
            valid_date = self.start_date <= date <= self.end_date
        else:
            msg = f"Valid date types are pandas.Timestamp or tuple('YYYY', 'MM', 'DD')."
            raise TypeError(msg)
        
        if valid_date:
            return str(self._category(date).date())
        else:
            return None

    def _category(self, date: pandas.Timestamp) -> pandas.Timestamp:
        """
        Get the category for a date.
        
        Args:
            date:

        Returns:
            The last day of the date's time category
        """
        days_to_end_date = (self.end_date - date).days
        category_day_delta = days_to_end_date // self.category_size * self.category_size
        category_timedelta = pandas.Timedelta(days=category_day_delta)
        category = self.end_date - category_timedelta
        return category


def create_blood_pressure_dataset(ds: pandas.DataFrame) -> pandas.DataFrame:
    """
    Convert a generic 'flat' health dataset into a blood pressure dataset.
    
    Input dataset:
    
    Data columns (total 3 columns):
        <class 'pandas.core.frame.DataFrame'>
         #   Column  Dtype
        ---  ------  -----
         0   value   int64
         1   type    object
         2   date    datetime64[ns]
         
    Args:
        ds: The dataset

    Returns:
        The blood pressure dataset:
        
        <class 'pandas.core.frame.DataFrame'>
         #   Column          Dtype
        ---  ------          -----
         0   date            datetime64[ns]
         1   systolic        int64
         2   diastolic       int64
         3   pulse pressure  int64
    
    """
    ds_sys = _create_stolic_dataset(ds, PRESSURE_SYSTOLIC, 'systolic')
    ds_dia = _create_stolic_dataset(ds, PRESSURE_DIASTOLIC, 'diastolic')
    bpds = ds_sys.merge(ds_dia, left_on=['date'], right_on=['date'])
    bpds['pulse pressure'] = bpds['systolic'] - bpds['diastolic']
    return bpds


def _create_stolic_dataset(ds: pandas.DataFrame, health_type: TOLICS, col_name: TOLIC_COL) -> pandas.DataFrame:
    """
    Convert a generic 'flat' health dataset into a systolic or diastolic dataset.

    Args:
        ds: The dataset
        health_type: An Apple constant used to differentiate types of health records.
        col_name: Name of the new column

    Returns:
        The stolic dataset:
        
            <class 'pandas.core.frame.DataFrame'>
             #   Column     Dtype
            ---  ------     -----
             0   date       datetime64[ns]
             1   <col_name> int64
             
    """
    wanted = ds['type'] == health_type
    sto_ds = ds.loc[wanted, ['date', 'value']]
    if len(sto_ds) is 0:
        msg = f"Type '{health_type}' was not found in the dataset."
        raise ValueError(msg)
    sto_ds = sto_ds.rename(columns={'value': col_name})
    return sto_ds
