import unittest
import os
from task_manager import TaskManager

class TestTaskManagerAdvanced(unittest.TestCase):

    def setUp(self):
        """Har test case se pehle naya TaskManager instance create hoga"""
        self.manager = TaskManager()

    def tearDown(self):
        """Test khatam hone ke baad agar backup file bani ho to use delete kar dega"""
        if os.path.exists("tasks.dat"):
            os.remove("tasks.dat")


    # ==========================================
    # PHASE 1: TESTING ADD TASK FUNCTIONALITY
    # ==========================================

    def test_add_task_success(self):
        """TC_01: Positive Test - Sahi data ke sath task successfully add hona chahiye"""
        self.manager.add_task("Complete SQE Assignment", "High", "20-05-2026")
        
        # Check karein ke list mein 1 task add hua ya nahi
        self.assertEqual(len(self.manager.tasks), 1)
        # Check karein ke data sahi save hua ya nahi
        self.assertEqual(self.manager.tasks[0]["title"], "Complete SQE Assignment")
        self.assertEqual(self.manager.tasks[0]["priority"], "High")

    def test_add_task_empty_title_bug(self):
        """TC_02: Negative Test (Bug Catching) - Empty title block hona chahiye"""
        # Bug Hunt: Humne code mein empty title ka check nahi lagaya, to yeh task add ho jayega
        self.manager.add_task("", "Medium", "25-05-2026")
        
        # Agar aapka validation code sahi hota, to len 0 honi chahiye thi. 
        # Lekin kyunke code mein BUG hai, yeh test pass ho jayega aur dikhayeay ga ke empty title bhi accept ho raha hai.
        self.assertEqual(len(self.manager.tasks), 1) 


    # ==========================================
    # PHASE 2: TESTING FILTER FUNCTIONALITY
    # ==========================================

    def test_view_tasks_filtering(self):
        """TC_03: Positive Test - Priority ke mutabik tasks filter hone chahiye"""
        self.manager.add_task("Task 1", "High", "18-05-2026")
        self.manager.add_task("Task 2", "Low", "19-05-2026")
        self.manager.add_task("Task 3", "High", "20-05-2026")

        # Hum main code ke view_tasks ko manually test karte hain loop chala kar
        high_priority_tasks = [t for t in self.manager.tasks if t["priority"].lower() == "high"]
        
        # Check karein ke sirf 2 tasks High priority wale hain
        self.assertEqual(len(high_priority_tasks), 2)


    # ==========================================
    # PHASE 3: TESTING UPDATE FUNCTIONALITY
    # ==========================================

    def test_update_status_success(self):
        """TC_04: Positive Test - Valid ID ke sath status update hona chahiye"""
        self.manager.add_task("Learn SonarQube", "Medium", "22-05-2026")
        
        # Task ID 1 ka status change karein
        self.manager.update_status(1, "In-Progress")
        
        # Check karein ke status change hua ya nahi
        self.assertEqual(self.manager.tasks[0]["status"], "In-Progress")

    def test_update_status_invalid_id_crash_bug(self):
        """TC_05: Negative Test (Bug Catching) - String ID dene par system crash ka check"""
        self.manager.add_task("Learn Snyk", "High", "23-05-2026")
        
        # Bug Hunt: Agar user input mein 'abc' de de numerical ID ki jagah, 
        # to hamara code int('abc') karne ki koshish karega aur ValueError throw karega.
        # Yeh assert raises check karega ke system crash (ValueError) hota hai ya nahi.
        with self.assertRaises(ValueError):
            self.manager.update_status("abc", "Completed")


    # ==========================================
    # PHASE 4: TESTING FILE HANDLING / SECURITY
    # ==========================================

    def test_save_data_creates_file(self):
        """TC_06: Positive Test - Backup save karne par file create honi chahiye"""
        self.manager.add_task("GitHub Push", "Low", "24-05-2026")
        self.manager.save_data_insecurely("tasks.dat")
        
        # Check karein ke file physical storage mein bani ya nahi
        self.assertTrue(os.path.exists("tasks.dat"))

if __name__ == '__main__':
    unittest.main()