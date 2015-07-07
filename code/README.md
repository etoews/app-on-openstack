# Local Development

## Database

1. Install MySQL
1. Reboot machine
1. Start MySQL
  1. Open System Preferences
  1. MySQL
  1. Start MySQL Server

## API

```bash
cd app-on-openstack/code/api/
mkvirtualenv --python=`which python3` api-on-os
pip install -r requirements.txt
python manage.py create_all
python manage.py runserver --port 5000
```

## Worker

```bash
cd app-on-openstack/code/app/
mkvirtualenv --python=`which python3` -p python3 worker-on-os
pip install -r requirements.txt
python watermark/worker.py
```

## App

```bash
cd app-on-openstack/code/app/
mkvirtualenv --python=`which python3` app-on-os
pip install -r requirements.txt
python manage.py runserver --port 8000
```

open http://localhost:8000
