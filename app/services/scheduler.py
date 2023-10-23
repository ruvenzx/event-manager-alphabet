import asyncio
from datetime import datetime
from app.services.service import service

class BackgroundRunner:
    
    async def send_reminder(self, event):
        ### fake sending mechanism ###
        ### would have also marked this notification as sent to not abuse ###
        pass
   
    async def check_for_events(self, now):
        events = await service.get_all()
        for event in events:
            if event.date < now:
                print(f"SENDING REMINDER FOR EVENT {event.id}")
                await self.send_reminder(event)
    
    async def run_main(self):
        while True:
            now = datetime.now()
            print('Background Task Running', now)
            await asyncio.sleep(60)
            await self.check_for_events(now)

runner = BackgroundRunner()