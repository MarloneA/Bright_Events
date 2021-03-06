import os
import sys
import coverage
import unittest
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import db, create_app
from app import models


config_name = os.getenv('FLASK_CONFIG')
app = create_app(config_name)
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

COV = None
if os.environ.get('FLASK_COVERAGE'):
    COV = coverage.coverage(branch=True, include='app/*')
    COV.start()

@manager.command
def test(coverage=False):
    """
    Run the unit tests
    """
    if coverage and not os.environ.get('FLASK_COVERAGE'):

        os.environ['FLASK_COVERAGE'] = '1'
        os.execvp(sys.executable, [sys.executable] + sys.argv)

    tests = unittest.TestLoader().discover('tests')
    test_results = unittest.TextTestRunner(verbosity=2).run(tests)

    if test_results.wasSuccessful():

        if COV:
            COV.stop()
            COV.save()
            print('Coverage Summary:')
            COV.report()
            basedir = os.path.abspath(os.path.dirname(__file__))
            covdir = os.path.join(basedir, 'tmp/coverage')
            COV.html_report(directory=covdir)
            print('HTML version: file://%s/index.html' % covdir)
            COV.erase()

        return 0
    return 1

if __name__ == '__main__':
    manager.run()
