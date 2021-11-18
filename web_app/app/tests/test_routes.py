"""
test_routes.py

For testing the routes of the app
"""

import pytest
import json
import pandas as pd

from fixtures import client

def test_health_check_returns_ok(client):
    # Arrange

    # Act
    response = client.get('/health-check')

    # Assert
    print('Data:', response.data)
    print('Status_Code', response.status_code)
    assert response.data == b'OK'
    
    assert response.status_code == 200
class Test_Get_All_Data:

    def test_when_auth_correct(self, client):
        # Arrange
        
        # Act
        response = client.get('/get_all_data',
                            headers = {'Authorization': 'Bearer:ER5Q6zlKkf'})

        data = pd.DataFrame(json.loads(response.data))

        # Assert
        print('Data:', data)
        print('Status_Code', response.status_code)
        print(data.columns.to_list())
        assert data.columns.to_list() ==  ['index',
                                'Origin_airport',
                                'Destination_airport',
                                'Origin_city',
                                'Destination_city',
                                'Passengers',
                                'Seats',
                                'Flights',
                                'Distance',
                                'Fly_date',
                                'Origin_population',
                                'Destination_population',
                                'Org_airport_lat',
                                'Org_airport_long',
                                'Dest_airport_lat',
                                'Dest_airport_long']

        assert data.shape[0] == 100
        assert response.status_code == 200

    def test_when_auth_incorrect(self, client):
        # Arrange

        # Act
        response = client.get('/get_all_data',
                            headers = {'Authorization': 'wrong-auth'})
 
        # Assert
        print('Status_Code:', response.status_code)
        print('Data:', response.data)

        assert response.status_code == 400
        assert response.data == b'Do not have the correct auth token'

class Test_Get_Airport_Data:

    def test_auth_incorrect(self, client):
        # Arrange

        # Act
        response = client.post('/get_origin_airport_data',
                            headers = {'Authorization': 'wrong-auth'},
                            data = json.dumps({'params':{}}))
 
        # Assert
        print('Status_Code:', response.status_code)
        print('Data:', response.data)

        assert response.status_code == 400
        assert response.data == b'Do not have the correct auth token'

    def test_airport_not_in_params(self, client):
        # Arrange

        # Act
        response = client.post('/get_origin_airport_data',
                            headers = {'Authorization': 'Bearer:ER5Q6zlKkf'},
                            data = json.dumps({'params':{'not-airport':'not a param'}}))
 
        # Assert
        print('Status_Code:', response.status_code)
        print('Data:', response.data)

        assert response.status_code == 400
        assert response.data == b'Missing arguement: airport'

    def test_airport_in_params(self, client):
        # Arrange

        # Act
        response = client.post('/get_origin_airport_data',
                            headers = {'Authorization': 'Bearer:ER5Q6zlKkf'},
                            data = json.dumps({'airport':'EUG'}))

        data = pd.DataFrame(json.loads(response.data))
    
        # Assert
        print('Data:', data.columns)
        print('Status_Code', response.status_code)

        assert data.columns.to_list() ==  ['index',
                                'Origin_airport',
                                'Destination_airport',
                                'Origin_city',
                                'Destination_city',
                                'Passengers',
                                'Seats',
                                'Flights',
                                'Distance',
                                'Fly_date',
                                'Origin_population',
                                'Destination_population',
                                'Org_airport_lat',
                                'Org_airport_long',
                                'Dest_airport_lat',
                                'Dest_airport_long']

        assert data.shape[0] > 0
        assert response.status_code == 200

