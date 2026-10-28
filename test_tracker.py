import unittest

from tracker import pull_shark_progress


class PullSharkProgressTests(unittest.TestCase):
    milestones = [2, 16, 128, 1024]

    def test_every_milestone_boundary(self):
        for index, target in enumerate(self.milestones):
            with self.subTest(target=target):
                before = pull_shark_progress(target - 1, self.milestones)
                self.assertEqual((before["next"], before["remaining"]), (target, 1))
                at = pull_shark_progress(target, self.milestones)
                self.assertEqual(at["reached"], target)
                following = self.milestones[index + 1:index + 2]
                self.assertEqual(at["next"], following[0] if following else None)

    def test_new_account(self):
        self.assertEqual(pull_shark_progress(0, self.milestones),
                         {"merged": 0, "reached": 0, "next": 2, "remaining": 2})

    def test_above_highest_milestone(self):
        self.assertEqual(pull_shark_progress(2000, self.milestones),
                         {"merged": 2000, "reached": 1024, "next": None, "remaining": 0})

    def test_negative_count_is_rejected(self):
        with self.assertRaises(ValueError):
            pull_shark_progress(-1, self.milestones)


if __name__ == "__main__":
    unittest.main()
