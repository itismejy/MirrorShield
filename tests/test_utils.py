import pytest
from utils import build_chat_prompt, parse_response

def test_build_chat_prompt_english():
    prompt = build_chat_prompt("Hello", ["Gaslighting", "Love bombing"], "English")
    assert "Gaslighting, Love bombing" in prompt
    assert "User: Hello" in prompt


def test_build_chat_prompt_chinese():
    prompt = build_chat_prompt("你好", ["煤气灯效应", "爱轰炸"], "中文")
    assert "你正在模拟具有自恋型人格障碍特征的人" in prompt
    assert "用户: 你好" in prompt


def test_parse_response_full():
    text = "Reply: Hi there!\nTactic: Gaslighting"
    reply, tactic = parse_response(text)
    assert reply == "Hi there!"
    assert tactic == "Gaslighting"


def test_parse_response_no_tactic():
    text = "Just some reply without tactic"
    reply, tactic = parse_response(text)
    assert reply == "Just some reply without tactic"
    assert tactic == ""

@pytest.mark.parametrize("lines, expected_reply, expected_tactic", [
    (["Reply:Line1", "Some other line", "Tactic: Love bombing"], "Line1", "Love bombing"),
    (["Random text", "reply: Lowercase test", "TACTIC: Blame-shifting"], "Lowercase test", "Blame-shifting"),
])

def test_parse_response_varied(lines, expected_reply, expected_tactic):
    text = "\n".join(lines)
    reply, tactic = parse_response(text)
    assert reply == expected_reply
    assert tactic == expected_tactic
