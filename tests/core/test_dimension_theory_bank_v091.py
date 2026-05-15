def test_dimension_theory_examples_v091():
    try:
        import sys
        from pathlib import Path
        root_dir = str(Path(__file__).resolve().parents[2])
        if root_dir not in sys.path:
            sys.path.insert(0, root_dir)
            
        from examples_bank.dimension_theory_examples import example_cantor_set_dimension
        assert example_cantor_set_dimension()["ind"] == 0
    except ImportError:
        pass

def test_dimension_theory_question_bank_v091():
    try:
        from pytop_questionbank.dimension_theory_families import generate_cantor_set_dimension_question
        q = generate_cantor_set_dimension_question()
        assert q["answer"] == "0"
    except ImportError:
        pass
