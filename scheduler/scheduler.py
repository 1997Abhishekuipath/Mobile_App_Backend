from apscheduler.schedulers.background import BackgroundScheduler
from .updater import update
from .updater import insert_sd
from .updater import insert_tickets
from .updater import insert_SdStage
from .updater import insert_SdStatus
from .updater import insert_SdPriority
from .updater import insert_SdSeverity
from .updater import insert_PcvEng
from .updater import insert_cusFields
from .updater import insert_tickets_updated
from .updater import cat_for_desk
from .updater import cat_for_partition

def start():
    print('schedular-in')
    scheduler = BackgroundScheduler()
    # scheduler.add_job(update, 'interval', seconds = 60)sch
    
    # scheduler.add_job(insert_sd, 'interval', seconds = 86400)
    # scheduler.add_job(insert_SdStage, 'interval', seconds = 86400) # 86400 = 1 day
    # scheduler.add_job(insert_SdStatus, 'interval', seconds = 86400)
    # scheduler.add_job(insert_SdPriority, 'interval', seconds = 86400)
    # scheduler.add_job(insert_SdSeverity, 'interval', seconds = 86400)
    scheduler.add_job(insert_tickets, 'interval' , seconds = 300) #86400 = 24 Hours
    # scheduler.add_job(insert_cusFields, 'interval', seconds = 86400)
    scheduler.add_job(insert_tickets_updated, 'interval' , seconds = 60) #120 = 2 minutes

    # scheduler.add_job(cat_for_partition, 'interval', seconds = 5) incomplete
    # scheduler.add_job(cat_for_desk, 'interval', seconds = 5) incomplete
    scheduler.add_job(insert_PcvEng, 'interval', seconds = 60)
    scheduler.start() 


