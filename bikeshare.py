import time
import pandas as pd

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

months = ["january", "february", "march", "april", "may", "june", "all"]
days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday", "all"]


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US Bikeshare data!')
    city, month, day = "", "", ""

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while city not in CITY_DATA.keys():
        city = input("Would you like to see data for Chicago, New York City, or Washington?\n").lower()

    # get user input for month (all, january, february, ... , june)
    while month not in months:
        month = input("Which month - January, February, March, April, May, June, or All?\n").lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while day not in days:
        day = input("Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, or All?\n").lower()

    print('-' * 40)
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
    file_name = CITY_DATA.get(city)
    df = pd.read_csv(file_name)

    # convert "Start Time" column from string to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # create new column "Month" by extracting the month form datetime
    df['Month'] = df['Start Time'].dt.month

    # create new column "Day" by extracting the day form datetime
    df['Day'] = df['Start Time'].dt.day_name()
    df['Day'] = df['Day'].str.lower()

    # filter by month
    if month != "all":
        month_index = months.index(month) + 1
        df = df[df['Month'] == month_index]

    # filter by day
    if day != "all":
        df = df[df['Day'] == day]

    return df


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if month == "all":
        freq_month = df['Month'].mode()[0]
        print("Most common month: " + months[freq_month - 1].title())

    # display the most common day of week
    if day == "all":
        freq_day = df['Day'].mode()[0]
        print("Most common day: " + freq_day.title())

    # display the most common start hour
    df['Hour'] = df['Start Time'].dt.hour
    freq_hour = df['Hour'].mode()[0]
    print("Most common start hour: " + str(freq_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    freq_start_station = df['Start Station'].mode()[0]
    print("Most common start station: " + freq_start_station)

    # display most commonly used end station
    freq_end_station = df['End Station'].mode()[0]
    print("Most common end station: " + freq_end_station)

    # display most frequent combination of start station and end station trip
    start, end = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print("Most common trip: From \'" + start + "' To \'" + end + "'")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print("Total travel time: " + str(df['Trip Duration'].sum()) + " seconds")

    # display mean travel time
    print("Mean travel time: " + str(df['Trip Duration'].mean()) + " seconds")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df, city):
    """Displays statistics on Bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # display counts of user types
    count_user_type = df['User Type'].value_counts()
    print("Total number of subscribers: " + str(count_user_type[0]))
    print("Total number of customers: " + str(count_user_type[1]))

    # display counts of gender
    if city != list(CITY_DATA.keys())[2]:
        count_gender = df['Gender'].value_counts()
        print("\nTotal number of males: " + str(count_gender[0]))
        print("Total number of females: " + str(count_gender[1]))

    # display earliest, most recent, and most common year of birth
    if city != list(CITY_DATA.keys())[2]:
        print("\nEarliest year of birth: " + str(df['Birth Year'].min()).split('.')[0])
        print("Most recent year of birth: " + str(df['Birth Year'].max()).split('.')[0])
        print("Most common year of birth: " + str(df['Birth Year'].mode()[0]).split('.')[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def display_data(df):
    """Displays 5 rows of data and asks the user whether he wants to view more or not"""

    start_row = 0
    first_or_next_time = " the first "

    while True:
        should_view_data = ""
        while should_view_data != "yes" and should_view_data != "no":
            print("\nDo you want to see{}5 rows of data?".format(first_or_next_time))
            should_view_data = input("Type \'Yes' to see th data or \'No' to end the program\n").lower()

        if should_view_data == "yes":
            first_or_next_time = " the next "
            if df.iloc[start_row:start_row + 5].empty:
                print("\nNo more data")
                break
            else:
                print(df.iloc[start_row:start_row + 5])
                start_row += 5
        else:
            break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        # print(df.info())

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
