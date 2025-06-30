import json
import pytest
from utilities import ApiUtils

class TestAPIOperations:

    @pytest.mark.regression
    def test_get_user(self):
        response, status_code = ApiUtils.get_user(1, return_status=True)
        assert status_code == 200
        assert response["id"] == 1
        assert "firstName" in response
        assert "lastName" in response

    @pytest.mark.regression
    def test_add_user(self):
        # create user using below loaded data
        with open("Testdata/api/adduser.json") as adduser_file:
            self.create_user_test_data = json.load(adduser_file)
        response, status_code = ApiUtils.create_user(self.create_user_test_data, return_status=True)
        print(f"[DEBUG] User creation response: {response}")
        assert status_code in [200, 201]
        assert "firstName" in response
        assert response["firstName"] == self.create_user_test_data["firstName"]
        self.created_user_id = response.get("id")
        if not self.created_user_id:
            raise Exception(f"[ERROR] User creation failed with an error: {response}")

    @pytest.mark.regression
    def test_update_user(self):
        # update user using below loaded data
        with open("Testdata/api/updateuser.json") as updateuser_file:
            self.update_user_test_data = json.load(updateuser_file)
        response, status_code = ApiUtils.update_user(2, self.update_user_test_data, return_status=True)
        print(f"[DEBUG] User update response: {response}")
        assert status_code == 200
        assert response["id"] == 2
        assert "firstName" in response
        assert response["firstName"] == self.update_user_test_data["firstName"]
        assert "lastName" in response
        assert response["lastName"] == self.update_user_test_data["lastName"]

    @pytest.mark.regression
    def test_delete_user(self):
        response, status_code = ApiUtils.delete_user(1, return_status=True)
        print(f"[DEBUG] User deletion response: {response}")
        assert status_code == 200
        assert response["id"] == 1
        assert "firstName" in response
        assert "lastName" in response