import numpy as np
import pandas as pd
import time

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

months = ['january', 'february', 'march', 'april', 'may', 'june']
week_days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
#define several "yes" answers. That is not necessary.
specific_yes_answers = ['yes','yepp','yay','sure']

def get_filters():
    print('-'*40)
    print(\n)
    print(\n)
    print('Hey there! Lets analyze some bikesharing data.\nWe can provide you with data for the following cities:\n-----')
    #showing the cities which can be selected
    for key,value in CITY_DATA.items() :
        print(key.upper())
    city = input('-----\nWhich city do you like to analyze? ').lower()

    while city not in CITY_DATA:
        print('Sorry, the city does not exist in our database. Right now you can filter for: ')
        #showing the cities again while city is no key in CITY_DATA
        for key,value in CITY_DATA.items():
            print(key.upper())
        city = input('Please try again and choose a city: ').lower()

    print('Alright, the choosen city is:',city.upper())
    print('-'*40)

    specific_month = input('Do you like to analyse data for a specific month?\nPlease answer with "yes" or "no": ')

    if specific_month not in specific_yes_answers:
        month = 'all'
    else:
        print('Please note that the following months are available:\n-----')
        #showing the available months because the data is restricted and their is not a data set for every month
        for i in months:
            print(i.upper())
        month = input('-----\nWhich month do you like to analyse? ').lower()
        z = 0
        #In case the user types in a month which is not available for 5 times, the data set is filtered by "all month"
        while month not in months and month != 'all':
            if z is 5:
                month = 'all'
                print('Sorry, that did not work several times. Let us try it with ALL months.')
            else:
                z += 1
                print('Ops, something went wrong.\nPlease remember that the following months are available:')
                for i in months:
                    print(i.upper())
                month = input('Which one do you like to choose? ').lower()
        month = months.index(month) + 1

    print('-'*40)

    specific_day = input('Do you like to analyse data for a specific week day in the choosen month(s)?\nPlease answer with "yes" or "no": ')

    if specific_day not in specific_yes_answers:
        day = 'all'
    else:
        day = input('Alright, which week day do you like to analyse? ').lower()
        y = 0
        #In case the user types in a week day which is not available for 5 times, the data set is filtered by "all week days"
        while day not in week_days and day != 'all':
            if y is 5:
                day = 'all'
                print('Sorry, that did not work. Let us try it with ALL week days.')
            else:
                y += 1
                day = input('Ooops, something went wrong. That is not a week day.\nNext chance: which week day do you like to choose? ').lower()
    return city, month, day

    print('-'*40)

