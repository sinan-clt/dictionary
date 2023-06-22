from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import serializers


class Register(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        mutable = request.POST._mutable
        request.POST._mutable = True
        request.POST['username'] = request.POST['email']
        request.POST._mutable = mutable
        serializer = UserSerializer(data=request.data)
        validate = serializer.is_valid()
        if validate is False:
            return Response({"status": 400, "message": "Incorrect Inputs", "data": serializer.errors})

        user = User.objects.create_user(name=request.POST['name'], mobile_number=request.POST['mobile_number'], username=request.POST['email'],
                                        email=request.POST['email'], password=request.POST['password'])
        user.is_active = True
        user.save()

        fields = ('id', 'username', 'email', 'mobile_number', 'name')
        data = UserSerializer(user, many=False, fields=fields)
        response = {
            'success': 'True',
            'status': 200,
            'message': 'User created successfully',
            'data': data.data,
        }

        return Response(response)



class UserLogin(APIView):
    permission_classes = [AllowAny]

    class Validation(serializers.Serializer):
        email = serializers.CharField()
        password = serializers.CharField()

    def post(self, request):

        validation = self.Validation(data=request.data)
        validate = validation.is_valid()
        if validate is False:
            return Response({"status": 400, "message": "Incorrect Inputs", "data": validation.errors})

        user = User.objects.filter(
            email=request.POST['email']).first()

        if user:
            mutable = request.POST._mutable
            request.POST._mutable = True
            request.POST['password'] = request.POST['password']
            request.POST._mutable = mutable
            serializer = UserLoginSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            fields = ('id', 'username', 'email', 'phone_number', 'name')
            data = UserSerializer(user, many=False, fields=fields)
            response = {
                'success': 'True',
                'status': 200,
                'message': 'User logged in successfully',
                'token': serializer.data['token'],
                'data': data.data,
            }

            return Response(response)



class authenticatedUserDetails(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        items = User.objects.filter(id=request.user.id)
        serializer = UserSerializer(items, many=True)
        return Response({'data':serializer.data,'status': 200, "message": "success"})



            
class ListwordsAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        words = Dictionary.objects.filter(is_deleted=False)
        serializer = WordSerializer(words, many=True)
        data = {
            'words': serializer.data
        }
        return Response(data)


from django.db.models import
class SearchWordSerializer(serializers.Serializer):
    query = serializers.CharField()

class SearchWordAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = SearchWordSerializer(data=request.GET)
        serializer.is_valid(raise_exception=True)
        query = serializer.validated_data['query']

        word = Dictionary.objects.filter(label=query, is_deleted=False).first()
        if word:
            word.search_count = F('search_count') + 1
            word.save()

        serializer = WordSerializer(word)
        
        data = {
            'word': serializer.data
        }
        return Response(data)



class CreateAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = WordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DetailAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, word_id):
        try:
            word = Dictionary.objects.get(id=word_id)
            serializer = WordSerializer(word)
            return Response(serializer.data)
        except Dictionary.DoesNotExist:
            return Response({'error': 'Word not found'}, status=status.HTTP_404_NOT_FOUND)


class UpdateAPI(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, word_id):
        try:
            word = Dictionary.objects.get(id=word_id)
            serializer = WordSerializer(word, data=request.data)
            if serializer.is_valid():
                serializer.save()
                serialized_data = serializer.data
                return Response(serialized_data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Dictionary.DoesNotExist:
            return Response({'error': 'Word not found'}, status=status.HTTP_404_NOT_FOUND)
            
        
class DeleteAPI(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, word_id):
        try:
            word = Dictionary.objects.get(id=word_id)
            word.is_deleted = True
            word.save()
            remaining_words = Dictionary.objects.filter(user=request.user, is_deleted=False)
            serializer = WordSerializer(remaining_words, many=True)
            data = {
                'message': "Word deleted succesfully",
                'status':status.HTTP_200_OK,
                'words': serializer.data
            }
            return Response(data)

        except Dictionary.DoesNotExist:
            return Response({'error': 'Word not found'}, status=status.HTTP_404_NOT_FOUND)

