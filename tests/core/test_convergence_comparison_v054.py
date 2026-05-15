from pytop import (
    ConvergenceComparisonRow,
    convergence_comparison_row,
    convergence_comparison_table,
    render_convergence_comparison_table,
)


def test_convergence_comparison_table_has_three_standard_rows():
    rows = convergence_comparison_table()
    assert len(rows) == 3
    assert all(isinstance(row, ConvergenceComparisonRow) for row in rows)
    assert [row.key for row in rows] == ["sequence", "net", "filter"]


def test_convergence_comparison_rows_record_public_helpers():
    sequence = convergence_comparison_row("seq")
    net = convergence_comparison_row("nets")
    filtr = convergence_comparison_row("süzgeç")

    assert "sequence_converges_to" in sequence.pytop_helpers
    assert "net_converges_to" in net.pytop_helpers
    assert "filter_converges_to" in filtr.pytop_helpers
    assert "is_finer_filter" in filtr.pytop_helpers


def test_render_convergence_comparison_table_is_markdown():
    rendered = render_convergence_comparison_table()
    assert "| Tool |" in rendered
    assert "Sequences" in rendered
    assert "Nets" in rendered
    assert "Filters" in rendered
    assert "`analyze_filter`" in rendered


def test_unknown_convergence_comparison_key_raises_keyerror():
    try:
        convergence_comparison_row("ultranet")
    except KeyError as exc:
        assert "ultranet" in str(exc)
    else:  # pragma: no cover
        raise AssertionError("Expected KeyError")
