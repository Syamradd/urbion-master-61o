from urbion_gemini_redteam import build_redteam_prompt


def test_gemini_prompt_scrubs_secret_like_fields_recursively():
    prompt = build_redteam_prompt(
        {
            "api_key": "TOP-SECRET",
            "nested": {
                "gemini_api_key": "TOP-SECRET-2",
                "safe": "kept",
                "items": [{"authorization": "Bearer SECRET"}, {"value": "ok"}],
            },
        }
    )
    assert "TOP-SECRET" not in prompt
    assert "TOP-SECRET-2" not in prompt
    assert "Bearer SECRET" not in prompt
    assert '"safe":"kept"' in prompt
    assert '"value":"ok"' in prompt
