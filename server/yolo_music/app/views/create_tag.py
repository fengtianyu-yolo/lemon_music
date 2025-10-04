from django.http import JsonResponse
from ..models import Song
from ..models import UnmatchedMusic
from ..models import Tag
from urllib.parse import parse_qs, unquote


def create_tag(request):
    """
    查询所有标签，并以 JSON 返回
    """
    body = request.body.decode('utf-8')
    params = parse_qs(body)
    tag = unquote(params.get('tag', [''])[0])
    tag, created = Tag.objects.get_or_create(name=tag)
    if created:
        return JsonResponse({"success": True, "message": "标签创建成功", "tag": {"id": f"{tag.id}", "name": tag.name}})
    else:
        return JsonResponse({"success": False, "message": "标签已存在", "tag": {"id": f"{tag.id}", "name": tag.name}})