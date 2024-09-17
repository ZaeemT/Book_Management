from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Book
from .serializers import BookSerializer

# Create your views here.
class BookListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.is_superuser:
            books = Book.objects.all()
        else:
            books = Book.objects.filter(owner=request.user)
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class BookDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        try:
            return Book.objects.get(pk=pk, owner=user)
        except Book.DoesNotExist:
            return None

    def get(self, request, pk):
        book = self.get_object(pk, request.user)
        if book is not None:
            serializer = BookSerializer(book)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(status=status.HTTP_404_NOT_FOUND)  
    

    def put(self, request, pk):
        book = self.get_object(pk, request.user)
        if book is not None:
            serializer = BookSerializer(book, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_404_NOT_FOUND)
    

    def delete(self, request, pk):
        book = self.get_object(pk, request.user)
        if book is not None:
            book.delete()
            return Response({
                'message': 'Book deleted successfully',
            }, status=status.HTTP_204_NO_CONTENT)
        return Response({
            'message': 'Book not found'
        }, status=status.HTTP_404_NOT_FOUND)
    
    
