from .config import conf


class QualityReviewScore:
    def __init__(self):
        self.company_name = ""
        self.company_type = ""
        self.company_accreditations = ""
        self.expected_accreditations = ""
        self.accreditation_score = 0
        self.company_change = 0
        self.company_change_details = ""
        self.accreditation_change = 0
        self.accreditation_change_details = ""
        self.attachments = 0
        self.attachments_names = []
        self.company_change_comment = ""
        self.accreditation_change_comment = ""
        self.attachments_comment = ""
        self.supplier_comments = ""
        self.actions = []
        self.lower_score_threshold = conf["scoring"]["quality"]["score_thresholds"][
            "lower_score_threshold"
        ]
        self.upper_score_threshold = conf["scoring"]["quality"]["score_thresholds"][
            "upper_score_threshold"
        ]
        self.top_rating = conf["scoring"]["quality"]["ratings"]["top"]
        self.middle_rating = conf["scoring"]["quality"]["ratings"]["middle"]
        self.bottom_rating = conf["scoring"]["quality"]["ratings"]["bottom"]

    def summary_score(self):
        total_score = (
            self.accreditation_score
            + self.company_change
            + self.accreditation_change
            + self.attachments
        )
        return total_score

    def rate_score(self):
        total_score = self.summary_score()
        rating = ""
        if total_score <= self.lower_score_threshold:
            rating = self.bottom_rating
        elif self.lower_score_threshold < total_score < self.upper_score_threshold:
            rating = self.middle_rating
        elif total_score >= self.upper_score_threshold:
            rating = self.top_rating
        return rating

    def get_comments(self):
        comments = ""
        comment_list = [
            self.company_change_comment,
            self.accreditation_change_comment,
            self.attachments_comment,
        ]
        for c in comment_list:
            comments += f"\n{c}"
        return comments

    def get_comments_html(self):
        comments = ""
        comment_list = [
            self.company_change_comment,
            self.accreditation_change_comment,
            self.attachments_comment,
        ]
        for c in comment_list:
            comments += f"\n{c}"
        return comments

    def compare_accreditations(self):
        held_set = set(self.company_accreditations)
        expected_set = set(self.expected_accreditations)
        accreditation_difference = expected_set.difference(held_set)
        r_str = ""
        for i in accreditation_difference:
            self.accreditation_score = self.accreditation_score - 10
            r_str += f"\n{str(i)}"
        return r_str

    def compare_accreditations_html(self):
        held_set = set(self.company_accreditations)
        expected_set = set(self.expected_accreditations)
        accreditation_difference = expected_set.difference(held_set)
        r_str = ""
        for i in accreditation_difference:
            self.accreditation_score = self.accreditation_score - 10
            r_str += f"\n{str(i)}"
        return r_str

    def missing_accreditations(self):
        missing = self.compare_accreditations_html()
        return missing

    def held_accreditation_string(self):
        held_accreditations = "<br>"
        if len(self.company_accreditations) != 0:
            for a in self.company_accreditations:
                held_accreditations += f"{a}\n"
        else:
            held_accreditations += "None.\n"
        return held_accreditations

    def expected_accreditation_string(self):
        if len(self.expected_accreditations) != 0:
            expected_accreditations = "\n"
            for b in self.expected_accreditations:
                expected_accreditations += f"{b}\n"
        else:
            expected_accreditations = "None."
        return expected_accreditations

    def attachments_string(self):
        attachments = ""
        if len(self.attachments_names) != 0:
            for c in self.attachments_names:
                attachments += f"{c}\n"
        else:
            pass
        return attachments

    def action_string(self):
        if len(self.actions) != 0:
            i = 1
            to_action = "\n"
            for d in self.actions:
                to_action += f"Action {i} - {str(d)}\n"
                i = i + 1
        else:
            to_action = "\nNo Actions."
        return to_action

    def generate_review_dict(self):
        missing = self.missing_accreditations()
        score = self.summary_score()
        rating = self.rate_score()
        comments = self.get_comments_html()
        held_accreditations = self.held_accreditation_string()
        expected_accreditations = self.expected_accreditation_string()
        review_dict = {
            "company_name": self.company_name,
            "company_type": self.company_type,
            "company_change_comment": self.company_change_comment,
            "company_change_details": self.company_change_details,
            "accreditation_change_comment": self.accreditation_change_comment,
            "accreditation_change_details": self.accreditation_change_details,
            "attachments_comment": self.attachments_comment,
            "supplier_comments": self.supplier_comments,
            "missing": missing,
            "score": score,
            "rating": rating,
            "comments": comments,
            "held_accreditations": held_accreditations,
            "expected_accreditations": expected_accreditations,
            "attachments": self.attachments,
            "to_action": self.actions,
        }

        return review_dict


