from inference_lab.quality import score

def test_qa(): assert score("qa", "Paris", "Paris") == 1
def test_json():
    assert score("structured_extraction", '{"customer":"Acme","amount":1250}', {"customer":"Acme","amount":1250}) == 1
def test_invalid_json(): assert score("structured_extraction", "not json", {"x":1}) == 0

