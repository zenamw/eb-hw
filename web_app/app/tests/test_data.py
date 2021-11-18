"""
test_data.py
"""
import pytest
import sys
import logging 
from sqlalchemy import create_engine

from configs import App_Configs
from data import PG_Data


class Test_Get_Connection:

    def test_engine_connects(self, monkeypatch):
        # Arrange
        monkeypatch.setattr(App_Configs, 'pg_user', 'postgres')
        monkeypatch.setattr(App_Configs, 'pg_pass', 'aserverfortheages!')
        monkeypatch.setattr(App_Configs, 'pg_host', 'database-2.cc9fdxmr2mkl.us-west-2.rds.amazonaws.com')
        monkeypatch.setattr(App_Configs, 'pg_port', '5432')
        monkeypatch.setattr(App_Configs, 'pg_db', 'airport')


        # Act
        sut = PG_Data()
        actual = sut._PG_Data__get_engine()

        # Assert
        print(str(type(actual)))

        assert str(type(actual)) == "<class 'sqlalchemy.engine.base.Engine'>"

    def test_engine_does_not_connect(self, monkeypatch, capsys):
        # Arrange
        monkeypatch.setattr(App_Configs, 'pg_host', 'fake_host')

        # Act
        sut = PG_Data()
        with pytest.raises(Exception):
            sut._PG_Data__get_engine()

        captured = capsys.readouterr()
        # Assert
        assert captured.out == "Unable to make engine connect to Postgres\n"

class Test_Close_Engine:    

    def test_engine_is_none(self, capsys):
        # Arrange

        engine = None

        # Act
        sut = PG_Data()
        sut._PG_Data__close_engine(engine)

        captured = capsys.readouterr()

        # Assert
        assert captured.out == ''

    def test_engine_is_disposed(self, monkeypatch, capsys):
        # Arrange
        monkeypatch.setattr(App_Configs, 'pg_user', 'postgres')
        monkeypatch.setattr(App_Configs, 'pg_pass', 'aserverfortheages!')
        monkeypatch.setattr(App_Configs, 'pg_host', 'database-2.cc9fdxmr2mkl.us-west-2.rds.amazonaws.com')
        monkeypatch.setattr(App_Configs, 'pg_port', '5432')
        monkeypatch.setattr(App_Configs, 'pg_db', 'airport')

        engine =  create_engine('postgresql://{user}:{password}@{host}:{port}/{db}'.format(user = App_Configs.pg_user,
                                                                                  password = App_Configs.pg_pass,
                                                                                  host = App_Configs.pg_host,
                                                                                  port = App_Configs.pg_port,
                                                                                  db = App_Configs.pg_db))

        engine.connect()

        # Act
        sut = PG_Data()
        actual = sut._PG_Data__close_engine(engine)

        captured = capsys.readouterr()

        # Assert
        assert captured.out == 'disposing engine\n'


class Test_Get_All_Data:

    def test_airline_data_is_collected(self, monkeypatch):
        # Arrange
        monkeypatch.setattr(App_Configs, 'pg_user', 'postgres')
        monkeypatch.setattr(App_Configs, 'pg_pass', 'aserverfortheages!')
        monkeypatch.setattr(App_Configs, 'pg_host', 'database-2.cc9fdxmr2mkl.us-west-2.rds.amazonaws.com')
        monkeypatch.setattr(App_Configs, 'pg_port', '5432')
        monkeypatch.setattr(App_Configs, 'pg_db', 'airport')

        # Act
        sut = PG_Data()
        actual = sut.get_all_data()

        # Assert
        assert actual.columns.to_list() == ['index',
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

        assert actual.shape[0] == 100
    
    def test_airline_data_not_collected(self, monkeypatch, capsys):
        # Arrange
        monkeypatch.setattr(App_Configs, 'pg_db', 'airport')
        monkeypatch.setattr(App_Configs, 'pg_host', 'fake_host')

        # Act
        sut = PG_Data()
        with pytest.raises(Exception):
            sut.get_all_data()

        captured = capsys.readouterr()

        # Assert
        assert captured.out == 'Unable to make engine connect to Postgres\n'

class Test_Get_Airport_Data:

    def test_airline_data_returned(self, monkeypatch):
        # Arrange
        monkeypatch.setattr(App_Configs, 'pg_user', 'postgres')
        monkeypatch.setattr(App_Configs, 'pg_pass', 'aserverfortheages!')
        monkeypatch.setattr(App_Configs, 'pg_host', 'database-2.cc9fdxmr2mkl.us-west-2.rds.amazonaws.com')
        monkeypatch.setattr(App_Configs, 'pg_port', '5432')
        monkeypatch.setattr(App_Configs, 'pg_db', 'airport')

        airport = 'EUG'
        # Act
        sut = PG_Data()
        actual = sut.get_airport_data(airport)

        # Assert
        assert actual.columns.to_list() == ['index',
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
 

        assert actual.shape[0] > 0

    def test_no_data_returned(self, monkeypatch, capsys):
        # Arrange
        monkeypatch.setattr(App_Configs, 'pg_db', 'airport')
        monkeypatch.setattr(App_Configs, 'pg_host', 'fake_host')

        airport = 'EUG'

        # Act
        sut = PG_Data()
        actual = sut.get_airport_data(airport)

        captured = capsys.readouterr()

        # Assert
        assert captured.out == 'Unable to make engine connect to Postgres\nUnable to get data from airport \n'
        assert actual == None