#Importing the correct csv and creating a dataframe depending on the defined filters
def load_data(city, month, day):
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['starting_hour'] = df['Start Time'].dt.hour

    if month != 'all':
        df = df[df['month'] == month]
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('-'*40)
    print('\n--Section about The Most Frequent Times of Travel--\n')

    #Interpolating NaN Values to make sure that arithmetic operations work.
    #That is not necessary for every function so that it is defined here and not in general.
    df.interpolate(method = 'linear', axis = 0, inplace = True)

    if input('Do you like to have a look at the raw data before running the calculation? ') == 'yes':
        print(df.head(5))
        input('\nPlease type in ANY KEY and press ENTER to continue with the calculation.')
        print('\nCalculating The Most Frequent Times of Travel...\n')
    else:
        print('\nCalculating The Most Frequent Times of Travel...\n')

    start_time = time.time()

    popular_month = df['month'].mode()[0]
    print('The most popular month was:',months[popular_month-1].title(),'\n')

    # TO DO: display the most common day of week

    popular_day = df['day_of_week'].mode()[0]
    print('The most popular week day was:',popular_day,'\n')

    # TO DO: display the most common start hour

    popular_hour = df['starting_hour'].mode()[0]
    print('The most popular hour was:',popular_hour,'\n')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('-'*40)
    print('\n--Section about The Most Popuar Stations and Trips--\n')


    if input('Do you like to have a look at the raw data before running the calculation? ') == 'yes':
        print(df.head(5))
        input('\nPlease type in ANY KEY and press ENTER to continue with the calculation.')
        print('\nCalculating The Most Popular Stations and Trip...\n')
    else:
        print('\nCalculating The Most Popular Stations and Trip...\n')

    start_time = time.time()

    # display most commonly used start station
    popular_station = df['Start Station'].mode()[0]
    print('The most popular start station was:',popular_station,'\n')

    # display most commonly used end station
    popular_station_end = df['End Station'].mode()[0]
    print('The most popular end station was:',popular_station_end,'\n')

    # display most frequent combination of start station and end station trip
    df['station_combi'] = df['Start Station'].str.cat(df['End Station'],sep=" -> ")
    popular_station_combi = df['station_combi'].mode()[0]
    print('The most popular station combi was:',popular_station_combi,'\n')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('-'*40)
    print('\n--Section about The Total and Average Trip Duration--\n')

    if input('Do you like to have a look at the raw data before running the calculation? ') == 'yes':
        print(df.head(5))
        input('\nPlease type in ANY KEY and press ENTER to continue with the calculation.')
        print('\nCalculating The Total and Average Trip Duration...\n')
    else:
        print('\nCalculating The Total and Average Trip Duration...\n')

    start_time = time.time()

    #I'm not sure if this is necessary
    df.interpolate(method = 'linear', axis = 0, inplace = True)

    #Converting End Time and Start Time to datetime64 (without "ns")
    #That was necessary because the subtract function did not work with datetime[ns]
    df['Start Time'] = df['Start Time'].values.astype('datetime64')
    df['End Time'] = df['End Time'].values.astype('datetime64')
    df['diff'] = df['End Time'].subtract(df['Start Time'])
    total_travel = df['diff'].sum()
    print('The total travel time was:',total_travel,'\n')

    #display mean travel time
    #For sure it would be more convenient to see the mean travel time in minutes here.
    #but data scientists will understand :)
    mean_travel = df['diff'].mean()
    print('Average rent length was:',mean_travel,'\n')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


#"city" has to be inserted in the function as well because if not it can not be called.
def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('-'*40)
    print('\n--Section about Statistics on Bikeshare Users--\n')

    if input('Do you like to have a look at the raw data before running the calculation? ') == 'yes':
        print(df.head(5))
        input('\nPlease type in ANY KEY and press ENTER to continue with the calculation.')
        print('\nCalculating Statistics on Bikeshare Users...\n')
    else:
        print('\nCalculating Statistics on Bikeshare Users...\n')

    df.interpolate(method = 'linear', axis = 0, inplace = True)
    start_time = time.time()

    #Display counts of user types

    print('The counts of user types were the following:')
    user_type = df['User Type'].value_counts().to_frame()
    print (user_type)
    #Also showing the relative distribution
    print('\nThis results in the following distribution:')
    user_type_r = df['User Type'].value_counts(normalize=True).to_frame()
    print (user_type_r)

    #Display counts of gender & Display earliest, most recent, and most common year of birth
    #There is no gender / birth date data for washington so we have to insert the function in a if else statement

    if city == 'washington':
        print('\nSorry, there is no gender or birth date data available for Washington.\n')
    else:
        print('\nThe counts of gender were the following:')
        gender = df['Gender'].value_counts().to_frame()
        print (gender)
        print('\nThis results in the following distribution:')
        #Also showing the relative distribution
        gender_r = df['Gender'].value_counts(normalize=True).to_frame()
        print (gender_r)

        df['Birth Year'] = df['Birth Year'].astype(int)
        popular_birth_year = df['Birth Year'].mode()[0]
        print('\nThe most common users birth year was:', popular_birth_year,'\n')
        earliest_birth = df['Birth Year'].min()
        print('The earliest users birth year was:',earliest_birth,'\n')
        most_recent_birth = df['Birth Year'].max()
        print('The most recent users birth year was:',most_recent_birth,'\n')
        #To be honest I was not 100 % sure what is meant by "most recent". Hopefully you mean the "youngest" user.


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        #"city" has to be inserted in the function as well because if not it can not be called.
        user_stats(df,city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
