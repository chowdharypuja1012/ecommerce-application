from django.db import connection
from django.db.migrations.executor import MigrationExecutor
from django.test import TestCase, TransactionTestCase


class CatalogueMigrationTest(TransactionTestCase):
    def test_0001_initial_migration_applied(self):
        executor = MigrationExecutor(connection)
        applied_migrations = executor.loader.applied_migrations
        self.assertIn(("catalogue", "0001_initial"), applied_migrations)
