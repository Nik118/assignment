from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Location, Department, Category, SubCategory, SKU
from .serializers import LocationSerializer
# Create your views here.


class LocationViewSet(ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    filter_backends = [OrderingFilter, SearchFilter]
    ordering = ['name']
    search_fields = ['name']


class DepartmentView(APIView):

    def get(self, request, location_id, format=None):
        output = []
        departments = Department.objects.filter(location=location_id)
        for department in departments:
            output.append({'id': department.id, 'name': department.name})
        return Response(output)
    
    def post(self, request, location_id):
        data = request.data
        try:
            name = data['name']
            try:
                location_obj = Location.objects.get(id=location_id)
                department_obj, success = Department.objects.get_or_create(location=location_obj, name=name)
                return Response({'status': 'success'}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, location_id, department_id):
        try:
            Department.objects.get(location=location_id, id=department_id).delete()
            return Response({'status': 'success'})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def put(self, request, location_id, department_id):
        data = request.data
        try:
            name = data['name']
            try:
                department_obj = Department.objects.get(location=location_id, id=department_id)
                department_obj.name = name
                department_obj.save()
                return Response({'status': 'success'})
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class CategoryView(APIView):

    def get(self, request, location_id, department_id, format=None):
        output = []
        categories = Category.objects.filter(department=department_id, department__location=location_id)
        for category in categories:
            output.append({'id': category.id, 'name': category.name})
        return Response(output)
    
    def post(self, request, location_id, department_id):
        data = request.data
        try:
            name = data['name']
            try:
                department_obj = Department.objects.get(id=department_id, location=location_id)
                category_obj, success = Category.objects.get_or_create(department=department_obj, name=name)
                return Response({'status': 'success'}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, location_id, department_id, category_id):
        try:
            Category.objects.get(department__location=location_id, department=department_id,
                                id=category_id
                                ).delete()
            return Response({'status': 'success'})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def put(self, request, location_id, department_id, category_id):
        data = request.data
        try:
            name = data['name']
            try:
                category_obj = Category.objects.get(department__location=location_id,
                                                    department=department_id, id=category_id
                                                    )
                category_obj.name = name
                category_obj.save()
                return Response({'status': 'success'})
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class SubCategoryView(APIView):

    def get(self, request, location_id, department_id, category_id, format=None):
        output = []
        sub_categories = SubCategory.objects.filter(category=category_id, category__department=department_id,
                                                    category__department__location=location_id
                                                    )
        for sub_category in sub_categories:
            output.append({'id': sub_category.id, 'name': sub_category.name})
        return Response(output)
    
    def post(self, request, location_id, department_id, category_id):
        data = request.data
        try:
            name = data['name']
            try:
                category_obj = Category.objects.get(id=category_id, department=department_id,
                                                    department__location=location_id)
                subcategory_obj, success = SubCategory.objects.get_or_create(category=category_obj, name=name)
                return Response({'status': 'success'}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, location_id, department_id, category_id, subcategory_id):
        try:
            SubCategory.objects.get(id=subcategory_id, category=category_id,
                                   category__department=department_id,
                                   category__department__location=location_id
                                   ).delete()
            return Response({'status': 'success'})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def put(self, request, location_id, department_id, category_id, subcategory_id):
        data = request.data
        try:
            name = data['name']
            try:
                subcategory_obj = SubCategory.objects.get(id=subcategory_id, category=category_id,
                                                         category__department=department_id,
                                                         category__department__location=location_id
                                                         )
                subcategory_obj.name = name
                subcategory_obj.save()
                return Response({'status': 'success'})
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class SKUView(APIView):
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['location__name', 'department__name', 'category__name', 'sub_category__name']

    def filter_queryset(self, queryset):
        """
        Given a queryset, filter it with whichever filter backend is in use.
        You are unlikely to want to override this method, although you may need
        to call it either from a list view, or from a custom `get_object`
        method if you want to apply the configured filtering backend to the
        default queryset.
        """
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset
    
    def get_queryset(self):
        return SKU.objects.all()

    def get(self, request, format=None):
        location = request.query_params.get('location__name', None)
        department = request.query_params.get('department__name', None)
        category = request.query_params.get('category__name', None)
        sub_catgeory = request.query_params.get('sub_category__name', None)

        if not (location and department and category and sub_catgeory):
            return Response({'error': 'Please provide all the required data'}, status=status.HTTP_400_BAD_REQUEST)
        
        output = []
        skus = self.filter_queryset(self.get_queryset())

        for sku in skus:
            output.append({'location': sku.location.name,
                           'department': sku.department.name,
                           'category': sku.category.name,
                           'sub_category': sku.sub_category.name,
                           'name': sku.name,
                           'id': sku.id
                           })
        return Response(output)