from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Member
from .serializers import MemberSerializer

from .utils import exchange_gifts


class MemberList(generics.ListCreateAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

class MemberDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

class GiftExchangeAPI(APIView):
    def get(self, request):
        queryset = Member.objects.all()
        if not queryset.exists():
            return Response({'error': 'Member list empty, please add members first'}, status=status.HTTP_200_OK)
        try:
            result = exchange_gifts(queryset)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        # Add member name along with its ID for final response obj
        exchanges = {}
        for key, value in result.items():
            new_key = Member.objects.get(id=key)
            if value == '-1':
                new_value = 'No eligible receiver'
            else:
                new_value = Member.objects.get(id=value)
            exchanges[str(new_key)] = str(new_value)
        return Response(exchanges, status=status.HTTP_200_OK)
