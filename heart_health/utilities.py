"""Utility functions to support Apple Medical notebooks."""

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

from dataclasses import dataclass, field
from typing import ClassVar, Literal, Optional, Union

import pandas


PRESSURE_SYSTOLIC = 'HKQuantityTypeIdentifierBloodPressureSystolic'
PRESSURE_DIASTOLIC = 'HKQuantityTypeIdentifierBloodPressureDiastolic'
TOLICS = Literal[PRESSURE_SYSTOLIC: str, PRESSURE_DIASTOLIC: str]
TOLIC_COL = Literal['systolic', 'diastolic']


@dataclass
class TimeBins:
    """
    This class enables the easy conversion of matplotlib date ranges into matplotlib categories. The categories are
    represented by 'bins' of date sequences. Each bin is identified by its last date.
    
    The bins are aligned with the end_date. Consider the problem of the date range January 1st to January 10th with
    bins of eight days. If uncorrected, this would create one bin of eight days and one of two days. In this case the
    start date would be normalized to January 3rd and the range would contain a single bin.
    
    Args:
        Three of these arguments must be supplied. One of the three may be the default value for bin_count.
        start_date: Inclusive start date of range. Note that this may be normalized to a different date.
        end_date: Inclusive end date of range.
        bin_size: The size of the bin in days.
        bin_count: The number of bins.

    Raises
        ValueError:
            If the end_date precedes the start_date.
            If a calculated bin_size or bin_count results in a value of zero or less.

    Example usage within pandas, matplotlib or seaborn:
        # Create a TimeBins object
        start = pandas.Timestamp(2021, 11, 26)
        end = pandas.Timestamp(2021, 12, 5)
        bin_size = 3
        time_categories = TimeBins(start, end, bin_size=bin_size)
        
        # Create a new column 'category'
        dataset['category'] = dataset['date'].apply(time_categories.get_bin)
    """
    start_date:  pandas.Timestamp = field(default=None, kw_only=True)
    end_date:  pandas.Timestamp = field(default=None, kw_only=True)
    bin_size: int = field(default=None, kw_only=True)
    bin_count: int = field(default=None, kw_only=True)
    
    bin_count_default: ClassVar = field(default=10, init=False, repr=False)
    one_day: pandas.Timedelta = field(default=pandas.Timedelta(1, 'd'), init=False, repr=False)
    
    def __post_init__(self):
        # Validate arguments
        arg_count = len([arg for arg in [self.start_date, self.end_date, self.bin_size, self.bin_count]
                         if arg])
        bin_count_in_args = bool(self.bin_count)
        
        match arg_count, bin_count_in_args:
            # Use default bin_count?…
            case 2, False:
                self.bin_count = self.bin_count_default
            
            # …otherwise 3 is the only valid number of arguments
            case 3, _:
                pass
        
            case _:
                msg = (f"Invalid number of arguments. Supply three. If you are using the default bin_size then "
                       f"supply two others. You supplied {arg_count}. {self}.")
                raise ValueError(msg)
        
        # Calculate start date if missing
        if not self.start_date:
            self.start_date = self._start_date(self.end_date, self.bin_count, self.bin_size)

        # Calculate end date if missing
        elif not self.end_date:
            time_span = pandas.Timedelta(self.bin_count * self.bin_size, 'd')
            self.end_date = self.start_date + time_span - self.one_day

        # Calculate bin_size if missing
        elif not self.bin_size:
            time_span = self._time_span(self.start_date, self.end_date)

            self.bin_size = time_span.days // self.bin_count
            if self.bin_size <= 0:
                msg = f'The arguments have created a calculated amd invalid bin size of {self.bin_size}. {self}'
                raise ValueError(msg)
            
            # Normalize the start data
            self.start_date = self._start_date(self.end_date, self.bin_count, self.bin_size)

        # Calculate bin_count if missing
        elif not self.bin_count:
            time_span = self._time_span(self.start_date, self.end_date)

            self.bin_count = time_span.days // self.bin_size
            if self.bin_count <= 0:
                msg = f'The arguments have created a calculated amd invalid bin size of {self.bin_count}. {self}'
                raise ValueError(msg)

            # Normalize the start date
            self.start_date = self._start_date(self.end_date, self.bin_count, self.bin_size)

        else:
            msg = "An unexpected and unhandled combination of arguments has been encountered."
            raise UnexpectedCondition(msg)

    def get_bin(self, date: Union[pandas.Timestamp, tuple[int, int, int]]) -> Optional[str]:
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
            return str(self._bin(date).date())
        else:
            return None

    def _time_span(self, start_date: pandas.Timestamp, end_date: pandas.Timestamp):
        """
        Return the number of days between two dates including the two dates.
        
        Args:
            start_date:
            end_date:

        Returns:
            Time span in days
            
        Raises:
            ValueError: If the start date is after the end date.
        """
        time_span = end_date - start_date + self.one_day
        if time_span.days <= 0:
            msg = f'The start date {start_date} must precede the end date {end_date}.'
            raise ValueError(msg)
        return time_span

    def _start_date(self, end_date: pandas.Timestamp, bin_count: int, bin_size: int):
        """
        Return a start date calculated from the end date, the bin size and the number of bins.
        
        Args:
            end_date: date
            bin_count: Number of bins
            bin_size: Sie of bins in days

        Returns:
            start date
        """
        time_span = pandas.Timedelta(bin_count * bin_size, 'd')
        return end_date - time_span + self.one_day

    def _bin(self, date: pandas.Timestamp) -> pandas.Timestamp:
        """
        Get the category for a date.
        
        Args:
            date:

        Returns:
            The last day of the date's time category
        """
        days_to_end_date = (self.end_date - date).days
        bin_day_delta = days_to_end_date // self.bin_size * self.bin_size
        bin_timedelta = pandas.Timedelta(days=bin_day_delta)
        bin_date = self.end_date - bin_timedelta
        return bin_date


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
        msg = f"No records of type '{health_type}' were found in the dataset."
        raise NoDataSupplied(msg)
    sto_ds = sto_ds.rename(columns={'value': col_name})
    return sto_ds


class UtilitiesException(Exception):
    pass
    
    
class UnexpectedCondition(UtilitiesException):
    pass


class NoDataSupplied(UtilitiesException):
    pass
