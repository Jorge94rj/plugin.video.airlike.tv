from cron import CronManager,CronJob
from resources.lib.db.debug_createdb import createDB
from resources.lib.db.importer import importDB

command = 'RunScript(special://home/addons/plugin.video.airlike.tv/resources/lib/contentmanager.py)'

def initCron():
    manager = CronManager()
    jobs = list(manager.getJobs())

    airlikeJob = list(filter(lambda cj: cj.name == "airlike.checker", jobs))

    if len(airlikeJob) == 0:
        job = CronJob()
        job.name = "airlike.checker"
        job.command = command
        # job.expression = "*/1 * * * *"
        job.expression = "0 */1 * * *"
        job.show_notification = "false"
        manager.addJob(job)


if __name__ == '__main__':
    initCron()
