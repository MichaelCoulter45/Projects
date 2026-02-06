



# Get user's distance
# Calculate per day miles and for what purpose.


# Structured Zones % of weekly distance
zone2_percent = 80
quality_percent = 20


def find_weekly_plan():
    print(f"How many miles are you planning to run this week?")
    weekly_distance = float(input())
    
    long_day = weekly_distance * 0.20
    remaining_distance = weekly_distance - long_day
    
    print(f"How many days are you running this week?")
    running_days = float(input())
    miles_per_day = remaining_distance / (running_days - 1)
    
    print(f"""Each day you should be running {miles_per_day} miles
and {long_day} miles for your long run.
""")








def main():
    find_weekly_plan()


if __name__ == "__main__":
    main()














# easy = (weekly_distance * zone2_percent) / 100
#     quality = (weekly_distance * controlled_aerobic_quality_percent) / 100
#     threshold = (weekly_distance * threshold_percent) / 100
    
#     # print(f"How many days are you planning to run this week?")
#     # days_run = float(input())
    
#     print(f"How many easy days?")
#     days_easy = float(input())
    
    
#     easy_day = (easy / days_easy) - warm_up - cool_down
#     interval_day = quality + warm_up + cool_down
#     threshold_day = threshold + warm_up + cool_down
#     long_day = weekly_distance * 0.25
    
#     print(f"""Since you're running {weekly_distance} miles, the breakdown is:
#     {zone2_percent}% Easy: {easy}
#     {controlled_aerobic_quality_percent}% Quality: {quality}
#     {threshold_percent}% Threshold: {threshold}
    
#         Monday (Easy): {easy_day}
#         Tuesday (Intervals): {interval_day}
#         Wednesday (Easy): {easy_day}
#         Thursday (Threshold): {threshold_day}
#         Friday (Easy): {easy_day}
#         Sat or Sun (Long): {long_day}
#     """)