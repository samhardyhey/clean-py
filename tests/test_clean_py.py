from clean_py.clean_py import clean_python_code


def test_clean_source_apply_all(black_playground_template_input, apply_all):
    res = clean_python_code(black_playground_template_input)
    assert res == apply_all


def test_clean_source_apply_black(black_playground_template_input, black_only):
    res = clean_python_code(
        black_playground_template_input, isort=False, black=True, autoflake=False
    )
    assert res == black_only


# def test_clean_source_apply_isort(black_playground_template_input, isort_only):
#     res = clean_python_code(black_playground_template_input, isort=True, black=False, autoflake=False)
#     assert res == isort_only


def test_clean_source_apply_autoflake(black_playground_template_input, autoflake_only):
    res = clean_python_code(
        black_playground_template_input, isort=False, black=False, autoflake=True
    )
    assert res == autoflake_only
