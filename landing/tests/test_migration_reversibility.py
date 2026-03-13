from __future__ import annotations

from django.db import connection
from django.db.migrations.executor import MigrationExecutor
from django.db.migrations.loader import MigrationLoader
from django.test import TransactionTestCase


class MigrationReversibilityTests(TransactionTestCase):
    databases = {"default"}

    def test_landing_migration_operations_are_marked_reversible(self) -> None:
        loader = MigrationLoader(connection, ignore_no_migrations=True)
        irreversible_ops: list[str] = []

        for (app_label, migration_name), migration in loader.disk_migrations.items():
            if app_label != "landing":
                continue
            for idx, operation in enumerate(migration.operations):
                if getattr(operation, "reversible", True):
                    continue
                irreversible_ops.append(
                    f"{app_label}.{migration_name} operation[{idx}] "
                    f"{operation.__class__.__name__}"
                )

        self.assertEqual(
            irreversible_ops,
            [],
            msg=(
                "Irreversible migration operations detected. "
                "Add reverse_code/reverse_sql or redesign migration: "
                + ", ".join(irreversible_ops)
            ),
        )

    def test_latest_landing_migration_can_rollback_one_step_and_reapply(self) -> None:
        executor = MigrationExecutor(connection)
        leaves = executor.loader.graph.leaf_nodes("landing")
        self.assertTrue(leaves, "No landing migrations found.")
        self.assertEqual(
            len(leaves), 1, f"Expected one landing migration leaf, found {leaves}"
        )
        latest_target = leaves[0]

        node = executor.loader.graph.node_map[latest_target]
        parent_keys = [parent.key for parent in node.parents]
        self.assertTrue(
            parent_keys, f"Migration {latest_target} has no parent to rollback."
        )
        rollback_target = parent_keys[0]

        # Ensure latest state first, then rollback one step, then migrate forward again.
        executor.migrate([latest_target])
        executor = MigrationExecutor(connection)
        executor.migrate([rollback_target])
        executor = MigrationExecutor(connection)
        executor.migrate([latest_target])
