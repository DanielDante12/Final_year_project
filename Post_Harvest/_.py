# @permission_classes([isAuthenticated])
# @api_view(['GET'])
# def posts_view(request):
#     if request.user.role != "admin":
#         return Response(status=status.HTTP_400_BAD_REQUEST)
    
#     posts = ["one", "two"]
#     serialized = PostSerializer(posts, many = True)
#     return Response(serialized.data)