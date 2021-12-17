"""Utility functions to support Apple Medical notebooks."""

#  Copyright ©2022. Stephen Rigden.
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

from dataclasses import dataclass
from typing import Optional, Union

import pandas


@dataclass
class TimeCategories:
    """
    Support the conversion of matplotlib date ranges into matplotlib categories. The categories are
    represented by 'buckets' of date sequences. They are identified by the last date in the bucket.
    
    The buckets are aligned with the end_date. Since this could lead to the first bucket containing less
    than the full number of days defined by 'bucket_size' the 'start_date' is normalized to the
    beginning of the first complete bucket.
    For example, with start date = 2021-12-10, end_date = 2021-12-15, bucket_size = 4 the start date
    will be normalized to 2021-12-12.
    Also with start date = 2021-12-10, end_date = 2021-12-15, bucket_size = 6 the start date
    will be unchanged at 2121-12-10.

    Usage within matplotlib/seaborn:
        # Create a TimeCategories object
        start = pandas.Timestamp(2021, 11, 26)
        end = pandas.Timestamp(2021, 12, 5)
        bucket_size = 3
        time_categories = TimeCategories(start, end, bucket_size)
        
        # Create a new column 'bucket'
        df['bucket'] = df['date'].apply(time_categories.get_bucket)
    """
    start_date:  pandas.Timestamp
    end_date:  pandas.Timestamp
    bucket_size: int
    
    def __post_init__(self):
        if self.end_date < self.start_date:
            msg = f'The start date {self.start_date} must precede the end date {self.end_date}.'
            raise ValueError(msg)

        date_range = (self.end_date - self.start_date).days + 1
        if self.bucket_size > date_range:
            msg = (f"The bucket_size '{self.bucket_size}' must be less than the time span between the "
                   f"start and end dates ({date_range}).")
            raise ValueError(msg)
        
        # Normalize the start date to the first day of the first full bucket.
        one_day = pandas.Timedelta('1 day')
        start_date_bucket = self._bucket(self.start_date)
        yesterdays_bucket = self._bucket(self.start_date - one_day)
        if start_date_bucket == yesterdays_bucket:
            self.start_date = start_date_bucket + one_day

    def get_bucket(self, date: Union[pandas.Timestamp, tuple[int, int, int]]) -> Optional[str]:
        """
        Return the bucket that contains the date.
        
        Args:
            date: pandas,Timestamp or ('YYYY', 'MM', 'DD') tuple are acceptable types.
            
        Raises:
            TypeError: If the date is not an acceptable type.

        Returns:
            The last day of the time bucket formatted as a date string (YYYY-MM-DD) or
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
            return str(self._bucket(date).date())
        else:
            return None

    def _bucket(self, date: pandas.Timestamp) -> pandas.Timestamp:
        """
        Get the bucket for a date.
        
        Args:
            date:

        Returns:
            The last day of the date's time bucket
        """
        days_to_end_date = (self.end_date - date).days
        bucket_day_delta = days_to_end_date // self.bucket_size * self.bucket_size
        bucket_timedelta = pandas.Timedelta(days=bucket_day_delta)
        bucket = self.end_date - bucket_timedelta
        return bucket
