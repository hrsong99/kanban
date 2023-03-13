# import requirements (i.e. unittest and everything from app.py)
import unittest
from app import *

# create class for testing the functions of the table
class TestTable(unittest.TestCase):
    """
    Test the functions of the table
    """
    def test_add_task(self):
        # use app_context so that the database can be accessed and used
        with app.app_context():
            """
            Test that you can add a task to the tasks table
            """
            # create a new task called "Test Task" in the "Todo" column, then add and commit
            new_task = Tasks(content="Test Task", column="Todo")
            db.session.add(new_task)
            db.session.commit()
            # assert True that a task with the id of the new_task created above exists in the Tasks table
            self.assertTrue(Tasks.query.where(Tasks.id==new_task.id).all())
    def test_move_task(self):
        with app.app_context():
            """
            Test that you can move a task from Todo to Doing
            """
            # query the Tasks table for a task with "Test Task" content in the "Todo" column, and get the first one
            task = Tasks.query.where(Tasks.content=="Test Task" and Tasks.column=="Todo").first()
            move_doing(task.id) # run the function that moves a task to the Doing column
            # assert True that the task queried above is now in the "Doing" column (found by using its unique id)
            self.assertTrue(Tasks.query.where(Tasks.id==task.id and Tasks.column=="Doing").all())
    def test_delete_task(self):
        with app.app_context():
            """
            Test that you can delete a task
            """
            # query the Tasks table for a task with "Test Task" content in the "Doing" column, and get the first one
            task = Tasks.query.where(Tasks.content=="Test Task" and Tasks.column=="Doing").first()
            # delete the task and commit
            db.session.delete(task)
            db.session.commit()
            # assert False that the task with the unique id exists in the Tasks table
            self.assertFalse(Tasks.query.where(Tasks.id==task.id).all())
    
#For some reason, the test does not go in order and deletes the file first before moving it. 
# If they are run in order individually, there should not be any errors.

if __name__ == '__main__':
    unittest.main()