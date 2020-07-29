from orquesta import conducting
from orquesta.specs import native as native_specs
from orquesta import statuses
from orquesta.tests.unit import base as test_base


class WorkflowConductorExtendedTaskTest(test_base.WorkflowConductorTest):
    def test_init_task_with_no_action(self):
        wf_def = """
        version: 1.0
        tasks:
          task1:
            next:
              - publish: xyz=123
                do: task2
          task2:
            action: core.noop
        """

        spec = native_specs.WorkflowSpec(wf_def)
        conductor = conducting.WorkflowConductor(spec)
        conductor.request_workflow_status(statuses.RUNNING)

        # Process task1.
        task_name = "task1"
        expected_task_ctx = {}
        self.assert_next_task(conductor, task_name, expected_task_ctx)
        self.forward_task_statuses(conductor, task_name, [statuses.RUNNING, statuses.SUCCEEDED])

        # Process task2.
        task_name = "task2"
        expected_task_ctx = {"xyz": 123}
        self.assert_next_task(conductor, task_name, expected_task_ctx)
        self.forward_task_statuses(conductor, task_name, [statuses.RUNNING, statuses.SUCCEEDED])

        self.assertEqual(conductor.get_workflow_status(), statuses.SUCCEEDED)
