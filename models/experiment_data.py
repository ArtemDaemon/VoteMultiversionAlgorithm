class ExperimentData:
    def __init__(self, version_name, version_answer, correct_answer):
        """
        Initialize an ExperimentData object with the given version name, version answer, and correct answer.

        :param version_name: The name of the version.
        :param version_answer: The answer provided by this version.
        :param correct_answer: The correct answer for the experiment.
        """
        self.version_name = version_name
        self.version_answer = version_answer
        self.correct_answer = correct_answer
