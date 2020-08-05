from orquesta import conducting
from orquesta.specs import native as native_specs
from orquesta import statuses
from orquesta.tests.unit import base as test_base


class WorkflowConductorExtendedTaskTest(test_base.WorkflowConductorTest):
    def test_task(self):
        wf_def = """
        version: 1.0
        
        vars:
          - var_cpu: null
          - var_res_cpu: null
          

        tasks:
           
          task_cpu:
            action: core.local cmd="mpstat | awk '$3 ~ /CPU/ { for(i=1;i<=NF;i++) { if ($i ~ /%idle/) field=i } } $3 ~ /all/ { printf(100 - $field) }'"
            next:
                - when: <% succeeded() %>
                  do:
                    - post_cpu_success_to_slack
         
          post_cpu_success_to_slack :
            action: chatops.post_message
            input:
              channel: 'mychannel'
              message: "cpu is under_utilized on localhost."
            next:
              - publish:
                  - task1_status: <% task_status(task_cpu) %>
                  - task2_status: <% task_status(post_cpu_success_to_slack) %>
                  
        output:
          - task1_status: <% ctx(task1_status) %>
          - task2_status: <% ctx(task2_status) %>
          
        
        """
        
        expected_errors = []
        expected_output = {
            "task1_status": "succeeded",
            "task2_status": "succeeded",
            
        }
     
        spec = native_specs.WorkflowSpec(wf_def)
        conductor = conducting.WorkflowConductor(spec)
        conductor.request_workflow_status(statuses.RUNNING)
        self.assertEqual(conductor.get_workflow_status(), statuses.RUNNING)
        self.assertListEqual(conductor.errors, expected_errors)
       

        # Process task1.
        task_name = "task_cpu"
        self.forward_task_statuses(conductor, task_name, [statuses.RUNNING, statuses.SUCCEEDED])

        # Process task2.
        task_name = "post_cpu_success_to_slack"
        self.forward_task_statuses(conductor, task_name, [statuses.RUNNING, statuses.SUCCEEDED])
        
       

        conductor.render_workflow_output()
        self.assertEqual(conductor.get_workflow_status(), statuses.SUCCEEDED)
        self.assertListEqual(conductor.errors, expected_errors)
        self.assertDictEqual(conductor.get_workflow_output(), expected_output)


       
