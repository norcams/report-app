from flask import current_app as app

INSTANCE = {
    'demo': {
        'name': 'demo-api-instance',
        'ip':   '127.0.0.1'
    }
}

def list_instances():
    return [INSTANCE[key] for key in sorted(INSTANCE.keys())]

def add_instance_report(instance):
    print instance
    print app.config
    return 'report added for %s' % instance['ip'], 201
