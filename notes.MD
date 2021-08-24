Install redis globally in linux distro and check that is working
- start `redis-server` in one terminal
- open another terminal and check response with `redis-cli ping`

Create virtual environment and install `django, celery, django-celery-beat, django-celery-results` and `redis`
Start django project, add django_celery_beat and django_celery_results to `INSTALLED_APPS` and configure celery in `settings.py `
Create celery app in project root and add to init module.
Create django app and add `tasks.py` module at app root folder. Giving a name to a task makes it easier to call it to scheduling
Keep 3 terminals open
- One with redis-server running or start a redis process
- One with celery running by calling `celery -A tat worker -l info` at the root of the project (same level as `manage.py`)
- One with django

When a task runs, thanks to the celery task decorator (`@task()`), the celery server knows that it has work to do. For example I can open the django shell and do the following
```
from billing.tasks import sum, mult
add.delay(32,11)
```
The delay method acquired through @task, sends the operation of adding 32 and 11 to the celery server. In the celery server log something like this will be shown:
```
[2021-07-26 19:21:41,040: INFO/MainProcess] Task sum_two_numbers[4bded252-391f-4a40-a233-a2ce3aea29eb] received
[2021-07-26 19:21:41,126: INFO/ForkPoolWorker-2] Task sum_two_numbers[4bded252-391f-4a40-a233-a2ce3aea29eb] succeeded in 0.07426669999949809s: 43
```
The fun part would be adding meaningful tasks and calling them through the view functions, to generate emails, for example.

## What happens if celery server is not running? 
Still can run delay on tasks, and the messages are kept in redis message queue. Once the celery server comes up again, it will look for the redis queue to know if there are tasks pending.

### Celery beat
It's used to schedule task. If I go to admin, I'll see that there are sections to add this scheduled jobs from tasks defined in the registered apps every period of time I decide. The configuration needed in the celery app is:

```
from celery.schedules import crontab

app.conf.beat_schedule = {
    'add-every-minute-contrab':{
        'task':'multiply_two_numbers',
        'schedule':crontab(),
        'args':(16,16)
    },
    'add-every-5-seconds':{
        'task':'multiply_two_numbers',
        'schedule':5.0,
        'args':(16,16)
    },
}
```
Also, besides redis-server and the celery worker, I need to start a celery beat in a terminal.
```
celery -A tat beat -l info
```