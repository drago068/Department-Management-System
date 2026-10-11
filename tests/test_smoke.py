import os

def test_project_structure():
    assert os.path.exists("frontend/src/modules/student")
    assert os.path.exists("frontend/src/modules/staff")
    assert os.path.exists("frontend/src/modules/admin")
    assert os.path.exists("frontend/src/modules/auth")
    assert os.path.exists("backend/app")
    assert os.path.exists("docs")