class BusinessReviewScore:
    def __init__(self):
        self.company_name = ""
        self.company_type = ""
        self.company_accreditation = ""
        self.company_change = 0
        self.company_change_details = ""
        self.attachments = 0
        self.attachments_names = ""
        self.company_change_comment = ""
        self.attachments_comment = ""
        self.supplier_comments = ""

    def summary_score(self):
        total_score = self.company_change + self.attachments
        return total_score

    def rate_score(self):
        total_score = self.company_change + self.attachments
        rating = ""
        if total_score <= -10:
            rating = "Poor"
        elif -10 < total_score < 10:
            rating = "OK"
        elif total_score >= 10:
            rating = "Good"
        return rating

    def get_comments_html(self):
        comments = ""
        comment_list = [self.company_change_comment, self.attachments_comment]
        for c in comment_list:
            comments += f"<br>{c}"
        return comments

    def generate_review_dict(self):
        missing = self.missing_accreditations()
        score = self.summary_score()
        rating = self.rate_score()
        comments = self.get_comments_html()
        held_accreditations = self.held_accreditation_string()
        expected_accreditations = self.expected_accreditation_string()
        review_dict = {
            "company_name": self.company_name,
            "company_type": self.company_type,
            "company_change_comment": self.company_change_comment,
            "company_change_details": self.company_change_details,
            "accreditation_change_comment": self.accreditation_change_comment,
            "accreditation_change_details": self.accreditation_change_details,
            "attachments_comment": self.attachments_comment,
            "supplier_comments": self.supplier_comments,
            "missing": missing,
            "score": score,
            "rating": rating,
            "comments": comments,
            "held_accreditations": held_accreditations,
            "expected_accreditations": expected_accreditations,
            "attachments": self.attachments,
            "to_action": self.actions,
        }

        return review_dict


class OtherReviewScore:
    def __init__(self):
        self.company_name = ""
        self.company_type = ""
        self.company_accreditations = ""
        self.company_change = 0
        self.company_change_details = ""
        self.attachments = 0
        self.attachments_names = ""
        self.company_change_comment = ""
        self.attachments_comment = ""
        self.supplier_comments = ""

    def summary_score(self):
        total_score = self.company_change + self.attachments
        return total_score

    def rate_score(self):
        total_score = self.company_change + self.attachments
        rating = ""
        if total_score <= -10:
            rating = "Poor"
        elif -10 < total_score < 10:
            rating = "OK"
        elif total_score >= 10:
            rating = "Good"
        return rating

    def get_comments_html(self):
        comments = ""
        comment_list = [self.company_change_comment, self.attachments_comment]
        for c in comment_list:
            comments += f"\n{c}"
        return comments

    def generate_review_dict(self):
        missing = self.missing_accreditations()
        score = self.summary_score()
        rating = self.rate_score()
        comments = self.get_comments_html()
        held_accreditations = self.held_accreditation_string()
        expected_accreditations = self.expected_accreditation_string()
        review_dict = {
            "company_name": self.company_name,
            "company_type": self.company_type,
            "company_change_comment": self.company_change_comment,
            "company_change_details": self.company_change_details,
            "accreditation_change_comment": self.accreditation_change_comment,
            "accreditation_change_details": self.accreditation_change_details,
            "attachments_comment": self.attachments_comment,
            "supplier_comments": self.supplier_comments,
            "missing": missing,
            "score": score,
            "rating": rating,
            "comments": comments,
            "held_accreditations": held_accreditations,
            "expected_accreditations": expected_accreditations,
            "attachments": self.attachments,
            "to_action": self.actions,
        }

        return review_dict
