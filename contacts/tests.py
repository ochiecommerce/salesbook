from django.test import TestCase

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

class PhonebookAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.phonebook_url = reverse('phonebook-list')
        self.contact_url = lambda phonebook_id: reverse('custom_contacts', args=[phonebook_id])
    
    def test_create_phonebook(self):
        response = self.client.post(self.phonebook_url, {'name': 'Test Phonebook'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('pk', response.data)
    
    def test_create_contact(self):
        phonebook_response = self.client.post(self.phonebook_url, {'name': 'Test Phonebook'}, format='json')
        phonebook_id = phonebook_response.data['pk']
        
        response = self.client.post(
            self.contact_url(phonebook_id),
            {'name': 'John Doe', 'phone': '1234567890'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('pk', response.data)

    def test_list_contacts(self):
        phonebook_response = self.client.post(self.phonebook_url, {'name': 'Test Phonebook'}, format='json')
        phonebook_id = phonebook_response.data['pk']
        
        self.client.post(
            self.contact_url(phonebook_id),
            {'name': 'John Doe', 'phone': '1234567890'},
            format='json'
        )
        
        response = self.client.get(self.contact_url(phonebook_id), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data['data']), 0)

    def test_create_column(self):
        phonebook_response = self.client.post(self.phonebook_url, {'name': 'Test Phonebook'}, format='json')
        phonebook_id = phonebook_response.data['pk']
        
        response = self.client.post(
            reverse('column-list'),
            {'name': 'Test Column', 'phonebook': phonebook_id},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('pk', response.data)
        self.assertEqual(response.data['name'], 'Test Column')
        self.assertEqual(response.data['phonebook'], phonebook_id)
    
    def test_create_note(self):
        phonebook_response = self.client.post(self.phonebook_url, {'name': 'Test Phonebook'}, format='json')
        phonebook_id = phonebook_response.data['pk']
        
        contact_response = self.client.post(
            self.contact_url(phonebook_id),
            {'name': 'John Doe', 'phone': '1234567890'},
            format='json'
        )
        contact_id = contact_response.data['pk']
        
        response = self.client.post(
            reverse('note-list'),
            {'contact': contact_id, 'note': 'This is a test note.'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('pk', response.data)
        self.assertEqual(response.data['note'], 'This is a test note.')

    def test_username_check(self):
        response = self.client.get(reverse('username_check'), {'username': 'testuser'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('exists', response.data)
        self.assertIsInstance(response.data['exists'], bool)
        self.assertFalse(response.data['exists'])
        # Assuming 'testuser' does not exist in the database
    
    def test_user_search(self):
        response = self.client.get(reverse('user_search'), {'query': 'test'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertIsInstance(response.data['results'], list)
    
    

