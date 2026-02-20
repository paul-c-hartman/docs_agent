from docs_agent.helpers.filesize import filesize_to_english

def test_filesize_to_english():
    assert filesize_to_english(0) == "0.0 B"
    assert filesize_to_english(512) == "512.0 B"
    assert filesize_to_english(1024) == "1.0 KB"
    assert filesize_to_english(1536) == "1.5 KB"
    assert filesize_to_english(1048576) == "1.0 MB"
    assert filesize_to_english(1073741824) == "1.0 GB"
    assert filesize_to_english(1099511627776) == "1.0 TB"
    assert filesize_to_english(None) == "N/A"