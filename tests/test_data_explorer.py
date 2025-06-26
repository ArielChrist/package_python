import unittest
from unittest.mock import patch, Mock
import pandas as pd
import json
import pytest
from data_explorer.getter import get_worldbank_data, get_export, get_import, get_pib


class TestDataExplorer(unittest.TestCase):
    
    @patch('data_explorer.getter.requests.get')
    def test_get_worldbank_data(self, mock_get):
        # Création d'une réponse simulée
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        
        # Données simulées de l'API World Bank
        mock_data = [
            {"page": 1, "pages": 1, "per_page": 50, "total": 2},
            [
                {
                    "indicator": {"id": "NY.GDP.MKTP.CD", "value": "PIB ($ US courants)"},
                    "country": {"id": "FR", "value": "France"},
                    "countryiso3code": "FRA",
                    "date": "2022",
                    "value": 2782905499081.76,
                    "unit": "",
                    "obs_status": "",
                    "decimal": 0
                },
                {
                    "indicator": {"id": "NY.GDP.MKTP.CD", "value": "PIB ($ US courants)"},
                    "country": {"id": "FR", "value": "France"},
                    "countryiso3code": "FRA",
                    "date": "2021",
                    "value": 2957879759912.54,
                    "unit": "",
                    "obs_status": "",
                    "decimal": 0
                }
            ]
        ]
        
        mock_response.content = json.dumps(mock_data).encode('utf-8')
        mock_get.return_value = mock_response
        
        # Appel de la fonction à tester
        result = get_worldbank_data("FR", "2021", "2022", "NY.GDP.MKTP.CD")
        
        # Vérifications
        mock_get.assert_called_once()
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), 2)
        self.assertIn('country_name', result.columns)
        self.assertIn('indicator_name', result.columns)
        self.assertEqual(result['country_name'].iloc[0], "France")
        self.assertEqual(result['indicator_code'].iloc[0], "NY.GDP.MKTP.CD")
        self.assertEqual(result['value'].iloc[0], 2782905499081.76)
    
    @patch('data_explorer.getter.get_worldbank_data')
    def test_get_export(self, mock_get_worldbank_data):
        # Configuration du mock
        mock_df = pd.DataFrame({'test': [1, 2, 3]})
        mock_get_worldbank_data.return_value = mock_df
        
        # Appel de la fonction à tester
        result = get_export("FR", "2021", "2022")
        
        # Vérifications
        mock_get_worldbank_data.assert_called_once_with("FR", "2021", "2022", "NE.EXP.GNFS.CD")
        self.assertIs(result, mock_df)
    
    @patch('data_explorer.getter.get_worldbank_data')
    def test_get_import(self, mock_get_worldbank_data):
        # Configuration du mock
        mock_df = pd.DataFrame({'test': [1, 2, 3]})
        mock_get_worldbank_data.return_value = mock_df
        
        # Appel de la fonction à tester
        result = get_import("FR", "2021", "2022")
        
        # Vérifications
        mock_get_worldbank_data.assert_called_once_with("FR", "2021", "2022", "NE.IMP.GNFS.CD")
        self.assertIs(result, mock_df)
    
    @patch('data_explorer.getter.get_worldbank_data')
    def test_get_pib(self, mock_get_worldbank_data):
        # Configuration du mock
        mock_df = pd.DataFrame({'test': [1, 2, 3]})
        mock_get_worldbank_data.return_value = mock_df
        
        # Appel de la fonction à tester
        result = get_pib("FR", "2021", "2022")
        
        # Vérifications
        mock_get_worldbank_data.assert_called_once_with("FR", "2021", "2022", "NY.GDP.MKTP.CD")
        self.assertIs(result, mock_df)
    
    @patch('data_explorer.getter.requests.get')
    def test_empty_response(self, mock_get):
        # Création d'une réponse simulée vide
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        
        # Données simulées de l'API World Bank (vides)
        mock_data = [
            {"page": 1, "pages": 1, "per_page": 50, "total": 0},
            []
        ]
        
        mock_response.content = json.dumps(mock_data).encode('utf-8')
        mock_get.return_value = mock_response
        
        # Appel de la fonction à tester
        result = get_worldbank_data("XX", "2021", "2022", "NY.GDP.MKTP.CD")
        
        # Vérifications
        self.assertIsInstance(result, pd.DataFrame)
        self.assertTrue(result.empty)


if __name__ == '__main__':
    unittest.main()