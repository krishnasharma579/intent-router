from test_router import TEST_QUERIES, run_tests


def test_run_tests_success_path():
    def fake_classifier(_: str) -> str:
        return "general_chat"

    successful = run_tests(fake_classifier)

    assert successful == len(TEST_QUERIES)


def test_run_tests_handles_expected_errors():
    def fake_classifier(_: str) -> str:
        raise RuntimeError("mock failure")

    successful = run_tests(fake_classifier)

    assert successful == 0
