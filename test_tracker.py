import unittest

from tracker import live_snapshot, parse_achievements, pull_shark_progress


class ProfileParserTests(unittest.TestCase):
    def test_deduplicates_desktop_and_mobile_badges(self):
        badge = '<img alt="Achievement: Pull Shark" src="pull-shark-bronze.png">'
        self.assertEqual(parse_achievements(badge * 2),
                         [{"name": "Pull Shark", "image_url": "pull-shark-bronze.png"}])

    def test_ignores_other_images_text_and_empty_names(self):
        html = ('<img alt="Avatar" src="avatar.png">Achievement: YOLO'
                '<div alt="Achievement: Fake"></div><img alt="Achievement: ">')
        self.assertEqual(parse_achievements(html), [])

    def test_tolerates_missing_image_url(self):
        self.assertEqual(parse_achievements('<img alt="Achievement: YOLO">'),
                         [{"name": "YOLO", "image_url": ""}])

    def test_invalid_username_is_rejected_before_network_access(self):
        for user in ("", "../other", "--help", "a b", "a" * 40):
            with self.subTest(user=user), self.assertRaises(ValueError):
                live_snapshot(user)


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
