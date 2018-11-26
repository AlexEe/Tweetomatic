from crontab import CronTab

my_cron = CronTab(user='alex')

for job in my_cron:
    print(job)
