NREC report application
=======================

This is a simple web application for a RESTful API for collecting and querying instance information.

Development
-----------

You will need to install python36+ and pyton virtualenv first.

**Install:**

```
git clone https://github.com/norcams/report-app.git
cd report-app
virtualenv -p /path/to/python3 .
source bin/activate
pip install -r requirements.txt
python setup.py develop
```

**Run**:

```
python app.py
```

**Test example with curl**

```
curl -X POST -H "Authorization: Bearer xg7ek8fj2HmOk3Qff95pgbmQCv4ZpGeH" \
-H 'Content-Type: application/json' \
-H 'Accept: application/problem+json' \
-d '{"message": "The new gold image for Fedora 56 is now available", "message_type": "important" }' \
'https://report.vagrant.iaas.intern/api/v1/status'
```
