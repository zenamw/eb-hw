"""
test_verify.py
"""
from verify import verify
from configs import App_Configs

class Test_Verify:

    def test_bearer_not_in_token(self, monkeypatch):
        # Arrange
        token = 'not-using-right-token'
        monkeypatch.setattr(App_Configs, 'authorization', 'ER5Q6zlKkf')

        # Act
        actual = verify(token)

        # Assert
        assert actual == False

    def test_token_is_none(self, monkeypatch):
        # Arrange
        token = None
        monkeypatch.setattr(App_Configs, 'authorization', 'ER5Q6zlKkf')

        # Act
        actual = verify(token)

        # Assert
        assert actual == False

    def test_auth_is_incorrect(self, monkeypatch):
        # Arrange
        token = 'Bearer:incorrect-pass'
        monkeypatch.setattr(App_Configs, 'authorization', 'ER5Q6zlKkf')
        
        # Act
        actual = verify(token)

        # Assert
        assert actual == False
    
    def test_auth_is_correct(self, monkeypatch):
        # Arrange
        token = 'Bearer:ER5Q6zlKkf'
        monkeypatch.setattr(App_Configs, 'authorization', 'ER5Q6zlKkf')

        # Act
        actual = verify(token)

        # Assert
        assert actual == True