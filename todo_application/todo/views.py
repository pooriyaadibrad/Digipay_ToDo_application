from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from . import serializers, paginations, models
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse


class TodoListCreateApiView(APIView):
    serializer_class = serializers.ToDoSerializer
    permission_classes = (permissions.AllowAny,)
    pagination_class = paginations.CustomPagination

    @extend_schema(tags=['ToDo'],
                   summary='this get all todo information or'
                           'search todo  by specific field',
                   responses={
                       status.HTTP_200_OK: OpenApiResponse(
                           response=serializer_class,
                           description='i see this status when'
                                       'the api work great',
                       ),
                       status.HTTP_404_NOT_FOUND: OpenApiResponse(
                           description='i see this status when'
                                       'i have not any data or'
                                       'i have not any response from'
                                       'database'
                       )
                   },
                   parameters=[
                       OpenApiParameter(
                           name=field,
                           location=OpenApiParameter.QUERY,
                           type=type(field),
                       )for field in serializer_class().fields.keys()
                   ]
                   )
    def get(self, request):
        todo_s = models.Todo.objects.all()

        due_date = request.query_params.get('due_date', None)
        if due_date:
            todo_s = todo_s.filter(due_date=due_date)

        created_at = request.query_params.get('created_at', None)
        if created_at:
            todo_s = todo_s.filter(created_at=created_at)

        title = request.query_params.get('title', None)
        if title:
            todo_s = todo_s.filter(title__icontains=title)
        description = request.query_params.get('description', None)
        if description:
            todo_s = todo_s.filter(description__icontains=description)

        paginator = self.pagination_class()
        page = paginator.paginate_queryset(todo_s, request=request)

        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        return Response({'details:"not results found."'}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(tags=['ToDo'],
                   summary='this post todo information to server',
                   responses={
                       status.HTTP_201_CREATED: OpenApiResponse(
                           response=serializer_class,
                           description='i see this status when'
                                       'the api post that work great',
                       ),
                       status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                           description='when my api`s body is not valid'
                                       'is see the response'
                       )
                   },
                   parameters=[
                       OpenApiParameter(
                           name=field,
                           location=OpenApiParameter.QUERY,
                           type=type(field),
                       ) for field in serializer_class().fields.keys()
                   ]
                   )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)