from unittest import TestCase

from code_writer_flow import CodeWriterFlow


class TestCodeWriterFlow(TestCase):
    def test_code_writer_flow(self):
        print("Testing code writing prompt")
        your_flow = CodeWriterFlow()
        result_of_flow = your_flow.kickoff(
            {
                "user_query": "Write a python function to find the Greatest Common divisor"
            }
        )

        print(result_of_flow)

    def test_file_analyser(self):
        print("Testing file analysis")
        your_flow = CodeWriterFlow()
        result_of_flow = your_flow.kickoff(
            {"user_query": "Analyse the file at ./analyser_test.py"}
        )

        print(result_of_flow)

    def test_other_flow(self):
        print("Testing code writing prompt")
        your_flow = CodeWriterFlow()
        # print(your_flow.state)
        result_of_flow = your_flow.kickoff(
            {"user_query": "Where is Rio de janiero located"}
        )

        print(result_of_flow)
