from datetime import datetime, timedelta

class GateHelper:
    minuteInterval = 10

    @staticmethod
    def currentMinute() -> int:
        return datetime.now().minute

    #gates are running minutes 0 to 10, 20 to 30, 40 to 50(only on odd minutes)
    @staticmethod
    def isGateRunning() -> bool:
        return GateHelper.currentMinute() // GateHelper.minuteInterval % 2 == 0

    @staticmethod
    def toNextGateEventMin() -> int:
        return GateHelper.minuteInterval - GateHelper.currentMinute() % GateHelper.minuteInterval

    @staticmethod
    def nextTenMinStrippedToHour() -> datetime:
        now = datetime.now()
        neededDateTime = now + timedelta(minutes=GateHelper.toNextGateEventMin())
        return datetime(year=neededDateTime.year,
                         month=neededDateTime.month,
                           day=neededDateTime.day,
                             hour=neededDateTime.hour, 
                             minute=neededDateTime.minute, 
                             second=1)

    @staticmethod
    def toTextMin() -> int:
        return (GateHelper.nextTenMinStrippedToHour() - datetime.now()).seconds