from django.test import TestCase, Client
from django.urls import reverse

import json

from .models import Member

# Create your tests here.
class GiftExchangeTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        
    def test_list_members(self):
        members_url = reverse('members')
        response = self.client.get(members_url)
        self.assertEquals(response.status_code, 200)
        
    def test_retrieve_member_success(self):
        member = Member.objects.create(name="Alice")
        url = reverse('members-detail', args=[member.id])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        
    def test_retrieve_member_not_found(self):
        url = reverse('members-detail', args=[1])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)
    
    def test_create_member(self):
        url = reverse('members')
        response = self.client.post(url, data={'name': 'Alice'})
        self.assertEquals(response.status_code, 201)
        obj = json.loads(response.content.decode())
        self.assertEquals(obj.get('name'), 'Alice')
        
    def test_update_member(self):
        member = Member.objects.create(name="Alice")
        url = reverse('members-detail', args=[member.id])
        response = self.client.put(url, data={'id': member.id, 'name': 'NewAlice'}, content_type='application/json')
        self.assertEquals(response.status_code, 200)
        obj = json.loads(response.content.decode())
        self.assertEquals(obj.get('name'), 'NewAlice')
        
    def test_delete_member(self):
        member = Member.objects.create(name="Alice")
        url = reverse('members-detail', args=[member.id])
        response = self.client.delete(url)
        self.assertEquals(response.status_code, 204)
 
    def test_gift_exchange_with_no_member(self):
        gift_exchange_url = reverse('gift-exchange')
        response = self.client.get(gift_exchange_url)
        self.assertEquals(response.status_code, 200)
        
        # If no member, we expect to see an error with below response description
        obj = json.loads(response.content.decode())
        self.assertEquals(obj.get('error'), 'Member list empty, please add members first')
        
    def test_gift_exchange_with_one_member(self):
        gift_exchange_url = reverse('gift-exchange')
        member = Member.objects.create(name="Alice")
        response = self.client.get(gift_exchange_url)
        self.assertEquals(response.status_code, 200)

        # If only one member exists, 
        # we expect to see the value in the response dictionary
        # always to be the below description
        obj = json.loads(response.content.decode())
        self.assertEquals(obj.get(str(member)), 'No eligible receiver')
    
    def test_gift_exchange_with_one_member_for_multiple_years(self):
        gift_exchange_url = reverse('gift-exchange')
        member = Member.objects.create(name="Alice")
        # If only one member exists, 
        # we expect to see the value in the response dictionary
        # always to be the below description
        # no matter which year we are in(run gift exchange for five years in this case)
        for _ in range(5):
            response = self.client.get(gift_exchange_url)
            self.assertEquals(response.status_code, 200)

            obj = json.loads(response.content.decode())
            self.assertEquals(obj.get(str(member)), 'No eligible receiver')
    
    def test_gift_exchange_with_two_members_year1(self):
        gift_exchange_url = reverse('gift-exchange')
        member1 = Member.objects.create(name="Alice")
        member2 = Member.objects.create(name="Barry")
        response = self.client.get(gift_exchange_url)
        self.assertEquals(response.status_code, 200)

        # If only two member exists, 
        # we expect to see the value in the response dictionary
        # to be the other member for year 1
        obj = json.loads(response.content.decode())
        self.assertEquals(obj.get(str(member1)), str(member2))
        self.assertEquals(obj.get(str(member2)), str(member1))
        
    def test_gift_exchange_with_two_members_year2(self):
        gift_exchange_url = reverse('gift-exchange')
        member1 = Member.objects.create(name="Alice")
        member2 = Member.objects.create(name="Barry")
        response = self.client.get(gift_exchange_url)
        response = self.client.get(gift_exchange_url)
        self.assertEquals(response.status_code, 200)

        # If only two member exists, 
        # we expect to see the value in the response dictionary
        # to be 'No eligible receiver' for year 2
        obj = json.loads(response.content.decode())
        self.assertEquals(obj.get(str(member1)), 'No eligible receiver')
        self.assertEquals(obj.get(str(member2)), 'No eligible receiver')
    
    def test_gift_exchange_with_two_members_year5(self):
        gift_exchange_url = reverse('gift-exchange')
        member1 = Member.objects.create(name="Alice")
        member2 = Member.objects.create(name="Barry")
        for _ in range(5):
            response = self.client.get(gift_exchange_url)
        self.assertEquals(response.status_code, 200)

        # If only two member exists, 
        # we expect to see the value in the response dictionary
        # to be the other member again for year 5
        obj = json.loads(response.content.decode())
        self.assertEquals(obj.get(str(member1)), str(member2))
        self.assertEquals(obj.get(str(member2)), str(member1))
    
    def test_gift_exchange_with_three_members(self):
        gift_exchange_url = reverse('gift-exchange')
        member1 = Member.objects.create(name="Alice")
        member2 = Member.objects.create(name="Barry")
        member3 = Member.objects.create(name="Caroline")
        response = self.client.get(gift_exchange_url)
        self.assertEquals(response.status_code, 200)

        # If three members exist, it could be shuffled in order,
        # either no one is left out 1->2,2->3,3->1  1->3,2->1,3->2
        # or one member is left out 1->2,2->1,3->x  1->3,3->1,2->x  1->x,2->3,3->2
        obj = json.loads(response.content.decode())
        container = set()
        for value in obj.values():
            container.add(value)
        if 'No eligible receiver' not in container:
            self.assertEquals(len(container), 3)
        else:
            container.remove('No eligible receiver')
            self.assertEquals(len(container), 2)
