import pandas as pd


def validate(users, login_data, checkout_data, invalid_checkout_list, dayoff_data, invalid_dayoff_list):
    for user in users:
        login_days = login_data.loc[login_data['USER'] == user]['LOGIN_DATE']
        # checkout
        checkout(login_days, checkout_data, user, invalid_checkout_list)

        # dayoff
        dayoff(login_days, dayoff_data, user, invalid_dayoff_list)
    print(invalid_dayoff_list)
    print(invalid_checkout_list)


def dayoff(login_days, dayoff_data, user, invalid_dayoff_list):
    dayoff_users = dayoff_data['USER']
    for dayoff_user in dayoff_users:
        if user == dayoff_user:
            dayoff_dates = dayoff_data[dayoff_data['USER'] == dayoff_user].values
            for dayoff in dayoff_dates:
                start_date = pd.to_datetime(dayoff[0], format='%d/%m/%Y')
                end_date = pd.to_datetime(dayoff[1], format='%d/%m/%Y')
                for login_date in login_days:
                    if start_date <= pd.to_datetime(login_date) <= end_date:
                        invalid_user = {'user': user, 'start-date': start_date, 'end_date': end_date}
                        print(invalid_user)
                        if invalid_user not in invalid_dayoff_list:
                            invalid_dayoff_list.append(invalid_user)


def checkout(login_days, checkout_data, user, invalid_checkout_list):
    checkout_users = checkout_data['USER']
    for checkout_user in checkout_users:
        if user == checkout_user:
            checkout_date = checkout_data[checkout_data['USER'] == checkout_user]['CHECKOUT_DATE']
            for login_date in login_days:
                if login_date > checkout_date.values[0]:
                    invalid_user = {'user': user, 'check-out-date': checkout_date.values[0]}
                    if invalid_user not in invalid_checkout_list:
                        invalid_checkout_list.append(invalid_user)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    login_data_1 = pd.read_excel('PART 1.xlsx', sheet_name='login_data')
    login_data_2 = pd.read_excel('PART 2.xlsx', sheet_name='login_data')

    # user data
    user_1 = login_data_1['USER'].unique()
    user_2 = login_data_2['USER'].unique()

    # checkout
    checkout_data = pd.read_excel('PART 1.xlsx', sheet_name='checkout_data')
    # dayoff
    dayoff_data = pd.read_excel('PART 1.xlsx', sheet_name='dayoff_data')

    # Result
    invalid_checkout_list = []
    invalid_dayoff_list = []

    validate(user_1, login_data_1, checkout_data, invalid_checkout_list, dayoff_data, invalid_dayoff_list)
    validate(user_2, login_data_2, checkout_data, invalid_checkout_list, dayoff_data, invalid_dayoff_list)

    df1 = pd.DataFrame(invalid_checkout_list)
    df2 = pd.DataFrame(invalid_dayoff_list)

    with pd.ExcelWriter("output.xlsx") as writer:
        df1.to_excel(writer, sheet_name='invalid_checkout_list', index=False)
        df2.to_excel(writer, sheet_name='invalid_dayoff_list', index=False)
