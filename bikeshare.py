import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = ""
    while city not in (['chicago','washington','new york city']):
        city = str(input('Please enter a valid city value: ')).lower()

    # TO DO: get user input for month (all, january, february, ... , june)
    month = ""
    while month not in (['all','january','february','march','april','may','june']):
        month = str(input('Please enter a valid month value: ')).lower()

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = ""
    while day not in (['all','monday','tuesday','wednesday','thursday','friday','saturday','sunday']):
        day = str(input('Please enter a valid day of week value: ')).lower()

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # TO DO: display the most common month
    df['month'] = df['Start Time'].dt.month
    popular_month = df['month'].mode()[0]
    print('Most Popular Month:', popular_month)

    # TO DO: display the most common day of week
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    popular_day_of_week = df['day_of_week'].mode()[0]
    print('Most Popular Day of Week:', popular_day_of_week)

    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Popular Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('Most Popular Start Station:', popular_start_station)

    # TO DO: display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('Most Popular End Station:', popular_end_station)

    # TO DO: display most frequent combination of start station and end station trip
    df['Start & End Station'] = df['Start Station'] + ' - ' + df['End Station']
    popular_start_end_station = df['Start & End Station'].mode()[0]

    #My Attempt at this using groupby but still confused about it -- can Udacity attach code to use groupby for this?
    #popular_stations = df.groupby(['Start Station','End Station'])['End Station'].count().sort_values(ascending=False)
    #popular_start_end_station = pd.DataFrame(popular_stations[['Start Station','End Station']])

    print('Most Popular Trip (Start & End Station):', popular_start_end_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['Travel Time'] = (df['End Time'] - df['Start Time']).dt.seconds / 60
    sum_time_min = df['Travel Time'].sum()

    print('Total travel time in minutes:', sum_time_min)

    # TO DO: display mean travel time
    mean_time_min = df['Travel Time'].mean()

    print('Mean travel time in minutes:', mean_time_min)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df.groupby(['User Type'])['User Type'].count().sort_values(ascending=False)
    print(user_types)

    # TO DO: Display counts of gender
    try:
        genders = df.groupby(['Gender'])['Gender'].count().sort_values(ascending=False)
        print(genders)
    except:
        print('Gender is not defined for this city')

    # TO DO: Display earliest, most recent, and most common year of birth
    try:
        print('The Max birth year is: ',int(df['Birth Year'].max()))
        print('The Min birth year is: ',int(df['Birth Year'].min()))
        print('The Most Common birth year is: ',int(df['Birth Year'].mode()[0]))
    except:
        print('Birth Year is not defined for this city')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def print_output(df):
    """Asks user if they want to see raw data and displays the raw data (in blocks of 5 lines) if they do"""

    # Ensure Valid ('yes' or 'no') User Input
    ans = ''
    while ans not in (['no','yes']):
        ans = str(input('Would you like to see 5 lines of raw data? ')).lower()

    # Iterate and add 5 lines so long as the user keeps saying 'yes'
    i = 0
    while ans != 'no':
        print(df[i:i+5])
        ans = str(input('Would you like to see 5 additional lines of raw data? ')).lower()
        i += 5


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        print_output(df) ### Added this function into main to run new function

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
