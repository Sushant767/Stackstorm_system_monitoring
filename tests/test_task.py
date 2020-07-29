from orquesta import conducting
from orquesta.specs import native as native_specs
from orquesta import statuses
from orquesta.tests.unit import base as test_base


class WorkflowConductorExtendedTaskTest(test_base.WorkflowConductorTest):
    def test_part_of_workflow(self):
        wf_def = """
        version: 1.0

        input:
        - cmd_cpu
        - cmd_results_cpu
        - cmd_mem
        - cmd_results_mem

        vars:
        - var_cpu: null
        - var_res_cpu: null
        - var_mem: null
        - var_res_mem: null 
        - stderr_cpu: null
        - stderr_mem: null

        tasks:

        setup_task:
        #parallel task for checking cpu consumption and memory usage and subsequently generating alert message to slack channel if limit is crossed.
        next:
        - do:
          - task_cpu
          - task_mem
   
        task_cpu:
        action: core.local cmd=<% ctx(cmd_cpu) %>
            next:
               - when: <% succeeded() and result().stdout <= 50 %>
                 publish: var_cpu=<% result().stdout %>
                 do:
                    - post_cpu_success_to_slack
               - when: <% succeeded() and result().stdout >= 50 %>
                 publish: var_cpu=<% result().stdout %>
                 do: 
                    - perform_cpu_analysis
               - when: <% failed() %>
                 publish: stderr_cpu=<% result().stderr %>
                 do:
                    - post_error_to_slack
     
        """



        spec = native_specs.WorkflowSpec(wf_def)
        conductor = conducting.WorkflowConductor(spec)
        conductor.request_workflow_status(statuses.RUNNING)

        # Process setup task.
        task_name = "setup_task"
        expected_task_ctx = {}
        self.assert_next_task(conductor, task_name, expected_task_ctx)
        self.forward_task_statuses(conductor, task_name, [statuses.RUNNING, statuses.SUCCEEDED])

        # Process task_cpu.
        task_name = "task_cpu"
        expected_task_ctx = {}
        self.assert_next_task(conductor, task_name, expected_task_ctx)
        self.forward_task_statuses(conductor, task_name, [statuses.RUNNING, statuses.SUCCEEDED])

        self.assertEqual(conductor.get_workflow_status(), statuses.SUCCEEDED)

