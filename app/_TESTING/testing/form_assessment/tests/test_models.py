import unittest

from ..score_models import QualityReviewScore


class QualityReviewScoreTest(unittest.TestCase):
    def setUp(self):
        self.score = QualityReviewScore()

    def test_summary_score(self):
        self.score.accreditation_score = 10
        self.score.company_change = 10
        self.score.accreditation_change = 10
        self.score.attachments = 10
        self.assertEqual(self.score.summary_score(), 40)

    def test_rate_score_poor(self):
        self.score.accreditation_score = -10
        self.score.company_change = -10
        self.score.accreditation_change = -10
        self.score.attachments = -10
        self.assertEqual(self.score.rate_score(), "Poor")

    def test_rate_score_ok(self):
        self.score.accreditation_score = -5
        self.score.company_change = -5
        self.score.accreditation_change = -5
        self.score.attachments = -5
        self.assertEqual(self.score.rate_score(), "OK")

    def test_rate_score_ok(self):
        self.score.accreditation_score = -1
        self.score.company_change = 1
        self.score.accreditation_change = -1
        self.score.attachments = 1
        self.assertEqual(self.score.rate_score(), "Good")

    def test_get_comments_html(self):
        self.score.company_change_comment = "Company Change Comment"
        self.score.accreditation_change_comment = "Accreditation Change Comment"
        self.score.attachments_comment = "Attachment Comment"
        self.assertEqual(
            self.score.get_comments_html(),
            "<br>Company Change Comment<br>Accreditation Change Comment<br>Attachment Comment",
        )

    def test_compare_accreditations_html(self):
        self.score.company_accreditations = ["a", "c", "d"]
        self.score.expected_accreditations = ["a", "b", "c", "d", "e"]
        self.assertEqual(self.score.compare_accreditations_html(), "<br>b<br>e")

    def test_generate_assessment_document_html(self):
        # Might be a pain/unnecessary - consider
        pass
