import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    check = True
    while True:
        try:
            if check:
                city = input(
                    "Which city data do you want to explore please choose one from the given cities (chicago, new york city, washington)?\n").lower()
                check = False
            if city not in ('chicago', 'new york city', 'washington'):
                city = input(
                    "Wrong input please choose one city from (chicago, new york city, washington).\n").lower()
                if city in ('chicago', 'new york city', 'washington'):
                    break
            else:
                break
        except:
            print("\nInvalid input try again.\n")

    while True:
        try:
            if not check:
                month = input(
                    "Which month: (all, January, February, March, April, May, June)?\n").lower()
                check = True
            if month not in ("all", "january", "february", "march", "april", "may", "june"):
                month = input(
                    "Wrong input please choose one month from (all, January, February, March, April, May, June).\n").lower()
                if month in ("all", "january", "february", "march", "april", "may", "june"):
                    break
            else:
                break
        except:
            print("\nInvalid input please try again.\n")

    while True:
        try:
            if check:
                day = input(
                    "Which day: (all, Monday, Tuesday, Wedsenday, Thursday, Friday, Saturday, Sunday)?\n").lower()
                check = False
            if day not in ("all", "monday", "tuesday", "wedsenday", "thursday", "friday", "saturday", "sunday"):
                day = input(
                    "Wrong input please choose one month from (all, January, February, March, April, May, June).\n").lower()
                if day in ("all", "monday", "tuesday", "wedsenday", "thursday", "friday", "saturday", "sunday"):
                    break
            else:
                break
        except:
            print("\nInvalid input try again.\n")

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
    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    if month != "all":
        months = ["january", "february", "march", "april", "may", "june"]
        month = months.index(month)+1
        df = df[df['month'] == month]

    if day != "all":
        df = df[df['day_of_week'] == day.title()]

    df = df[df['User Type'] != 'Dependent']

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    most_common_month = df['month'].mode()[0]
    months = ["january", "february", "march", "april", "may", "june"]
    most_common_month = months[most_common_month-1]
    print("The most popular month is:  {}\n".format(most_common_month))

    most_common_day = df['day_of_week'].mode()[0]
    print("The most popular day is:  {}\n".format(most_common_day))

    df['hour'] = df['Start Time'].dt.hour
    most_common_hour = df['hour'].mode()[0]
    print("The most popular hour is:  {}\n".format(most_common_hour))

    print("\nThis took %s seconds.\n" % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    most_common_start_station = df['Start Station'].mode()[0]
    print("The most popular Start Station is:  {}\n".format(
        most_common_start_station))

    most_common_end_station = df['End Station'].mode()[0]
    print("The most popular End Station is:  {}\n".format(most_common_end_station))

    df['track'] = df['Start Station'] + "/" + df['End Station']
    most_common_track = df['track'].mode()[0]
    print("The most popular track is:  {}\n".format(most_common_track))

    print("\nThis took %s seconds.\n" % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_time = (df['Trip Duration']/60).sum().round()
    print("The total travel time in mins: {}\n".format(total_time))

    avg_time = (df['Trip Duration']/60).mean().round()
    print("The average travel time in mins: {}\n".format(avg_time))

    print("\nThis took %s seconds.\n" % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    user_types_count = df['User Type'].value_counts().to_frame()
    print(user_types_count)
    print()
    print('-'*40)
    print()

    if city != "washington":
        gender_count = df['Gender'].value_counts().to_frame()
        print(gender_count)
        print()
        most_common_year = df['Birth Year'].mode()[0]
        most_recent_year = df['Birth Year'].max()
        earliest_year = df['Birth Year'].min()
        print("The most common birth year: {}\n".format(most_common_year))
        print("The most recent birth year: {}\n".format(most_recent_year))
        print("The earliest birth year: {}\n".format(earliest_year))

    print("\nThis took %s seconds.\n" % (time.time() - start_time))
    print('-'*40)


def display(df):
    """
    prompt the user if they want to see the next 5 lines of raw data

    """
    start_time = time.time()
    print("\nChecking raw data...\n")
    answer = "yes"
    start = 0
    end = 5
    check = True
    while answer != 'no' and end < df.shape[0]:
        try:
            if check:
                answer = input(
                    "Do you to want to see five rows of the data: (Enter yes or no). \n").lower()
                check = False
            if answer not in ['yes', 'no']:
                answer = input("invalid input please enter, yes or no. \n")
            if answer == 'yes':
                print(df[start:end])
                start += 5
                end += 5
                check = True
        except:
            print("\nInvalid input please try again.\n")
    print("\nThis took {} seconds.\n".format(time.time() - start_time))
    print('-'*40)


def remove_na(df):
    """
    Remove all rows that contain NaN values

    """
    start_time = time.time()
    print("\nChecking if data has missing values...\n")
    prev_rows = df.shape[0]
    df.dropna(axis=0, inplace=True)
    curr_rows = df.shape[0]
    if (prev_rows-curr_rows) != 0:
        print("{} rows have been deleted due to having missing values\n".format(
            prev_rows-curr_rows))
    else:
        print("the data has no missing values")
    print("\nThis took {} seconds.\n".format(time.time() - start_time))
    print('-'*40)


def remove_duplicate(df):
    """

    Remove all duplicate rows in the data

    """
    start_time = time.time()
    print("\nChecking if data has duplicate rows...\n")
    prev_rows = df.shape[0]
    df.drop_duplicates(inplace=True)
    curr_rows = df.shape[0]
    if (prev_rows-curr_rows) != 0:
        print("{} rows have been deleted due to duplicate rows\n".format(
            prev_rows-curr_rows))
    else:
        print("the data has no duplicate rows")
    print("\nThis took {} seconds.\n".format(time.time() - start_time))
    print('-'*40)


def main():
    while True:
        check = True
        no = False
        city, month, day = get_filters()
        df = load_data(city, month, day)
        remove_na(df)
        remove_duplicate(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display(df)

        while True:
            try:
                if check:
                    answer = input(
                        "Do you to want to restart: (Enter yes or no). \n").lower()
                    check = False
                if answer not in ['yes', 'no']:
                    answer = input("invalid input please enter, yes or no. \n")
                else:
                    if answer == 'no':
                        no = True
                    break
            except:
                print("\nInvalid input please try again.\n")
        if no:
            break
        else:
            continue


if __name__ == "__main__":
    main()
